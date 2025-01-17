import paramiko

def ssh_connect():
    hostname = input("Entrer l'adresse IP de la machine: ")
    username = input("Entrer le nom d'utilisateur: ")
    password = input("Entrer le mot de passe: ")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client, password

def run_command(client, command, sudo_password):
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(sudo_password + '\n')
    stdin.flush()
    print(stdout.read().decode())
    error = stderr.read().decode()
    if error:
        print(f"[ERROR] {command}. Error: {error}")
    else:
        print(f"[SUCCESS] {command}.")

def install_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt update && sudo apt install -y {package_name}", sudo_password)

def uninstall_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt remove -y {package_name}", sudo_password)
    run_command(client, f"sudo apt purge -y {package_name}", sudo_password)