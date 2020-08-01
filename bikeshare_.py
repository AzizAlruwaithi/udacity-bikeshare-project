import time
from datetime import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_q = input('Please select one the following cities: \nchicago, new york city, washington ')

    while city_q.lower() not in CITY_DATA.keys():
        print('Invalid input!')
        city_q = input('Please select one the following cities: \nchicago, new york city, washington ')
    city = CITY_DATA[city_q.lower()]

    # Asking the user if they want to add a filter
    date_filter = input('Would you like to apply a filter for the day, the month, both, or none? \n(Day / Month / both / none) ')
    month_q = ['month', 'Month', 'MONTH']
    day_q = ['DAY', 'day', 'Day']
    both_s = ['both', 'Both', 'BOTH']


    while date_filter not in month_q and date_filter not in day_q and date_filter not in both_s and date_filter.lower() != 'none':
        print('invalid input! \ntype (day), (month), or type (both)')
        date_filter = input('Would you like to filter by day, month, both or none? ')

    if date_filter not in both_s:

        if date_filter in day_q:
            day_que = input('Please choose a day \n Su, Mon, Tues, Wed, Thur, Fri, Sat: ')
            days_dict = {'su': 'Sunday', 'mon': 'Monday', 'tues': 'Tuesday', 'wed': 'Wednesday', 'thurs': 'Thursday',
                         'fri': 'Friday', 'sat': 'Saturday'}
            while day_que.lower() not in days_dict.keys():
                print('Invalid answer!')
                day_que = input('Please choose a day from the list below \n Su, Mon, Tues, Wed, Thur, Fri, Sat: ')

            day = days_dict[day_que]

        if date_filter in month_q:
            month_que = input('Please choose a month between (1-6): ')
            month_dict = {'1': 'january', '2': 'february', '3': 'march', '4': 'april', '5': 'may', '6': 'june'}

            while month_que not in month_dict.keys():
                print('Invalid answer!')
                month_que = input('Please choose a month between (1-6): ')
            month = month_dict[month_que]
    else:
    # get user input for day of week (all, monday, tuesday, ... sunday)
        day_que = input('Please choose a day \n Su, Mon, Tues, Wed, Thur, Fri, Sat: ')
        days_dict = {'su': 'Sunday', 'mon': 'Monday', 'tues': 'Tuesday', 'wed': 'Wednesday', 'thurs': 'Thursday',
                 'fri': 'Friday', 'sat': 'Saturday'}
        while day_que.lower() not in days_dict.keys():
            print('Invalid answer!')
            day_que = input('Please choose a day from the list below \n Su, Mon, Tues, Wed, Thur, Fri, Sat: ')

        day = days_dict[day_que.lower()]

        month_que = input('Please choose a month between (1-6): ')
        month_dict = {'1': 'january', '2': 'february', '3': 'march', '4': 'april', '5': 'may', '6': 'june'}

        while month_que.lower() not in month_dict.keys():
            print('Invalid answer!')
            month_que = input('Please choose a month between (1-6): ')

        month = month_dict[month_que]

    if date_filter.lower() == 'none':
        month = 'all'
        day = 'all'
    elif date_filter.lower() == 'day':
        month = 'all'
    else:
        day = 'all'

    print('-'*40)
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


    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    dates = df['Start Time']
    hours = []
    months = []
    days = []


    for date in dates:
    #convertint string to datetime
        hour = date.hour # this one will show the exact day on the list
        month = date.month  # this one will show the exact day on the list
        day = (date.ctime())[:3]

    #comment------------
        hours.append(hour)
        months.append(month)
        days.append(day)
    date_parts = {"months":pd.Series(months), "days":pd.Series(days),
                  "hours":pd.Series(hours)}

    x = pd.DataFrame(date_parts)

    # display the most common month
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                  7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    months_count = x.groupby(['months'])['months'].count().sort_values().groupby(level=0).tail(1)
    months_df = pd.DataFrame(months_count)
    print('The most common month: ',month_dict[months_df.last_valid_index()])


    # display the most common day of week
    days_count = ((x.groupby(['days'])['days']).count().sort_values().groupby(level=0).tail(1))
    days_df = pd.DataFrame(days_count)
    print('The most common day: ',days_df.last_valid_index())

    # display the most common start hour
    hours_count = ((x.groupby(['hours'])['hours']).count().sort_values().groupby(level=0).tail(1))
    hours_df = pd.DataFrame(hours_count)
    print('The most common start hour: ', hours_df.last_valid_index())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if city == 'washington.csv':
        df_df = pd.DataFrame(df[['User Type','Unnamed: 0']])
        # Display counts of user types
        users_count = df_df.groupby(['User Type'])['Unnamed: 0'].count().groupby(level=0).tail(2)
        users_count = pd.DataFrame(users_count)
        indices = users_count.index
        print('The count of users based on type: ')
        for i in range(len(users_count)):
            print(indices[i],':', users_count['Unnamed: 0'][i])
    else:
        df_d = pd.DataFrame(df[['User Type', 'Unnamed: 0', 'Gender', 'Birth Year']])
    # Display counts of user types
        users_count = df_d.groupby(['User Type'])['Unnamed: 0'].count().groupby(level=0).tail(2)
        users_count = pd.DataFrame(users_count)
        indices = users_count.index
        print('The count of users based on type: ')
        for i in range(len(users_count)):
            print(indices[i], ':', users_count['Unnamed: 0'][i])

    # Display counts of gender
        gender_count = df_d.groupby(['Gender'])['Unnamed: 0'].count().groupby(level=0).tail(2)
        gender_count = pd.DataFrame(gender_count)
        indices = gender_count.index
        print('The count of users based on Gender: ')
        for i in range(len(gender_count)):
            print(indices[i],':', gender_count['Unnamed: 0'][i])

    # Display earliest, most recent, and most common year of birth
        age = df_d['Birth Year']
        most_common_year = df_d.groupby(['Birth Year'])['Unnamed: 0'].count().sort_values().groupby(level=0).tail(1)
        print('Costumer with the earliest birth year:',int(age.min()))
        print('Costumer with the earliest birth year:', int(age.max()))
        most_common_year = pd.DataFrame(most_common_year)
        print('Most common birth year:',int(most_common_year['Unnamed: 0'].last_valid_index()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        user_stats(df, city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
