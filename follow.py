
'''
self.curs.execute(
    """
    SELECT follower 
    FROM follows
    WHERE username = %s
    """, 
    [username,]
)

self.curs.execute(
      """
      INSERT INTO follows (follower, following)
      VALUES(%s,%s)
      """, 
      [username, username2]
)


self.curs.execute(
      """
      SELECT username
      FROM \"user\" 
      WHERE email = %s
      """, 
      [email,]
)

INSERT INTO follows (follower, following)
VALUES ('%s', '%s')

SELECT * FROM follows
WHERE follower='%s';

DELETE FROM follows
WHERE (follower='%s' and following='%s');

SELECT * FROM follows
WHERE follower='%s';

SELECT username FROM "user"
WHERE email='msnaddin1@t.co'

self.conn.commit()
'''
def follow(self):
    action = input("Would you like to\n\t[1]: follow\n\t[2] unfollow\na user? ").lower()
    user = input("what is the name of the user in question? ").lower()
    if "@" in user:
        user = getUsername(user)
    
    if action[0] in ('1', 'f'):
        followUsername(user)
    elif action[0] in ('2'):
        unfollow(user)


def getUsername(self,email):
    try:
        self.curs.execute(
            """
            SELECT username FROM "user"
            WHERE email='%s'
            """,
            [email]
        )
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
            VALUES ('%s', '%s')
            """,
            [self.username, user]
        )
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
    

def unfollow(self, user):
    try:
        self.curs.execute(
            """
            DELETE FROM follows
            WHERE (follower='%s' and following='%s');
            """,
            [self.username, user]
        )
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

if __name__ == '__main__':
    follow(None)