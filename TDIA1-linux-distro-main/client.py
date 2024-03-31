import rpyc
import sys
import logging
import base64
import login as lg

import subprocess


# logging and logger settings:
le_logs = logging.getLogger()
le_logs.setLevel(level=logging.DEBUG)

file = logging.FileHandler("log/TDIA_FS_client.log")
le_logs.addHandler(file)
file.setLevel(level=logging.WARNING)
fileformat = logging.Formatter("%(name)s:%(asctime)s:%(levelname)s:%(message)s")
file.setFormatter(fileformat)

consolehandler = logging.StreamHandler(stream=sys.stdout)
consolehandler.setLevel(logging.DEBUG)
streamformat = logging.Formatter("%(levelname)s:%(message)s")
consolehandler.setFormatter(streamformat)
le_logs.addHandler(consolehandler)


# ID1FS commands
def sortir(metre, file):
    file_table = metre.read(file)
    if not file_table:
        logging.info("fichier introuvable!")
        return

    for bloc in file_table:
        for host, port in bloc['bloc_adrs']:
            try:
                con = rpyc.connect(host, port=port).root
                data = con.sortir(bloc['bloc_id'])
                if data:
                    fh = open('data/' + file, 'ab')
                    fh.write(base64.b64decode(data))
                    fh.close()
                    break
            except Exception as e:
                continue
        else:
            logging.error("bloc introuvable. peut-étre un fichier corrompu")


def entrer(metre, source, dest):
    with open(source, 'rb') as imagefile:
        byteform = base64.b64encode(imagefile.read())
    dest_b = byteform
    size = len(dest_b)
    blocs = metre.write(dest, size)
    DATA_splited = [dest_b[i:i + metre.bloc_size] for i in range(0, len(dest_b), metre.bloc_size)]
    i = 0
    for bloc in blocs:
        data = DATA_splited[i]
        i = i + 1
        bloc_id = bloc['bloc_id']
        serveurs= bloc['bloc_adrs']
        serveur_donne = serveurs[0]
        serveurs = serveurs[1:]
        host, port = serveur_donne

        con = rpyc.connect(host, port=port)
        con.root.entrer(bloc_id, data, serveurs)


def help():
    logging.debug("TDIA_FS help!")
    print("help   : afficher tous les commande exist dans TDIA_FS>>> help")
    print("entrer   : Télécharger un fichier du local vers TDIA_FS >>> entrer [source file path][destination name]")
    print("sortir   : Exporter un fichier de TDIA_FS vers local >>> sortir [destination name]")
    print("suprimer : Supprimer un fichier de TDIA_FS>>> suprimer  [destination name]")
    print("lister  : Lister tous les fichier existe >>> lister ")
    print("open  : ouvrir un fichier >>> ouvre [destination name]")
    print("status : Vérifier l'état actuel (Haut/Bas) >>> status")
    print("change_mdp : Changer le mots de passe >>> change_mdp")

def openn(file):
    try:
        subprocess.call(["open", 'data/' + file])
    except Exception as e:
        logging.error(e)


def suprimerr(metre , file):
    file_table = metre.read(file)
    if not file_table:
        logging.error("fichier introuvable!")
        return
    try:
        for bloc in file_table:
            for host, port in bloc['bloc_adrs']:
                try:
                    con = rpyc.connect(host, port=port).root
                    con.suprimer(bloc['bloc_id'])
                except Exception as e:
                    continue
    except KeyError:
        logging.error("Fichier introuvable!")

    try:
        metre.suprimer(file)
    except:
        logging.error("Une erreur s'est produite, fichier introuvable!")

def listerr(metre):
    all_files = metre.lister()
    if len(all_files) == 0:
        print("Aucun fichier n'est importé")
    else:
        print('Fichiers existants:')
        for i in all_files:
            print(i)


def main(args):
    try:
        con = rpyc.connect("localhost", port=2131)
        metre = con.root

        if args[0] == "sortir":
            if lg.login():
                try:
                    sortir(metre, args[1])
                    logging.debug("Le fichier a été importé avec succès")
                except KeyError:
                    logging.error("Le fichier n'existe pas !")
            else:
                logging.error("mot de passe incorrect!")
        elif args[0] == "entrer":
            if lg.login():
                try:
                    entrer(metre, args[1], args[2])
                    logging.debug("Le fichier a été exporté avec succès")
                except IndexError:
                    logging.error("Erreur de syntaxe de la commande entrer, essayez l'aide!")
                except FileNotFoundError as e:
                    logging.error(e)
            else:
                logging.error("Mauvais mot de passe!")
        elif args[0] == "help":
            help()
        elif args[0] == "open":
            openn(args[1])
        elif args[0] == "suprimer":
            if lg.login():
                try:
                    suprimerr(metre, args[1])
                    logging.debug("Le fichier a été supprimé avec succès")
                except KeyError:
                    logging.error("Fichier introuvable!")
            else:
                logging.error("Mauvais mot de passe")
        elif args[0] == "lister":
            listerr(metre)
        elif args[0] == "status":
            logging.debug("le serveur est actif!")
        elif args[0] == "change_mdp":
            if lg.login():
                if lg.change():
                    logging.debug("Le mot de passe a été modifié avec succès")
            else:
                logging.error("Mauvais mot de passe!")
        else:
            logging.error("Commande non trouvée! Essayez help")
    except ConnectionRefusedError:
        logging.error("Une erreur s'est produite. Le serveur est indisponible!")


if __name__ == "__main__":
    main(sys.argv[1:])
