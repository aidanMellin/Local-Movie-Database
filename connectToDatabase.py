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

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print ("Database connection established")

except:
    print ("Connection failed")