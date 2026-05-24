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

<img width="1909" height="962" alt="Screenshot 2026-05-24 164719" src="https://github.com/user-attachments/assets/ca577e3b-bdff-436a-8998-5421cdebb8c8" />

<img width="1911" height="979" alt="Screenshot 2026-05-24 165521" src="https://github.com/user-attachments/assets/28db8180-3f7b-476f-bd43-efe85c8a3fa3" />

<img width="1918" height="983" alt="Screenshot 2026-05-24 165421" src="https://github.com/user-attachments/assets/c95e2953-8b55-4c29-bbac-271c7e71eea8" />

<img width="1874" height="980" alt="Screenshot 2026-05-24 165555" src="https://github.com/user-attachments/assets/173cd98b-06fa-421b-8c40-9bf12e41c002" />

<img width="1239" height="351" alt="Screenshot 2026-05-24 165735" src="https://github.com/user-attachments/assets/0cb4a830-df26-4f76-9185-e7362bfbb6ff" />
