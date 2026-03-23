# EEG Reward Replication – Team Elephant

## Overview

This project replicates reward-related ERP effects using EEG data from dataset **ds004147**.
The analysis focuses on two main ERP components:

* **FRN (Feedback-Related Negativity)** at **FCz**
* **P300** at **Pz**

The code is organized as a modular Python pipeline for:

* loading EEG data
* preprocessing raw recordings
* epoching around feedback events
* computing ERPs
* extracting mean amplitudes
* running paired statistical comparisons
* generating ERP figures and sanity-check outputs

The two main scripts to run are:

* `scripts/run_pipeline.py`
* `scripts/make_grand_average_figure.py`

---

## Project Structure

```text
eeg_reward_replication_elephant/
│
├── data/
│   └── ds004147/
│
├── scripts/
│   ├── __init__.py
│   ├── config.py
│   ├── load_data.py
│   ├── preprocess.py
│   ├── epoch.py
│   ├── erp.py
│   ├── statistics.py
│   ├── figures.py
│   ├── run_pipeline.py
│   └── make_grand_average_figure.py
│
├── outputs/
│   ├── figures/
│   ├── results/
│   ├── sanity_checks/
│   └── logs/
│
├── report/
│   ├── Final Report.pdf
│   └── Final Report.docx
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Dataset Setup

Download the dataset **ds004147** and place it in the following directory:

```
data/ds004147/
```

Example structure:

```
data/ds004147/sub-27/
data/ds004147/sub-28/
...
```

The code automatically searches each subject folder for `.vhdr` files.

---

## Environment Setup

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Recommended Python version: **3.10 or 3.11**

---

## How to Run

### Step 1: Run full pipeline

```bash
python scripts/run_pipeline.py
```

This will:

* process all subjects
* compute ERPs
* extract mean amplitudes
* run statistical tests
* generate subject-level plots

---

### Step 2: Generate grand-average figure

```bash
python scripts/make_grand_average_figure.py
```

This will:

* compute grand-average ERP across subjects
* generate the main P300 plot

---

## Output Files

After running the scripts, the following outputs are generated:

### outputs/figures/

* `sub-XX_erp.png` → ERP plots for each subject
* `grand_average_pz.png` → Grand-average ERP figure

### outputs/results/

* `mean_amplitudes.csv` → FRN and P300 values
* `statistics.csv` → statistical comparison results

### outputs/sanity_checks/

* `sanity_checks.txt` → pipeline validation checks

### outputs/logs/

* `pipeline.log` → execution logs

---

## Configuration

Key parameters are defined in:

```
scripts/config.py
```

This includes:

* subject list
* ERP time windows
* channel selection (FCz, Pz)
* output paths

You can modify this file to change analysis settings.

---

## Reproducibility

This project is designed for reproducible EEG analysis:

* modular pipeline structure
* fixed processing steps
* automatic output generation
* logging of all operations

All results can be reproduced by running the two main scripts.

---

## Report

The final report is included in:

```
report/Final Report.pdf
```

---

## Authors

Team Elephant

* Siddhant Sharma
* Pawan
