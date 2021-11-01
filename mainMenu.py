import search
import follow


def mainMenu(self):
    exit = False
    quit = False
    while not exit:
        print("\t===Main Menu===\n"
            "[1] Collections\n"
            "[2] Watch/Play\n"
            "[3] Search\n"
            "[4] Followers\n"
            "[5] Display Main Menu\n"
            "[6] Logout of this account\n"
            "[7] Quit")
        try:
            val = int(input("Choose an option by typing a number: "))

            if val == 3:
                search.search(self)
            elif val == 4:
                follow.follow(self)
            elif val == 6:
                exit = True
            elif val == 7:
                quit = True
                exit = True
            else:
                print("Invalid choice. Please input a valid number.\n")
        except ValueError:
            print("Invalid choice. Please input a valid number.\n")

    return quit