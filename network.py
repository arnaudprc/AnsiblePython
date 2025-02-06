import paramiko

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

def configure_network(client, sudo_password, interface, address, gateway, dns):
    netplan_config = f"""
network:
  version: 2
  ethernets:
    {interface}:
      addresses:
        - {address}
      gateway4: {gateway}
      nameservers:
        addresses: [{dns}]
"""
    command = f"echo '{netplan_config}' | sudo tee /etc/netplan/50-cloud-init.yaml"
    run_command(client, command, sudo_password)
    run_command(client, "sudo netplan apply", sudo_password)

def main():
    hostname = input("Entrez le nom d'hôte ou l'adresse IP de la machine distante: ")
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    interface = input("Entrez le nom de l'interface réseau : ")
    address = input("Entrez l'adresse IP avec le masque CIDR : ")
    gateway = input("Entrez l'adresse de la passerelle : ")
    dns = input("Entrez l'adresse du serveur DNS : ")

    configure_network(client, password, interface, address, gateway, dns)

    client.close()

if __name__ == "__main__":
    main()