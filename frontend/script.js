let latestResults = [];
let bloomChart = null;
let coChart = null;

// Try same-origin request first (works when served by Flask),
// fallback to the Flask backend at 127.0.0.1:5000 (works when using Live Server)
async function apiFetch(path, options) {
    const sameOriginUrl = window.location.origin + path;
    const fallbackUrl = 'http://127.0.0.1:5000' + path;

    // Try same-origin first
    try {
        const resp = await fetch(sameOriginUrl, options);

        // If same-origin responded OK and returned JSON, use it
        const ct = resp.headers.get('content-type') || '';
        if (resp.ok && ct.includes('application/json')) return resp;

        // Otherwise try fallback backend
    }
    catch (e) {
        // network error — try fallback to Flask backend
    }

    // Final attempt to fallback URL (may throw to caller)
    return fetch(fallbackUrl, options);
}

async function analyzeQuestion() {
    try {
        console.log("Button clicked");

        const question = document.getElementById("question").value.trim();
        console.log("Question:", question);

        if (!question) {
            alert("Please enter a question");
            return;
        }

        clearResults();
        setStatus("Analyzing question...");
        setButtonsDisabled(true);

        const response = await apiFetch('/predict', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            let text = await response.text();
            throw new Error(`Server error ${response.status}: ${text}`);
        }

        const contentType = response.headers.get("content-type") || "";
        if (!contentType.includes("application/json")) {
            const text = await response.text();
            throw new Error("Invalid JSON response from server: " + text);
        }

        const data = await response.json();

        document.getElementById("bloom").innerText = data.bloom || "";
        document.getElementById("bloomExplanation").innerText = data.bloom_explanation || "";
        document.getElementById("co").innerText = data.co || "";
        document.getElementById("coExplanation").innerText = data.co_explanation || "";
        document.getElementById("po").innerText = (data.po || []).join(", ");
        document.getElementById("poExplanation").innerHTML = (data.po_details || []).map(p => `${p.code} - ${p.description}`).join("<br>");

        setStatus("Analysis complete");
        loadStats();
        setButtonsDisabled(false);
    }
    catch (error) {
        console.error("ERROR FOUND:", error);
        setStatus("Error: " + (error.message || error));
        setButtonsDisabled(false);
    }
}

function setStatus(msg) {
    let s = document.getElementById("status");
    if (!s) {
        s = document.createElement("div");
        s.id = "status";
        s.style.marginTop = "10px";
        s.style.fontWeight = "bold";
        const statsCard = document.getElementById("stats");
        if (statsCard && statsCard.parentNode) statsCard.parentNode.insertBefore(s, statsCard);
        else document.body.insertBefore(s, document.body.firstChild);
    }
    s.innerText = msg;
}

function setButtonsDisabled(disabled) {
    const buttons = document.querySelectorAll(".button-group button");
    buttons.forEach(b => b.disabled = disabled);
}

function clearResults() {
    latestResults = [];
    document.getElementById("bloom").innerText = "";
    document.getElementById("bloomExplanation").innerText = "";
    document.getElementById("co").innerText = "";
    document.getElementById("coExplanation").innerText = "";
    document.getElementById("po").innerText = "";
    document.getElementById("poExplanation").innerHTML = "";
    document.getElementById("tableBody").innerHTML = "";
    document.getElementById("summary").innerHTML = "";
}

async function bulkAnalysis() {

    try {

        const input =
            document.getElementById("question").value;

        const questions =
            input
                .split("\n")
                .filter(
                    q => q.trim() !== ""
                );

        clearResults();
        setStatus("Running bulk analysis...");
        setButtonsDisabled(true);

        const response = await apiFetch('/bulk_predict', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ questions: questions })
        });

        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Server error ${response.status}: ${text}`);
        }

        const ct = response.headers.get('content-type') || '';
        if (!ct.includes('application/json')) {
            const text = await response.text();
            throw new Error('Invalid JSON response from server: ' + text);
        }

        const data = await response.json();

        latestResults =
            data.results;

        let rows = "";

        data.results.forEach(item => {

            rows += `
            <tr>
                <td>${item.question}</td>
                <td>${item.bloom}</td>
                <td>${item.co}</td>
                <td>${item.po.join(", ")}</td>
            </tr>`;
        });

        document.getElementById(
            "tableBody"
        ).innerHTML = rows;

        document.getElementById(
            "summary"
        ).innerHTML =

            `
            <h3>Total Questions:
                ${data.total_questions}
            </h3>

            <h3>Bloom Distribution</h3>

            <pre>
