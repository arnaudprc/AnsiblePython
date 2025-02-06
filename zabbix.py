import paramiko
import time

def run_command(client, command, sudo_password):
    print(f"[INFO] Exécution de la commande : {command}")
    stdin, stdout, stderr = client.exec_command(f"echo {sudo_password} | sudo -S {command}", get_pty=True)
    stdin.write(sudo_password + '\n')
    stdin.flush()
    
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            output = stdout.read().decode()
            print(f"[OUTPUT] {output}")
        if stderr.channel.recv_stderr_ready():
            error = stderr.read().decode()
            print(f"[ERROR] {error}")
        time.sleep(1)

    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print(f"[SUCCESS] Commande exécutée avec succès : {command}")
    else:
        print(f"[ERROR] Erreur lors de l'exécution de la commande : {command}. Exit status: {exit_status}")

def install_zabbix(client, sudo_password):
    DB_NAME = "zabbix"
    DB_USER = "zabbix"
    DB_PASS = "Zabbix123!"
    ZBX_VERSION = "7.0"
    TIMEZONE = "Europe/Paris"

    # Mise à jour du système
    run_command(client, "apt update && apt upgrade -y", sudo_password)

    # Vérification et installation des paquets nécessaires
    packages = [
        "mariadb-server", "mariadb-client", "apache2", "php", "php-mysql", "php-bcmath",
        "php-mbstring", "php-gd", "php-xml", "php-curl", "snmp", "iptables"
    ]
    for pkg in packages:
        run_command(client, f"dpkg -l | grep -q '^ii  {pkg} ' || apt install -y {pkg}", sudo_password)

    # Activation et démarrage de MariaDB
    run_command(client, "systemctl enable --now mariadb", sudo_password)

    # Vérification et création de la base de données
    run_command(client, f"mysql -e \"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;\"", sudo_password)
    run_command(client, f"mysql -e \"CREATE USER IF NOT EXISTS '{DB_USER}'@'localhost' IDENTIFIED BY '{DB_PASS}';\"", sudo_password)
    run_command(client, f"mysql -e \"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_USER}'@'localhost';\"", sudo_password)
    run_command(client, "mysql -e \"FLUSH PRIVILEGES;\"", sudo_password)

    # Sécurisation de MariaDB
    run_command(client, "echo -e 'n\ny\ny\ny\ny' | mariadb-secure-installation", sudo_password)

    # Vérification et installation de Zabbix
    run_command(client, f"dpkg -l | grep -q '^ii  zabbix-server-mysql ' || (wget -q https://repo.zabbix.com/zabbix/{ZBX_VERSION}/ubuntu/pool/main/z/zabbix-release/zabbix-release_{ZBX_VERSION}-1+ubuntu$(lsb_release -rs)_all.deb && dpkg -i zabbix-release_{ZBX_VERSION}-1+ubuntu$(lsb_release -rs)_all.deb && apt update && apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-agent)", sudo_password)

    # Importation du schéma Zabbix si non existant
    run_command(client, f"mysql -u{DB_USER} -p{DB_PASS} -e \"USE {DB_NAME}; SHOW TABLES;\" | grep -q 'users' || zcat /usr/share/doc/zabbix-server-mysql/create.sql.gz | mysql -u{DB_USER} -p{DB_PASS} {DB_NAME}", sudo_password)

    # Configuration des fichiers de Zabbix
    run_command(client, f"sed -i 's/# DBPassword=/DBPassword={DB_PASS}/' /etc/zabbix/zabbix_server.conf", sudo_password)
    run_command(client, f"sed -i 's/^;date.timezone =.*/date.timezone = {TIMEZONE}/' /etc/php/*/apache2/php.ini", sudo_password)

    # Configuration des règles iptables
    run_command(client, "iptables -A INPUT -p tcp --dport 80 -j ACCEPT", sudo_password)
    run_command(client, "iptables -A INPUT -p tcp --dport 443 -j ACCEPT", sudo_password)
    run_command(client, "iptables -A INPUT -p tcp --dport 10050 -j ACCEPT", sudo_password)
    run_command(client, "iptables -A INPUT -p tcp --dport 10051 -j ACCEPT", sudo_password)
    run_command(client, "iptables-save > /etc/iptables/rules.v4", sudo_password)

    # Activation et redémarrage des services
    run_command(client, "systemctl enable apache2 zabbix-server zabbix-agent mariadb", sudo_password)
    run_command(client, "systemctl restart apache2 zabbix-server zabbix-agent", sudo_password)

    # Message final
    run_command(client, "echo 'Installation réussie ! Accédez à Zabbix : http://$(hostname -I | awk '{print $1}')/zabbix'", sudo_password)
    run_command(client, "echo 'Identifiants par défaut : Admin / zabbix'", sudo_password)