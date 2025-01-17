def run_command(client, command, sudo_password):
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
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

def configure_https_and_hardening(client, sudo_password):
    commands = [
        "sudo apt-get install -y openssl",
        "sudo a2enmod ssl",
        "sudo systemctl restart apache2",
        "sudo mkdir -p /etc/apache2/ssl",
        "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt -subj '/CN=esgi.com'",
        "sudo bash -c 'echo \"<VirtualHost *:443>\n    SSLEngine on\n    SSLCertificateFile /etc/apache2/ssl/apache.crt\n    SSLCertificateKeyFile /etc/apache2/ssl/apache.key\n    ServerAdmin webmaster@localhost\n    DocumentRoot /var/www/html\n    <Directory /var/www/html>\n        Options Indexes FollowSymLinks\n        AllowOverride All\n        Require all granted\n    </Directory>\n    ErrorLog /var/log/apache2/error.log\n    CustomLog /var/log/apache2/access.log combined\n</VirtualHost>\" > /etc/apache2/sites-available/default-ssl.conf'",
        "sudo a2ensite default-ssl",
        "sudo systemctl reload apache2"
    ]
    for command in commands:
        run_command(client, command, sudo_password)