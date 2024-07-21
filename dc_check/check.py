import os
import subprocess
import sys
import venv

def create_virtualenv(venv_path):
    """Create a virtual environment."""
    venv.EnvBuilder(clear=True, with_pip=True).create(venv_path)

def run_command(command, env_path=None):
    """Run a command in the shell."""
    if env_path:
        command = f"{os.path.join(env_path, 'bin', 'python')} -m {command}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def install_requirements(requirements_file, env_path):
    """Install requirements using pip-tools in the virtual environment."""
    pip_install = f"{os.path.join(env_path, 'bin', 'pip')} install pip-tools"
    run_command(pip_install)

    pip_sync = f"{os.path.join(env_path, 'bin', 'pip-sync')} {requirements_file}"
    stdout, stderr, returncode = run_command(pip_sync)
    return stdout, stderr, returncode

def check_requirements(requirements_file):
    """Check for dependency conflicts."""
    venv_path = "temp_env"
    create_virtualenv(venv_path)

    stdout, stderr, returncode = install_requirements(requirements_file, venv_path)
    if returncode != 0:
        print("Failed to install requirements:")
        print(stderr)
        cleanup(venv_path)
        return

    pip_compile = f"{os.path.join(venv_path, 'bin', 'pip-compile')} {requirements_file}"
    stdout, stderr, returncode = run_command(pip_compile)
    if returncode != 0:
        print("Dependency conflicts detected:")
        print(stderr)
    else:
        print("No dependency conflicts detected.")
    
    cleanup(venv_path)

def cleanup(venv_path):
    """Remove the virtual environment."""
    if os.path.exists(venv_path):
        if sys.platform == "win32":
            run_command(f"rmdir /S /Q {venv_path}")
        else:
            run_command(f"rm -rf {venv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_dependencies.py requirements.txt")
        sys.exit(1)

    requirements_file = sys.argv[1]
    if not os.path.isfile(requirements_file):
        print(f"File not found: {requirements_file}")
        sys.exit(1)

    check_requirements(requirements_file)
