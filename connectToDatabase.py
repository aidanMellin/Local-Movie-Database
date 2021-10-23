import psycopg2
from sshtunnel import SSHTunnelForwarder
from os import getenv
from os.path import exists
from dotenv import load_dotenv

"""
Check if .env file already exists, if not, create and ask user to populate for first time
"""
if not exists(".env"):
    uInput = input("What is your CS@RIT Username: ")
    pInput = input("What is your CS@RIT Password: ")
    with open(".env", "w+") as f:
        f.write("# .env\n")
        f.write("USERNAME="+uInput+"\n")
        f.write("PASSWORD="+pInput+"\n")

"""
Load dotenv file
"""
load_dotenv()
USERNAME=getenv('USERNAME')
PASSWORD=getenv('PASSWORD')


class Database:
    def __init__(self):
        try:
            with SSHTunnelForwarder(
                'starbug.cs.rit.edu',
                ssh_username=USERNAME,
                ssh_password=PASSWORD,
                remote_bind_address=('localhost', 5432)) as server:

                server.start()
                print ("SSH tunnel established")

                params = {
                'database': 'p320_14',
                'user': USERNAME,
                'password': PASSWORD,
                'host': 'localhost',
                'port': server.local_bind_port
                }

                self.conn = psycopg2.connect(**params)
                self.curs = self.conn.cursor()
                print ("Database connection established")

                #Basic idea of what we do python CLI integration
                self._execute("SELECT * FROM genres;")
                print(self.curs.fetchone())

                #Close the connections after they're done
                self.curs.close()
                self.conn.close()

        except:
            print ("Connection failed")

    def _execute(self, command):
        self.curs.execute("SELECT * FROM genres;")
        self.conn.commit()

if __name__ == "__main__":
    db = Database()