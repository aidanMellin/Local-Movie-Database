import search
import follow
import collection
import profile
import recommendation


def mainMenu(self):
    exit = False
    quit = False
    while not exit:
        print("\t===Main Menu===\n"
              "[1] Collections\n"
              "[2] Search\n"
              "[3] Followers\n"
              "[4] View Profile\n"
              "[5] View Recommendations\n"
              "[6] Logout of this account\n"
              "[7] Quit")
        try:
            val = int(input("Choose an option by typing a number: "))

            if val == 1:
                collection.collection(self)
            elif val == 2:
                search.search(self)
            elif val == 3:
                follow.follow(self)
            elif val == 4:
                profile.profile(self)
            elif val == 5:
                recommendation.recommendation(self)
            elif val == 6:
                exit = True
            elif val == 7:
                quit = True
                exit = True
            else:
                print("Invalid choice. Please input a valid number.\n\n")
        except ValueError:
            print("Invalid choice. Please input a valid number.\n\n")

    return quit
