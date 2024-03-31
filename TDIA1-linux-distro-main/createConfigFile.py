from configparser import ConfigParser

config = ConfigParser()

config["DEFAULT"] = {
    # serveur_metre:
    "bloc_SIZE": "100",
    "REPLICATION_FACTOR": "2",
    "serveurs": {"1": ("127.0.0.1", 8000), "2": ("127.0.0.1", 9000)},
    # serveur_donne:
    "DATA_DIR": "/tmp/serveur_donne/",
    "PORT": "8888",
}

with open("TDIA_FSconfig.conf", "w") as f:
    config.write(f)
