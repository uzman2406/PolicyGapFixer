# PolicyGapFixer: Offline LLM Policy Auditor

An offline, local LLM-based system for analyzing and improving cybersecurity policies against CIS/NIST standards.

## Features
- 🔒 **100% Offline Operation**: No internet connection required
- 📊 **Gap Analysis**: Compare policies against CIS MS-ISAC NIST Framework
- ✍️ **Policy Revision**: Automatically suggest improvements
- 🗺️ **Roadmap Generation**: NIST-aligned implementation plan
- 🏠 **Local LLM**: Runs on consumer hardware (Llama 3.2 3B)

## Installation

### Prerequisites
- Python 3.8+
- 8GB RAM minimum (16GB recommended)
- 5GB free disk space

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd PolicyGapFixer

Step 2: Set Up Virtual Environment
bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Install Ollama
Download and install Ollama from https://ollama.ai/download

Step 5: Download LLM Model
bash
ollama pull llama3.2:3b
Step 6: Prepare Reference Data
Download the CIS MS-ISAC NIST Cybersecurity Framework Policy Template Guide (2024)

Save as data/cis-ms-isac-nist-cybersecurity-framework-policy-template-guide-2024.pdf

Build knowledge base:

bash
python src/build_knowledge_base.py
Usage
Basic Usage
bash
# Process a single policy file
python src/main.py path/to/your_policy.txt

# Process all test policies
python src/main.py
Using as Module
python
from src.main import PolicyGapFixer

fixer = PolicyGapFixer()
results = fixer.process_policy(policy_text, "policy_name")
Test Run
bash
python test_quick.py
Project Structure
text
PolicyGapFixer/
├── src/                    # Source code
│   ├── main.py           # Main pipeline
│   ├── llm_handler.py    # LLM interface
│   ├── embedding_system.py # Vector store
│   ├── gap_analyzer.py   # Gap analysis logic
│   └── policy_reviser.py # Policy revision logic
├── data/                  # Reference documents
├── models/               # FAISS index & embeddings
├── test_policies/        # Sample policies
├── outputs/              # Generated results
├── requirements.txt      # Dependencies
└── README.md            # This file
