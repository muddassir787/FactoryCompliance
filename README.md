# FactoryCompliance
# Factory Compliance & Alert Escalation System

## Overview

The Factory Compliance & Alert Escalation System is an AI-powered workplace safety monitoring platform that automatically detects unsafe behaviors from factory surveillance videos, classifies risk severity, generates compliance reports, stores audit records, and visualizes alerts through a live monitoring dashboard.

The system combines Computer Vision, Rule-Based Compliance Checking, Database Logging, and Real-Time Monitoring into a single end-to-end pipeline.

---

# Project Objective

The goal of this project is to automate Occupational Health and Safety (OHS) compliance monitoring by:

* Processing factory surveillance videos.
* Detecting unsafe worker behaviors.
* Comparing observations against compliance policy rules.
* Classifying risk severity.
* Triggering alerts.
* Generating compliance reports.
* Maintaining an audit trail.
* Providing a live operations dashboard.

---

# Compliance Behaviors Monitored

The system currently supports the following unsafe behaviors:

| Class ID | Behavior                  |
| -------- | ------------------------- |
| 0        | Safe Walkway Violation    |
| 1        | Unauthorized Intervention |
| 2        | Opened Panel Cover        |
| 3        | Forklift Overload         |

---

# System Architecture

```text
Factory Video
      │
      ▼
Video Reader
(OpenCV)
      │
      ▼
Object Detection
(YOLO)
      │
      ▼
Violation Detection Engine
      │
      ▼
Severity Classification
      │
      ▼
Escalation Engine
      │
      ├────────► Alert Generation
      │
      ▼
Report Generator
(JSON)
      │
      ▼
SQLite Database
(compliance.db)
      │
      ▼
Streamlit Dashboard
```

---

# Project Structure

```text
FactoryCompliance/

├── data/
│   ├── videos/
│ 
│
├── database/
│   ├── db.py
│   └── compliance.db
│
├── outputs/
│   └── reports/
│
├── src/
│   ├── detection/
│   │   ├── video_reader.py
│   │   ├── person_detector.py
│   │   └── walkway.py
│   │
│   ├── policy/
│   │   └── rules.py
│   │
│   ├── severity/
│   │   └── severity.py
│   │
│   ├── escalation/
│   │   └── escalate.py
│   │
│   ├── reports/
│   │   └── report.py
│   │
│   └── dashboard/
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Technology Stack

## Computer Vision

* YOLOv11
* OpenCV

## Backend

* Python

## Database

* SQLite

## Reporting

* JSON

## Dashboard

* Streamlit

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-repository/factory-compliance-system.git

cd factory-compliance-system
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the System

## Step 1: Run Detection Engine

```bash
python main.py
```

The system will:

1. Read video frames.
2. Detect workers.
3. Check compliance rules.
4. Identify violations.
5. Assign severity.
6. Generate reports.
7. Save results to SQLite.

---

## Step 2: Run Dashboard

Open a second terminal:

```bash
streamlit run app.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

# End-to-End Workflow

## Phase 1 — Video Processing

The video reader loads surveillance footage frame-by-frame.

```text
Video
  ↓
Frames
```

---

## Phase 2 — Object Detection

YOLO detects workers and relevant objects.

```text
Frame
  ↓
YOLO
  ↓
Bounding Boxes
```

Example:

```text
Person
Forklift
Machine
Panel
```

---

## Phase 3 — Compliance Checking

Detected objects are evaluated against safety rules.

Example:

```text
Worker outside safe walkway
      ↓
Walkway Violation
```

---

## Phase 4 — Severity Classification

Each violation is assigned a severity level.

| Severity | Description              |
| -------- | ------------------------ |
| LOW      | Minimal risk             |
| MEDIUM   | Unsafe behavior observed |
| HIGH     | Significant safety risk  |
| CRITICAL | Immediate danger         |

Example Mapping:

```text
Opened Panel → LOW

Walkway Violation → MEDIUM

Unauthorized Intervention → HIGH

Forklift Overload → CRITICAL
```

---

## Phase 5 — Escalation

Severity determines the response.

### LOW / MEDIUM

```text
Database Log Only
```

### HIGH / CRITICAL

```text
Database Log
+
Real-Time Alert
```

---

## Phase 6 — Report Generation

A structured JSON report is automatically created.

Example:

```json
{
  "event_id": "123",
  "behavior_class": "walkway_violation",
  "severity": "MEDIUM"
}
```

Stored in:

```text
outputs/reports/
```

---

## Phase 7 — Database Storage

Reports are inserted into:

```text
database/compliance.db
```

Table:

```text
violations
```

---

# Database Schema

```sql
CREATE TABLE violations(

event_id TEXT PRIMARY KEY,

timestamp TEXT,

clip_id TEXT,

zone TEXT,

behavior_class TEXT,

policy_rule_ref TEXT,

event_description TEXT,

severity TEXT,

escalation_action TEXT

);
```

---

# Dashboard Features

## Live Feed Monitor

Displays:

* Processed video
* Detection status
* Active alerts

---

## Alert Timeline

Displays:

* Chronological events
* Severity indicators
* Real-time updates

---

## Historical Logs

Supports:

* Severity filtering
* Behavior filtering
* CSV export

---

# Sample Flow

```text
Factory Video
      ↓
Person Detected
      ↓
Outside Walkway
      ↓
Violation Detected
      ↓
Severity = MEDIUM
      ↓
JSON Report Created
      ↓
Inserted into compliance.db
      ↓
Displayed on Dashboard
```

---

# Output Files

## JSON Reports

```text
outputs/reports/
```

Example:

```text
2fd6a7e9.json
```

---

## SQLite Database

```text
database/compliance.db
```

---

# Future Improvements

The current implementation is a Minimum Viable Product (MVP).

Future enhancements:

* Forklift Detection
* Block Counting
* Electrical Panel Detection
* Safety Vest Detection
* Real-Time CCTV Streaming
* FastAPI Backend
* WebSocket Alerts
* PostgreSQL
* Docker Deployment
* Kubernetes Deployment
* Multi-Camera Support
* LLM-Based Policy Parsing
* RAG Compliance Assistant

---

# Author

Muddassir Hussain

BS Data Science

Factory Compliance & Alert Escalation System

AI + Computer Vision + Safety Monitoring Platform
