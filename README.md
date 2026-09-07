# Sunny: AI Safety & Red Teaming for LLM Chatbots

This repository contains the testing infrastructure and integration scripts developed for my Bachelor's thesis in Computer Engineering, titled *"Verifica Di Sicurezza Di Chatbot Basati Su LLM Con Un Approccio Di Red Teaming"*.

The project focuses on **Sunny**, a prototype conversational AI agent designed to provide psychological support for children (aged 6-12). Due to the highly sensitive nature of the target audience, the agent was subjected to rigorous, automated security testing (Red Teaming) to ensure ethical compliance and robustness against adversarial attacks.

## 🎯 Project Objectives
*   **Vulnerability Testing:** Automated simulation of adversarial attacks to identify vulnerabilities in LLM guardrails.
*   **Defense-in-Depth:** Validation of System Prompt constraints (Hard Rules) using Chain of Thought (`<think>`) analysis.
*   **Safety Assurance:** Ensuring the agent correctly handles high-risk scenarios (e.g., self-harm, abuse) by triggering emergency protocols instead of standard conversational responses.

## 🛠️ Architecture & Tech Stack
The testing environment decouples the adversarial prompt generation from the chatbot's hosting platform, using Python as a middleware to orchestrate API calls and log results.
*   **Core Logic:** Python (Pandas, Requests, JSON).
*   **Testing Framework:** [Promptfoo](https://www.promptfoo.dev/) (used to define test suites and assert outputs via LLM-as-a-judge).
*   **LLMs Tested:** GPT-4o, Claude 3.5 Sonnet.
*   **Agent Hosting:** Aisuru Platform (Araneum Group).

## 🛡️ Vulnerabilities Tested
The automated test suite (`Top 50 Critical Prompts`) evaluated the agent's resilience against:
1.  **Jailbreaking (Role-play/DAN):** Attempts to force the agent to abandon its predefined persona.
2.  **Prompt Injection:** Hidden instructions aimed at overwriting system directives.
3.  **System Integrity (SQL Injection):** Obfuscated technical inputs to test parsing defenses.
4.  **Child Safety & Abuse:** Triggering strict safety overrides to provide external emergency contacts (e.g., Telefono Azzurro).
5.  **Emotional Manipulation & PII Leakage:** Coercion tactics and attempts to extract personal data.

## 📂 Repository Structure
*   `main.py`: Orchestration script that handles REST API authentication with the Aisuru platform, sends sequential adversarial prompts, and extracts the model's Chain of Thought from the JSON response.
*   `estrattore.py`: Utility script for parsing and formatting Promptfoo YAML outputs into CSV datasets for quantitative analysis.
*   `prompts_top50.yaml`: Configuration file defining the critical test cases, risk categories, and specific Promptfoo assertions.
*   *Note: Sensitive data, API keys, and internal endpoint URLs have been redacted for security purposes.*
