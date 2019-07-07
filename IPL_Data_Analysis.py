import numpy as np # numerical computing
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Set ipython's max row display
#pd.set_option('display.max_row', 1000)

# Set iPython's max column width to 50
#pd.set_option('display.max_columns', 50)

#load the data
file_path = 'datasets/'
matches = pd.read_csv(file_path+'Match.csv')
teams = pd.read_csv(file_path+'Team.csv')
season = pd.read_csv(file_path+'Season.csv')
player = pd.read_csv(file_path+'Player.csv')

'''
# Let us get some basic stats #
print(matches.describe())
print(matches.info())
print(matches.head())
print("Number of matches played so far : ", matches.shape)
'''

print('=============== How many matches we’ve got in the dataset? ===============')
print('Number of Unique Rows for Match Id Column',len(matches['Match_Id'].unique()))
print('Max value for Unique Match Id Column',matches['Match_Id'].unique().max())
print('Max value for Match Id Column',matches['Match_Id'].max())
#print(matches.max())

print('=============== How many seasons we’ve got in the dataset? ===============')
print('Number of seasons : ',len(matches['Season_Id'].unique()))

#print(season[season.Season_Id.isin(matches['Season_Id'])]['Season_Year']);

'''
sns.countplot(x=season['Season_Id'], data=matches)
plt.show()
'''
print('=============== Which Team had won by maximum runs? ===============')
criteria = matches['Win_Type'].notnull() & (matches['Win_Type'] == "by runs")
win_by_runs = matches[criteria]
# -- OR
win_by_runs = matches[matches['Win_Type'].notnull() & (matches['Win_Type'] == "by runs")]

'''
print('City Name :',matches.iloc[win_by_runs['Won_By'].idxmax()]['City_Name']);
print('max :',matches.iloc[win_by_runs['Won_By'].idxmax()])
print('Team Name ID :',matches.iloc[win_by_runs['Won_By'].idxmax()]['Team_Name_Id'])
'''
team_name_id = matches.iloc[win_by_runs['Won_By'].idxmax()]['Team_Name_Id'];
print(teams[teams.Team_Id.isin([team_name_id])])


print('=============== Which Team had won by maximum wickets? ===============')
win_by_wickets = matches[matches['Win_Type'].notnull() & (matches['Win_Type'] == "by wickets")]

'''
print(matches.iloc[win_by_runs['Won_By'].idxmax()]['City_Name']);
print(matches.iloc[win_by_runs['Won_By'].idxmax()])
print(matches.iloc[win_by_runs['Won_By'].idxmax()]['Team_Name_Id'])
'''
team_name_id = matches.iloc[win_by_wickets['Won_By'].idxmax()]['Team_Name_Id'];
print(teams[teams.Team_Id.isin([team_name_id])])

print('=============== Which Team had won by (closest margin) minimum runs? ===============')
print(teams[teams.Team_Id.isin([matches.iloc[win_by_runs['Won_By'].idxmin()]['Match_Winner_Id']])]);


print('=============== Which Team had won by minimum wickets? ===============')
print(teams[teams.Team_Id.isin([matches.iloc[win_by_wickets['Won_By'].idxmin()]['Match_Winner_Id']])]);


print('=============== Which season had most number of matches? ===============')
#group matches by Season_Id
temp_df = matches.groupby(['Season_Id']).size().reset_index(name="counts");

#merge two data frame with same column name from two dataframe
temp_df = pd.merge(season, temp_df, on='Season_Id')

#Get max of counr and return row for the same
temp_df = temp_df[temp_df.Season_Id.isin([temp_df.iloc[temp_df['counts'].idxmax()]['Season_Id']])]

#select the column
print(temp_df[['Season_Id','Season_Year','counts']])



print('=============== Which team is most successful IPL Team? ===============')
#Group matches by Match_Winner_Id
matchWinner_df = matches.groupby(['Match_Winner_Id']).size().reset_index(name="counts");

#merge two data frame with different column name to get ID and Name matching for Team
matchWinner_df = pd.merge(teams, matchWinner_df, left_on='Team_Id', right_on='Match_Winner_Id')

# Get row index with maximum count for winner id and check the index location in datafram and retun the entire row for the same.
matchWinner_df = matchWinner_df[matchWinner_df.Match_Winner_Id.isin([matchWinner_df.iloc[matchWinner_df['counts'].idxmax ()]['Match_Winner_Id']])]
print(matchWinner_df)


print('=============== Who is top player of the match Winners? ===============')
#check if toss winner is always a winner
criteria = matches['IS_Result'].notnull() & (matches['IS_Result'] == 1)
toss_winner_df = matches[criteria]
toss_winner_df = pd.merge(player, toss_winner_df, left_on='Player_Id', right_on='Man_Of_The_Match_Id')
print(toss_winner_df[['Match_Id','Match_Date','Player_Id','Player_Name','Country','Venue_Name']].head())


print('=============== Has Toss-winning helped in Match-winning? ===============')
#check if toss winner is always a winner
toss_winner_df = matches['Toss_Winner_Id'] == matches['Match_Winner_Id']

#Group by to get the count
toss_winner_df = toss_winner_df.groupby(toss_winner_df).size()
print(toss_winner_df)
