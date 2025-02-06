def add_user():
    run_command(client, f"sudo adduser {username}")
    
def add_user_sudo():
    run_command(client, f"sudo adduser {username} group sudo")