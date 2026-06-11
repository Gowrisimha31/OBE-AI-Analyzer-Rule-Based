from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import webbrowser
import subprocess
import shutil
import os
import pandas as pd
from werkzeug.utils import secure_filename
import io
from datetime import datetime

SESSION_ANALYSIS_COUNT = 0

from scripts.predict_bloom import predict_bloom
from scripts.predict_co import predict_co
from scripts.predict_po import predict_po
from scripts.history_manager import save_prediction

CORS_ORIGINS = "*"

# Serve frontend files from the 'frontend' folder so the UI is available
app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

BLOOM_EXPLANATIONS = {

    "Remember": "Recall facts, definitions, concepts, or basic information.",

    "Understand": "Explain ideas, interpret concepts, and demonstrate understanding.",

    "Apply": "Use knowledge, formulas, methods, or procedures to solve problems.",

    "Analyze": "Break information into parts and examine relationships or patterns.",

    "Evaluate": "Make judgments, justify decisions, and assess alternatives.",

    "Create": "Design, construct, develop, or formulate new solutions."
}

CO_EXPLANATIONS = {

    "CO1": "Operating System Fundamentals and System Calls",

    "CO2": "Process Management and CPU Scheduling",

    "CO3": "Synchronization and Deadlock Management",

    "CO4": "Memory Management and Virtual Memory",

    "CO5": "File Systems, Storage, and Protection"
}

PO_EXPLANATIONS = {

    "PO1": "Engineering Knowledge",

    "PO2": "Problem Analysis",

    "PO3": "Design / Development of Solutions",

    "PO4": "Investigation of Complex Problems",

    "PO5": "Modern Tool Usage"
}


@app.route("/")
def home():
    # Serve the frontend index.html so the UI is loaded over HTTP
    return app.send_static_file('index.html')


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    question = data.get("question", "")

    bloom = predict_bloom(question)
    co = predict_co(question)
    po = predict_po(question)

    save_prediction(
        question,
        bloom,
        co,
        po
    )

    global SESSION_ANALYSIS_COUNT
    SESSION_ANALYSIS_COUNT += 1

    po_details = []

    for p in po:

        po_details.append({
            "code": p,
            "description": PO_EXPLANATIONS[p]
        })

    return jsonify({

        "question": question,

        "bloom": bloom,
        "bloom_explanation":
            BLOOM_EXPLANATIONS[bloom],

        "co": co,
        "co_explanation":
            CO_EXPLANATIONS[co],

        "po": po,

        "po_details": po_details
    })


@app.route("/bulk_predict", methods=["POST"])
def bulk_predict():

    data = request.get_json()

    questions = data.get(
        "questions",
        []
    )

    results = []

    bloom_count = {}
    co_count = {}

    global SESSION_ANALYSIS_COUNT

    for question in questions:

        bloom = predict_bloom(question)
        co = predict_co(question)
        po = predict_po(question)

        save_prediction(
            question,
            bloom,
            co,
            po
        )

        bloom_count[bloom] = (
            bloom_count.get(bloom, 0) + 1
        )

        co_count[co] = (
            co_count.get(co, 0) + 1
        )

        results.append({

            "question": question,
            "bloom": bloom,
            "co": co,
            "po": po
        })

    SESSION_ANALYSIS_COUNT += len(questions)

    return jsonify({

        "total_questions":
            len(questions),

        "bloom_distribution":
            bloom_count,

        "co_distribution":
            co_count,

        "results":
            results
    })


@app.route("/stats")
def stats():

    file_path = "dataset/prediction_history.csv"

    if not os.path.exists(file_path):

        return jsonify({

            "total_questions": 0,
            "bloom_levels": 0,
            "co_count": 0,
            "po_count": 0,
            "bloom_distribution": {
                "Remember": 0,
                "Understand": 0,
                "Apply": 0,
                "Analyze": 0,
                "Evaluate": 0,
                "Create": 0
            }
        })

    df = pd.read_csv(file_path)

    unique_pos = set()

    if "po" in df.columns:

        for po_value in df["po"].dropna():

            po_list = str(po_value).split(",")

            for p in po_list:
                unique_pos.add(p.strip())

    # Calculate bloom distribution
    bloom_dist = df["bloom"].value_counts().to_dict()
    
    # Ensure all bloom levels are present (even with count 0)
    bloom_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    bloom_distribution = {level: bloom_dist.get(level, 0) for level in bloom_levels}

    # Calculate CO distribution
    co_dist = df["co"].value_counts().to_dict()
    co_levels = ["CO1", "CO2", "CO3", "CO4", "CO5"]
    co_distribution = {level: co_dist.get(level, 0) for level in co_levels}

    return jsonify({

        "total_questions": len(df),

        "bloom_levels":
            df["bloom"].nunique(),

        "co_count":
            df["co"].nunique(),

        "po_count":
            len(unique_pos),

        "bloom_distribution":
            bloom_distribution,

        "co_distribution":
            co_distribution
    })


