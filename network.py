import paramiko
import time
from ssh import run_command, ssh_connect

# Fonction pour obtenir la liste des interfaces réseau
def get_network_interfaces(client):
    stdin, stdout, stderr = client.exec_command("ip link show")
    output = stdout.read().decode()
    interfaces = []
    for line in output.split('\n'):
        if ': ' in line:
            interface = line.split(': ')[1].split('@')[0]
            if interface != 'lo':  # Exclure l'interface loopback
                interfaces.append(interface)
    return interfaces

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
        addresses:
          - {dns}
"""
    command = f"echo '{netplan_config}' | sudo bash -c 'cat > /etc/netplan/50-cloud-init.yaml'"
    run_command(client, command, sudo_password, "Configuration du réseau")
    run_command(client, "sudo netplan apply", sudo_password, "Application de la configuration réseau")
    run_command(client, "sudo systemctl restart systemd-networkd", sudo_password, "Redémarrage de systemd-networkd")

    # Nouvelle adresse IP
    new_ip = address.split('/')[0]
    
    print(f"[INFO] Fermeture de l'ancienne connexion SSH...")
    client.close()
    
    # Tentative de reconnexion
    max_attempts = 10
    wait_time = 5

    for attempt in range(max_attempts):
        try:
            print(f"Tentative de reconnexion à {new_ip}... (Essai {attempt + 1}/{max_attempts})")
            new_client, new_sudo_password = ssh_connect(new_ip)
            print(f"Reconnexion réussie à {new_ip} !")
            return new_client, new_sudo_password
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(f"Connexion échouée. Nouvelle tentative dans {wait_time} secondes...")
            time.sleep(wait_time)

    print("Échec de la reconnexion après plusieurs tentatives.")
    return None, None
