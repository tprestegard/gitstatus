import shlex
import subprocess


def run_command(cmd: str, fail_on_error: bool = True) -> str:

    # Set up subprocess
    p = subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Run and handle any errors occurring while running
    try:
        stdout, stderr = p.communicate()
    except Exception as ex:
        print(f'Error executing command "{cmd}": {str(ex)}')
        raise SystemExit(1)

    # Return output
    if p.returncode > 0:
        if fail_on_error:
            raise RuntimeError(f"Command {cmd} failed: {stderr.decode()}")
        return stderr.decode()
    else:
        return stdout.decode()
