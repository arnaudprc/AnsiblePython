def apache(client, password):
    print("Apache2 Configuration")
    print("Activation du module SSL")
    
    command = "sudo a2enmod ssl"
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(password + '\n')
    stdin.flush()
    
    print(stdout.read().decode())
    print(stderr.read().decode())

def generate_cert(client, password):
    print("Génération du certificat SSL")

    country = input("Entrez le pays (ex: FR) : ")
    state = input("Entrez l'état ou la province : ")
    city = input("Entrez la ville : ")
    org = input("Entrez le nom de l'organisation : ")
    unit = input("Entrez le nom de l'unité organisationnelle : ")
    common_name = input("Entrez le nom commun (CN) : ")
    email = input("Entrez l'adresse e-mail : ")

    command = (
        f"sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 "
        f"-keyout /etc/ssl/private/selfsigned.key "
        f"-out /etc/ssl/certs/selfsigned.crt "
        f"-subj \"/C={country}/ST={state}/L={city}/O={org}/OU={unit}/CN={common_name}/emailAddress={email}\""
    )

    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(password + '\n')
    stdin.flush()

    stdout_output = stdout.read().decode()
    stderr_output = stderr.read().decode()

    if stdout_output:
        print("Sortie standard :")
        print(stdout_output)

    if stderr_output:
        print("Sortie d'erreur :")
        print(stderr_output)

    if not stderr_output:
        print("Certificat SSL généré avec succès.")
    
def configure_virtual_host(client, password):
    config_content = """
<VirtualHost *:443>
    ServerName localhost 
    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/selfsigned.crt
    SSLCertificateKeyFile /etc/ssl/private/selfsigned.key
</VirtualHost>
"""
    command = f'echo "{config_content}" | sudo tee /etc/apache2/sites-available/000-default.conf'
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(password + '\n')
    stdin.flush()
    
    print(stdout.read().decode())
    print(stderr.read().decode())

    command = 'sudo a2ensite 000-default.conf'
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(password + '\n')
    stdin.flush()
    
    print(stdout.read().decode())
    print(stderr.read().decode())

    command = 'sudo systemctl restart apache2'
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(password + '\n')
    stdin.flush()
    
    print(stdout.read().decode())
    print(stderr.read().decode())