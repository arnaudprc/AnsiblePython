import paramiko
import sys

def configure_https_and_hardening(client, sudo_password):
    try:
        commands = [
            f'echo {sudo_password} | sudo -S apt-get install -y openssl',
            f'echo {sudo_password} | sudo -S a2enmod ssl',
            f'echo {sudo_password} | sudo -S systemctl restart apache2',
            # Best practices for Apache2 configuration
            f'echo {sudo_password} | sudo -S mkdir -p /etc/apache2/ssl',
            f'echo {sudo_password} | sudo -S openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=example.com"',
            f'echo {sudo_password} | sudo -S bash -c "echo \'<VirtualHost *:443>\n    SSLEngine on\n    SSLCertificateFile /etc/apache2/ssl/apache.crt\n    SSLCertificateKeyFile /etc/apache2/ssl/apache.key\n    ServerAdmin webmaster@localhost\n    DocumentRoot /var/www/html\n    <Directory /var/www/html>\n        Options Indexes FollowSymLinks\n        AllowOverride All\n        Require all granted\n    </Directory>\n    ErrorLog /var/log/apache2/error.log\n    CustomLog /var/log/apache2/access.log combined\n</VirtualHost>\' > /etc/apache2/sites-available/default-ssl.conf"',
            f'echo {sudo_password} | sudo -S a2ensite default-ssl',
            f'echo {sudo_password} | sudo -S systemctl reload apache2'
        ]

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            print("Executing: ", command)
            for line in stdout:
                print(line.strip())
            for line in stderr:
                print(line.strip())

        print("HTTPS and best practices configuration for Apache2 completed successfully.")
    except Exception as e:
        print(f"An error occurred during HTTPS and Apache2 hardening configuration: {e}")

def install_package(client, sudo_password):
    package_name = input("Enter the package name to install: ")
    try:
        command = f'echo {sudo_password} | sudo -S apt-get update && echo {sudo_password} | sudo -S apt-get install -y {package_name}'
        stdin, stdout, stderr = client.exec_command(command)
        print("Output:")
        for line in stdout:
            print(line.strip())
        print("Error:")
        for line in stderr:
            print(line.strip())
        print(f"Package '{package_name}' installed successfully.")

        # Configure HTTPS and hardening if the installed package is 'apache2'
        if package_name == 'apache2':
            configure_https_and_hardening(client, sudo_password)
    except Exception as e:
        print(f"An error occurred: {e}")

def uninstall_package(client, sudo_password):
    package_name = input("Enter the package name to uninstall: ")
    try:
        command = f'echo {sudo_password} | sudo -S apt-get remove -y {package_name}'
        stdin, stdout, stderr = client.exec_command(command)
        print("Output:")
        for line in stdout:
            print(line.strip())
        print("Error:")
        for line in stderr:
            print(line.strip())
        print(f"Package '{package_name}' uninstalled successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def ssh_connect():
    hostname = input("Enter the server hostname or IP address: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        print("Connected to the server successfully.")
        sudo_password = input("Enter your sudo password for the server: ")
        return client, sudo_password
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        return None, None

def main():
    client, sudo_password = ssh_connect()
    if not client:
        print("Exiting due to connection failure.")
        sys.exit()

    while True:
        print("\nMenu:")
        print("1 - Install a package (apache2)")
        print("2 - Uninstall a package (apache2)")
        print("3 - Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            install_package(client, sudo_password)
        elif choice == '2':
            uninstall_package(client, sudo_password)
        elif choice == '3':
            print("Exiting the menu. Goodbye!")
            client.close()
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
