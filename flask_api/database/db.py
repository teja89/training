import yaml
import mysql.connector
import os


def connect_db():
    env = os.environ["ENV"]
    with open('mysql_config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    cnx = mysql.connector.connect(**config[env])

    return cnx
