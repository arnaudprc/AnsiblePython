import paramiko

def ssh_connect():
    hostname = input("Entrer l'adresse IP de la machine: ")
    username = input("Entrer le nom d'utilisateur: ")
    password = input("Entrer le mot de passe: ")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client, password

def run_command(client, command, sudo_password, description):
    print(f"[INFO] {description}...")
    
    # Exécute la commande sur la machine distante avec sudo
    stdin, stdout, stderr = client.exec_command(f"echo {sudo_password} | sudo -S {command}", get_pty=True)
    
    # Lit la sortie de la commande
    output = stdout.read().decode()
    error = stderr.read().decode()

    # Affiche la sortie de la commande si elle existe
    if output:
        print(output)

    # Affiche l'erreur de la commande si elle existe
    if error:
        print(f"[ERROR] {description}. Error: {error}")
    else:
        print(f"[SUCCESS] {description}.")

def install_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt update && sudo apt install -y {package_name}", sudo_password)

def uninstall_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt remove -y {package_name}", sudo_password)
    run_command(client, f"sudo apt purge -y {package_name}", sudo_password)