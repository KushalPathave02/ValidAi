from typing import List, TypedDict

class ValidationResult(TypedDict):
    is_valid: bool
    errors: List[str]
    warnings: List[str]
