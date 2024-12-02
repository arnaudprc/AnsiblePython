import inquirer
import os

def main():
    questions = [
        inquirer.List('choice',
                      message="What do you want to do?",
                      choices=['Connect to ssh','Install packages', 'Configure the service','Back', 'Quit'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    print(f"You chose: {answers['choice']}")
        
    if answers['choice'] == 'Install packages':
        package_name = input("Enter the package name to install: ")
        os.system(f"sudo apt-get install -y {package_name}")
        print(f"Package {package_name} installed successfully")

    if answers['choice'] == 'Configure the service':
        service_name = input("Enter the service name to configure: ")
        os.system(f"sudo systemctl start {service_name}")
        print(f"Service {service_name} started successfully")

    if answers['choice'] == 'Back':
        main()

    if answers['choice'] == 'Quit':
        return

if __name__ == "__main__":
    main()