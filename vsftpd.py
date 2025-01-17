def configure_vsftpd(client, sudo_password):
    """Install, configure, and secure vsftpd."""
    def run_command(command, description):
        """Execute a shell command and print its status."""
        print(f"[INFO] {description}...")
        try:
            stdin, stdout, stderr = client.exec_command(command, get_pty=True)
            stdin.write(sudo_password + '\n')
            stdin.flush()
            print(f"[SUCCESS] {description}.")
            print(stdout.read().decode())
            print(stderr.read().decode())
        except Exception as e:
            print(f"[ERROR] {description}. Error: {e}")
            exit(1)

    print("[INFO] Starting vsftpd installation and configuration...")

    # Install vsftpd
    run_command("sudo apt update", "Updating package list")
    run_command("sudo apt install -y vsftpd", "Installing vsftpd")

    # Backup existing configuration
    run_command("sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.backup", "Backing up vsftpd.conf")

    # Write a secure configuration
    config = """anonymous_enable=NO
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
    config_path = "/etc/vsftpd.conf"
    with open("temp_vsftpd.conf", "w") as file:
        file.write(config)
    run_command(f"sudo mv temp_vsftpd.conf {config_path}", "Applying new vsftpd configuration")

    # Generate SSL certificates
    cert_dir = "/etc/ssl/certs/vsftpd.pem"
    key_dir = "/etc/ssl/private/vsftpd.key"
    run_command(
        f"sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout {key_dir} -out {cert_dir} -subj '/CN=vsftpd'",
        "Generating SSL certificates",
    )

    # Add users to whitelist
    users = ["ftpuser1", "ftpuser2"]  # Replace with your desired users
    whitelist_path = "/etc/vsftpd.userlist"
    with open("temp_userlist", "w") as file:
        file.write("\n".join(users) + "\n")
    run_command(f"sudo mv temp_userlist {whitelist_path}", "Updating vsftpd user whitelist")

    # Configure firewall
    run_command("sudo ufw allow 21/tcp", "Allowing FTP port 21")
    run_command("sudo ufw allow 40000:50000/tcp", "Allowing passive mode ports")
    run_command("sudo ufw reload", "Reloading UFW rules")

    # Restart and enable vsftpd service
    run_command("sudo systemctl restart vsftpd", "Restarting vsftpd service")
    run_command("sudo systemctl enable vsftpd", "Enabling vsftpd service on startup")

    print("[SUCCESS] vsftpd has been successfully installed and configured.")