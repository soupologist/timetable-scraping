import tabula
import pandas as pd


tables = tabula.read_pdf("timetable.pdf", pages= '7-66')
df = pd.concat(tables)

# Removing carriage returns(\r) using regex
df = df.replace(r'\r', ' ', regex= True)

# Getting column names from table
df.columns = df.iloc[0]
df = df.drop(0, axis=0)

# Keeping only essential columns and renaming them
df = df.iloc[:, [1, 2, 6, 7, 8, 9, 10]]
df = df.rename(columns={'ROOM': 'SECTION', 
                        'DAYS': 'INSTRUCTOR', 
                        'HOUR S': 'ROOM',
                        'MID SEMESTER EXAMINATION': 'DAYS', 
                        'COMPRE DATE & SESSION': 'HOURS'
                        })

df = df.dropna(subset=['DAYS']) # Removing redundant rows
df = df.reset_index(drop= True) # Resetting indexing
df = df.ffill() # Filling details into empty cells


# Getting set of all rooms
rooms = df['ROOM'].unique()

days_of_week = {"M", "T", "W", "Th", "F", "S"}

# Making one dataframe for each day
df_dict = {}
for day in days_of_week:
    df_dict[day] = pd.DataFrame({'ROOM': rooms},  columns= ['ROOM', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    df_dict[day] = df_dict[day].set_index('ROOM', drop= False)

# Looping through main dataframe
for i in df.index:
    days = df.loc[i]['DAYS'].split()
    
    # For each day, finding the hour of the class
    for day in days:
        hours = df.loc[i]['HOURS'].split()

        # Inserting data into the day dataframe
        for hour in hours:
            df_dict[day].loc[df.loc[i]['ROOM']][hour] = df.loc[i]['COURSE NO.']         

# Resetting indexes and sorting by room number and then exporting
for day in days_of_week:
    df_dict[day] = df_dict[day].reset_index(drop= True)
    df_dict[day] = df_dict[day].sort_values(by= ['ROOM'])
    df_dict[day].to_csv(day, index= False)

df.to_csv('full.csv', index= False)


