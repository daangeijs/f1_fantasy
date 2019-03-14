import pandas as pd
import numpy as np
from itertools import combinations

# Load excel file
drivers = pd.read_excel('F1.xlsx', sheetname=1)
prediction = pd.read_excel('F1.xlsx', sheetname=0)
constructors = pd.read_excel('F1.xlsx', sheetname=2)

# Cleanup prediction
prediction.columns = prediction.loc[20].values
prediction = prediction.drop(np.arange(0,21))
prediction.index = np.arange(1,len(prediction)+1)

# Calculate possible team combinations
teams = [list(comb) for comb in combinations(np.arange(1,11),5)]

stats = pd.DataFrame()
# Determine best turbo driver
# If turbo racer in team count points for best turbo racer twice
turbo_names = drivers['Name'].loc[drivers['Turbo'] > 0]
best_turbo = prediction.loc[prediction['Name'].isin(turbo_names)]['Race points'].argmax()
turbo_name = prediction['Name'].loc[best_turbo]

# Calculate costs and total points per team
for team in teams:
    team_prediction = prediction.loc[team]
    members = team_prediction['Name'].tolist()
    member_data = drivers.loc[drivers['Name'].isin(members)]
    team_price = member_data['Price'].sum()
    team_points = team_prediction['Race points'].sum()
    # Calculate total price and total points for each constructor added to a team
    for idx, constructor in constructors.iterrows():
        members_constructor = drivers.loc[drivers['Constructor'] == constructor['Name']]['Name']
        constructor_points = prediction.loc[prediction['Name'].isin(members_constructor)]['Race points'].sum()
        points = team_points + constructor_points
        price = team_price + constructor['Price']
        team_row = pd.Series({'constructor': constructor['Name'], 'member_id': team, 'members': members, 'turbo_driver': turbo_name,  'price': price, 'points': points})
        stats = stats.append(team_row, ignore_index=True)
# Valid teams are teams with value <= 100
possible = stats.loc[stats['price'] <= 100]
best_team = possible.loc[possible['points'].argmax()]
print(best_team)
