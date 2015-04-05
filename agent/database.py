import sqlite3 as lite


table_name = 'PACKETS'

# Connect to dump database. Create if it doesnt exist.
datab = lite.connect('agent/dump.db', isolation_level=None, check_same_thread=False)
#Create table if it doesnt exist
write = datab.cursor()
read = datab.cursor()

datab.execute('''CREATE TABLE IF NOT EXISTS PACKETS
   (ID  INTEGER PRIMARY KEY AUTOINCREMENT,
   TYPE         TEXT,
   SRCMAC       TEXT,
   DSTMAC       TEXT,
   PROTOCOL     TEXT,
   VERSION      TEXT,
   IPHL         TEXT,
   TTL          TEXT,
   SRCADR       TEXT,
   DSTADR       TEXT,
   SRCPRT       TEXT,
   DSTPRT       TEXT,
   SEQUENCE     TEXT,
   ACK          TEXT,
   TCPHL        TEXT,
   ICMPTYPE     TEXT,
   CODE         TEXT,
   CHCKSM       TEXT,
   LENGTH       TEXT,
   DATA         TEXT);''')


def add_tcp_packet(type, smac, dmac, prot, ver, iphl, ttl, srcadr, dstadr, srcprt, dstprt, seq, ack, tcphl):
    """Insert a channel in the database"""
    try:
        write.execute('''INSERT INTO PACKETS (TYPE, SRCMAC, DSTMAC, PROTOCOL, VERSION, IPHL, TTL, SRCADR, DSTADR, SRCPRT,
        DSTPRT, SEQUENCE, ACK, TCPHL)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (type, smac, dmac, prot, ver, iphl, ttl, srcadr, dstadr, srcprt, dstprt, seq, ack, tcphl))
    except lite.OperationalError:
            pass

def add_icmp_packet(type, smac, dmac, prot, ver, iphl, ttl, srcadr, dstadr, cmptyp, code, chksm):
    """Insert a channel in the database"""
    try:
        write.execute('''INSERT INTO PACKETS (TYPE, SRCMAC, DSTMAC, PROTOCOL, VERSION, IPHL, TTL, SRCADR, DSTADR, ICMPTYPE,
        CODE, CHCKSM)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (type, smac, dmac, prot, ver, iphl, ttl, srcadr, dstadr, cmptyp, code, chksm))
    except lite.OperationalError:
            pass

def add_udp_packet(type, smac, dmac, prot, ver, iphl, ttl, srcadr, dstadr, srcprt, dstprt, len, chksm):
    """Insert a channel in the database"""
    try:
        write.execute('''INSERT INTO PACKETS (TYPE, SRCMAC, DSTMAC, PROTOCOL, VERSION, IPHL, TTL, SRCADR, DSTADR, SRCPRT,
        DSTPRT, LENGTH, CHCKSM)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (type, smac, dmac, prot, ver, iphl, ttl, srcadr, dstadr, srcprt, dstprt, len, chksm))
    except lite.OperationalError:
        pass

def get_last_packet(amount):
    with datab:
        try:
            read.execute('''SELECT * FROM (SELECT ID, TYPE, SRCADR, DSTADR, VERSION, SRCPRT, DSTPRT, TTL FROM PACKETS ORDER BY ID DESC LIMIT 13)
            ORDER BY ID''')
            data = read.fetchall()
            return data
        except lite.OperationalError:
            pass