import subprocess
from datetime import datetime
from collections import OrderedDict


def get_linux_command_stdout(command: str, args: str):
    stdout = subprocess.run([command, args], capture_output=True).stdout.decode()
    return stdout


def get_ps_stdout_dict():
    ps_aux_stdout = get_linux_command_stdout(command="ps", args="aux")
    processes_list = ps_aux_stdout.split("\n")[:-1]  # excluding columns' names [0] and trailing \n [-1]
    processes_headers_list = processes_list.pop(0).split()

    processes_dict_raw = {}
    for process in processes_list:
        process_values = process.split(None, 10)  # n=10 to avoid splitting last column "COMMAND" (may contain spaces)
        processes_dict_raw.update({process_values[1]: dict(zip(processes_headers_list, process_values))})

    # convert strings to integers or float
    processes_dict = {}
    for i in processes_dict_raw.items():
        k, v = i[0], i[1]
        processes_dict.update({
            int(k): {
                "USER": v["USER"],
                "PID": int(v["PID"]),
                "%CPU": float(v["%CPU"]),
                "%MEM": float(v["%MEM"]),
                "COMMAND": v["COMMAND"]
            }
        })
    return processes_dict


def ps_aux_stats(to_file=True):
    processes = get_ps_stdout_dict()

    # users
    users = set()
    for process in processes.items():
        users.add(process[1]["USER"])
    users_str = str(users)[1:-1].replace(", ", "\n")

    # total processes
    total_processes_running = len(processes)

    # users' processes
    user_processes = {user: 0 for user in users}
    for process in processes.items():
        user = process[1]["USER"]
        user_processes[user] += 1
    user_processes = OrderedDict(sorted(user_processes.items(), key=lambda t: -t[1]))
    user_processes_str = str(user_processes)[14:-3].replace("), (", "\n    ")
    # total memory and CPU used
    total_memory_used = 0
    total_cpu_used = 0
    for process in processes.items():
        total_memory_used += process[1]["%MEM"]
        total_cpu_used += process[1]["%CPU"]

    # processes with the greatest memory or CPU usage
    max_memory = (None, 0)
    max_cpu = (None, 0)
    for process in processes.values():
        name, cpu, mem = process["COMMAND"], process["%CPU"], process["%MEM"]
        max_cpu = (name, cpu) if cpu > max_cpu[1] else max_cpu
        max_memory = (name, mem) if mem > max_memory[1] else max_memory

    if to_file:
        with open(f"{datetime.utcnow()}-ps_aux_stdout.txt", mode="w") as file:
            file.write(f""">>>>> SYSTEM REPORT <<<<<

* Total processes running: {total_processes_running}
\\__Active users and how many processes run on their behalf: 
    {user_processes_str}

* Total memory used: {round(total_memory_used, 2)} mb
\\__ Process with the greatest memory usage ({max_memory[1]} mb): 
     '{max_memory[0]}'

* Total CPU used: {round(total_cpu_used, 2)}%
\\__ Process with the greatest CPU usage ({max_cpu[1]}%): 
     '{max_cpu[0]}' 
""")


if __name__ == "__main__":
    ps_aux_stats()
