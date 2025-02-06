import paramiko

def ssh_connect(hostname=None):
    while True:
        try:
            if hostname is None:
                hostname = input("Entrer l'adresse IP de la machine: ")
            username = input("Entrer le nom d'utilisateur: ")
            password = input("Entrer le mot de passe: ")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, username=username, password=password)
            print("[INFO] Connexion réussie")
            return client, password
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("[ERROR] Connexion échouée : Adresse IP invalide ou inaccessible. Veuillez réessayer.")
            hostname = None
        except paramiko.AuthenticationException:
            print("[ERROR] Connexion échouée : Authentification échouée. Veuillez vérifier le nom d'utilisateur et le mot de passe.")
        except Exception as e:
            print(f"[ERROR] Connexion échouée : {str(e)}. Veuillez réessayer.")