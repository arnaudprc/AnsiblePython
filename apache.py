from ssh import run_command

# Fonction pour configurer Apache
def configure_https_and_hardening(client, sudo_password):
    commands = [
        ("apt-get install -y openssl", "Installation d'OpenSSL"),
        ("a2enmod ssl", "Activation du module SSL"),
        ("a2enmod rewrite", "Activation du module Rewrite"),
        ("systemctl restart apache2", "Redémarrage du service Apache"),
        ("mkdir -p /etc/apache2/ssl", "Création du répertoire SSL"),
        ("openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt -subj '/CN=esgi.com'", "Génération du certificat SSL"),
        ("bash -c 'echo \"RewriteEngine On\n    RewriteCond %{SERVER_PORT} 80\n    RewriteRule .* https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]\" > /var/www/html/.htaccess'", "Configuration de la redirection HTTPS"),
        ("bash -c 'echo \"<VirtualHost *:443>\n    DocumentRoot /var/www/html\n    SSLEngine on\n    SSLCertificateFile /etc/apache2/ssl/apache.crt\n    SSLCertificateKeyFile /etc/apache2/ssl/apache.key\n</VirtualHost>\" > /etc/apache2/sites-available/default-ssl.conf'", "Configuration du site SSL par défaut"),
        ("a2ensite default-ssl.conf", "Activation du site SSL par défaut"),
        ("systemctl reload apache2", "Rechargement du service Apache")
    ]

    for command, description in commands:
        run_command(client, command, sudo_password, description)