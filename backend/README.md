# Backend: LLM Validation Engine

This directory contains the core of the LLM-powered validation system. It is designed as a thin orchestration layer where all validation *reasoning* is delegated to an LLM, while the Python code is responsible only for orchestration and schema enforcement.

## Architecture

The backend follows a simple, modular architecture:

```
validate_user.py (CLI Entry Point)
       ↓
app.validator.validate_user_input()
       ↓
app.llm_client.get_llm_response(prompt, input)
       ↓
   OpenAI API
       ↓
Structured JSON Response
```

### Core Principle

**Python does not contain any validation rules.** Its only jobs are:

1.  To load a JSON input.
2.  To send the input and a carefully engineered prompt to the LLM.
3.  To parse the LLM's JSON response.
4.  To ensure the response conforms to the expected output schema.
5.  To fail gracefully if the LLM returns a malformed response.

## Module Responsibilities

*   `validate_user.py`: The main command-line entry point. It handles file I/O and invokes the validator.

*   `app/validator.py`: The central orchestrator. It combines the prompt and user input, calls the LLM client, and performs a crucial safety check on the returned JSON to ensure it matches the expected schema.

*   `app/llm_client.py`: A dedicated client for communicating with the OpenAI API. It manages the API key, sets model parameters for deterministic output (`temperature=0`, `response_format='json_object'`), and handles basic API call errors.

*   `app/prompt.py`: A single source of truth for the validation logic. This file contains the system prompt that instructs the LLM on its role, the high-level validation constraints, the distinction between errors and warnings, and the strict output contract.

*   `app/schema.py`: Defines the `ValidationResult` TypedDict, which serves as the formal contract for the expected JSON output. This is used to prevent the system from accepting hallucinated or malformed fields from the LLM.

## How It Works: LLM as a Reasoning Engine

The system is designed to treat the LLM as a reasoning engine, not a simple string-matching tool. The prompt in `app/prompt.py` is the most critical component. It achieves determinism and accuracy through four key sections:

1.  **Role**: Defines the LLM's purpose (`You are a strict JSON input validator`).
2.  **Input Grounding**: Instructs the LLM to only use the provided data and not to invent missing fields.
3.  **Validation Intent**: Explains the high-level meaning of a valid profile and clearly separates blocking **errors** from non-blocking **warnings**.
4.  **Output Contract**: Forces the LLM to return *only* a JSON object that matches the exact schema, with no explanatory text.

This separation of concerns—reasoning in the prompt, orchestration in Python—creates a system that is both powerful and testable.
