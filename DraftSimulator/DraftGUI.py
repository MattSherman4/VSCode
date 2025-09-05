import pandas as pd
import tkinter as tk
from tkinter import ttk

draft_pool = pd.read_csv('Data\DraftPool.csv', index_col = False)
draft = pd.read_csv('Data\DraftOrder.csv', index_col = False)
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
draft['Selection'] = ''

draft_pool = draft_pool.drop(['SOURCE', 'Weight', 'Height', '40YD', 'Summary'], axis = 1)
draft_pool.insert(2, "Rating", draft_pool.pop("Rating"))

draft_pool_no_search = draft_pool.copy()

# DRAFT START
pick = 1
final_pick = draft['Pick'].iloc[-1]
selections = []

# DRAFT FUNCTIONS
def draft_selected_player():
    global draft_pool
    global draft_pool_no_search

    # Get selected player
    drafted_player_id = search_tree.selection()[0]
    drafted_player = search_tree.item(drafted_player_id).get('values')[:2]
    
    # Update draft DataFrame
    selections.append(drafted_player[1])
    draft['Selection'] = pd.Series(selections)
    draft['Selection'] = draft['Selection'].fillna('')
    
    # Clear the selected_tree
    for item in selected_tree.get_children():
        selected_tree.delete(item)

    # Insert selected_tree data from draft
    selected_columns = draft[['Team', 'Round', 'Pick', 'Selection']]
    for index, row in selected_columns.iterrows():
        selected_tree.insert("", tk.END, values=list(row))

    # Update draft_pool DataFrames
    draft_pool_no_search = draft_pool_no_search[(draft_pool_no_search['Player'] != drafted_player[1]) & (draft_pool_no_search['Rank'] != drafted_player[0])].copy()
    draft_pool = draft_pool_no_search.copy()
    
    # Clear the search_tree
    for item in search_tree.get_children():
        search_tree.delete(item)

    # Insert search_tree data from draft, width=0
    available_columns = draft_pool_no_search[['Rank', 'Player', 'Rating']]
    for index, row in available_columns.iterrows():
        search_tree.insert("", tk.END, values=list(row))
        

def trade_picks():
    # Get input
    trade = trade_entry.get()

    # Seperate input
    trade = "".join(trade.split())
    trade = trade.split(',')

    # Get max pick
    max_pick = draft['Pick'].astype(int).max()
    
    # Check input for errors, do nothing if error
    if len(trade) != 2:
        return
    try:
        pick1 = int(trade[0])
    except:
        print('Invalid pick 1')
        return
    try:
        pick2 = int(trade[1])
    except:
        print('Invalid pick 2')
        return
    
    if pick1 > max_pick:
        print('Too big pick 1')
        return
    if pick2 > max_pick:
        print('Too big pick 2')
        return

    # Update draft DataFrame
    team1 = draft.iloc[pick1 - 1]['Team']
    team2 = draft.iloc[pick2 - 1]['Team']
    draft.iat[pick1 - 1, 0] = team2
    draft.iat[pick2 - 1, 0] = team1

    # Clear the selected_tree
    for item in selected_tree.get_children():
        selected_tree.delete(item)

    # Insert selected_tree data from draft
    selected_columns = draft[['Team', 'Round', 'Pick', 'Selection']]
    for index, row in selected_columns.iterrows():
        selected_tree.insert("", tk.END, values=list(row))
    
    # Clear trade_entry
    trade_entry.delete(0, tk.END)


def end():
    global draft
    
    # Get input
    name = end_entry.get()

    # Update draft DataFrame
    draft_end = draft[draft['Selection'] != '']

    # Save draft
    draft_end[['Team', 'Round', 'Pick', 'Selection']].to_csv(f'{name}_mock_draft.csv')

    # Create label
    global label
    label = tk.Label(root, text=f"Send {name}_mock_draft.csv file to mattsherman107@gmail.com", fg="red")
    label.grid(row=4, column=1, columnspan=3)


def skip():
    global draft
    
    # Get input
    skip_to = int(skip_entry.get())

    # Do nothing if skipping backwards
    if skip_to <= len(selections):
        return

    # Update selections
    for i in range(len(selections), skip_to - 1):
        selections.append('-')

    # Update draft DataFrame
    draft['Selection'] = pd.Series(selections)
    draft['Selection'] = draft['Selection'].fillna('')
    
    # Clear the selected_tree
    for item in selected_tree.get_children():
        selected_tree.delete(item)

    # Insert selected_tree data from draft
    selected_columns = draft[['Team', 'Round', 'Pick', 'Selection']]
    for index, row in selected_columns.iterrows():
        selected_tree.insert("", tk.END, values=list(row))

    # Clear skip_entry
    skip_entry.delete(0, tk.END)

