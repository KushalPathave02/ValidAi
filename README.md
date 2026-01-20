# LLM-Powered Input Validator

This project demonstrates a modern approach to input validation by delegating the core reasoning to a Large Language Model (LLM) instead of using traditional, rule-based validation libraries like regex or Pydantic. The Python code acts as a thin orchestrator, while the LLM is responsible for interpreting high-level constraints and producing a structured JSON output.

## Data Validation Image : <img width="1437" height="842" alt="Screenshot 2026-01-20 at 8 46 25 PM" src="https://github.com/user-attachments/assets/dced4fc8-bc21-4d7c-800e-f8aac2150965" />

## Data Invalidation Image :<img width="1437" height="842" alt="Screenshot 2026-01-20 at 8 51 49 PM" src="https://github.com/user-attachments/assets/cbf8d267-700c-4219-813c-784d48c2fed1" />

## Project Goal

The primary goal is to build a deterministic, testable, and LLM-native validation system that can:

1.  Read a raw JSON user profile.
2.  Use an LLM to decide if the input is valid based on high-level constraints.
3.  Distinguish between critical **errors** (which invalidate the input) and non-blocking **warnings**.
4.  Return a strict, predictable JSON output.
5.  Be rigorously tested using an automated evaluation framework (`promptfoo`).

## Design Philosophy: Reasoning over Rules

This project is founded on the principle that LLMs excel at reasoning about intent rather than just matching patterns. Instead of providing a brittle list of low-level rules (e.g., "phone must be 10 digits"), we provide high-level, real-world constraints (e.g., "phone must follow the E.164 international standard").

This approach offers several advantages:

*   **Flexibility**: The validation logic is more adaptable to complex, real-world standards.
*   **Maintainability**: Prompts are often easier to read and modify than complex regex or nested conditional logic.
*   **Holistic Reasoning**: The LLM can reason about the relationships between fields (e.g., a mismatch between a phone country code and the user's country).

Python's role is strictly limited to orchestration and schema enforcement, ensuring that the final output is always predictable and safe to consume, even if the LLM's response is malformed.

## How to Run the Validator

### Prerequisites

*   Python 3.7+
*   A Groq API key.

### 1. Set Up the Backend

1.  **Navigate to the backend directory:**

    ```bash
    cd llm-input-validator/backend
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**

    *   Create a `.env` file by copying the example:

        ```bash
        cp .env.example .env
        ```

    *   Add your Groq API key to the `.env` file:

        ```
        GROQ_API_KEY="your_groq_api_key_here"
        ```

        Optionally, you can override the default Groq model:

        ```
        GROQ_MODEL="llama-3.1-8b-instant"
        ```

### 2. Run the CLI Validator

You can use the simple CLI wrapper in the `frontend` directory to test the validator with sample inputs.

1.  **Navigate to the CLI directory:**

    ```bash
    cd llm-input-validator/frontend/cli
    ```

2.  **Run with a valid user profile:**

    ```bash
    python run_validator.py sample_inputs/valid_user.json
    ```

3.  **Run with an invalid user profile:**

    ```bash
    python run_validator.py sample_inputs/invalid_user.json
    ```

### 3. Run the Web UI

The project includes a simple static web UI in `frontend/web` and a small API server in the backend.

1.  **Start the backend API server (in one terminal):**

    ```bash
    cd llm-input-validator/backend
    uvicorn server:app --reload --port 8000
    ```

2.  **Serve the web UI (in another terminal):**

    ```bash
    cd llm-input-validator
    python3 -m http.server 5173 --directory frontend/web
    ```

3.  **Open the app:**

    Visit `http://localhost:5173/index.html`.

## How to Run Evaluations

Automated evaluations are managed by `promptfoo`. This allows us to test the prompt's stability and correctness across multiple test cases.

### 1. Install Promptfoo

If you don't have it installed, you can install it via npm:

```bash
npm install -g promptfoo
```

### 2. Run the Evals

1.  **Navigate to the `evals` directory:**

    ```bash
    cd llm-input-validator/evals
    ```

2.  **Run the evaluation suite:**

    ```bash
    promptfoo eval
    ```

    This command will execute the test cases defined in `promptfoo.yaml` against the prompt and assert that the outputs are correct.

## Design Tradeoffs

*   **Latency**: LLM-based validation will inherently have higher latency than traditional, local validation libraries. This approach is best suited for asynchronous validation or scenarios where a few hundred milliseconds of delay is acceptable.
*   **Cost**: Every validation is an API call, which incurs a cost. This may not be suitable for high-throughput, low-cost validation scenarios.
*   **Determinism**: While we enforce determinism by setting `temperature=0` and using a specific model version, the underlying model can change, potentially affecting validation outcomes over time. Regular evaluation is crucial to mitigate this risk.
