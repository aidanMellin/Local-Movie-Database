def follow(self):
    print(True)
    action = input("Would you like to\n\t[1]: follow\n\t[2] unfollow\na user? ").lower()
    user = input("what is the name of the user in question? [email or username] ").lower()
    if "@" in user:
        print("translating from email. user old =", user)
        print("have self.username =",self.username)
        user = getUsername(user)
        print("username:",user)
    
    if action[0] in ('1', 'f'):
        followUsername(user)
    elif action[0] in ('2'):
        unfollow(user)


def getUsername(self,email):
    try:
        self.curs.execute(
            """
            SELECT username FROM user
            WHERE email=%s
            """,
            [email]
        )
        print(self.fetchone())
        return self.fetchone()
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
        return False

def followUsername(self, user):
    try:
        self.curs.execute(
            """
            INSERT INTO follows (follower, following)
            VALUES (%s, %s)
            """,
            [self.username, user]
        )
        print("User followed successfully.")
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
        print("User unfollowed successfully")
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()