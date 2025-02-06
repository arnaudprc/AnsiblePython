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

def add_user(client, sudo_password, username, user_password):
    run_command(client, f"adduser --disabled-password --gecos '' {username}", sudo_password, f"Ajout de l'utilisateur {username}")
    run_command(client, f"echo '{username}:{user_password}' | sudo chpasswd", sudo_password, f"Définition du mot de passe pour l'utilisateur {username}")

def add_user_sudo(client, sudo_password, username, user_password):
    add_user(client, sudo_password, username, user_password)
    run_command(client, f"usermod -aG sudo {username}", sudo_password, f"Ajout de l'utilisateur {username} au groupe sudo")
