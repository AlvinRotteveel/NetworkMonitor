import sqlite3 as lite


# Connect to dump database. Create if it doesnt exist.
datab = lite.connect('dump.db')
#Create table if it doesnt exist
datab.execute('''CREATE TABLE IF NOT EXISTS PACKETS
       (ID  INTEGER PRIMARY KEY AUTOINCREMENT,
       DESTMAC          TEXT    NOT NULL,
       SRCMAC           TEXT    NOT NULL,
       PROTOCOL         TEXT    NOT NULL);''')


def add_packet(destmac, srcmac, protocol):
    """Insert a channel in the database"""
    datab.execute("INSERT INTO PACKETS (DESTMAC,SRCMAC,PROTOCOL) "
                  "VALUES (" + destmac + ", " + srcmac + ", " + protocol + ")")