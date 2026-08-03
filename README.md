# ⚡ Accelerated Code Engine (ACE)
> **Hybrid AI & AST Mathematical Reduction Engine for High-Performance Code Refactoring**

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-000000.svg)](https://nextjs.org/)
[![Ollama](https://img.shields.io/badge/AI Engine-Ollama%20Local-FF6F61.svg)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Overview

**Accelerated Code Engine (ACE)** is an advanced, privacy-first Full-Stack developer tool designed to detect algorithmic bottlenecks and automatically refactor low-efficiency source code across multiple programming languages. 

By combining **AST (Abstract Syntax Tree)** static analysis with **Local Large Language Models (LLMs via Ollama)**, ACE transforms high-complexity nested control structures—such as triple-nested loops $O(n^3)$ or unsafe pointer manipulations—into closed-form mathematical equations $O(1)$ or high-throughput functional paradigms (e.g., Rust Iterators, JS Chained Streams, C++ STL algorithms).

---

## 🔥 Key Features

- **🧮 Mathematical Loop Reduction $O(n^k) \rightarrow O(1)$:** Automatically isolates nested summations and replaces recursive/iterative runtime overhead with direct mathematical formulas.
- **⚡ Modern Idiomatic Refactoring:** Rewrites legacy C-style loops into modern, high-performance constructs (`filter`, `map`, `reduce`, Java `IntStream`, Rust closures).
- **🔒 Privacy-First & Offline Engine:** Runs 100% locally via **Ollama** (`llama3.1` / `deepseek-coder`). Zero source code is exposed to external cloud APIs.
- **🌐 Multi-Language Support:** Full optimization pipeline tailored for **Python**, **C**, **C++**, **Java**, **JavaScript**, and **Rust**.
- **💻 Interactive Side-by-Side UI:** Next.js & Tailwind CSS frontend displaying real-time code diffing, mathematical explanations, and complexity analysis.

---

## 🏗️ Architecture & Technology Stack



┌─────────────────┐       JSON Payload       ┌────────────────────────┐
│   Next.js UI    │  ────────────────────►   │   FastAPI Backend      │
│ (Monaco/Diffs)  │  ◄────────────────────   │ (API Router & Engine)  │
└─────────────────┘      Refactored Code     └───────────┬────────────┘
│
Local HTTP POST /generate
│
▼
┌────────────────────────┐
│   Ollama Local LLM     │
│  (llama3.1 / DeepSeek) │
└────────────────────────┘






* **Frontend:** Next.js 14, React, Tailwind CSS, Lucide Icons.
* **Backend:** FastAPI (Python 3.11), Uvicorn, Pydantic.
* **AI Inference:** Ollama local server running quantized open-source LLMs.

---

## 🚀 Quick Start & Installation

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://www.python.org/) (v3.11+)
- [Ollama](https://ollama.ai/) installed and running locally.

---

### 1️⃣ Setup Local LLM Model
Ensure Ollama is running and pull your preferred model:
```bash
ollama run llama3.1
2️⃣ Backend Setup (FastAPI)
Bash
# Clone repository
git clone [https://github.com/YOUR_USERNAME/accelerated-code-engine.git](https://github.com/YOUR_USERNAME/accelerated-code-engine.git)
cd accelerated-code-engine

# Create & activate virtual environment (Optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn requests pydantic

# Start backend server
python -m uvicorn backend.app.api:app --reload --port 8000
Backend will be live at: http://localhost:8000

3️⃣ Frontend Setup (Next.js)
Open a new terminal window:

Bash
cd accelerated-code-engine/frontend

# Install Node dependencies
npm install

# Run development server
npm run dev
Frontend will be live at: http://localhost:3000
🛡️ License
Distributed under the MIT License. See LICENSE for more information.
