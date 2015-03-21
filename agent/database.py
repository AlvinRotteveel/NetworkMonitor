import sqlite3 as lite


table_name = 'PACKETS'

# Connect to dump database. Create if it doesnt exist.
datab = lite.connect('dump.db', isolation_level=None)
#Create table if it doesnt exist
c = datab.cursor()


datab.execute('''CREATE TABLE IF NOT EXISTS PACKETS
   (ID  INTEGER PRIMARY KEY AUTOINCREMENT,
   DSTMAC       TEXT,
   SRCMAC       TEXT,
   PROTOCOL     TEXT);''')


def add_packet(dmac, smac, prot):
    """Insert a channel in the database"""
    c.execute('''INSERT INTO PACKETS (DSTMAC, SRCMAC, PROTOCOL) VALUES (?,?,?)''',
        (dmac, smac, prot))