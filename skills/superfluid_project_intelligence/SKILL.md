# 🧠 Project Intelligence Skill

> AI-powered blockchain project intelligence and research skill for analyzing Web3 ecosystems.

---

## Overview

Project Intelligence Skill enables AI assistants and developers to analyze blockchain projects automatically by collecting information from official sources, GitHub repositories, and project documentation.

It transforms raw project information into structured intelligence reports including project summaries, SDK detection, technology stack analysis, recommendations, integration guides, and exportable reports.

---
## ✨ Capabilities

This skill provides a complete intelligence pipeline for blockchain and Web3 projects.

### 🔍 Project Discovery

- Detects the project's official website
- Finds the official GitHub repository
- Extracts repository metadata

### 📊 Repository Analysis

- GitHub statistics
- Programming languages
- Repository activity
- Stars, forks, and contributors
- License detection

### 🧩 Technology Detection

Automatically detects:

- SDKs
- Frameworks
- Libraries
- Blockchain ecosystems
- Development tools

### 🤖 AI Intelligence

Generates:

- Executive Summary
- Project Score
- Strength Analysis
- Weakness Analysis
- Recommendations
- Integration Guide

### 📦 Export Formats

Supports exporting reports as:

- Markdown (.md)
- JSON (.json)

### ⚡ Batch Processing

Analyze multiple projects in a single execution.
---

# 📥 Inputs

The skill accepts one of the following inputs:

### Project Name

Example:

```text
Superfluid
```

### GitHub Repository

Example:

```text
https://github.com/superfluid-finance/protocol-monorepo
```

### Official Website

Example:

```text
https://www.superfluid.finance
```

### Batch File

A text file containing one project per line.

Example:

```text
Superfluid
Aave
Uniswap
EigenLayer
```

---

# 📤 Outputs

The skill generates a complete intelligence report containing:

- Project Overview
- Official Website
- GitHub Repository
- Repository Statistics
- Programming Languages
- SDK Detection
- Technology Stack
- AI-generated Summary
- Project Score
- Recommendations
- Integration Guide
- Code Examples
- Exported Markdown Report
- Exported JSON Report
---

# 🔄 Workflow

The Project Intelligence Skill follows a structured multi-stage analysis pipeline.

```text
               User Input
                    │
                    ▼
        Project Discovery
                    │
                    ▼
     Official Website Detection
                    │
                    ▼
     GitHub Repository Analysis
                    │
                    ▼
     Technology Stack Detection
                    │
                    ▼
        SDK Identification
                    │
                    ▼
      AI Intelligence Engine
                    │
                    ▼
      Scoring & Recommendation
                    │
                    ▼
      Report Generation
                    │
                    ▼
        Markdown / JSON Export
```

---

## Analysis Pipeline

### 1. Project Discovery

The skill identifies the project using:

- Project name
- Official website
- GitHub repository URL

---

### 2. Repository Research

The skill collects:

- Repository metadata
- Repository statistics
- Programming languages
- Activity metrics
- License information

---

### 3. Technology Analysis

The source code is analyzed to detect:

- SDKs
- Frameworks
- Blockchain protocols
- APIs
- Development libraries

---

### 4. Intelligence Generation

The AI engine generates:

- Executive Summary
- Project Score
- Strengths
- Weaknesses
- Recommendations
- Integration Guide

---

### 5. Report Export

The final intelligence report can be exported as:

- Markdown
- JSON

---

# ⚙️ Configuration

The skill can be configured through the project's configuration file.

## Configuration File

```text
config.py
```

### Main Configuration

| Setting | Description |
|----------|-------------|
| `APP_NAME` | Application name |
| `APP_VERSION` | Current application version |
| `GITHUB_API_URL` | GitHub API endpoint |
| `REQUEST_TIMEOUT` | HTTP request timeout |
| `MAX_RESULTS` | Maximum search results |

---

## Environment

### Python

- Python 3.11+

### Supported Platforms

- Windows
- Linux
- macOS

---

## Dependencies

Main dependencies include:

- requests
- beautifulsoup4
- ddgs
- rich

Install them using:

```bash
pip install -r requirements.txt
```

---

# 💻 Examples

## Example 1 — Analyze a Project by Name

```python
from skill import run

result = run("Superfluid")

print(result)
```

---

## Example 2 — Analyze a GitHub Repository

```python
from skill import run

result = run(
    "https://github.com/superfluid-finance/protocol-monorepo"
)

print(result)
```

---

## Example 3 — Export Intelligence Report

```python
from skill import run

result = run("Superfluid")

result.export_markdown()

result.export_json()
```

---

## Example 4 — Batch Analysis

```python
projects = [
    "Superfluid",
    "Aave",
    "Uniswap",
    "EigenLayer"
]

for project in projects:
    run(project)
```

---

## Example Output

```text
==========================================
PROJECT INTELLIGENCE REPORT
==========================================

Project:
Superfluid

Official Website:
https://www.superfluid.finance

GitHub:
https://github.com/superfluid-finance/protocol-monorepo

Project Score:
94/100

Technology Stack:
• Solidity
• TypeScript
• React

SDKs:
• ethers.js
• web3.js

Recommendation:
Highly recommended for integration.

Export:
reports/superfluid.md
reports/superfluid.json
```
---

# 🗺️ Roadmap

The following improvements are planned for future releases.

## Version 1.1

- Enhanced AI summarization
- Better repository ranking algorithm
- Additional SDK detection
- Improved recommendation engine

---

## Version 1.2

- GitLab support
- Bitbucket support
- Docker image
- REST API

---

## Version 2.0

- Web Dashboard
- Interactive Visual Reports
- LLM-powered Insights
- Multi-language Support
- Plugin Architecture
- Real-time Repository Monitoring

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to improve this skill:

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Open a Pull Request

Please read:

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md

before submitting contributions.

---

# 📄 License

This project is released under the MIT License.

See the LICENSE file for more information.

---

# 👨‍💻 Maintainer

**TEGUH572**

GitHub:

https://github.com/TEGUH572

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest new features
- 🤝 Submit Pull Requests

Every contribution helps improve the Project Intelligence Skill.

---

# 🚀 Project Intelligence Engine

> Empowering AI agents with intelligent blockchain project analysis.