def search():
    global draft_pool
    global draft_pool_no_search
    
    # Get input
    name = str(search_entry.get())

    # Clear if empty
    if name == '':
        draft_pool = draft_pool_no_search.copy()
    else:
    # Search draft_pool
        draft_pool = draft_pool[draft_pool['Player'].str.contains(name, case = False)]

    # Clear the search_tree
    for item in search_tree.get_children():
        search_tree.delete(item)

    # Insert search_tree data from draft, width=0
    available_columns = draft_pool[['Rank', 'Player', 'Rating']]
    for index, row in available_columns.iterrows():
        search_tree.insert("", tk.END, values=list(row))

# DEFINE APP 
root = tk.Tk()
root.title("Draft Simulator")

# GRAPHICS
graphic_frame = tk.Frame(root)
graphic_frame.grid(row=0, column=0, columnspan=3)

# LEFT SIDE, SELECTED
selected_frame = tk.Frame(graphic_frame, width=200, height=400)
selected_frame.pack(side=tk.LEFT, padx=10, pady=(0,5))
selected_label = tk.Label(selected_frame, text="Selected")
selected_label.pack()
selected_columns = draft[['Team', 'Round', 'Pick', 'Selection']]
selected_tree = ttk.Treeview(selected_frame, columns=list(selected_columns.columns), show="headings", selectmode="none")
selected_columns_width = [100, 50, 50, 100]
count = 0

for col in selected_columns.columns:
    selected_tree.heading(col, text=col)
    selected_tree.column(col, width=selected_columns_width[count])
    count += 1

for index, row in selected_columns.iterrows():
    selected_tree.insert("", tk.END, values=list(row))

selected_tree.pack()

# RIGHT SIDE, SEARCH
search_frame = tk.Frame(graphic_frame, width=200, height=400)
search_frame.pack(side=tk.RIGHT, padx=10, pady=(0,5))
search_label = tk.Label(search_frame, text="Available")
search_label.pack()
search_columns = draft_pool[['Rank', 'Player', 'Rating']]
search_tree = ttk.Treeview(search_frame, columns=list(search_columns.columns), show="headings", selectmode="browse")
search_columns_width = [50, 100, 50]
count = 0

for col in search_columns.columns:
    search_tree.heading(col, text=col)
    search_tree.column(col, width=search_columns_width[count])
    count += 1

for index, row in search_columns.iterrows():
    search_tree.insert("", tk.END, values=list(row))

search_tree.pack()

# Option Grid
options_frame = tk.Frame(root)
options_frame.grid(row=1, column=0, columnspan=3)

# Draft
draft_label = tk.Label(options_frame, text="Draft selected player:")
draft_label.grid(row=0, column=0, padx=10, pady=(0,5))

draft_draft = tk.Button(options_frame, text="Draft", command=draft_selected_player)
draft_draft.grid(row=0, column=1, padx=10, pady=(0,5))

# Skip Pick
skip_label = tk.Label(options_frame, text="Skip to pick:")
skip_label.grid(row=1, column=0, padx=10, pady=(0,5))

skip_button = tk.Button(options_frame, text="Skip", command=skip)
skip_button.grid(row=1, column=1, padx=10, pady=(0,5))

skip_entry = tk.Entry(options_frame, width=10)
skip_entry.grid(row=1, column=2, padx=10, pady=(0,5))

# Trade Entry
trade_label = tk.Label(options_frame, text="To trade, input two picks, seperated by a comma:")
trade_label.grid(row=2, column=0, padx=10, pady=(0,5))

trade_button = tk.Button(options_frame, text="Trade", command=trade_picks)
trade_button.grid(row=2, column=1, padx=10, pady=(0,5))

trade_entry = tk.Entry(options_frame, width=10)
trade_entry.grid(row=2, column=2, padx=10, pady=(0,5))

# Search Entry
search_label = tk.Label(options_frame, text="Search player by name, empty to clear:")
search_label.grid(row=3, column=0, padx=10, pady=(0,5))

search_button = tk.Button(options_frame, text="Search", command=search)
search_button.grid(row=3, column=1, padx=10, pady=(0,5))

search_entry = tk.Entry(options_frame, width=10)
search_entry.grid(row=3, column=2, padx=10, pady=(0,5))

# End Entry
end_label = tk.Label(options_frame, text="To end, name your mock and click 'End':")
end_label.grid(row=4, column=0, padx=10, pady=(0,5))

end_button = tk.Button(options_frame, text="End", command=end)
end_button.grid(row=4, column=1, padx=10, pady=(0,5))

end_entry = tk.Entry(options_frame, width=10)
end_entry.grid(row=4, column=2, padx=10, pady=(0,5))

root.mainloop()