import psycopg2
import login
from sshtunnel import SSHTunnelForwarder
from os import getenv
from os.path import exists
from dotenv import load_dotenv

def loginSequence(self):
    print("\n\nWelcome to the gitBash Movie Database.\n")
    val = input("Choose an option by typing a number:\n[1]. Login to account\n[2]. Create an account\n")
    if val in ('1', 'L', 'l', 'login', 'Login'):
        escape = False
        while(escape != True):
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            try:
                self.curs.execute(
                    """
                    SELECT * 
                    FROM \"user\" 
                    WHERE username = %s AND password = %s
                    """, 
                    [username, password,]
                )
                match = self.curs.fetchone()
                if(match is not None):
                    print("Welcome, " + username)
                    escape = True
                else:
                    print("Incorrect username or password.\n")
            except:
                print("something wrong")
    elif val in ('2', 'C', 'c', 'create', 'Create'):
        print("Create account selected.")