${JSON.stringify(
    data.bloom_distribution,
    null,
    2
)}
            </pre>

            <h3>CO Distribution</h3>

            <pre>
${JSON.stringify(
    data.co_distribution,
    null,
    2
)}
            </pre>
            `;

        loadStats();
        await generateCoverageReport();
        setStatus("Bulk analysis complete");
        setButtonsDisabled(false);
    }
    catch(error) {
        console.error("BULK ERROR:", error);
        setStatus('Error: ' + (error.message || error));
        setButtonsDisabled(false);
    }
}

function exportCSV() {

    if (
        latestResults.length === 0
    ) {

        alert(
            "Run Bulk Analysis First"
        );

        return;
    }

    let csv =
        "Question,Bloom,CO,PO\n";

    latestResults.forEach(row => {

        csv +=
            `"${row.question}","${row.bloom}","${row.co}","${row.po.join(", ")}"\n`;
    });

    const blob =
        new Blob(
            [csv],
            {
                type:
                    "text/csv"
            }
        );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(blob);

    link.download =
        "OBE_Report.csv";

    link.click();
}

async function loadStats() {

    try {

        setStatus('Loading stats...');

        const response = await apiFetch('/stats');

        if (!response.ok) {

            const text = await response.text();

            throw new Error(
                `Server error ${response.status}: ${text}`
            );
        }

        const data = await response.json();

        document.getElementById("totalQuestions").textContent =
            data.total_questions;

        document.getElementById("bloomLevels").textContent =
            data.bloom_levels;

        document.getElementById("coCovered").textContent =
            data.co_count;

        document.getElementById("poCovered").textContent =
            data.po_count;

        // Update Bloom Distribution Chart
        if (data.bloom_distribution) {
            renderBloomChart(data.bloom_distribution);
        }

        // Update CO Distribution Chart
        if (data.co_distribution) {
            renderCOChart(data.co_distribution);
        }

        setStatus('');

    }
    catch(error){

        console.error(error);

        setStatus(
            'Stats error: ' +
            (error.message || error)
        );
    }
}

function renderBloomChart(bloomDistribution) {
    const ctx = document.getElementById('bloomChart');
    if (!ctx) return;

    const labels = Object.keys(bloomDistribution);
    const data = Object.values(bloomDistribution);

    // Define colors for bloom levels
    const colors = [
        '#FF6384',  // Remember - Red
        '#36A2EB',  // Understand - Blue
        '#FFCE56',  // Apply - Yellow
        '#4BC0C0',  // Analyze - Cyan
        '#9966FF',  // Evaluate - Purple
        '#FF9F40'   // Create - Orange
    ];

    // Destroy existing chart if it exists
    if (bloomChart) {
        bloomChart.destroy();
    }

    // Create new chart
    bloomChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            return label + ': ' + value;
                        }
                    }
                }
            }
        }
    });
}

function renderCOChart(coDistribution) {
    const ctx = document.getElementById('coChart');
    if (!ctx) return;

    const labels = Object.keys(coDistribution);
    const data = Object.values(coDistribution);

    // Define colors for CO levels
    const colors = [
        '#4ECDC4',  // CO1 - Teal
        '#44A08D',  // CO2 - Green
        '#FF6B6B',  // CO3 - Red
        '#FFE66D',  // CO4 - Yellow
        '#95E1D3'   // CO5 - Light Teal
    ];

    // Destroy existing chart if it exists
    if (coChart) {
        coChart.destroy();
    }

    // Create new chart
    coChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Questions',
                data: data,
                backgroundColor: colors,
                borderColor: '#333',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'x',
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + ' questions';
                        }
                    }
                }
            }
        }
    });
}

async function generateCoverageReport() {
    if (latestResults.length === 0) {
        setStatus('No results to generate report');
        return;
    }

    try {
        setStatus('Generating coverage report...');

        const response = await apiFetch('/coverage_report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ results: latestResults })
        });

        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Server error ${response.status}: ${text}`);
        }

        const data = await response.json();

        // Display coverage report
        document.getElementById('reportTotalQuestions').textContent = data.total_questions;
        document.getElementById('reportUniqueBlooms').textContent = data.unique_blooms;
        document.getElementById('reportUniqueCOs').textContent = data.unique_cos;
        document.getElementById('reportUniquePOs').textContent = data.unique_pos;
        document.getElementById('reportBloomDist').textContent = data.bloom_distribution;
        document.getElementById('reportCODist').textContent = data.co_distribution;

        // Build coverage evaluation HTML
        let evalHTML = '';
        data.coverage_evaluation.forEach(check => {
            evalHTML += `<p><strong>${check.status}</strong> ${check.message}</p>`;
        });
        document.getElementById('reportCoverageEval').innerHTML = evalHTML;

        document.getElementById('coverageReport').style.display = 'block';
        setStatus('Coverage report generated');
    }
    catch (error) {
        console.error('COVERAGE REPORT ERROR:', error);
        setStatus('Error: ' + (error.message || error));
    }
}

