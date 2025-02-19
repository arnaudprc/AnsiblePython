from ssh import run_command

# Fonction pour installer et configurer vsftpd
def configure_vsftpd(client, sudo_password):
    print("[INFO] Début de l'installation et de la configuration de vsftpd...")

    run_command(client, "sudo apt update && sudo apt install -y vsftpd", sudo_password, "Installation de vsftpd")
    run_command(client, "sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.backup", sudo_password, "Sauvegarde du fichier de configuration original")

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

    # Écrire la configuration directement dans le fichier distant
    command = f"echo '{config}' | sudo bash -c 'cat > /etc/vsftpd.conf'"
    run_command(client, command, sudo_password, "Écriture de la configuration vsftpd")

    run_command(client, "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/vsftpd.key -out /etc/ssl/certs/vsftpd.pem -subj '/CN=vsftpd'", sudo_password, "Génération du certificat SSL")

    utilisateurs = ["lab"]
    userlist = "\n".join(utilisateurs)
    command = f"echo '{userlist}' | sudo tee /etc/vsftpd.userlist"
    run_command(client, command, sudo_password, "Écriture de la liste des utilisateurs vsftpd")

    run_command(client, "sudo ufw allow 21/tcp && sudo ufw allow 40000:50000/tcp && sudo ufw reload", sudo_password, "Configuration du pare-feu")

    run_command(client, "sudo systemctl restart vsftpd && sudo systemctl enable vsftpd", sudo_password, "Redémarrage et activation du service vsftpd")

    print("[SUCCÈS] vsftpd a été installé et configuré avec succès.")