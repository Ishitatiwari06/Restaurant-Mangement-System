import os

import mysql.connector


def get_database_config() -> dict[str, object]:
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "root"),
        "database": os.getenv("MYSQL_DATABASE", "RestaurantDB"),
    }


def get_connection():

    connection = mysql.connector.connect(**get_database_config())

    return connection