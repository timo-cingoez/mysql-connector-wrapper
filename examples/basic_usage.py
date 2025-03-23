from mysql_connector_wrapper import Connection

with Connection("127.0.0.1", "root", "root", "3308", "crm_timo") as db:
    db.connect()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM crm_cfg LIMIT 1;")
        print(cursor.fetchall()[0]["cfg_id"])
