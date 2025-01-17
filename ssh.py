import paramiko

def ssh_connect():
    hostname = input("Enter the server hostname or IP address: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client, password

def install_package(client, package_name, sudo_password):
    try:
        command = f'echo {sudo_password} | sudo -S apt-get update && echo {sudo_password} | sudo -S apt-get install -y {package_name}'
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        print("Output:")
        for line in stdout:
            print(line.strip())
        print("Error:")
        for line in stderr:
            print(line.strip())
        print(f"Package '{package_name}' installed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def uninstall_package(client, sudo_password):
    package_name = input("Enter the package name to uninstall: ")
    try:
        command = f'echo {sudo_password} | sudo -S apt-get remove -y {package_name}'
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        print("Output:")
        for line in stdout:
            print(line.strip())
        print("Error:")
        for line in stderr:
            print(line.strip())
        print(f"Package '{package_name}' uninstalled successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")