

# main function for user profile
# shows profile info and allows user to go back to the Main Menu
def profile(self):
    exit = False
    while not exit:
        print("\t\nMy Profile===\n"
              "Number of Collections: " + get_number_of_collections(self) + "\n"
              "Followers: " + get_followers(self) + "\n"
              "Following: \n"
              "Top 10 Movies: \n\n"
              "[1] Back to Main Menu"
              )
        try:
            val = int(input("Choose an option by typing a number: "))

            if val == 1:
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