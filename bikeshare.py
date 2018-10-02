import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june','july'] #Will be used by multiple functions
months.extend(['august','september','october','november','december'])  

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print("For each of the filter either type all or asked value in lowercase\n")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input("Enter the city name\n")
    city=city.lower()
    Cities= ['chicago','new york city','washington']
    while city not in Cities:
      city=input("Invalid Input, Enter the correct city name\n") 
        # TO DO: get user input for month (all, january, february, ... , june) 
    month=input("Enter the month\n")
    while month not in months+['all']:
        month=input("Invalid Month , Enter correct month\n")
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=input("Enter the day\n")
    while day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
      day=input("Invalid day , Enter correct day\n")
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
        df - pandas DataFrame containing city data filtered by month and day
    """
     #Lambda Expression to replace functions
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = df['Start Time'].apply(lambda x: pd.to_datetime(x))
    df['End Time'] = df['End Time'].apply(lambda x: pd.to_datetime(x))
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.weekday_name)  #Weekday name give the day in terms of name day 
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1   #Array is indexed with 0 and increment of 1 is necessary
        # filter by month to create the new dataframe
        df = df[df.month==month]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day=day.title()
        df = df[df.day_of_week==day]
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    print("The most common month for travelling",months[(df['month'].mode()[0]-1)],"\n") #Using Indices to find day
    # TO DO: display the most common day of week
    print("The most Common day for travelling" , df['day_of_week'].mode()[0],"\n")        
    df['Most_Common_Hour']=df['Start Time'].apply(lambda x: x.hour)
    # TO DO: display the most common start hour
    print("People usually starts traveling at about ", df['Most_Common_Hour'].mode()[0],"Hours\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
                
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    print("The most Common Start Station is - ",df['Start Station'].mode()[0],"\n")
    # TO DO: display most commonly used end station
    print("The most common End station or Stop spot is - ",df['End Station'].mode()[0],"\n")
    # TO DO: display most frequent combination of start station and end station trip
    Combination = df['Start Station']+" ---> "+df['End Station']
    print("The people most likely to start and stop at stations", Combination.mode()[0],"\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    Difference=df['End Time'] - df['Start Time']
    DifferenceSec = Difference.apply(lambda x:x.total_seconds())  #Convert into Time
    print("The Total Travel Time amounts to",sum(DifferenceSec),"Seconds\n")
    # TO DO: display mean travel time
    print("The Mean Travel Time amounts to",np.mean(DifferenceSec),"Seconds \n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    print("User Types corresponds to \n",df['User Type'].value_counts(),"\n")
    # TO DO: Display counts of gender
    try:
        print("Information regarding the different Gender\n",df['Gender'].value_counts(),"\n")
    except:
        print("Information regarding Gender not availaible\n")
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print("The person with earliest Birth Year was born on",min(df['Birth Year']),"\n")
        print("The person with most recent Birth Year was born on",max(df['Birth Year']),"\n")
        print("The Most Common Year the people were born corresponds to",df['Birth Year'].mode()[0],"\n")
    except:
        print("Information regarding the Birth not availaible","\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data():
    Light=input("Would you like to see the stastics regarding the bikeshare data. Type yes to continue\n")
    if(Light=="yes"):
        return True
    else:
        return False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        for functions in [time_stats,station_stats,trip_duration_stats,user_stats]: #functions is used as a placeholder for Function
            if (display_data()):
                functions(df)  #Calling the next function in line if the decision is positive
            else:
                break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
