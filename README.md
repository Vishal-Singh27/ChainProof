# ⛓️ ChainProof — Blockchain-Verified ML Model Registry & Governance

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Cryptography](https://img.shields.io/badge/Cryptography-SHA--256-4F46E5.svg)](https://en.wikipedia.org/wiki/SHA-2)
[![Blockchain](https://img.shields.io/badge/DLT-Proof--of--Work-6366F1.svg)](https://ethereum.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Cryptographic AI Governance & Supply-Chain Integrity: Anchors machine learning model weight fingerprints, performance metrics, and data-leakage certifications to an immutable blockchain ledger.**

---

## 🌟 Overview
In enterprise AI deployments (Healthcare, Fintech, Autonomous Systems), **model poisoning, unauthorized weight swaps, and unverified shadow deployments** pose severe security and regulatory risks. **ChainProof** introduces cryptographic immutability to the ML lifecycle. By computing deterministic SHA-256 binary digests of trained model artifacts (`.pkl`, `.pt`, `.onnx`) and mining governance blocks with Proof-of-Work, ChainProof guarantees that only audited, certified models execute in production serving environments.

---

## 🚀 Key Features

- **📦 Cryptographic Model Fingerprinting**: Computes byte-level SHA-256 digests for model binaries of any framework (PyTorch, Scikit-Learn, XGBoost, ONNX).
- **📋 Immutable Governance Ledger**: Records semantic versioning, training dataset references, validation scores, and data-leakage audit compliance.
- **⛏️ Proof-of-Work Mining Engine**: Mines blocks linking model hashes with difficulty-targeted cryptographic nonces and previous block hashes.
- **🔍 Production Verification Gateway**: Upload any deployed model to instantly verify if it matches the certified weights or has been tampered with.
- **⛓️ Visual Ledger Explorer**: Inspect the full historical audit trail, block difficulty, timestamps, and metric metadata.
- **📁 Pre-Packaged Demo Models**: Ships with sample model artifacts (`churn_rf_v1.pkl`, `mri_efficientnet_b0_v2.bin`) for immediate testing.

---

## 🏗️ System Architecture

```
[ Model Training Pipeline (PyTorch / Scikit-Learn / XGBoost) ]
                               │
                               ▼
        [ Exported Binary Weights (.pkl, .pt, .onnx) ]
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
    [ SHA-256 Fingerprinting ]     [ Metadata & Leakage Certification ]
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
            [ Proof-of-Work Mining Engine ]
                               │
                               ▼
            [ Immutable Governance Ledger ]
                               ▲
                               │
        [ Production Verification Gateway / CI-CD ]
```

---

## 🛠️ Tech Stack
- **Interface / Dashboard**: Streamlit with custom CSS cards and state tracking
- **Blockchain & Hashing**: Python `hashlib` SHA-256 engine, PoW mining, JSON state serialization
- **Machine Learning**: Scikit-Learn, PyTorch binary artifact support

---

## 📦 Project Structure
```
ChainProof/
├── app.py                      # Streamlit interactive application
├── registry_chain.py           # Blockchain ledger & verification methods
├── create_samples.py           # Generates sample model binaries
├── models_repo/                # Sample pre-trained models
│   ├── churn_rf_v1.pkl
│   └── mri_efficientnet_b0_v2.bin
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml             # UI theme settings
└── README.md
```

---

## ⚡ Quickstart

### Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/Vishal-Singh27/ChainProof.git
cd ChainProof

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🎯 Alignment with Datopic Technologies
Datopic delivers high-assurance product engineering across healthcare (HL7 FHIR compliance) and financial systems where verifiable AI governance and audit trails are mandatory. **ChainProof uniquely fuses machine learning model deployment with blockchain cryptography.**

---

## 📄 License
This project is licensed under the MIT License.
