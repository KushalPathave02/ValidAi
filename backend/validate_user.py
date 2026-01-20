import sys
import json
from app.validator import validate_user_input

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_user.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        sys.exit(1)

    result = validate_user_input(user_data)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
