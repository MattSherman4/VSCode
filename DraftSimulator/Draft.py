import pandas as pd
import numpy as np
import tkinter as tk

draft = pd.read_csv('Data\DraftOrder.csv', index_col = False)
draft_pool = pd.read_csv('Data\DraftPool.csv', index_col = False)
teams = pd.read_csv('Data\Teams.csv', index_col = False)

source = draft['SOURCE'][0]

draft = draft.merge(teams, left_on = ['Team'], right_on = [source], how = 'left')
draft = draft.drop(['SOURCE', 'Team', 'Tankathon'], axis = 1)
draft.insert(0, 'Team', draft['City'] + ' ' + draft['Name'])

counts_per_round = draft['Round'].value_counts().sort_index()
round_pick = []
for value in counts_per_round:
    round_pick = round_pick + list(range(1, value + 1))

draft.insert(2, 'Round Pick', round_pick)
draft = draft.drop(['City', 'Name'], axis = 1)
draft['Selection'] = np.nan

draft_pool = draft_pool.drop(['SOURCE', 'Weight', 'Height', '40YD', 'Summary'], axis = 1)
draft_pool.insert(2, "Rating", draft_pool.pop("Rating"))

def valid_selection(name):
    df = draft_pool[draft_pool['Player'] == name]
    if len(df) == 0:
        return False
    return True

# Draft Start
pick = 1
final_pick = draft['Pick'].iloc[-1]
selections = []

while pick <= final_pick:
    if pick == 1:
        print('Welcome to the NFL Draft!')
    row = draft.iloc[pick - 1]
    team = row['Team']
    round = row['Round']
    round_pick = row['Round Pick']
    
    print(f"Who's up?\t{team}")
    print(f'Current Selection: {round}.{round_pick}')
    print(f'Top 10 players available:')
    print(draft_pool.head(10))

    while True:
        player_name = input(f'Enter the name of your selection: ')
        if valid_selection(name = player_name):
            draft_pool = draft_pool[draft_pool['Player'] != player_name]
            draft_pool.reset_index(drop = True, inplace = True)
            selections.append(player_name)
            draft['Selection'] = pd.Series(selections)
            break
        if player_name.upper() == 'END':
            break
    
    if player_name.upper() == 'END':
        break

    pick += 1

print(f'Final Draft Results: ')
print(draft)


