import logging
#from cassandra.cluster import Cluster
#from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster


keyspace="mnist_data"
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

cluster = Cluster(contact_points=['172.18.0.2'],port=9042)
session = cluster.connect()

def createKeySpace():

        log.info("Creating keyspace...")
        try:
           session.execute("""
               CREATE KEYSPACE %s
               WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
               """ %keyspace)

           log.info("setting keyspace...")
           session.set_keyspace(keyspace)

        except Exception as e:
           log.error("Unable to create keyspace")
           log.error(e)

        try:
            log.info("creating table...")
            session.execute("USE %s"%keyspace)
            session.execute("""
                                CREATE TABLE newtable (   
                                pic_name text ,
                                upload_time text,
                                result text,
                                PRIMARY KEY (pic_name,upload_time)
                                                  )
                                   """)  # set the table name
        except Exception as ex:
            log.info("unable to create table")
            log.info(ex)


def insert_data(name,upload_time,result):
        session.execute("USE %s"%keyspace)
        session.execute('''
        INSERT INTO newtable (pic_name, upload_time, result) VALUES (%s,%s,%s)
        ''',[name,upload_time,result])


def test():
        session.execute("USE %s" %keyspace)
        results=session.execute("SELECT * FROM newtable")
        for i in results:
            print(i)


def delete():
        try:
            session.execute("USE %s" %keyspace)
            session.execute("DROP TABLE newtable")
        except Exception as e:
            print(e)

