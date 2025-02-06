import paramiko
from user import run_command  # Assurez-vous que run_command est défini dans user.py

def ssh_connect():
    hostname = input("Entrer l'adresse IP de la machine: ")
    username = input("Entrer le nom d'utilisateur: ")
    password = input("Entrer le mot de passe: ")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client, password

def install_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt update && sudo apt install -y {package_name}", sudo_password)

def uninstall_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt remove -y {package_name}", sudo_password)