import yaml
import mysql.connector


def connect_db():
    with open('mysql_config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    cnx = mysql.connector.connect(**config)

    return cnx
