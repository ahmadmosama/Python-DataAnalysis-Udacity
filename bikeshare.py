import time
import pandas as pd
import numpy as np
import glob

pd.set_option('display.max_columns', None)


CITY_DATA = { "Chicago": "chicago.csv",
              "New York City": "new_york_city.csv",
              "Washington": "washington.csv"}


MONTH_DATA = ["January", "February", "March", "April", "May", "June", "All"]

DAY_DATA = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "All"]

DAY_OF_WEEK ={  0: "Monday",
                1: "Tuesday",
                2: "Wednesday",
                3: "Thursday",
                4: "Friday",
                5: "Saturday",
                6: "Sunday" }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\"s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_input = input("\nPlease enter the name of the city you want to analyze: (e.g. Chicago, Washington or New York City)\n")
        city = city_input.title()
        if city not in CITY_DATA:
            print("\nSorry you entered a wrong value. Kindly, enter a valid city (e.g. Chicago, Washington or New York City)")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
      month_input = input("\nPlease enter the name of the month you want to analyze: (e.g. either All if you do not want to filter or choose a month between January and June)\n")
      month = month_input.title()
      if month not in MONTH_DATA:
        print("\nSorry you entered a wrong value. Kindly, enter a valid month (e.g. either All if you do not want to filter or choose a month between January and and June)")
      else:
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day_input = input("\nPlease enter the name of the day you want to analyze: (e.g. either All if you do not want to filter or choose a day between Monday and Sunday)\n")
      day = day_input.title()
      if day not in DAY_DATA:
        print("\nSorry you entered a wrong value. Kindly, enter a valid month (e.g. either All if you do not want to filter or choose a day between Monday and Sunday)")
        continue
      else:
        break

    print("-"*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
 
    df = pd.read_csv(CITY_DATA[city.title()])

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # filter by month if applicable
    if month != "All":
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df["month"] == month]

    # filter by day of week if applicable
    if day != "All":
        # filter by day of week to create the new dataframe
        df = df.loc[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # display the most common month
    df["month"] = df["Start Time"].dt.month
    popular_month = df["month"].mode().iloc[0]
    print("\nThe most common month from the chosen data is: " + MONTH_DATA[popular_month].title())

    # display the most common day of week
    df["day_of_week"] = df["Start Time"].dt.dayofweek
    most_common_day_of_week = df["day_of_week"].mode()[0]
    popular_day_of_week = DAY_OF_WEEK[most_common_day_of_week]
    print("\nThe most common day of week from the chosen data is: " + popular_day_of_week)

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_start_hour = df["hour"].mode()[0]
    print("\nThe most common start hour from the chosen data is: " + str(popular_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].value_counts().idxmax()
    print("\nMost Popular start station is:", popular_start_station)

    # display most commonly used end station
    popular_end_station = df["End Station"].value_counts().idxmax()
    print("\nMost Popular end station is:", popular_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_trip = (df['Start Station'] + "_" + df['End Station']).mode()[0]
    print("\nMost Popular trip combination of start and end stations is: From", str(most_frequent_trip.split("_")[0]), " AND To ", str(most_frequent_trip.split("_")[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    travel_time_total_mins = df["Trip Duration"].sum()/60
    travel_time_total_hrs = df["Trip Duration"].sum()/3600
    travel_time_total_days = df["Trip Duration"].sum()/86400
    travel_time_total_weeks = df["Trip Duration"].sum()/604800
    print("\nTotal travel time from the chosen data is: " + str(travel_time_total_mins) + " minutes")
    print("\nTotal travel time from the chosen data is: " + str(travel_time_total_hrs) + " hours")
    print("\nTotal travel time from the chosen data is: " + str(travel_time_total_days) + " days")
    print("\nTotal travel time from the chosen data is: " + str(travel_time_total_weeks) + " weeks")

    # display mean travel time
    travel_time_mean_mins = df["Trip Duration"].mean()/60
    travel_time_mean_hrs = df["Trip Duration"].mean()/3600
    travel_time_mean_days = df["Trip Duration"].mean()/86400
    travel_time_mean_weeks = df["Trip Duration"].mean()/604800
    print("\n")
    print("\nMean travel time from the chosen data is: " + str(travel_time_mean_mins) + " minutes")
    print("\nMean travel time from the chosen data is: " + str(travel_time_mean_hrs) + " hours")
    print("\nMean travel time from the chosen data is: " + str(travel_time_mean_days) + " days")
    print("\nMean travel time from the chosen data is: " + str(travel_time_mean_weeks) + " weeks")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("\nuser Type(s) count from the chosen data is: \n" + str(user_types)) 

    print("\nPlease note that only Chicago and New York City includes data for Gender and Birthyear."
        "\nThe following user stats will display no data if the choise is Washington."
        "\nMoreover, please note that some customers did not provide their Gender and/or Birthyear for Chicago and New York City")

    # Display counts of gender
    try:
      gender = df["Gender"].value_counts()
      print("\nGender count from the chosen data is: \n", gender)
    except KeyError:
      print("\nGender count: No data available for this choice.\n")

    # Display earliest, most recent, and most common year of birth
    try:
      earliest_birthyear = df["Birth Year"].min()
      print("\nEarliest Birth Year from the chosen data is: \n", earliest_birthyear)
    except KeyError:
      print("\nEarliest Birth Year: No data available for this choice.\n")

    try:
      most_recent_birthyear = df["Birth Year"].max()
      print("\nMost recent Birth Year from the chosen data is: \n", most_recent_birthyear)
    except KeyError:
      print("\nMost recent Birth Year: No data available for this choice.\n")

    try:
      popular_birthyear = df["Birth Year"].mode()
      print("\nMost Common Birth Year from the chosen data is: \n", popular_birthyear)
    except KeyError:
      print("\nMost Common Birth Year: No data available for this choice.\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        i = 0
        while i < len(pd.read_csv(CITY_DATA[city.title()]).index):
            head = input("\nWould you like to see part of the raw data? Enter yes or no.\n")
            if head.lower() != "yes":
                break
            else:
                print(pd.read_csv(CITY_DATA[city.title()]).iloc[i:i+5])
                i = i+5

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
	main()
