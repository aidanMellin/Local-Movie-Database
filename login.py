import psycopg2
import login
from sshtunnel import SSHTunnelForwarder
from os import getenv
from os.path import exists
from dotenv import load_dotenv
from datetime import datetime

def loginSequence(self):
    print("\n\nWelcome to the gitBash Movie Database.\n")
    val = input("Choose an option by typing a number:\n[1]. Login to account\n[2]. Create an account\n")
    escape = False
    if val in ('1', 'l', 'login'):
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
        adate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        


    elif val in ('2', 'c', 'create'):
        while(escape != True):
            username = input("Please enter a username of 20 characters or less: ")
            try:
                self.curs.execute(
                    """
                    SELECT * 
                    FROM \"user\" 
                    WHERE username = %s
                    """, 
                    [username]
                )
                match = self.curs.fetchone()
                if(match is None):
                    escape = True
                else:
                    print("This username is already in use. Please choose another.\n")
            except:
                print("something wrong")
        escape = False
        while(escape != True):
            email = input("Please enter your email address: ")
            try:
                self.curs.execute(
                    """
                    SELECT * 
                    FROM \"user\" 
                    WHERE email = %s
                    """, 
                    [email]
                )
                match = self.curs.fetchone()
                if(match is None):
                    escape = True
                else:
                    print("This email is already in use. Please use another.\n")
            except:
                print("something wrong")
        password = input("Please enter a password of 20 characters or less: ")
        fname = input("Please enter your first name: ")
        lname = input("Please enter your last name: ")
        cdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.curs.execute(
                """
                INSERT INTO user (username, password, email, fname, lname, accessdate, createdate)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
                """, 
                [username, password, email, fname, lname, cdate, cdate,]
            )
            self.conn.commit()
        except:
            print("something wrong")
