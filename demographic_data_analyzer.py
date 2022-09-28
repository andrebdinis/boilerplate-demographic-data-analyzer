import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(
        'adult.data.csv',
        header=0,
        #dtype={'race': 'object'},
        index_col=['race'],
        sep=',',
        na_values=['','?','-']
    )

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.index.value_counts()

    # What is the average age of men?
    mask = (df['sex'] == 'Male')
    average_age_men = round(df.loc[mask, 'age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    mask = (df['education'] == 'Bachelors')
    total_bachelors = df[mask].shape[0]
    total_people = df.shape[0]
    percentage = round((total_bachelors / total_people) * 100, 1)
    percentage_bachelors = percentage

  
    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    maskAdvEdu = ((df['education'] == 'Bachelors') | (df['education'] == 'Masters') | (df['education'] == 'Doctorate'))
    maskAbove50K = (df['salary'] == '>50K')
    maskTotal = maskAdvEdu & maskAbove50K
  
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df.loc[maskAdvEdu, 'salary'].shape[0]
    lower_education = df.loc[(~maskAdvEdu), 'salary'].shape[0] # 25070    

    # percentage with salary >50K
    adv_edu_gain_50k_plus = df.loc[maskTotal, 'salary'].shape[0]
    percentage = round((adv_edu_gain_50k_plus / higher_education) * 100, 1)  
    higher_education_rich = percentage
    maskTotal = (~maskAdvEdu) & maskAbove50K
    without_adv_edu_gain_50k_plus = df.loc[maskTotal, 'salary'].shape[0] # 4355
    percentage = round((without_adv_edu_gain_50k_plus / lower_education) * 100, 1)
    lower_education_rich = percentage


    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = round(df['hours-per-week'].min(), 1)

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    maskOne = (df['hours-per-week'] == min_work_hours) # 1
    maskTwo = (df['salary'] == '>50K')
    maskTotal = maskOne & maskTwo
    total_people_work_min_hrs = df.loc[maskOne, 'hours-per-week'].shape[0] # 20
    num_min_workers = df.loc[maskTotal, ['hours-per-week', 'salary']].shape[0] # 2
    percentage = round((num_min_workers / total_people_work_min_hrs) * 100, 1)
    rich_percentage = percentage

  
    # What country has the highest percentage of people that earn >50K?
    maskOne = (df['salary'] == '>50K')
    people_earn_50k_plus_per_country = df.loc[maskOne, 'native-country'].value_counts().to_frame()
    people_per_country = df['native-country'].value_counts().to_frame()
    countries_percentage = round((people_earn_50k_plus_per_country / people_per_country) * 100, 1)
    countries_percentage = countries_percentage.sort_values(['native-country'], ascending=False)
    country = countries_percentage.head(1).index[0]
    percentage = countries_percentage.head(1).values[0][0]

    highest_earning_country = country
    highest_earning_country_percentage = percentage

  
    # Identify the most popular occupation for those who earn >50K in India.
    maskOne = (df['native-country'] == 'India')
    maskTwo = (df['salary'] == '>50K')
    maskTotal = maskOne & maskTwo
    pop_occups_india = df.loc[maskTotal, 'occupation'].value_counts()
    pop_occup_name = pop_occups_india.head(1).index[0] # 'Prof-specialty'
    top_IN_occupation = pop_occup_name

  
    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
