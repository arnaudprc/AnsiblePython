import sys
import os
import inquirer

# Ajouter le répertoire courant au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ssh import ssh_connect, install_package, uninstall_package
from apache import configure_https_and_hardening
from vsftpd import configure_vsftpd
from network import configure_network, get_network_interfaces
from user import add_user, add_user_sudo
from ldap import configure_ldap, test_ldap

# Fonction pour afficher le menu principal
def main_menu(client, password):
    while True:
        questions = [
            inquirer.List('choice',
                          message="Que voulez-vous faire ?",
                          choices=['Installer un package (apache2, vsftpd, ldap)', 'Configurer la carte réseau', 'Désinstaller un package', 'Ajouter un utilisateur', 'Quitter'],
                          ),
        ]
        answers = inquirer.prompt(questions)
        print(f"Votre choix: {answers['choice']}")

        if answers['choice'] == 'Installer un package (apache2, vsftpd, ldap)':
            package_name = input("Entrer le nom du package à installer (apache2 ou vsftpd, ldap): ")
            if package_name == 'ldap':
                configure_ldap(client, password)
                test_ldap(client, password)
            else:
                install_package(client, package_name, password)
                if package_name == 'apache2':
                    configure_https_and_hardening(client, password)
                elif package_name == 'vsftpd':
                    configure_vsftpd(client, password)


        elif answers['choice'] == 'Configurer la carte réseau':
            interfaces = get_network_interfaces(client)
            print("Interfaces réseau disponibles :")
            for i, interface in enumerate(interfaces):
                print(f"{i + 1}. {interface}")

            interface_index = int(input("Choisissez l'interface à configurer (numéro) : ")) - 1
            interface = interfaces[interface_index]

            address = input("Entrez l'adresse IP avec le masque CIDR : ")
            gateway = input("Entrez l'adresse de la passerelle : ")
            dns = input("Entrez l'adresse du serveur DNS : ")
            configure_network(client, password, interface, address, gateway, dns)

            print("[INFO] Configuration réseau terminée. Reconnexion SSH nécessaire.")
            client.close()

            # Reconnexion SSH après changement d'adresse IP
            client, password = ssh_connect(address.split('/')[0])

            print("[INFO] Reconnexion SSH réussie après changement d'adresse IP.")
            # Relancer le menu principal après la reconnexion
            main_menu(client, password)

        elif answers['choice'] == 'Désinstaller un package':
            package_name = input("Entrer le nom du package à désinstaller: ")
            uninstall_package(client, package_name, password)

        elif answers['choice'] == 'Ajouter un utilisateur':
            username = input("Entrez le nom de l'utilisateur à ajouter: ")
            user_password = input("Entrez le mot de passe pour l'utilisateur: ")
            sudo = inquirer.confirm("L'utilisateur doit-il être ajouté au groupe sudo ?", default=False)
            if sudo:
                add_user_sudo(client, password, username, user_password)
            else:
                add_user(client, password, username, user_password)

        elif answers['choice'] == 'Quitter':
            break

    client.close()

if __name__ == "__main__":
    client, password = ssh_connect()
    main_menu(client, password)