import paramiko

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