from mysql_connector_wrapper import Connection
import os
from dotenv import load_dotenv

load_dotenv()

with Connection(
    os.getenv("DB_HOST"),
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_PORT"),
    os.getenv("DB_DATABASE"),
) as db:
    db.connect()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM crm_cfg LIMIT 1;")
        print(cursor.fetchall()[0]["cfg_id"])
