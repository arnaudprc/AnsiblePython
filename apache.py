from ssh import run_command

# Fonction pour configurer Apache
def configure_https_and_hardening(client, sudo_password):
    commands = [
        "apt-get install -y openssl",
        "a2enmod ssl",
        "a2enmod rewrite",
        "systemctl restart apache2",
        "mkdir -p /etc/apache2/ssl",
        "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt -subj '/CN=esgi.com'",
        "bash -c 'echo \"RewriteEngine On\n    RewriteCond %{SERVER_PORT} 80\n    RewriteRule .* https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]\" > /var/www/html/.htaccess'",
        "bash -c 'echo \"<VirtualHost *:443>\n    DocumentRoot /var/www/html\n    SSLEngine on\n    SSLCertificateFile /etc/apache2/ssl/apache.crt\n    SSLCertificateKeyFile /etc/apache2/ssl/apache.key\n</VirtualHost>\" > /etc/apache2/sites-available/default-ssl.conf'",
        "a2ensite default-ssl.conf",
        "systemctl reload apache2"
    ]

    for command in commands:
        run_command(client, command, sudo_password)