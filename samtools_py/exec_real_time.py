import subprocess
import threading
import sys

def exec_real_time(command):
    """
    Executes a command and prints its stdout and stderr in real time.

    Args:
        command (list or str): The command to execute as a list of arguments
                               or a single string.
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Ensure output is treated as text
    )

    def print_stdout():
        for line in process.stdout:
            print(line, end='')  # Print without extra newline

    def print_stderr():
        for line in process.stderr:
            print(f"stderr: {line}", end='')

    stdout_thread = threading.Thread(target=print_stdout)
    stderr_thread = threading.Thread(target=print_stderr)

    stdout_thread.start()
    stderr_thread.start()

    process.wait()

    stdout_thread.join()
    stderr_thread.join()

    if process.returncode != 0:
        print(f"Command exited with code: {process.returncode}", file=sys.stderr)
