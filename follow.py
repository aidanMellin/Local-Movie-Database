def follow(self):
    escape = False
    skipcheck = False

    while not escape:
        action = input("What would you like to do?\n[1] Follow\n[2] Unfollow\n[3] Quit\n").lower()
        if action[0] in ('3', 'q'):
            return
        
        user = input("What is the username or email of the user?\n").lower()
        if "@" in user:
            user = getUsername(self,user)
            if user is None:
                skipcheck = True
            else:
                user = user[0]
        
        if action[0] in ('2'):
            unfollow(self,user)

        if not skipcheck:
            namecheck = checkName(self, user)
            copycheck = checkCopy(self, user)
            if namecheck and copycheck:
                escape = True
        if not namecheck or skipcheck:
            print("That is not a valid user. Please try again.")
            skipcheck = False
        elif not copycheck:
            print("You are already following this user.")
    if action[0] in ('1', 'f'):
        followUsername(self,user)
    

def checkName(self, name):
    try:
        self.curs.execute(
            """
            SELECT * 
            FROM \"user\"
            WHERE username=%s
            """,
            [name]
        )
        match = self.curs.fetchone()
        if(match is not None):
            return True
        else:
            return False
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
        return False

def checkCopy(self, name):
    try:
        self.curs.execute(
            """
            SELECT * 
            FROM follows
            WHERE follower=%s AND following=%s
            """,
            [self.username, name]
        )
        match = self.curs.fetchone()
        if(match is not None):
            return False
        else:
            return True
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
        return False

def getUsername(self,email):
    try:
        self.curs.execute(
            """
            SELECT username FROM \"user\"
            WHERE email=%s
            """,
            [email]
        )
        target = self.curs.fetchone()
        return target
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
        return False

def followUsername(self, user):
    print("in followUsername")
    try:
        self.curs.execute(
            """
            INSERT INTO follows (follower, following)
            VALUES (%s, %s)
            """,
            [self.username, user]
        )
        self.conn.commit()
        print("User followed successfully.\n")
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
    
def unfollow(self, user):
    try:
        self.curs.execute(
            """
            DELETE FROM follows
            WHERE (follower=%s and following=%s);
            """,
            [self.username, user,]
        )
        self.conn.commit()
        print("User unfollowed successfully\n")
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()