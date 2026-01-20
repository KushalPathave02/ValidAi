import sys
import subprocess
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_validator.py <path_to_json_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    backend_script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'validate_user.py')

    if not os.path.exists(input_file_path):
        print(f"Error: Input file not found at {input_file_path}")
        sys.exit(1)

    try:
        # Ensure the backend's dependencies are installed.
        # In a real project, you might handle this more gracefully (e.g., virtual environments).
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', os.path.join(os.path.dirname(backend_script_path), 'requirements.txt')], check=True, capture_output=True)
        
        # Run the backend validation script as a subprocess
        result = subprocess.run(
            [sys.executable, backend_script_path, input_file_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except FileNotFoundError:
        print(f"Error: Backend script not found at {backend_script_path}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print("Error running the validation script:")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
