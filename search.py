def search(self):
    goBack = False
    while not goBack:
        print("\t\n===Search Options===\n"
              "[1] By Name - Format: '1#movie_name'\n"
              "[2] By Release Date - Format: '2#YYYY-MM-DD'\n"
              "[3] By Cast Members - Format: '3#first_name#last_name'\n"
              "[4] By Studio - Format: '4#studio'\n"
              "[5] By Genre - Format: '5#genre'\n"
              "[6] Back to Main Menu - Format: '6'\n"
              )
        try:
            command = input("Type a search command: ").split('#')

            if int(command[0]) == 1 and len(command) == 2:
                searchByName(self, command[1])
                sort(self, int(command[0]), command[1])
            elif int(command[0]) == 2 and len(command) == 2:
                searchByReleaseDate(self, command[1])
                sort(self, int(command[0]), command[1])
            elif int(command[0]) == 3 and len(command) == 3:
                searchByCastMember(self, command[1], command[2])
                sort(self, int(command[0]), command[1], command[2])
            elif int(command[0]) == 4 and len(command) == 2:
                searchByStudio(self, command[1])
                sort(self, int(command[0]), command[1])
            elif int(command[0]) == 5 and len(command) == 2:
                searchByGenre(self, command[1])
                sort(self, int(command[0]), command[1])
            elif int(command[0]) == 6:
                print("Back to main menu...")
                goBack = True
            else:
                print("Invalid choice. Please input a valid search command\n\n")
        except ValueError:
            print("Invalid choice. Please input a valid search command\n\n")

def sort(self, command_num, var1, var2=None):
    commands = {1: searchByName, 2: searchByReleaseDate, 3: searchByCastMember,
                4: searchByStudio, 5: searchByGenre}
    quit = False
    while not quit:
        print("\t\n===Sort Options===\n"
              "[1] By Name - Format: '1#order' (order= ASC or DESC)\n"
              "[2] By Release Year - Format: '2#order' (order= ASC or DESC)\n"
              "[3] By Studio - Format: '3#order' (order= ASC or DESC)\n"
              "[4] By Genre - Format: '4#order' (order= ASC or DESC)\n"
              "[5] Back to Search Menu\n\n"
              "OR\n\n"
              "[6] Watch Movie - Format: '6#movie_name#release_date' (YYYY-MM-DD)\n"
              "[7] Get Movie Release Date - Format: '7#movie_name'\n"
              "[8] Rate Movie - Format: '8#movie_name#release_date#rating' (rating = 0.0-5.0)\n"
              )
        try:
            command = input("Type a command: ").split('#')

            sorts = {1: "movie.title", 2: "movie.reldate", 3: "movie.studio", 4: "categorized_as.gname"}

            if len(command) == 2 and int(command[0]) < 5:
                if 0 < int(command[0]) < 5 and (command[1] == "ASC" or command[1] == "DESC"):
                    if command_num == 3:
                        commands[command_num](self, var1, var2, sorts[int(command[0])], command[1])
                    else:
                        commands[command_num](self, var1, sorts[int(command[0])], command[1])
            elif int(command[0]) == 5:
                quit = True
            elif int(command[0]) == 6 and len(command) == 3:
                watchMovie(self, command[1], command[2])
            elif int(command[0]) == 7 and len(command) == 2:
                getRelDate(self, command[1])
            elif int(command[0]) == 8 and len(command) == 4:
                rateMovie(self, command[1], command[2], command[3])
            else:
                print("Invalid choice. Please input a valid command\n\n")
        except ValueError:
            print("Invalid choice. Please input a valid command\n\n")

def rateMovie(self, movie_name, rel_date, rating):
    try:
        self.curs.execute("""
            SELECT * FROM watches
            WHERE watches.username = '{0}'
            AND watches.title = '{1}'
            AND watches.reldate = '{2}'
        """.format(self.username, movie_name, rel_date))

        results = self.curs.fetchone()
        if results is not None:
            self.curs.execute("""
                UPDATE watches
                SET rating = '{3}'
                WHERE watches.username = '{0}'
                AND watches.title = '{1}'
                AND watches.reldate = '{2}'
            """.format(self.username, movie_name, rel_date, rating))
            self.conn.commit()
            self.curs.execute("""
                SELECT AVG(rating) FROM watches
                WHERE watches.title = '{0}'
                AND watches.reldate = '{1}'
            """.format(movie_name, rel_date))
            average = self.curs.fetchone()[0]
            self.curs.execute("""
                UPDATE movie
                SET avgrate = {0}
                WHERE movie.title = '{1}'
                AND movie.reldate = '{2}'
            """.format(average, movie_name, rel_date))
            self.conn.commit()
            print("Movie successfully rated!")
        else:
            print("Invalid input. Make sure you have watched this movie before and try again.")
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()


