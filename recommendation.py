from datetime import date


def recommendation(self):
    loop = True

    while loop:
        print("\t===Recommendation Menu===\n"
              "[1] Top 20 most popular movies in the last 90 days\n"
              "[2] The top 20 most popular movies among my friends\n"
              "[3] The top 5 new releases of the month (calendar month)\n"
              "[4] For you: Recommend movies to watch to based on your play history\n"
              "[5] Exit to Main Menu")

        try:
            val = int(input("Choose an option by typing a number: "))

            if val == 1:
                print("1")
            elif val == 2:
                topFriends(self)
            elif val == 3:
                topmonth(self)
            elif val == 4:
                print("4")
            elif val == 5:
                loop = False
            else:
                print("Invalid choice. Please input a valid number.\n")
        except ValueError:
            print("Invalid choice. Please input a valid number.\n")


def topFriends(self):
    friends = []
    try:
        self.curs.execute(
            """
            SELECT following 
            FROM \"follows\" 
            WHERE follower = %s
            """,
            [self.username, ]
        )
        friends = self.curs.fetchone()
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    if friends is None:
        print("You don't follow anyone...")
    else:
        for friend in friends:
            print()


def topmonth(self):
    today = date.today()
    if today.month == 12:
        max_limit = today.replace(year=date.today().year+1, month=1, day=1)
        min_limit = today.replace(day=1)
    else:
        max_limit = today.replace(month=date.today().month+1, day=1)
        min_limit = today.replace(day=1)
    movies = []
    try:
        self.curs.execute(
            """
            SELECT reldate, title, mpaa, avgrate 
            FROM \"movie\" 
            WHERE %s > reldate AND reldate >= %s
            ORDER BY avgrate ASC
            """,
            [max_limit, min_limit, ]
        )
        movies = self.curs.fetchall()
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
    if movies is None or len(movies) == 0:
        print("There are no movies from this month.")
    else:
        print("Top 5 Rated movies:")
        if len(movies) > 5:
            movies = movies[0:5]
        for i in range(len(movies)):
            movie = movies[i]
            if movie[3] is None:
                print(str(i+1) + ": " + movie[1] + ", " + movie[2])
            else:
                print(str(i+1) + ": " + movie[1] + ", " + movie[2] + " (" + movie[3] + "/5)")
