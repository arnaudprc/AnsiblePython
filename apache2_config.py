def apache():
    print("Apache2 Configuration")
    print("Activation du module SSL")
    
    command = "sudo a2enmod ssl"
    print(f"Veuillez taper la commande suivante : {command}")
    
    user_input = input("Tapez la commande ici : ")
    
    if user_input == command:
        print("Commande correcte, activation du module SSL en cours...")
    else:
        print("Commande incorrecte, veuillez réessayer.")
    
    return

def install_certbot():
    print("Installer Certbot")
    command = "sudo apt-get install -y certbot python3-certbot-apache"
    print(f"Veuillez taper la commande suivante : {command}")

    user_input = input("Tapez la commande ici : ")

    if user_input == command:
        print("Commande correcte, installation de Certbot en cours...")
    else:
        print("Commande incorrecte, veuillez réessayer.")
    
    return

def get_certssl():
    print("Obtenir un certificat SSL")
    domain = input("Entrez le nom de domaine pour lequel vous voulez obtenir un certificat SSL : ")
    email = input("Entrez votre adresse e-mail : ")
    command = f"sudo certbot --apache -d {domain} -m {email} --agree-tos"
    print(f"Veuillez taper la commande suivante : {command}")

    user_input = input("Tapez la commande ici : ")

    if user_input == command:
        print("Commande correcte, obtention du certificat SSL en cours...")
    else:
        print("Commande incorrecte, veuillez réessayer.")
    
    return

def virtualhost_https():
    print("Configurer un virtual host HTTPS")
    domain = input("Entrez le nom de domaine pour lequel vous voulez configurer un virtual host HTTPS : ")
    command = f"sudo a2ensite {domain}-le-ssl.conf"
    print(f"Veuillez taper la commande suivante : {command}")

    user_input = input("Tapez la commande ici : ")

    if user_input == command:
        print("Commande correcte, configuration du virtual host HTTPS en cours...")
    else:
        print("Commande incorrecte, veuillez réessayer.")
    
    return

def activate_virtualhost_https():
    print("Activer le virtual host HTTPS")
    command = "sudo systemctl reload apache2"
    print(f"Veuillez taper la commande suivante : {command}")

    user_input = input("Tapez la commande ici : ")

    if user_input == command:
        print("Commande correcte, activation du virtual host HTTPS en cours...")
    else:
        print("Commande incorrecte, veuillez réessayer.")
    
    return

def reload_apache():
    print("Reload Apache")
    command = "sudo systemctl reload apache2"
    print(f"Veuillez taper la commande suivante : {command}")

    user_input = input("Tapez la commande ici : ")

    if user_input == command:
        print("Commande correcte, redémarrage d'Apache en cours...")
    else:
        print("Commande incorrecte, veuillez réessayer.")
    
    return