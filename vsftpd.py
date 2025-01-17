def configure_vsftpd(client, sudo_password):
    """Installation, configuration et securisation de vsftpd."""
    def run_command(command, description):
        """Exécute une commande shell et affiche son statut."""
        print(f"[INFO] {description}...")
        stdin, stdout, stderr = client.exec_command(f"echo {sudo_password} | sudo -S {command}", get_pty=True)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(output)
        if error:
            print(f"[ERROR] {description}. Error: {error}")
        else:
            print(f"[SUCCESS] {description}.")

    print("[INFO] Début de l'installation et de la configuration de vsftpd...")

    run_command("sudo apt update && sudo apt install -y vsftpd", "Installation de vsftpd")
    run_command("sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.backup", "Sauvegarde vsftpd.conf")

    config = """anonymous_enable=NO
listen_port=22
local_enable=YES
write_enable=NO
chroot_local_user=YES
userlist_enable=YES
userlist_deny=NO
userlist_file=/etc/vsftpd.userlist
ssl_enable=YES
rsa_cert_file=/etc/ssl/certs/vsftpd.pem
rsa_private_key_file=/etc/ssl/private/vsftpd.key
force_local_logins_ssl=YES
force_local_data_ssl=YES
ssl_tlsv1_2=YES
ssl_ciphers=HIGH
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=50000
xferlog_enable=YES
log_ftp_protocol=YES
xferlog_file=/var/log/vsftpd.log
"""
    run_command(f"echo '{config}' | sudo tee /etc/vsftpd.conf", "Application de la nouvelle configuration de vsftpd")

    run_command(
        "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/vsftpd.key -out /etc/ssl/certs/vsftpd.pem -subj '/CN=vsftpd'",
        "Génération des certificats SSL",
    )
    run_command("sudo mv temp_userlist /etc/vsftpd.userlist", "Mise à jour de la liste blanche des utilisateurs de vsftpd")
    run_command("sudo ufw allow 21/tcp && sudo ufw allow 40000:50000/tcp && sudo ufw reload", "Configuration du pare-feu")
    run_command("sudo systemctl restart vsftpd && sudo systemctl enable vsftpd", "Redémarrage du service vsftpd et activation au démarrage de vsftpd")

    print("[SUCCESS] Installation et configuraiton de vsftpd.")