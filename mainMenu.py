import search
import follow
import collection


def mainMenu(self):
    exit = False
    quit = False
    while not exit:
        print("\t===Main Menu===\n"
              "[1] Collections\n"
              "[2] Search\n"
              "[3] Followers\n"
              "[4] Logout of this account\n"
              "[5] Quit")
        try:
            val = int(input("Choose an option by typing a number: "))

            if val == 1:
                collection.collection(self)
            elif val == 2:
                search.search(self)
            elif val == 3:
                follow.follow(self)
            elif val == 4:
                exit = True
            elif val == 5:
                quit = True
                exit = True
            else:
                print("Invalid choice. Please input a valid number.\n\n")
        except ValueError:
            print("Invalid choice. Please input a valid number.\n\n")

    return quit
