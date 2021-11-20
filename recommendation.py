from datetime import date, timedelta
import datetime


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
                rolling_ninety(self)
            elif val == 2:
                topFriends(self)
            elif val == 3:
                top_5(self)
            elif val == 4:
                print("4")
            elif val == 5:
                loop = False
            else:
                print("Invalid choice. Please input a valid number.\n")
        except ValueError:
            print("Invalid choice. Please input a valid number.\n")


def topFriends(self):
    movies = []
    try:
        self.curs.execute(
            """            
            SELECT title, rating
            FROM \"follows\" F, \"watches\" W
            WHERE follower = %s AND F.following = W.username
            ORDER BY rating DESC
            """,
            [self.username, ]
            # ["bmarritt9", ]
        )
        movies = self.curs.fetchall()
    except Exception as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    if movies is None or len(movies) == 0:
        print("There are no movies to display...")
    else:
        print("Top 20 rated movies among your friends:")
        if len(movies) > 20:
            movies = movies[0:20]
        for i in range(len(movies)):
            movie = movies[i]
            print(str(i+1) + ": " + str(movie[0]) + ", (" + str(movie[1]) + "/5.0)")


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
        print("Top 5 rated movies:")
        if len(movies) > 5:
            movies = movies[0:5]
        for i in range(len(movies)):
            movie = movies[i]
            if movie[3] is None:
                print(str(i+1) + ": " + movie[1] + ", " + movie[2])
            else:
                print(str(i+1) + ": " + movie[1] + ", " + movie[2] + " (" + movie[3] + "/5)")

#------------------------------------------------------------------------------------------------

def get_allAvg(self):
    try:
        self.curs.execute(
        """
        select rating
        from watches
        where rating is not NULL
        """
        )
        rtn = self.curs.fetchall()
        rtn = [float(str(i).split("'")[1]) for i in rtn]

    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    return sum(rtn) / len(rtn)

def get_movies(self, dateRange):
    totalAvgRate = get_allAvg(self)
    sorted_rates = []
    movieDict = {}
    try:
        self.curs.execute(
        """
        select watchtime.title, watchtime.watchtime, w.rating, w.watched
        from watchtime
        join watches w on watchtime.title = w.title
        ORDER BY watchtime DESC
        """
        )
        movies = self.curs.fetchall()

    except (Exception) as error:
        print("Something went wrong.\n", error)
        self.curs.close()
        self.conn.close()

    for i in movies:
            title, watchtime, rating, watched = i
            tdelta = datetime.datetime.now() - timedelta(days=dateRange) 
            if watchtime < tdelta:
                if title in movieDict.keys():
                    movieDict.get(title).update_all(watched, rating)
                else:
                    movieDict.update({title : Movie(title, totalAvgRate)})

    for i in movieDict.keys():
        sorted_rates.append([i, movieDict.get(i).adjRate])
    sorted_rates = quickSort(sorted_rates, 0, len(sorted_rates)-1)

    return sorted_rates

#-------- Quick Sort-------- -------- -------- -------
def partition(arr, low, high):
    i = (low-1)
    pivot = arr[high][1] #array is [[name, Move],[name, Movie]]

    for j in range(low, high):
        if arr[j][1] >= pivot: # >= inverses the list so it counts down 
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high)

        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)

    return arr

#------------------------------------------------------

def rolling_ninety(self):
    sorted = get_movies(self, 90)

    print("\t===Top 20 Movies over 90 Days===")
    for count, value in enumerate(sorted):
        if count < 20:
            print("{}.\t{}".format(count+1, value[0]))
    print("\n")

def top_5(self):
    sorted = get_movies(self, 30)
    print("\t===Top 5 Movies over 30 Days===")
    for count, value in enumerate(sorted):
        if count < 5:
            print("{}.\t{}".format(count+1, value[0]))
    print("\n")

def top_20_friends():
    ...

class Movie:
    def __init__(self, mTitle, avgRateMovies) -> None:
        self.rates = []
        self.title = mTitle
        self.m = 0                            # Times watched
        self.v = 0                            # number of ratings                    
        self.R = 0                            # avg rate for movie
        self.C = round(avgRateMovies , 3)  # avg rate for all movies

        self.adjRate = 0

    def update_adjusted_rate(self):
        denom = self.v + self.m
        adjRate = (self.v / denom) * self.R + (self.m / denom) * self.C

        return adjRate

    def update_avgRate(self):
        if None in self.rates:
            self.R = 0
        else:
            self.R = float(sum(self.rates) / len(self.rates))
    
    def update_all(self, wc, rate):
        self.m += wc
        self.v += 1
        self.rates.append(rate)
        self.update_avgRate()
        self.adjRate = self.update_adjusted_rate()