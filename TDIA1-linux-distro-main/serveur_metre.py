import rpyc
import uuid
import math
import random
import logging
import sys

from rpyc.utils.server import ThreadedServer
from configparser import ConfigParser

# paramètres de journalisation et d'enregistrer:
le_logs = logging.getLogger()
le_logs.setLevel(level=logging.INFO)

file = logging.FileHandler("log/TDIA_FS_serveur_metre.log")
le_logs.addHandler(file)
file.setLevel(level=logging.WARNING)
fileformat = logging.Formatter("%(name)s:%(asctime)s:%(levelname)s:%(message)s")
file.setFormatter(fileformat)

consolehandler = logging.StreamHandler(stream=sys.stdout)
consolehandler.setLevel(logging.INFO)
streamformat = logging.Formatter("%(levelname)s:%(message)s")
consolehandler.setFormatter(streamformat)
le_logs.addHandler(consolehandler)


class serveur_metreService(rpyc.Service):
    """
    file_bloc = {'file.txt': ["bloc1", "bloc2"]}
    bloc_serveur_donne = {"bloc1": [1,3]}
    serveurs = {"1": (127.0.0.1, 8000), "3": (127.0.0.1, 9000)}
    """
    # importer les variables utuliser config file
    config = ConfigParser()
    config.read("config/TDIA_FSconfig.conf")
    client = "DEFAULT"
    config_data = config[client]
    # declaration des variables utulise config file
    file_bloc = {}
    bloc_serveur_donne = {}
    bloc_size = int(config_data['BLOC_SIZE'])
    replication_factor = int(config_data['REPLICATION_FACTOR'])
    serveurs = config_data['SERVEURS']


    def exposed_read(self, file):

        all_files = self.file_bloc.keys()
        mapping = []
        # parcourir tous les blocs du fichier
        for rc in self.file_bloc[file]:
            serveur_donne_adrs = []
            # récupère tous les serveurs qui contiennent ce bloc
            for c_id in self.bloc_serveur_donne[rc]:
                serveur_donne_adrs.append(eval(self.serveurs)[c_id])

            mapping.append({"bloc_id": rc, "bloc_adrs": serveur_donne_adrs})
        return mapping

    def exposed_write(self, file, size):

        self.file_bloc[file] = []

        num_blocs = int(math.ceil(float(size) / self.bloc_size))
        return self.alloc_blocs(file, num_blocs)

    def exposed_lister(self):
        return self.file_bloc.keys()

    def exposed_suprimer(self, file):
        del self.file_bloc[file]

    def alloc_blocs(self, file, num_blocs):
        return_blocs = []
        for i in range(0, num_blocs):
            # générer un bloc 
            bloc_id = str(uuid.uuid1())
            # allouer le nombre de REPLICATION_FACTOR de serveurs
            serveur_donne_ids = random.sample(list(eval(self.serveurs).keys()), self.replication_factor)
            serveur_donne_adrs = [eval(self.serveurs)[m] for m in serveur_donne_ids]
            self.bloc_serveur_donne[bloc_id] = serveur_donne_ids
            self.file_bloc[file].append(bloc_id)  # Correction de la ligne avec "bloc_id" au lieu de "bloc_id_id"

            return_blocs.append(
                {"bloc_id": bloc_id, "bloc_adrs": serveur_donne_adrs})
        return return_blocs



if __name__== "__main__":
    t = ThreadedServer(serveur_metreService(), port=2131, protocol_config={
        'allow_public_attrs': True, })
    t.start()
