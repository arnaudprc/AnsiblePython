from ssh import run_command

def configure_ldap(client, sudo_password):
    # Installer les paquets LDAP
    run_command(client, "apt-get update", sudo_password, "Mise à jour des paquets")
    run_command(client, "apt-get install -y slapd ldap-utils", sudo_password, "Installation de LDAP")

    # Générer un mot de passe hashé pour LDAP
    ldap_password = input("Entrez le mot de passe LDAP: ")
    stdin, stdout, stderr = client.exec_command(f"slappasswd -s {ldap_password}", get_pty=True)
    password_hash = stdout.read().decode().strip()

    # Configurer LDAP
    ldap_config = f"""
dn: olcDatabase={{1}}mdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: dc=esgi,dc=local

dn: olcDatabase={{1}}mdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=admin,dc=esgi,dc=local

dn: olcDatabase={{1}}mdb,cn=config
changetype: modify
delete: olcRootPW

dn: olcDatabase={{1}}mdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {password_hash}
"""
    command = f"echo '{ldap_config}' | sudo ldapmodify -Y EXTERNAL -H ldapi:///"
    run_command(client, command, sudo_password, "Configuration de LDAP")

    # Démarrer et activer le service LDAP
    run_command(client, "systemctl enable slapd", sudo_password, "Activation du service LDAP")
    run_command(client, "systemctl start slapd", sudo_password, "Démarrage du service LDAP")

    # Ajouter l'entrée de base pour dc=esgi,dc=local
    base_entry = f"""
dn: dc=esgi,dc=local
objectClass: top
objectClass: dcObject
objectClass: organization
o: ESGI
dc: esgi

dn: cn=admin,dc=esgi,dc=local
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
userPassword: {password_hash}
description: LDAP administrator
"""
    command = f"echo '{base_entry}' | sudo ldapadd -x -D cn=admin,dc=esgi,dc=local -w '{ldap_password}'"
    run_command(client, command, sudo_password, "Ajout de l'entrée de base LDAP")

def test_ldap(client, sudo_password):
    # Tester la connexion LDAP
    command = "ldapsearch -x -LLL -b dc=esgi,dc=local"
    run_command(client, command, sudo_password, "Test de la connexion LDAP")