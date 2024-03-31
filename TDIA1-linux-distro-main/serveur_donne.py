import rpyc
import os
import sys
import logging
import subprocess


from configparser import ConfigParser
from rpyc.utils.server import ThreadedServer


# paramètres de jornalisation et d'enregisteur:
le_logs = logging.getLogger()
le_logs.setLevel(level=logging.DEBUG)
file = logging.FileHandler("log/TDIA_FS_serveur_donne.log")
le_logs.addHandler(file)
file.setLevel(level=logging.WARNING)
fileformat = logging.Formatter("%(name)s:%(asctime)s:%(levelname)s:%(message)s")
file.setFormatter(fileformat)

consolehandler = logging.StreamHandler(stream=sys.stdout)
consolehandler.setLevel(logging.DEBUG)
streamformat = logging.Formatter("%(levelname)s:%(message)s")
consolehandler.setFormatter(streamformat)
le_logs.addHandler(consolehandler)

# importer une variable a l aide du fichier de configuration
config = ConfigParser()
config.read("config/TDIA_FSconfig.conf")
client = "DEFAULT"
config_data = config[client]
# declarer les variable utilisent config file
PORT = int(config_data['PORT'])
DATA_DIR = config_data['DATA_DIR']


class serveur_donne(rpyc.Service):

    def exposed_entrer(self, bloc_id, data, serveurs):
        logging.debug("entrer bloc: " + bloc_id)
        out_path = os.path.join(DATA_DIR_c, bloc_id)
        with open(out_path, 'wb') as f:
            f.write(data)
        if len(serveurs) > 0:
            self.forward(bloc_id, data, serveurs)

    def exposed_sortir(self, bloc_id):
        logging.debug("sortir bloc: " + bloc_id)
        bloc_adrs = os.path.join(DATA_DIR_c, bloc_id)
        if not os.path.isfile(bloc_adrs):
            logging.debug("bloc est introuvable!")
            return None
        with open(bloc_adrs, 'rb') as f:
            return f.read()

    
    def exposed_suprimer(self, bloc_id):
        logging.debug("supriming bloc: " + bloc_id)
        bloc_adrs = os.path.join(DATA_DIR_c, bloc_id)
        if not os.path.isfile(bloc_adrs):
            logging.error("bloc est introuvable!")
            return None
        else:
            subprocess.call(["rm", bloc_adrs])
    def forward(self, bloc_id, data, serveurs):
        logging.debug("Expéditrice bloc: " + bloc_id + str(serveurs))
        next_serveur_donne = serveurs[0]
        serveurs = serveurs[1:]
        host, port = next_serveur_donne

        rpyc.connect(host, port=port).root.entrer(bloc_id, data, serveurs)


if __name__ == "__main__":

    PORT = int(sys.argv[1])
    DATA_DIR_c = sys.argv[2]

    if not os.path.isdir(DATA_DIR_c):
        os.mkdir(DATA_DIR_c)

    logging.debug("départ de serveur_donne")
    t = ThreadedServer(serveur_donne(), port=PORT, logger=le_logs, protocol_config=
    {'allow_public_attrs': True, })
    try:
        t.start()
    except Exception as e:
        logging.error(e)
