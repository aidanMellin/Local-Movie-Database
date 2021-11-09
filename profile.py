

# main function for user profile
# shows profile info and allows user to go back to the Main Menu
def profile(self):
    exit = False
    sort = "rating"
    while not exit:
        print("\t\n===My Profile===\n"
              "Number of Collections: " + get_number_of_collections(self) + "\n"
              "Followers: " + get_followers(self) + "\n"
              "Following: " + get_following(self) + "\n"
              "Top 10 Movies: "
              )
        get_top_ten_movies(self, sort)
        print("\n"
              "[1] Top 10 By Highest Rating\n"
              "[2] Top 10 By Most Plays\n"
              "[3] Top 10 By Highest Rating and Most Plays\n"
              "[4] Back to Main Menu"

              )
        try:
            val = int(input("Choose an option by typing a number: "))

            if val == 1:
                sort = "rating"
            elif val == 2:
                sort = "plays"
            elif val == 3:
                sort = "both"
            elif val == 4:
                exit = True
            else:
                print("Invalid choice. Please input a valid number.\n\n")
        except ValueError:
            print("Invalid choice. Please input a valid number.\n\n")

# returns the number of collections that a user has in string format
def get_number_of_collections(self):
    try:
        self.curs.execute("""
            SELECT COUNT(*) FROM collection
            WHERE collection.username = '{0}'
        """.format(self.username))

        return str(self.curs.fetchone()[0])

    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def get_followers(self):
    try:
        self.curs.execute("""
            SELECT COUNT(*) FROM follows
            WHERE follows.following = '{0}'
        """.format(self.username))

        return str(self.curs.fetchone()[0])

    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def get_following(self):
    try:
        self.curs.execute("""
            SELECT COUNT(*) FROM follows
            WHERE follows.follower = '{0}'
        """.format(self.username))

        return str(self.curs.fetchone()[0])

    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

def get_top_ten_movies(self, sort):
    if sort == "rating":
        try:
            self.curs.execute("""
                SELECT watches.title FROM watches
                WHERE watches.username = '{0}'
                ORDER BY watches.rating DESC
            """.format(self.username))

            movie_list = self.curs.fetchall()
            length = len(movie_list)

            if movie_list is not []:
                num = 1
                if length > 10:
                    for movie in movie_list:
                        if num <= 10:
                            print("\t" + str(num) + ": " + movie[0])
                            num += 1
                else:
                    for movie in movie_list:
                        print("\t" + str(num) + ": " + movie[0])
                        num += 1
            else:
                print("No movies watched")

        except (Exception) as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()

    elif sort == "plays":
        try:
            self.curs.execute("""
                SELECT watches.title FROM watches
                WHERE watches.username = '{0}'
                ORDER BY watches.watched DESC
            """.format(self.username))

            movie_list = self.curs.fetchall()
            length = len(movie_list)

            if movie_list is not []:
                num = 1
                if length > 10:
                    for movie in movie_list:
                        if num <= 10:
                            print("\t" + str(num) + ": " + movie[0])
                            num += 1
                else:
                    for movie in movie_list:
                        print("\t" + str(num) + ": " + movie[0])
                        num += 1
            else:
                print("No movies watched")

        except (Exception) as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()

    elif sort == "both":
        try:
            self.curs.execute("""
                SELECT watches.title FROM watches
                WHERE watches.username = '{0}'
                ORDER BY watches.rating DESC
            """.format(self.username))

            movie_list_1 = self.curs.fetchall()
            length = len(movie_list_1)

            if movie_list_1 is not []:
                index = 0
                final_dict = {}
                for movie in movie_list_1:
                    final_dict[movie[0]] = length - index
                    index += 1

                try:
                    self.curs.execute("""
                        SELECT watches.title FROM watches
                        WHERE watches.username = '{0}'
                        ORDER BY watches.watched DESC
                    """.format(self.username))

                    movie_list_2 = self.curs.fetchall()

                    index2 = 0
                    for movie in movie_list_2:
                        final_dict[movie[0]] += length - index2
                        index2 += 1

                    new_dict = dict(sorted(final_dict.items(), key=lambda item: item[1], reverse=True))

                    num = 1
                    if length > 10:
                        for movie in new_dict:
                            if num <= 10:
                                print("\t" + str(num) + ": " + movie)
                                num += 1
                    else:
                        for movie in new_dict:
                            print("\t" + str(num) + ": " + movie)
                            num += 1

                except (Exception) as error:
                    print("Something went wrong.\n", error)
                    self.curs.close()
                    self.conn.close()

            else:
                print("No movies watched")

        except (Exception) as error:
            print("Something went wrong.\n", error)
            self.curs.close()
            self.conn.close()