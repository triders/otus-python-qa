import subprocess
from datetime import datetime


def get_stdout(command: str, args: str, to_file=False):
    stdout = subprocess.run([command, args], capture_output=True).stdout.decode()
    if to_file:
        with open(f"{datetime.utcnow()}-stdout.txt", mode="w") as file:
            file.write(stdout)
    return stdout


def parse_ps_stdout_to_dict(stdout: str):
    """'USER', 'PID', '%CPU', '%MEM', 'VSZ', 'RSS', 'TT', 'STAT', 'STARTED', 'TIME', 'COMMAND'"""
    processes_list = stdout.split("\n")[:-1]  # excluding columns' names [0] and trailing \n [-1]
    processes_headers_list = processes_list.pop(0).split()

    processes_dict = {}
    for process in processes_list:
        process_values = process.split(None, 10)  # n=10 to avoid splitting last column "COMMAND" (may contain spaces)
        processes_dict.update({process_values[1]: dict(zip(processes_headers_list, process_values))})

    return processes_dict


if __name__ == "__main__":
    ps_stdout = get_stdout("ps", "aux", to_file=True)
    processes = parse_ps_stdout_to_dict(ps_stdout)
