# OBE AI Analyzer (Rule-Based Version)

## Overview

OBE AI Analyzer is a rule-based educational analytics system developed for Outcome-Based Education (OBE) analysis of Operating Systems question papers.

The system automatically classifies questions according to Bloom's Taxonomy, maps them to Course Outcomes (COs) and Program Outcomes (POs), performs bulk analysis, generates academic coverage reports, and provides dashboard-based analytics.

This version is implemented entirely using rule-based techniques without Machine Learning.

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

* CO1 – Operating System Fundamentals and System Calls
* CO2 – Process Management and CPU Scheduling
* CO3 – Synchronization and Deadlock Management
* CO4 – Memory Management and Virtual Memory
* CO5 – File Systems, Storage, and Protection

### Program Outcome (PO) Mapping

Maps questions to:

* PO1 – Engineering Knowledge
* PO2 – Problem Analysis
* PO3 – Design / Development of Solutions
* PO4 – Investigation of Complex Problems
* PO5 – Modern Tool Usage

---

## Analysis Modes

### Single Question Analysis

Analyze an individual question and obtain:

* Bloom Level
* Course Outcome
* Program Outcomes

### Bulk Question Analysis

Analyze multiple questions simultaneously and generate:

* Bloom Distribution
* CO Distribution
* Coverage Statistics

---

## Dashboard Analytics

The dashboard provides:

* Total Analyses Performed
* Most Common Bloom Level
* Most Common Course Outcome
* Historical Analysis Statistics

---

## Reporting

### CSV Export

Export bulk analysis results to CSV format for further academic review and documentation.

### Coverage Analysis

Automatically generates:

* Bloom Taxonomy Distribution
* Course Outcome Distribution
* Question Coverage Summary

---

## History Tracking

Stores analysis history and provides statistical insights from previously analyzed questions.

---

## Dataset Information

Current Dataset Size:

| Dataset       | Records        |
| ------------- | -------------- |
| Bloom Dataset | 973 Questions  |
| CO Dataset    | 1032 Questions |

The datasets were manually curated and expanded using Operating Systems question banks.

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
│   └── helper_scripts.py
│
├── models/
├── uploads/
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

### Data Storage

* CSV Files

---

## How It Works

### Step 1

Enter one or more Operating Systems questions.

### Step 2

The system performs:

* Bloom Taxonomy Classification
* Course Outcome Prediction
* Program Outcome Mapping

### Step 3

Results are displayed through:

* Analysis Dashboard
* Coverage Statistics
* Distribution Reports

### Step 4

Results can be exported as CSV files.

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
Enter Question(s)
        ↓
Bloom Classification
        ↓
CO Prediction
        ↓
PO Mapping
        ↓
Coverage Analysis
        ↓
Dashboard Statistics
        ↓
CSV Export
```

---

## Screenshots

### Main Dashboard

(Add screenshot)

### Single Question Analysis

(Add screenshot)

### Bulk Analysis

(Add screenshot)

### Coverage Statistics

(Add screenshot)

---

## Educational Applications

This system can be used by:

* Faculty Members
* Course Coordinators
* Academic Auditors
* Accreditation Teams
* Outcome-Based Education Analysts

---

## Key Highlights

* Fully Rule-Based Implementation
* No Machine Learning Used
* Real-Time Question Analysis
* OBE-Focused Evaluation
* Bulk Question Processing
* CSV Export Support
* Historical Analytics Tracking
* Expanded Academic Dataset
* Lightweight and Easy to Deploy

---

## Future Scope

### Version 2: Machine Learning Edition

Planned enhancements include:

* Machine Learning-Based Bloom Classification
* Automated CO Prediction Models
* NLP-Based Question Understanding
* Performance Evaluation Metrics
* Accuracy Comparison with Rule-Based System
* Advanced Academic Analytics Dashboard

---

## Author

**Gowri Simha**

Developed as an academic project for Outcome-Based Education (OBE) analysis of Operating Systems question papers.

---

## License

This project is intended for educational and academic use.

screenshots
<img width="949" height="498" alt="image" src="https://github.com/user-attachments/assets/90fd2c28-6c12-4484-a8eb-76cb7402da18" />
