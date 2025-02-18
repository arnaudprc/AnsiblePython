import paramiko

# Fonction pour exécuter une commande sur la machine distante
def run_command(client, command, sudo_password, description):
    print(f"[INFO] {description}...")
    stdin, stdout, stderr = client.exec_command(f"echo {sudo_password} | sudo -S {command}", get_pty=True)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(output)
    if error:
        print(f"[ERROR] {description}. Error: {error}")
    else:
        print(f"[SUCCESS] {description}.")

# Fonction pour se connecter à une machine distante via SSH
def ssh_connect(hostname=None):
    while True:
        try:
            if hostname is None:
                hostname = input("Entrer l'adresse IP de la machine: ")
            username = input("Entrer le nom d'utilisateur: ")
            password = input("Entrer le mot de passe: ")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, username=username, password=password)
            print("[INFO] Connexion réussie")
            return client, password
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("[ERROR] Connexion échouée : Adresse IP invalide ou inaccessible. Veuillez réessayer.")
            hostname = None
        except paramiko.AuthenticationException:
            print("[ERROR] Connexion échouée : Authentification échouée. Veuillez vérifier le nom d'utilisateur et le mot de passe.")
        except Exception as e:
            print(f"[ERROR] Connexion échouée : {str(e)}. Veuillez réessayer.")

# Fonction pour installer un package sur la machine distante
def install_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt update && sudo apt install -y {package_name}", sudo_password, f"Installation du package {package_name}")

# Fonction pour désinstaller un package sur la machine distante
def uninstall_package(client, package_name, sudo_password):
    run_command(client, f"sudo apt remove -y {package_name}", sudo_password, f"Désinstallation du package {package_name}")
    run_command(client, f"sudo apt purge -y {package_name}", sudo_password, f"Purge du package {package_name}")