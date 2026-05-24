# GenAI Intercept Node

**An Enterprise-Grade Data Leakage Prevention (DLP) Proxy for Large Language Models.**

## Overview

As corporate AI adoption accelerates, the risk of employees pasting sensitive PII or trade secrets into public LLMs is a massive security vulnerability. The GenAI Intercept Node acts as a secure reverse-proxy. It intercepts outbound prompts and file uploads, strips them of sensitive data using pattern recognition, and securely logs the breach attempt before allowing the sanitized data to reach the LLM.

## Architecture & Tech Stack

- **Backend:** Python / Flask
- **AI Engine:** Llama 3.1 (via Groq API)
- **Database:** SQLite (Secure Audit Vault)
- **Frontend:** HTML5 / Tailwind CSS (Custom Dark Mode UI)
- **Security Layer:** Real-time RegEx stream scanning and document parsing

## Core Features

1. **The Dual-AI Sentry:** Combines hardcoded RegEx stripping for structured data (Credentials, IDs, Credit Cards) with LLM behavioral alignment for unstructured data.
2. **File Intercept Engine:** Parses and scrubs raw `.txt` file uploads seamlessly before merging them with the user prompt.
3. **Zero-Trust Admin Vault:** Session-based authentication restricts access to the security logs.
4. **Compliance Reporting:** One-click CSV exports of all network intercept events.
