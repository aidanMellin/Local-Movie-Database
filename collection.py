from search import watchMovie


def collection(self):
    loop = True

    while loop:
        print("\t===Collection Menu===\n"
            "[1] View Collections\n"
            "[2] Create a new Collection\n"
            "[3] Delete a Collection\n"
            "[4] Add a Movie to a Collection\n"
            "[5] Remove a Movie to a Collection\n"
            "[6] Rename a Collection\n"
            "[7] Watch a movie from a Collection\n"
            "[8]. Exit to Main Menu")

        try:
            val = int(input("Choose an option by typing a number: "))

            if val == 1:
                printCollection(self)
            elif val == 2:
                createCollection(self)
            elif val == 3:
                deleteCollection(self)
            elif val == 4:
                addMovie(self)
            elif val == 5:
                removeMovie(self)
            elif val == 6:
                renameCollection(self)
            elif val == 7:
                watchMovie(self)
            elif val == 8:
                loop = False
            else:
                print("Invalid choice. Please input a valid number.\n")
        except ValueError:
            print("Invalid choice. Please input a valid number.\n")


def printCollection(self):
    try:
        self.curs.execute(
            """
            SELECT cname
            FROM \"collection\"
            WHERE username = %s
            ORDER BY cname ASC
            """,
            [self.username,]
        )
        match = self.curs.fetchall()
        if match is not None:
            for group in match:
                cname = group[0]
                self.curs.execute(
                    """
                    SELECT COUNT (*)
                    FROM \"contains\"
                    WHERE username = %s AND cname = %s
                    """,
                    [self.username, cname]
                )
                amount = self.curs.fetchone()
                self.curs.execute(
                    """
                    SELECT SUM(M.length) 
                    FROM \"movie\" M, \"contains\" C
                    WHERE C.username = %s AND C.cname = %s AND C.title = M.title AND C.reldate = M.reldate
                    """,
                    [self.username, cname]
                )
                total = self.curs.fetchone()
                if total[0] is None:
                    total = 0
                else:
                    total = total[0]
                print(cname + ", Movies in collection: " + str(amount[0]) +
                      ", Total length of movies: " + str(total // 60) + " hours:" + str(total % 60) + " minutes")
        else:
            print("You have no Collections...")
    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()


def createCollection(self):
    name = input("Please enter a name of 20 characters or less for the Collection: ")
    while len(name) > 20:
        name = input("That name was too long. Please enter a name of 20 characters or less: ")
    duplicate = False
    try:
        self.curs.execute(
            """
            SELECT * 
            FROM \"collection\" 
            WHERE username = %s AND cname = %s
            """,
            [self.username, name,]
        )
        match = self.curs.fetchone()
        if match is not None:
            duplicate = True
            print("You already have Collection with the name \""+name+"\"")
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
    if not duplicate:
        try:
            self.curs.execute(
                """
                INSERT INTO \"collection\" (cname, username)
                VALUES(%s,%s)
                """,
                [name, self.username,]
            )
            self.conn.commit()
        except (Exception) as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()


def deleteCollection(self):
    escape = False
    name = input("Please enter the name for the Collection you want to delete: ")
    try:
        self.curs.execute(
            """
            SELECT * 
            FROM \"collection\" 
            WHERE username = %s AND cname = %s
            """,
            [self.username, name,]
        )
        match = self.curs.fetchone()
        if match is None:
            escape = True
            print("You have no Collection with the name \""+name+"\"")
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    if not escape:
        print("Please confirm that you wanna delete the Collection \""+name+"\"")
        loop = True
        confirmation = ""
        while loop:
            confirmation = input("Please enter Yes or No: ").lower()
            if confirmation in ('yes', 'y', 'no', 'n',):
                loop = False
            else:
                print("Invalid entry.")
        if confirmation in ('yes', 'y',):
            try:
                self.curs.execute(
                    """
                    DELETE FROM \"collection\" 
                    WHERE username = %s AND cname = %s
                    """,
                    [self.username, name,]
                )
                self.conn.commit()
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()

            try:
                self.curs.execute(
                    """
                    DELETE FROM \"contains\" 
                    WHERE username = %s AND cname = %s
                    """,
                    [self.username, name,]
                )
                self.conn.commit()
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()


def renameCollection(self):
    escape = False
    name = input("Please enter the name for the Collection you want to rename: ")
    try:
        self.curs.execute(
            """
            SELECT * 
            FROM \"collection\" 
            WHERE username = %s AND cname = %s
            """,
            [self.username, name,]
        )
        match = self.curs.fetchone()
        if match is None:
            escape = True
            print("You have no Collection with the name \""+name+"\"")
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()
    if not escape:
        rename = input("Please enter a name of 20 characters or less for the Collection: ")
        while len(rename) > 20:
            rename = input("That name was too long. Please enter a name of 20 characters or less: ")
        duplicate = False

        try:
            self.curs.execute(
                """
                SELECT * 
                FROM \"collection\" 
                WHERE username = %s AND cname = %s
                """,
                [self.username, rename,]
            )
            match = self.curs.fetchone()
            if match is not None:
                duplicate = True
                print("You already have Collection with the name \""+rename+"\"")
        except Exception as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()

        if not duplicate:
            try:
                self.curs.execute(
                    """
                    INSERT INTO \"collection\" (cname, username)
                    VALUES(%s,%s)
                    """,
                    [rename, self.username,]
                )
                self.conn.commit()
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()

            try:
                self.curs.execute(
                    """
                    UPDATE \"contains\" 
                    SET cname = %s
                    WHERE username = %s AND cname = %s
                    """,
                    [rename, self.username, name,]
                )
                self.conn.commit()
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()

            try:
                self.curs.execute(
                    """
                    DELETE FROM \"collection\" 
                    WHERE username = %s AND cname = %s
                    """,
                    [self.username, name,]
                )
                self.conn.commit()
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()


def addMovie(self):
    escape = False
    cname = input("Please enter the name for the Collection you want to add to: ")
    try:
        self.curs.execute(
            """
            SELECT * 
            FROM \"collection\" 
            WHERE username = %s AND cname = %s
            """,
            [self.username, cname,]
        )
        match = self.curs.fetchone()
        if match is None:
            escape = True
            print("You have no Collection with the name \""+cname+"\"")
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    if not escape:
        mname = input("Please enter the name of the movie you want to add to "+cname+": ")
        found = False
        val = 0
        choice = None
        try:
            self.curs.execute(
                """
                SELECT title, reldate 
                FROM \"movie\" 
                WHERE title LIKE %(mname)s
                ORDER BY title ASC
                """,
                {'mname': '%{}%'.format(mname)}
            )
            match = self.curs.fetchall()
            if len(match) == 0:
                print("There are no movies with the name \""+mname+"\"")
            else:
                found = True
                print("Movies found in the search (" + str(len(match)) + "):")
                for i, movie in enumerate(match):
                    print(str(i+1) + ": " + movie[0] + ", " +
                          str(movie[1].month) + "/" + str(movie[1].day) + "/" + str(movie[1].year))

                try:
                    loop = True
                    while loop:
                        val = int(input("Please enter the number for which movie you want to add"
                                        " or \'0\' to not add any of them: "))
                        if val <= len(match):
                            loop = False
                            if val != 0:
                                choice = match[val-1]
                        else:
                            print("Invalid choice. Please input a valid number.\n")
                except ValueError:
                    print("Invalid choice. Please input a valid number.\n")
        except Exception as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()

        if found and val != 0:
            mname = choice[0]
            reldate = choice[1]
            duplicate = False
            try:
                self.curs.execute(
                    """
                    SELECT *
                    FROM \"contains\" 
                    WHERE username = %s AND cname = %s AND title = %s AND reldate = %s
                    """,
                    [self.username, cname, mname, reldate,]
                )
                match = self.curs.fetchone()
                if match is not None:
                    duplicate = True
                    print("You already have " + mname + " in " + cname)
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()
            if not duplicate:
                try:
                    self.curs.execute(
                        """
                        INSERT INTO \"contains\" 
                        VALUES (%s,%s,%s,%s)
                        """,
                        [mname, reldate, cname, self.username,]
                    )
                    self.conn.commit()
                except (Exception) as error:
                    print("Something went wrong.\n", error)
                    self.curs.close()
                    self.conn.close()


def removeMovie(self):
    escape = False
    cname = input("Please enter the name for the Collection you want to remove from: ")

    try:
        self.curs.execute(
            """
            SELECT * 
            FROM \"collection\" 
            WHERE username = %s AND cname = %s
            """,
            [self.username, cname,]
        )
        match = self.curs.fetchone()
        if match is None:
            escape = True
            print("You have no Collection with the name \""+cname+"\"")
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    if not escape:
        val = 0
        choice = None
        try:
            self.curs.execute(
                """
                SELECT * 
                FROM \"contains\"
                WHERE username = %s AND cname = %s
                """,
                [self.username, cname]
            )
            match = self.curs.fetchall()

            print("Items in collection: " + str(len(match)))
            for i, mname in enumerate(match):
                print(str(i+1) + ": " + mname[0])

            try:
                loop = True
                while loop:
                    val = int(input("Please enter the number for which movie you want to remove"
                                    " or \'0\' to not remove any of them: "))
                    if val <= len(match):
                        loop = False
                        if val != 0:
                            choice = match[val-1]
                    else:
                        print("Invalid choice. Please input a valid number.\n")
            except ValueError:
                print("Invalid choice. Please input a valid number.\n")
        except Exception as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()

        if val != 0:
            mname = choice[0]
            reldate = choice[1]
            try:
                self.curs.execute(
                    """
                    DELETE FROM \"contains\" 
                    WHERE username = %s AND cname = %s AND title = %s AND reldate = %s
                    """,
                    [self.username, cname, mname, reldate,]
                )
                self.conn.commit()
            except (Exception) as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()

def watchMovie(self):
    loop = True
    reldate = ""
    while loop:
        movieName = input("Please enter the name of the movie that you would like to watch: ").title()
        try:
            self.curs.execute("""
                SELECT movie.title, movie.reldate FROM movie
                WHERE movie.title LIKE '%{0}%'
            """.format(movieName))

            results = self.curs.fetchall()
            if results is not None:
                for movie in results:
                    loop = False
                    print(reldate)
            else:
                print("There are no movies with that name. Please try again.")
        except (Exception) as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()

    try:
        self.curs.execute(
            """
            SELECT *
            FROM watches
            WHERE username=%s AND title=%s;
            """,
            [self.username, movieName,]
        )
        match = self.curs.fetchone()
        if match is None:
            try:
                self.curs.execute(
                """
                INSERT INTO watches (username, reldate, title)
                VALUES (%s, %s, %s)
                """,
                [self.username, reldate, movieName,]
                )
                self.conn.commit()
            except Exception as error:
                print("Something went wrong.\n", error)
                self.curs.close()
                self.conn.close()       
        
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    try:
        self.curs.execute(
        """
        UPDATE watches
        SET watched = watched + 1
        WHERE username=%s AND title=%s;

        """,
        [self.username, movieName,]
        )
        self.conn.commit()
        print("Successfully logged your watching of", movieName+"\n")
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()