def watchMovie(self, movie_name, rel_date):
    try:
        self.curs.execute("""
            SELECT * FROM watches
            WHERE watches.username = '{0}'
            AND watches.title = '{1}'
            AND watches.reldate = '{2}'
        """.format(self.username, movie_name, rel_date))

        results = self.curs.fetchone()
        if results is not None:
            self.curs.execute("""
                UPDATE watches
                SET watched = watched + 1
                WHERE watches.username = '{0}'
                AND watches.title = '{1}'
                AND watches.reldate = '{2}'
            """.format(self.username, movie_name, rel_date))
            self.conn.commit()
            print("\n\nMovie Watched!")
        else:
            self.curs.execute("""
                INSERT INTO watches (username, reldate, title, rating, watched)
                VALUES (%s, %s, %s, %s, %s)
            """, (self.username, rel_date, movie_name, 0.0, 1))
            self.conn.commit()
            print("\nMovie Watched!")
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def getRelDate(self, movie_name):
    try:
        self.curs.execute("""
            SELECT movie.title, movie.reldate FROM movie
            WHERE movie.title LIKE '%{0}%'
        """.format(movie_name))

        results = self.curs.fetchall()
        if results is not None:
            for movie in results:
                print("Movie: " + movie[0] + "  Release Date: " + str(movie[1]))
        else:
            print("There are no movies with that name. Please try again.")
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def searchByName(self, name, sort_num="movie.title, movie.reldate", order="ASC"):
    try:
        self.curs.execute(
        """
        SELECT movie.title, acted_by.fname, acted_by.lname, directed_by.fname, directed_by.lname, movie.length, 
            movie.mpaa, movie.avgrate FROM movie
        INNER JOIN acted_by ON movie.title = acted_by.title
        INNER JOIN directed_by ON movie.title = directed_by.title
        INNER JOIN categorized_as ON movie.title = categorized_as.title
        WHERE movie.title LIKE '%{0}%'
        ORDER BY {1} {2}
        """.format(name, sort_num, order))
        result = self.curs.fetchall()
        if result is None:
            print("There are no movies with that title. Please try again")
        else:
            for entry in result:
                print(entry)
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def searchByStudio(self, studio, sort_num="movie.title, movie.reldate", order="ASC"):
    try:
        self.curs.execute("""
            SELECT movie.title, acted_by.fname, acted_by.lname, directed_by.fname, directed_by.lname, movie.length, 
                movie.mpaa, movie.avgrate FROM movie
            INNER JOIN acted_by ON movie.title = acted_by.title
            INNER JOIN directed_by ON movie.title = directed_by.title
            INNER JOIN categorized_as ON movie.title = categorized_as.title
            WHERE movie.studio LIKE '%{0}%'
            ORDER BY {1} {2}
        """.format(studio, sort_num, order))
        result = self.curs.fetchall()
        if result is None:
            print("There are no movies from that studio. Please try again")
        else:
            for entry in result:
                print(entry)
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def searchByGenre(self, genre, sort_num="movie.title, movie.reldate", order="ASC"):
    try:
        self.curs.execute("""
                    SELECT movie.title, acted_by.fname, acted_by.lname, directed_by.fname, directed_by.lname, movie.length, 
                        movie.mpaa, movie.avgrate FROM movie
                    INNER JOIN acted_by ON movie.title = acted_by.title
                    INNER JOIN directed_by ON movie.title = directed_by.title
                    INNER JOIN categorized_as ON movie.title = categorized_as.title
                    WHERE categorized_as.gname LIKE '%{0}%'
                    ORDER BY {1} {2}
                """.format(genre, sort_num, order))
        result = self.curs.fetchall()
        if result is None:
            print("There are no movies with that genre. Please try again")
        else:
            for entry in result:
                print(entry)
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def searchByCastMember(self, fname, lname, sort_num="movie.title, movie.reldate", order="ASC"):
    try:
        self.curs.execute("""
                    SELECT movie.title FROM movie
                    INNER JOIN acted_by ON movie.title = acted_by.title
                    INNER JOIN categorized_as ON movie.title = categorized_as.title
                    WHERE acted_by.fname = '{0}' AND acted_by.lname = '{1}'
                """.format(fname, lname))
        result = self.curs.fetchall()
        if result is None:
            print("There are no movies with that cast member. Please try again")
        else:
            for entry in result:
                searchByName(self, entry[0])
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def searchByReleaseDate(self, date, sort_num="movie.title, movie.reldate", order="ASC"):
    try:
        self.curs.execute("""
            SELECT movie.title, acted_by.fname, acted_by.lname, directed_by.fname, directed_by.lname, movie.length, 
                movie.mpaa, movie.avgrate FROM movie
            INNER JOIN acted_by ON movie.title = acted_by.title
            INNER JOIN directed_by ON movie.title = directed_by.title
            INNER JOIN categorized_as ON movie.title = categorized_as.title
            WHERE movie.reldate = '{0}'
            ORDER BY {1} {2}
        """.format(date, sort_num, order))
        result = self.curs.fetchall()
        if result is None:
            print("There are no movies from that studio. Please try again")
        else:
            for entry in result:
                print(entry)
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()