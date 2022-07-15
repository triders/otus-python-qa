import os
import paramiko

from ssh_auth import HOST, USERNAME, PASSWORD

PATH_TO_KEY = os.path.expanduser("~/.ssh/id_ed25519")


def connect_via_username_and_password(hostname, username, password) -> paramiko.client:
    with paramiko.client.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Starting connection to '{hostname}' via username '{username}'")

        client.connect(hostname=hostname, username=username, password=password)

        _, _stdout, _ = client.exec_command("ls ~")
        print(_stdout.read().decode())
        print(f"Closing connection to '{hostname}'")


def connect_via_ssh_key(hostname, path_to_sshkey) -> paramiko.client:
    with paramiko.client.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Starting connection to '{hostname}' via ssh key located at '{path_to_sshkey}'")

        client.connect(hostname=hostname, key_filename=path_to_sshkey)

        _, _stdout, _ = client.exec_command("ls ~")
        print(_stdout.read().decode())
        print(f"Closing connection to '{hostname}'")


if __name__ == "__main__":
    connect_via_username_and_password(hostname=HOST, username=USERNAME, password=PASSWORD)
    connect_via_ssh_key(hostname=HOST, path_to_sshkey=PATH_TO_KEY)