@app.route("/coverage_report", methods=["POST"])
def coverage_report():
    data = request.get_json()
    questions = data.get("questions", [])
    results = data.get("results", [])

    if not results:
        return jsonify({"error": "No results provided"}), 400

    # Calculate statistics
    bloom_counts = {}
    co_counts = {}
    po_set = set()
    bloom_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    co_levels = ["CO1", "CO2", "CO3", "CO4", "CO5"]

    for result in results:
        bloom = result.get("bloom", "")
        co = result.get("co", "")
        po = result.get("po", [])

        bloom_counts[bloom] = bloom_counts.get(bloom, 0) + 1
        co_counts[co] = co_counts.get(co, 0) + 1

        if isinstance(po, list):
            for p in po:
                po_set.add(p)
        elif isinstance(po, str):
            po_set.add(po)

    # Build report
    bloom_dist_summary = "\n".join([
        f"{level} : {bloom_counts.get(level, 0)}"
        for level in bloom_levels
    ])

    co_dist_summary = "\n".join([
        f"{level} : {co_counts.get(level, 0)}"
        for level in co_levels
    ])

    # Coverage evaluation
    coverage_checks = []
    missing_cos = [co for co in co_levels if co_counts.get(co, 0) == 0]
    missing_pos = [po for po in ["PO1", "PO2", "PO3", "PO4", "PO5"] if po not in po_set]
    missing_blooms = [b for b in bloom_levels if bloom_counts.get(b, 0) == 0]

    if not missing_cos:
        coverage_checks.append({"status": "✓", "message": "All COs Covered"})
    else:
        coverage_checks.append({"status": "⚠", "message": f"Missing: {', '.join(missing_cos)}"})

    if not missing_pos:
        coverage_checks.append({"status": "✓", "message": "All POs Covered"})
    else:
        coverage_checks.append({"status": "⚠", "message": f"Missing PO: {', '.join(missing_pos)}"})

    bloom_coverage = len([b for b in bloom_levels if bloom_counts.get(b, 0) > 0])
    if bloom_coverage >= 4:
        coverage_checks.append({"status": "✓", "message": "Bloom Taxonomy Coverage Adequate"})
    else:
        coverage_checks.append({"status": "⚠", "message": f"Limited Bloom Coverage ({bloom_coverage}/6)"})

    return jsonify({
        "total_questions": len(results),
        "unique_blooms": len(set(b for b in [r.get("bloom") for r in results])),
        "unique_cos": len(set(c for c in [r.get("co") for r in results])),
        "unique_pos": len(po_set),
        "bloom_distribution": bloom_dist_summary,
        "co_distribution": co_dist_summary,
        "coverage_evaluation": coverage_checks
    })


