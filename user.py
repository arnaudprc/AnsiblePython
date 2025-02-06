def run_command(client, command, sudo_password):
    print(f"[INFO] Exécution de la commande : {command}")
    stdin, stdout, stderr = client.exec_command(f"echo {sudo_password} | sudo -S {command}", get_pty=True)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(output)
    if error:
        print(f"[ERROR] Erreur lors de l'exécution de la commande : {command}. Error: {error}")
    else:
        print(f"[SUCCESS] Commande exécutée avec succès : {command}")

def add_user(client, sudo_password, username, user_password):
    run_command(client, f"adduser --disabled-password --gecos '' {username}", sudo_password)
    run_command(client, f"echo '{username}:{user_password}' | sudo chpasswd", sudo_password)

def add_user_sudo(client, sudo_password, username, user_password):
    add_user(client, sudo_password, username, user_password)
    run_command(client, f"usermod -aG sudo {username}", sudo_password)