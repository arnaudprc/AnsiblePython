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

def ldap():
