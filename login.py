from logging import error
import psycopg2
import login
from sshtunnel import SSHTunnelForwarder
from os import getenv
from os.path import exists
from dotenv import load_dotenv
from datetime import datetime


def loginSequence(self):
    print("\n\nWelcome to the gitBash Movie Database.\n")
    while True:
        val = input("Choose an option by typing a number:\n[1]. Login to account\n[2]. Create an account\n[3]. Quit\n")
        escape = False
        if val in ('1', 'l', 'L', 'login', 'Login',):
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
                        escape = True
                    else:
                        print("Incorrect username or password.\n")
                except (Exception) as error:
                    print("Something went wrong.\n", error)
                    self.curs.close()
                    self.conn.close()

            adate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                    self.curs.execute(
                        """
                        UPDATE \"user\"
                        SET accessdate = %s
                        WHERE username = %s
                        """, 
                        [adate, username,]
                    )
                    self.curs.execute(
                        """
                        INSERT INTO access_date (username, date)
                        VALUES(%s,%s)
                        """, 
                        [username, adate]
                    )
                    self.conn.commit()
                    # print("Welcome, " + username)
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()
            return username

        elif val in ('2', 'c', 'C', 'create', 'Create'):
            while(escape != True):
                username = input("Please enter a username of 20 characters or less: ")
                while (len(username) > 20):
                    username = input("That username was too long. Please enter a username of 20 characters or less: ")
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
                except (Exception) as error:
                    print("Something went wrong.\n", error)
                    self.curs.close()
                    self.conn.close()

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
                except (Exception) as error:
                    print("Something went wrong.\n", error)
                    self.curs.close()
                    self.conn.close()

            password = input("Please enter a password of 20 characters or less: ")
            while (len(password) > 20):
                password = input("That password was too long. Please enter a password of 20 characters or less: ")
            fname = input("Please enter your first name: ")
            lname = input("Please enter your last name: ")
            cdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                self.curs.execute(
                    """
                    INSERT INTO \"user\" (username, password, email, fname, lname, accessdate, createdate)
                    VALUES(%s,%s,%s,%s,%s,%s,%s)
                    """, 
                    [username, password, email, fname, lname, cdate, cdate,]
                )
                self.curs.execute(
                        """
                        INSERT INTO access_date (username, date)
                        VALUES(%s,%s)
                        """, 
                        [username, cdate]
                )
                self.conn.commit()
            except (Exception) as error:
                    print("Something went wrong.\n", error)
                    self.curs.close()
                    self.conn.close()
            return username

        elif val in ('3', 'q', 'Q', 'quit', 'Quit'):
            return None
        
        else:
            print("Invalid choice. Please input a valid number.\n")

