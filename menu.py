import sys
import os
import inquirer

# Ajouter le répertoire courant au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ssh import ssh_connect, install_package, uninstall_package
from apache import configure_https_and_hardening
from vsftpd import configure_vsftpd

def main_menu():
    client, password = ssh_connect()
    while True:
        questions = [
            inquirer.List('choice',
                          message="What do you want to do?",
                          choices=['Install packages (apache2, vsftpd)', 'Uninstall packages', 'Quit'],
                          ),
        ]
        answers = inquirer.prompt(questions)
        print(f"You chose: {answers['choice']}")

        if answers['choice'] == 'Install packages (apache2, vsftpd)':
            package_name = input("Enter the package name to install (apache2 or vsftpd): ")
            install_package(client, package_name, password)
            if package_name == 'apache2':
                configure_https_and_hardening(client, password)
            elif package_name == 'vsftpd':
                configure_vsftpd(client, password)

        elif answers['choice'] == 'Uninstall packages':
            package_name = input("Enter the package name to uninstall: ")
            uninstall_package(client, package_name, password)

        elif answers['choice'] == 'Quit':
            break

    client.close()

if __name__ == "__main__":
    main_menu()