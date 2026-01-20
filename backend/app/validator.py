import json
from typing import Dict, Any

from .llm_client import get_llm_response
from .prompt import SYSTEM_PROMPT
from .schema import ValidationResult

def validate_user_input(user_data: Dict[str, Any]) -> ValidationResult:
    raw_response = get_llm_response(SYSTEM_PROMPT, user_data)

    if not raw_response:
        return {
            "is_valid": False,
            "errors": ["Failed to get a response from the validation service."],
            "warnings": []
        }

    try:
        validated_data = json.loads(raw_response)
        
        # Basic schema check to ensure the LLM is behaving
        required_keys = {"is_valid", "errors", "warnings"}
        if not required_keys.issubset(validated_data.keys()):
            raise KeyError("LLM response is missing required keys.")

        return validated_data
    except (json.JSONDecodeError, KeyError) as e:
        return {
            "is_valid": False,
            "errors": [f"Failed to parse or validate the LLM response: {e}"],
            "warnings": []
        }
