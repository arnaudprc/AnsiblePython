import paramiko

def run_command(client, command, sudo_password):
    stdin, stdout, stderr = client.exec_command(f"echo {sudo_password} | sudo -S {command}", get_pty=True)
    stdin.write(sudo_password + '\n')
    stdin.flush()
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(output)
    if error:
        print(f"[ERROR] {command}. Error: {error}")
    else:
        print(f"[SUCCESS] {command}.")

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
    # Écrire la configuration directement dans le fichier distant
    command = f"echo '{netplan_config}' | sudo tee /etc/netplan/50-cloud-init.yaml"
    run_command(client, command, sudo_password)

    # Appliquer la nouvelle configuration sur la machine distante
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