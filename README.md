# OBE AI Analyzer (Rule-Based Version)

## Overview

OBE AI Analyzer is a Rule-Based Educational Analytics System developed for Outcome Based Education (OBE) analysis of Operating Systems question papers.

The system automatically classifies questions according to Bloom's Taxonomy, maps them to Course Outcomes (COs) and Program Outcomes (POs), generates coverage reports, visualizes academic analytics through dashboards, and supports CSV/PDF-based question paper analysis.

This project is implemented entirely using rule-based techniques without Machine Learning.

---

## Features

### Bloom Taxonomy Classification

Classifies questions into:

* Remember
* Understand
* Apply
* Analyze
* Evaluate
* Create

### Course Outcome (CO) Prediction

Maps questions to:

* CO1
* CO2
* CO3
* CO4
* CO5

### Program Outcome (PO) Mapping

Maps questions to:

* PO1
* PO2
* PO3
* PO4
* PO5

### Analysis Modes

* Single Question Analysis
* Bulk Question Analysis

### Dashboard Analytics

* Total Questions Analyzed
* Bloom Levels Covered
* CO Coverage
* PO Coverage

### Visualization

* Bloom Distribution Chart
* CO Distribution Chart

### Reporting

* Question Paper Coverage Report
* PDF Report Generation
* CSV Export

### File Upload Support

* CSV Question Upload
* PDF Question Paper Upload

### History Tracking

* Prediction History Storage
* Statistical Analysis from Historical Data

---

## Project Architecture

```text
OBE_AI_ANALYZER_V2/

├── app.py
│
├── dataset/
│   ├── bloom_dataset.csv
│   ├── co_dataset.csv
│   ├── co_topics.csv
│   ├── master_questions.csv
│   └── prediction_history.csv
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── scripts/
│   ├── predict_bloom.py
│   ├── predict_co.py
│   ├── predict_po.py
│   ├── history_manager.py
│   └── pdf_extractor.py
│
├── uploads/
├── requirements.txt
└── README.md
```

---

## Technology Stack

### Backend

* Python
* Flask
* Pandas

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### Reporting

* ReportLab

### File Processing

* CSV Processing
* PDF Text Extraction

---

## How It Works

### Step 1

Upload or enter one or more Operating Systems questions.

### Step 2

The system performs:

* Bloom Taxonomy Classification
* Course Outcome Mapping
* Program Outcome Mapping

### Step 3

Results are displayed through:

* Analysis Dashboard
* Charts
* Coverage Reports

### Step 4

Generate downloadable reports in PDF format.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Gowrisimha31/OBE-AI-Analyzer-Rule-Based.git
```

### Navigate to Project

```bash
cd OBE-AI-Analyzer-Rule-Based
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

---

## Sample Workflow

```text
Upload Question Paper
          ↓
Extract Questions
          ↓
Bloom Classification
          ↓
CO Mapping
          ↓
PO Mapping
          ↓
Coverage Analysis
          ↓
Dashboard Visualization
          ↓
Generate PDF Report
```

---

## Screenshots

### Dashboard

*Add dashboard screenshot here*

### Bloom Distribution Chart

*Add Bloom Chart screenshot here*

### CO Distribution Chart

*Add CO Chart screenshot here*

### Coverage Report

*Add Coverage Report screenshot here*

### PDF Upload and Analysis

*Add PDF Upload screenshot here*

---

## Educational Applications

This system can be used by:

* Faculty Members
* Course Coordinators
* Academic Auditors
* Accreditation Teams
* Outcome Based Education Analysts

---

## Key Highlights

* Fully Rule-Based Implementation
* No Machine Learning Used
* Real-Time Question Analysis
* OBE-Focused Evaluation
* Interactive Dashboard
* Automated Report Generation
* CSV and PDF Support
* Suitable for Academic Institutions

---

## Future Scope

### Version 2 (Machine Learning Based)

Future enhancements may include:

* Machine Learning-Based Bloom Classification
* Automated CO Prediction Models
* Recommendation Engine for Question Paper Improvement
* Advanced Analytics Dashboard
* Model Performance Comparison

---

## Author

**Gowri Simha**

Developed as an academic project for Outcome Based Education (OBE) analysis of Operating Systems question papers.

---

## License

This project is intended for educational and academic use.
