#below references were used to work on the final project
#referred practise questions
#https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python
#https://www.includehelp.com/python/unique-combinations-of-values-in-selected-columns-in-pandas-dataframe-and-count.aspx
#https://stackoverflow.com/questions/56310134/find-the-mode-across-multiple-columns-for-each-row-of-a-pandas-dataframe


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all','january','february','march','april','may','june']

DAYS_OF_WEEK = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']


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
    city_name = input("Enter City name (Info : Please enter the any of the following cities: chicago,new york city,washington): ").lower()

    while city_name not in ('chicago','new york city','washington') :
        city_name = input("Invalid Entery. Re-Enter City Name : ").lower()
        continue

    city = CITY_DATA[city_name]

    # get user input for month (all, january, february, ... , june)
    month = input('Enter month (Info : Please enter name of the month or "all", to apply no filter ): ').lower()
    while month not in MONTHS:
        month = input("Invalid Entry. Re-Enter month : ").lower()
        continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter day of week (Info : Please enetr name of the day to filter or "all" to apply no filter) : ').lower()
    while day not in DAYS_OF_WEEK:
        day = input("Invalid Entry. Re-Enter day : ").lower()
        continue

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

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['all','january', 'february', 'march', 'april', 'may', 'june']
        month = MONTHS.index(month)
        

        # filter by month to create the new dataframe
        df.loc[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        df = df.loc[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0]
    
    print('Most popualar month : ',month)
    print()

    # display the most common day of week
    day_of_week = df['day_of_week'].mode()[0]
    print('Most popular day : ',day_of_week)
    print()

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    hour = df['hour'].mode()[0]

    print('Most popular hour : ',hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]


    print('Most commonly used start station : ',start_station)
    print()

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]

    print('Most commonly used end station : ',end_station)
    print()

    # display most frequent combination of start station and end station trip

    print('most frequent combination of start station and end station trip : \n', (df['Start Station'] + '  --  '  + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total Travel time : ',total_travel_time)

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean()

    print('Mean travel time : ',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print('counts of user type : \n',user_types)
    print()

    # Display counts of gender
    try :
        gender_count = df['Gender'].value_counts()
        print('counts of gender : \n',gender_count)
        print()
    except KeyError :
        print("there isn't a [Gender] column in this spreadsheet")
    

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = int(df['Birth Year'].min())

        recent_year_of_birth = int(df['Birth Year'].max())

        common_year_of_birth = int(df['Birth Year'].mode())
        
        print('Earliest year is {}, most recent year is {} and common birth of year is {}'.format(earliest_year_of_birth,recent_year_of_birth,common_year_of_birth))
        print()
    except KeyError :

        print("there isn't a [Birth Year] column in this spreadsheet")
    

    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):

    """Display raw data on user request"""
    print(df.head())

    int_count = 0

    while True:
        view_df = input('Do you like to view next five lines of data : Type yes or no \n').lower()

        if view_df != 'yes':
            break
        else:
            int_count += 5
            print(df.iloc[int_count : int_count + 5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            user_input = input('Do you like to see the first five lines of raw data : Type yes or no \n').lower()

            if user_input != 'yes':
                break
            else:
                print(user_input)
                display_raw_data(df)
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

    


if __name__ == "__main__":
	main()
