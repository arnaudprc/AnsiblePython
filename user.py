from ssh import run_command

# Fonction pour ajouter un utilisateur sur la machine distante
def add_user(client, sudo_password, username, user_password):
    run_command(client, f"adduser --disabled-password --gecos '' {username}", sudo_password)
    run_command(client, f"echo '{username}:{user_password}' | sudo chpasswd", sudo_password)

# Fonction pour ajouter un utilisateur avec les droits sudo sur la machine distante
def add_user_sudo(client, sudo_password, username, user_password):
    add_user(client, sudo_password, username, user_password)
    run_command(client, f"usermod -aG sudo {username}", sudo_password)