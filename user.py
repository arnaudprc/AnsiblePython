def run_command(client, command, sudo_password):
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(sudo_password + '\n')
    stdin.flush()
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(output)
    if error:
        print(f"[ERROR] {command}. Error: {error}")
    else:
        print(f"[SUCCESS] {command}.")
