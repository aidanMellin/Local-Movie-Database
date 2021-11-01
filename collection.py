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
              "[7]. Exit to Main Menu")

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
                print("5")
            elif val == 6:
                renameCollection(self)
            elif val == 7:
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
        if(match is not None):
            for cname in match:
                print(cname[0])
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
                    UPDATE \"collection\" 
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