@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files are allowed"}), 400

        # Read CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        df = pd.read_csv(stream)

        if 'Question' not in df.columns:
            # Try alternative column names
            question_col = None
            for col in df.columns:
                if col.lower() in ['question', 'questions', 'q', 'query']:
                    question_col = col
                    break

            if not question_col:
                return jsonify({"error": "CSV must contain a 'Question' column"}), 400
        else:
            question_col = 'Question'

        # Extract questions and run analysis
        questions = df[question_col].dropna().astype(str).tolist()

        if not questions:
            return jsonify({"error": "No valid questions found in CSV"}), 400

        # Run bulk analysis
        results = []
        bloom_count = {}
        co_count = {}

        for question in questions:
            bloom = predict_bloom(question)
            co = predict_co(question)
            po = predict_po(question)

            save_prediction(question, bloom, co, po)

            bloom_count[bloom] = bloom_count.get(bloom, 0) + 1
            co_count[co] = co_count.get(co, 0) + 1

            results.append({
                "question": question,
                "bloom": bloom,
                "co": co,
                "po": po
            })

        global SESSION_ANALYSIS_COUNT
        SESSION_ANALYSIS_COUNT += len(questions)

        return jsonify({
            "total_questions": len(questions),
            "bloom_distribution": bloom_count,
            "co_distribution": co_count,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_pdf_report", methods=["POST"])
def generate_pdf_report():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.units import inch

        data = request.get_json()
        results = data.get("results", [])
        
        if not results:
            return jsonify({"error": "No results provided"}), 400

        # Generate PDF in memory
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#5d4037'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#795548'),
            spaceAfter=12,
            spaceBefore=12
        )

        # Title
        title = Paragraph("OBE AI Analyzer - Coverage Report", title_style)
        elements.append(title)
        
        # Date and time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_para = Paragraph(f"<b>Generated:</b> {timestamp}", styles['Normal'])
        elements.append(date_para)
        elements.append(Spacer(1, 0.2*inch))

        # Calculate statistics
        bloom_counts = {}
        co_counts = {}
        po_set = set()
        bloom_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
        co_levels = ["CO1", "CO2", "CO3", "CO4", "CO5"]

        for result in results:
            bloom = result.get("bloom", "")
            co = result.get("co", "")
            po = result.get("po", [])

            bloom_counts[bloom] = bloom_counts.get(bloom, 0) + 1
            co_counts[co] = co_counts.get(co, 0) + 1

            if isinstance(po, list):
                for p in po:
                    po_set.add(p)
            elif isinstance(po, str):
                po_set.add(po)

        # Basic Statistics
        elements.append(Paragraph("Basic Statistics", heading_style))
        stat_data = [
            ["Total Questions", str(len(results))],
            ["Unique Bloom Levels", str(len(set(r.get("bloom") for r in results)))],
            ["Unique COs", str(len(set(c for c in [r.get("co") for r in results])))],
            ["Unique POs", str(len(po_set))]
        ]
        stat_table = Table(stat_data, colWidths=[3*inch, 2*inch])
        stat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fafafa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(stat_table)
        elements.append(Spacer(1, 0.3*inch))

        # Bloom Distribution
        elements.append(Paragraph("Bloom Distribution", heading_style))
        bloom_data = [["Level", "Count"]]
        for level in bloom_levels:
            bloom_data.append([level, str(bloom_counts.get(level, 0))])
        
        bloom_table = Table(bloom_data, colWidths=[3*inch, 2*inch])
        bloom_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8d6555')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(bloom_table)
        elements.append(Spacer(1, 0.2*inch))

        # CO Distribution
        elements.append(Paragraph("Course Outcome Distribution", heading_style))
        co_data = [["CO", "Count"]]
        for level in co_levels:
            co_data.append([level, str(co_counts.get(level, 0))])
        
        co_table = Table(co_data, colWidths=[3*inch, 2*inch])
        co_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8d6555')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(co_table)
        elements.append(PageBreak())

        # Coverage Evaluation
        elements.append(Paragraph("Coverage Evaluation", heading_style))
        missing_cos = [co for co in co_levels if co_counts.get(co, 0) == 0]
        missing_pos = [po for po in ["PO1", "PO2", "PO3", "PO4", "PO5"] if po not in po_set]
        bloom_coverage = len([b for b in bloom_levels if bloom_counts.get(b, 0) > 0])

        eval_text = ""
        if not missing_cos:
            eval_text += "✓ All COs Covered<br/>"
        else:
            eval_text += f"⚠ Missing: {', '.join(missing_cos)}<br/>"

        if not missing_pos:
            eval_text += "✓ All POs Covered<br/>"
        else:
            eval_text += f"⚠ Missing PO: {', '.join(missing_pos)}<br/>"

        if bloom_coverage >= 4:
            eval_text += "✓ Bloom Taxonomy Coverage Adequate"
        else:
            eval_text += f"⚠ Limited Bloom Coverage ({bloom_coverage}/6)"

        elements.append(Paragraph(eval_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))

        # Analysis Table
        elements.append(Paragraph("Complete Analysis", heading_style))
        table_data = [["Question", "Bloom", "CO", "PO"]]
        for result in results:
            po_str = ", ".join(result.get("po", []))
            table_data.append([
                result.get("question", "")[:40] + ("..." if len(result.get("question", "")) > 40 else ""),
                result.get("bloom", ""),
                result.get("co", ""),
                po_str
            ])

        analysis_table = Table(table_data, colWidths=[2.5*inch, 1.2*inch, 0.8*inch, 0.7*inch])
        analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8d6555')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')])
        ]))
        elements.append(analysis_table)

        # Build PDF
        doc.build(elements)
        pdf_buffer.seek(0)

        return pdf_buffer.getvalue(), 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename="OBE_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        }

    except ImportError:
        return jsonify({"error": "reportlab not installed. Install with: pip install reportlab"}), 500
    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500


@app.route("/clear_history", methods=["POST"])
def clear_history():
    file_path = "dataset/prediction_history.csv"

    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"status": "ok", "message": "History cleared"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Try to open the app in Chrome; fall back to the default browser
    def open_in_chrome(url):
        # Try chrome on PATH
        chrome = shutil.which('chrome') or shutil.which('chrome.exe')
        if chrome:
            try:
                subprocess.Popen([chrome, url])
                return True
            except Exception:
                pass

        # Try common install locations
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    subprocess.Popen([p, url])
                    return True
                except Exception:
                    pass

        return False

    url = 'http://127.0.0.1:5000'
    threading.Timer(1.0, lambda: (open_in_chrome(url) or webbrowser.open(url))).start()
    app.run(debug=True)