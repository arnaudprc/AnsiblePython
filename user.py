def run_command(client, command, sudo_password, description):
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
        
def add_user():
    run_command(client, f"sudo adduser {username}")
    
def add_user_sudo():
    run_command(client, f"sudo adduser {username} group sudo")