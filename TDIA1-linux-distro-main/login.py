from cryptography.fernet import Fernet
import getpass


# PASSWORD
def write_key():
    key = Fernet.generate_key()
    with open("etc/TDIA_FS_key.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    file = open("etc/TDIA_FS_key.key", "rb")
    key = file.read()
    file.close()
    return key
def add():
    user = input("Nom du compte: ")
    passw = input("mot de pass: ")
    with open('.etc/mdp.txt', 'a') as f:  # au lieu d'ouvrir. colse.
        f.write(user + "| " + fer.encrypt(passw.encode()).decode() + "\n")
def view():
    passwords = {}
    with open('etc/mdp.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()  # rstrip ne lire pas \n
            user_, passw_ = data.split("|")  # "1|2|3" ==> ["1","2","3"]
            passwords[user_] = fer.decrypt(passw_.encode()).decode()
    return passwords
def login():
    psswrd = getpass.getpass("Enter votre mot de passe: ")
    if view()["root"] == psswrd:
        return True
    return False
def change():
    passw = getpass.getpass("votre nouvelle mot de passe: ")
    passw2 = getpass.getpass("Rentrer votre nouvelle mot de passe: ")
    if passw2 == passw:
        with open('etc/mdp.txt', 'w') as f:  #  au lieu d'ouvrir. colse.
            f.write("root| " + fer.encrypt(passw.encode()).decode() + "\n")
        return True
    else:
        print("mot de passe incorrecte ")
        return False



key = load_key()  # + master_passw.encode()
fer = Fernet(key)