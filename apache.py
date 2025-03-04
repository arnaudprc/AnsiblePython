from ssh import run_command

# Fonction pour configurer Apache avec 2 sites SSL
def configure_https_and_hardening(client, sudo_password):
    commands = [
        ("apt-get install -y openssl", "Installation d'OpenSSL"),
        ("a2enmod ssl", "Activation du module SSL"),
        ("a2enmod rewrite", "Activation du module Rewrite"),
        ("systemctl restart apache2", "Redémarrage du service Apache"),
        ("mkdir -p /etc/apache2/ssl", "Création du répertoire SSL"),
        
        # Création des certificats SSL pour esgi1.com et esgi2.com
        ("openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/esgi1.key -out /etc/apache2/ssl/esgi1.crt -subj '/CN=esgi1.com'", "Génération du certificat SSL pour esgi1.com"),
        ("openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/esgi2.key -out /etc/apache2/ssl/esgi2.crt -subj '/CN=esgi2.com'", "Génération du certificat SSL pour esgi2.com"),

        # Création des dossiers pour chaque site
        ("mkdir -p /var/www/esgi1", "Création du répertoire du site esgi1"),
        ("mkdir -p /var/www/esgi2", "Création du répertoire du site esgi2"),

        # Ajout d'un index.html pour chaque site
        ("bash -c 'echo \"<h1>Bienvenue sur ESGI1</h1>\" > /var/www/esgi1/index.html'", "Ajout de la page d'accueil pour esgi1.com"),
        ("bash -c 'echo \"<h1>Bienvenue sur ESGI2</h1>\" > /var/www/esgi2/index.html'", "Ajout de la page d'accueil pour esgi2.com"),

        # Création des VirtualHosts
        ("bash -c 'echo \"<VirtualHost *:443>\n"
         "    ServerName esgi1.com\n"
         "    ServerAlias esgi1.com\n"
         "    ServerAlias esgi1.com\n"
         "    DocumentRoot /var/www/esgi1\n"
         "    SSLEngine on\n"
         "    SSLCertificateFile /etc/apache2/ssl/esgi1.crt\n"
         "    SSLCertificateKeyFile /etc/apache2/ssl/esgi1.key\n"
         "    <Directory /var/www/esgi1>\n"
         "        AllowOverride All\n"
         "        Require all granted\n"
         "    </Directory>\n"
         "</VirtualHost>\" > /etc/apache2/sites-available/esgi1-ssl.conf'", "Configuration du VirtualHost SSL pour esgi1.com"),

        ("bash -c 'echo \"<VirtualHost *:443>\n"
         "    ServerName esgi2.com\n"
         "    ServerAlias esgi2.com\n"
         "    ServerAlias esgi2.com\n"
         "    DocumentRoot /var/www/esgi2\n"
         "    SSLEngine on\n"
         "    SSLCertificateFile /etc/apache2/ssl/esgi2.crt\n"
         "    SSLCertificateKeyFile /etc/apache2/ssl/esgi2.key\n"
         "    <Directory /var/www/esgi2>\n"
         "        AllowOverride All\n"
         "        Require all granted\n"
         "    </Directory>\n"
         "</VirtualHost>\" > /etc/apache2/sites-available/esgi2-ssl.conf'", "Configuration du VirtualHost SSL pour esgi2.com"),

        # Activation des sites et redémarrage d'Apache
        ("a2ensite esgi1-ssl.conf", "Activation du site esgi1.com"),
        ("a2ensite esgi2-ssl.conf", "Activation du site esgi2.com"),
        ("systemctl reload apache2", "Rechargement du service Apache"),

    ]

    for command, description in commands:
        run_command(client, command, sudo_password, description)

    run_command(client, "echo '127.0.0.1 esgi1.com' | sudo tee -a /etc/hosts", sudo_password, "Ajout des noms de domaine dans /etc/hosts")
    run_command(client, "echo '127.0.0.1 esgi2.com' | sudo tee -a /etc/hosts", sudo_password, "Ajout des noms de domaine dans /etc/hosts")