async function clearHistory() {
    try {
        setStatus('Clearing history...');

        const response = await apiFetch('/clear_history', { method: 'POST' });

        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Server error ${response.status}: ${text}`);
        }

        const data = await response.json();

        // Clear UI elements
        latestResults = [];
        document.getElementById('tableBody').innerHTML = '';
        document.getElementById('summary').innerHTML = '';
        document.getElementById('question').value = '';

        loadStats();
        setStatus(data.message || 'History cleared');
    }
    catch (error) {
        console.error('CLEAR HISTORY ERROR:', error);
        setStatus('Error: ' + (error.message || error));
    }
}

async function handleCSVUpload() {
    try {
        const fileInput = document.getElementById('csvFile');
        if (!fileInput.files || fileInput.files.length === 0) {
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        clearResults();
        setStatus('Uploading and analyzing CSV...');
        setButtonsDisabled(true);

        const response = await apiFetch('/upload_csv', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Server error ${response.status}: ${text}`);
        }

        const data = await response.json();

        latestResults = data.results;

        let rows = '';
        data.results.forEach(item => {
            rows += `
            <tr>
                <td>${item.question}</td>
                <td>${item.bloom}</td>
                <td>${item.co}</td>
                <td>${item.po.join(", ")}</td>
            </tr>`;
        });

        document.getElementById('tableBody').innerHTML = rows;
        document.getElementById('summary').innerHTML = `
            <h3>Total Questions: ${data.total_questions}</h3>
            <h3>Bloom Distribution</h3>
            <pre>${JSON.stringify(data.bloom_distribution, null, 2)}</pre>
            <h3>CO Distribution</h3>
            <pre>${JSON.stringify(data.co_distribution, null, 2)}</pre>
        `;

        loadStats();
        await generateCoverageReport();
        setStatus('CSV analysis complete');
        setButtonsDisabled(false);
        
        // Reset file input
        fileInput.value = '';
    }
    catch (error) {
        console.error('CSV UPLOAD ERROR:', error);
        setStatus('Error: ' + (error.message || error));
        setButtonsDisabled(false);
    }
}

async function downloadPDFReport() {
    if (!latestResults || latestResults.length === 0) {
        alert('No analysis results available. Please analyze questions first.');
        return;
    }

    try {
        setStatus('Generating PDF report...');
        setButtonsDisabled(true);

        // Use direct fetch for PDF (not apiFetch which expects JSON)
        const url = window.location.origin + '/generate_pdf_report';
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ results: latestResults })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error ${response.status}: ${errorText}`);
        }

        // Get response as Blob (PDF file)
        const blob = await response.blob();

        // Create download link
        const blobUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = blobUrl;

        // Generate timestamp for filename
        const now = new Date();
        const timestamp = now.getFullYear() + 
            String(now.getMonth() + 1).padStart(2, '0') + 
            String(now.getDate()).padStart(2, '0') + '_' +
            String(now.getHours()).padStart(2, '0') + 
            String(now.getMinutes()).padStart(2, '0') + 
            String(now.getSeconds()).padStart(2, '0');

        link.download = `OBE_Report_${timestamp}.pdf`;

        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(blobUrl);

        setStatus('PDF report downloaded successfully');
        setButtonsDisabled(false);
    }
    catch (error) {
        console.error('PDF DOWNLOAD ERROR:', error);
        setStatus('Error: ' + (error.message || error));
        setButtonsDisabled(false);
    }
}