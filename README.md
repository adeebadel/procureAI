# ProcureAI

### AI-Powered Tender & Bid Compliance Intelligence Platform

ProcureAI is an enterprise-oriented procurement intelligence platform that helps procurement teams analyze tender requirements, evaluate bidder submissions against those requirements, identify missing or conflicting evidence, and generate structured compliance reports.

The system is designed around **human-in-the-loop procurement**: ProcureAI assists reviewers by organizing evidence and highlighting potential compliance issues, while final procurement decisions remain with authorized human reviewers.

---

## 🚀 What Problem Does ProcureAI Solve?

Government and enterprise tenders can contain dozens of eligibility, financial, technical, certification, documentation, and delivery requirements.

Manually reviewing every bidder document can be:

* Time-consuming
* Difficult to track
* Prone to missed requirements
* Difficult to audit
* Difficult to compare consistently

ProcureAI turns lengthy tender and bidder documents into a structured compliance workflow.

---

## 🔄 How It Works

```text
Tender PDF
    ↓
Requirement Extraction
    ↓
Structured Compliance Checklist
    ↓
Bidder Documents
    ↓
Evidence Matching
    ↓
Compliance Analysis
    ↓
Human Review
    ↓
Downloadable Compliance Report
```

---

## ✨ Core Features

### 1. Tender Requirement Extraction

Upload a tender PDF and ProcureAI identifies potential requirements such as:

* Financial requirements
* Experience requirements
* Certifications
* Documentation
* Technical requirements
* Manpower requirements
* Equipment requirements
* Delivery requirements
* Security requirements
* Eligibility criteria

Each extracted requirement is associated with its source page.

---

### 2. Bidder Document Analysis

Upload one or multiple bidder PDF documents.

ProcureAI analyzes the submitted evidence against the extracted tender requirements.

---

### 3. Compliance Detection

Requirements are classified into:

| Status      | Meaning                                                   |
| ----------- | --------------------------------------------------------- |
| ✅ Satisfied | Evidence appears to support the requirement               |
| ⚠️ Review   | Potential evidence exists but requires human verification |
| ❌ Missing   | No sufficient supporting evidence was identified          |

---

### 4. Evidence Traceability

Instead of producing unexplained AI decisions, ProcureAI attempts to connect compliance findings to the source document and page.

Example:

```text
Requirement:
Average annual turnover of at least INR 5 crore

Result:
Satisfied

Evidence:
Bidder Financial Statement
Page 4
```

This makes the analysis easier for a human reviewer to verify.

---

### 5. Compliance Report Generation

ProcureAI generates a downloadable PDF report containing:

* Tender information
* Bidder information
* Overall compliance percentage
* Requirement-level results
* Evidence references
* Review items
* Missing requirements
* Human-review disclaimer

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     Tender PDF       │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │  Document Parser     │
                    │       pypdf           │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Requirement Extractor│
                    │  Rule-Based Engine   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Compliance Checklist │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   Bidder Documents   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Compliance Checker   │
                    │ Evidence Matching    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Human Review Layer   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   PDF Report         │
                    └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Gunicorn

### Document Processing

* pypdf

### Report Generation

* ReportLab

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* Render

### Version Control

* Git
* GitHub

---

## 📁 Project Structure

```text
procureai/
│
├── app.py
├── requirements.txt
├── Procfile
├── README.md
├── .gitignore
│
├── services/
│   ├── document_parser.py
│   ├── requirement_extractor.py
│   ├── compliance_checker.py
│   └── report_generator.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── uploads/
    └── .gitkeep
```

---

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd procureai
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

ProcureAI can be deployed as a Flask web service using Gunicorn.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

---

## 🧪 Testing

A sample tender and bidder document can be used to test the complete workflow.

### Test workflow

1. Upload the sample tender.
2. Review extracted requirements.
3. Upload bidder documents.
4. Run compliance analysis.
5. Review Satisfied / Review / Missing results.
6. Download the compliance report.

---

## 🔐 Human-in-the-Loop Design

ProcureAI is an **assistive procurement intelligence tool**, not an autonomous procurement decision-maker.

The system highlights potential compliance results and provides supporting evidence for human verification.

Final decisions regarding:

* Bid eligibility
* Technical qualification
* Financial qualification
* Contract awards
* Procurement outcomes

should remain with authorized procurement personnel.

---

## ⚠️ Current MVP Limitations

This project is currently an MVP.

Current limitations include:

* Rule-based requirement extraction
* PDF text extraction limitations for scanned documents
* Basic semantic/keyword evidence matching
* Limited numerical normalization
* In-memory application state
* Local file storage
* No authentication or role management
* No database-backed persistence
* No OCR pipeline for image-only PDFs

These limitations provide clear opportunities for future development.

---

## 🔮 Future Roadmap

### Phase 2 — Smarter Document Intelligence

* OCR for scanned tenders
* Table extraction
* Better numerical normalization
* Advanced semantic matching
* Local LLM integration
* Requirement dependency detection

### Phase 3 — Enterprise Features

* PostgreSQL/SQLite persistence
* User authentication
* Procurement officer roles
* Organization workspaces
* Tender version tracking
* Bidder comparison dashboards
* Audit logs

### Phase 4 — Advanced AI

* Retrieval-Augmented Generation
* Citation-aware LLM analysis
* Cross-document reasoning
* Contract clause comparison
* Automated clarification detection
* Explainable risk analysis

---

## 🎯 Why This Project?

ProcureAI demonstrates practical software engineering and applied AI concepts through a real-world enterprise workflow rather than a generic chatbot.

The project combines:

* Document processing
* Information extraction
* Rule-based intelligence
* Evidence matching
* Backend development
* Frontend development
* PDF generation
* Deployment
* Human-in-the-loop system design

---

## 👨‍💻 Project Status

**Current Version:** MVP

**Status:** Deployed

**Domain:** Procurement Technology / GovTech / Enterprise AI

**Architecture:** Flask-based web application

---

## 📌 Disclaimer

ProcureAI is a software engineering and AI prototype intended for research, demonstration, and workflow-assistance purposes.

It should not be used as the sole basis for procurement, legal, financial, eligibility, or contract-award decisions.
