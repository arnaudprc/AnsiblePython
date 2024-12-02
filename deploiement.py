import paramiko

def ssh_connect(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username=username, password=password)
    return client

def install_package(client, package_name):
    stdin, stdout, stderr = client.exec_command(f'sudo apt-get install -y {package_name}')
    print(stdout.read().decode())
    print(stderr.read().decode())

def configure_package(client, config_command):
    stdin, stdout, stderr = client.exec_command(config_command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def main():
    hostname = input("Entrez l'adresse IP de la machine distante : ")
    port = 22
    username = input("Entrez votre nom d'utilisateur : ")
    password = input("Entrez votre mot de passe : ")

    client = ssh_connect(hostname, port, username, password)

    while True:
        print("\nMenu:")
        print("1. Installer un package")
        print("2. Désinstaller un package")
        print("3. Configurer un package")
        print("4. Quitter")
        choice = input("Choisissez une option : ")

        if choice == '1':
            package_name = input("Entrez le nom du package à installer : ")
            install_package(client, package_name)

        elif choice == '2':
            package_name = input("Entrez le nom du package à désinstaller : ")
            stdin, stdout, stderr = client.exec_command(f'sudo apt-get remove -y {package_name}')
            print(stdout.read().decode())
            print(stderr.read().decode())

        elif choice == '3':
            config_command = input("Entrez la commande de configuration : ")
            configure_package(client, config_command)

        elif choice == '4':
            break
        
        else:
            print("Option invalide, veuillez réessayer.")

    client.close()

if __name__ == "__main__":
    main()