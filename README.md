# AnsiblePython

## 1. Clonez le dépôt:
git clone https://github.com/arnaudprc/AnsiblePython
cd AnsiblePython

## 2. Exécutez le script
python menu.py

## 3. Suivez les instructions à l'écran pour vous connecter à un serveur distant et choisir les actions à effectuer.

### Fonctionnalités

#### Installer un package : 
Vous pouvez installer des packages comme apache2, vsftpd et zabbix. Après l'installation, des configurations supplémentaires peuvent être appliquées automatiquement.

#### Configurer la carte réseau :
Vous pouvez configurer les interfaces réseau en spécifiant l'adresse IP, la passerelle et le serveur DNS.

#### Désinstaller un package : 
Vous pouvez désinstaller des packages installés sur le serveur distant.

#### Ajouter un utilisateur : 
Vous pouvez ajouter un utilisateur avec ou sans droits sudo.

#### Exemple d'utilisation :
1. Lancer le script: python menu.py
2. Suivez les instructions pour vous connecter à un serveur distant via SSH.

3. Choisissez une action dans le menu principal:
- Installer un package
- Configurer la carte réseau
- Désinstaller un package
- Ajouter un utilisateur
- Quitter