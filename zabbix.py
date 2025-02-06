import paramiko
import time

def execute_command(client, command, sudo_password=None):
    stdin, stdout, stderr = client.exec_command(command)
    if sudo_password:
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
        print(f"[SUCCESS] Command executed successfully: {command}")
    else:
        print(f"[ERROR] Error executing command: {command}. Exit status: {exit_status}")

def install_zabbix(client, sudo_password):
    # Mise à jour du système
    commands = [
        "sudo apt-get update",
        "sudo apt-get upgrade -y",
        
        # Installation de MySQL
        "sudo apt-get install -y mysql-server mysql-client",
        
        # Installation des paquets nécessaires pour Zabbix
        "sudo apt-get install -y apache2 libapache2-mod-php php php-mbstring php-gd php-xml php-bcmath php-ldap php-mysql",
        "sudo apt-get install -y zabbix-server-mysql zabbix-frontend-php zabbix-agent",
        
        # Configuration de la base de données MySQL pour Zabbix
        "sudo mysql -e \"CREATE DATABASE zabbix CHARACTER SET utf8 COLLATE utf8_bin;\"",
        "sudo mysql -e \"CREATE USER 'zabbix'@'localhost' IDENTIFIED BY 'Zabbix123!';\"",
        "sudo mysql -e \"GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';\"",
        "sudo mysql -e \"FLUSH PRIVILEGES;\"",
        
        # Configuration du frontend Zabbix
        "sudo cp /usr/share/zabbix/frontends/php/* /var/www/html/zabbix/",
        "sudo chown -R www-data:www-data /var/www/html/zabbix",
        
        # Redémarrage et activation des services
        "sudo systemctl restart apache2",
        "sudo systemctl restart zabbix-server",
        "sudo systemctl enable zabbix-server",
        "sudo systemctl enable apache2",
        
        # Démarrage des services
        "sudo systemctl start apache2",
        "sudo systemctl start zabbix-server"
    ]
    
    for command in commands:
        execute_command(client, command, sudo_password)

# Exemple d'utilisation :
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect('hostname', username='user', password='password')
# install_zabbix_and_mysql(client, 'your_sudo_password')
# client.close()
