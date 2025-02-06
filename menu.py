import sys
import os
import inquirer

# Ajouter le répertoire courant au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ssh import ssh_connect, install_package, uninstall_package
from apache import configure_https_and_hardening
from vsftpd import configure_vsftpd
from network import configure_network

def main_menu():
    client, password = ssh_connect()
    while True:
        questions = [
            inquirer.List('choice',
                          message="Que voulez-vous faire ?",
                          choices=['Installer un package (apache2, vsftpd)', 'Configurer la carte réseau', 'Désinstaller un package', 'Ajouter un utilisateur', 'Quitter'],
                          ),
        ]
        answers = inquirer.prompt(questions)
        print(f"Votre choix: {answers['choice']}")

        if answers['choice'] == 'Installer un package (apache2, vsftpd)':
            package_name = input("Entrer le nom du package à installer (apache2 ou vsftpd): ")
            install_package(client, package_name, password)
            if package_name == 'apache2':
                configure_https_and_hardening(client, password)
            elif package_name == 'vsftpd':
                configure_vsftpd(client, password)

        elif answers['choice'] == 'Configurer la carte réseau':
            interface = input("Entrez le nom de l'interface réseau : ")
            address = input("Entrez l'adresse IP avec le masque CIDR : ")
            gateway = input("Entrez l'adresse de la passerelle : ")
            dns = input("Entrez l'adresse du serveur DNS : ")
            configure_network(client, password, interface, address, gateway, dns)

        elif answers['choice'] == 'Désinstaller un package':
            package_name = input("Entrer le nom du package à désinstaller: ")
            uninstall_package(client, package_name, password)

        elif answers['choice'] == 'Ajouter un utilisateur':
            username = input("Entrez le nom de l'utilisateur à ajouter: ")
            sudo = inquirer.confirm("L'utilisateur doit-il être ajouté au groupe sudo ?", default=False)
            if sudo:
                add_user_sudo(client, username, password)
            else:
                add_user(client, username, password)

        elif answers['choice'] == 'Quitter':
            break

    client.close()

if __name__ == "__main__":
    main_menu()