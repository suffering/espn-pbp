import requests
import pandas as pd
import os
import json

years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
         2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

for year in years:
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?limit=1000&dates={year}"
    response = requests.get(url)
    data = response.json()
    
    if 'events' in data:
        game_ids = []
        for event in data['events']:
            if 'id' in event:
                game_ids.append(event['id'])
            else:
                print(f"'id' key not found for an event in year {year}")
        
        game_ids_df = pd.DataFrame(game_ids, columns=['Game ID'])
        
        print(f"Game IDs for year {year}:")
        print(game_ids_df.head())
    else:
        print(f"Key not found in the response for year {year}")

years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
         2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

for year in years:
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?limit=1000&dates={year}"
    response = requests.get(url)
    if response.status_code == 200 and response.text:
        data = response.json()
        
        if 'events' in data:
            game_ids = []
            for event in data['events']:
                if 'id' in event:
                    game_ids.append(event['id'])
                else:
                    print(f"'id' key not found for an event in year {year}")
            
            year_folder = f'json_data/{year}'
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)
            
            for EVENT_ID in game_ids:
                event_url = f"https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId={EVENT_ID}"
                event_response = requests.get(event_url)
                if event_response.status_code == 200 and event_response.text:
                    event_data = event_response.json()

                    game_folder = f'{year_folder}/{EVENT_ID}'
                    if not os.path.exists(game_folder):
                        os.makedirs(game_folder)

                    json_file_path = f'{game_folder}/{year}_{EVENT_ID}.json'
                    with open(json_file_path, 'w') as f:
                        json.dump(event_data, f)

                    print(f"Saved JSON data for game ID {EVENT_ID} for year {year} to {json_file_path}")
                else:
                    print(f"Failed to fetch data for game ID {EVENT_ID} or received empty response.")
        else:
            print(f"Key 'events' not found in the response for year {year}")
    else:
        print(f"Failed to fetch data for year {year} or received empty response.")

years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
         2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

all_game_ids_df = pd.DataFrame()

for year in years:
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?limit=1000&dates={year}"
    response = requests.get(url)
    data = response.json()
    
    if 'events' in data:
        game_ids = [event.get('id', 'ID not found') for event in data['events']]
        
        game_ids_df = pd.DataFrame(game_ids, columns=['game_id'])
        
        game_ids_df['year'] = year
        
        all_game_ids_df = pd.concat([all_game_ids_df, game_ids_df], ignore_index=True)
    else:
        print(f"Key 'events' not found in the response for year {year}")

print("All Game IDs collected from 2004 to 2024:")
print(all_game_ids_df.head())

years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
         2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

all_game_ids_df = pd.DataFrame()

for year in years:
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?limit=1000&dates={year}"
    response = requests.get(url)
    data = response.json()
    
    if 'events' in data:
        game_ids = [event.get('id', 'ID not found') for event in data['events']]
        
        game_ids_df = pd.DataFrame(game_ids, columns=['game_id'])
        
        game_ids_df['year'] = year
        
        all_game_ids_df = pd.concat([all_game_ids_df, game_ids_df], ignore_index=True)
    else:
        print(f"Key 'events' not found in the response for year {year}")

print("All Game IDs collected from 2004 to 2024:")
print(all_game_ids_df.head())

all_cleaned_data = []

for idx, row in all_game_ids_df.iterrows():
    year = row['year']
    game_id = row['game_id']
    file_path = f'json_data/{year}/{game_id}/{year}_{game_id}.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            gamepackage = data.get('gamepackageJSON', {})

            header = gamepackage.get('header', {})
            week = header.get('week', 'Unknown')
            year = header.get('season', {}).get('year', 'Unknown')  

            drives_data = gamepackage.get('drives', {}).get('previous', [])

            for drive in drives_data:
                drive_id = drive['id']
                team_abbreviation = drive.get('team', {}).get('abbreviation', 'Unknown')
                drive_result = drive.get('result', 'Unknown')
                offensive_plays = drive.get('offensivePlays', 0)
                
                for play in drive.get('plays', []):
                    play_data = {
                        'week': week,
                        'year': year,
                        'game_id': game_id,
                        'drive_id': drive_id,
                        'team_abbreviation': team_abbreviation,
                        'drive_result': drive_result,
                        'offensive_plays': offensive_plays,
                        'drive_description': drive.get('description', 'No description'),
                        'drive_start': drive.get('start', {}).get('text', 'Unknown'),
                        'drive_end': drive.get('end', {}).get('text', 'Unknown'),
                        'play_id': play.get('id', 'Unknown'),
                        'play_description': play.get('text', 'No description'),
                        'down': play.get('start', {}).get('down', 0),
                        'yards_to_go': play.get('start', {}).get('distance', 0),
                        'pos_team': team_abbreviation,
                        'quarter': play.get('period', {}).get('number', 0),
                        'time_remaining': play.get('clock', {}).get('displayValue', '00:00'),
                        'play_start': play.get('start', {}).get('downDistanceText', 'N/A'),
                        'play_end': play.get('end', {}).get('downDistanceText', 'N/A'),
                        'play_type': play.get('type', {}).get('text', 'Unknown'),
                        'play_yardline': play.get('start', {}).get('yardLine', 'Unknown'),
                        'play_yardline_end': play.get('end', {}).get('yardLine', 'Unknown'),
                        'play_team': team_abbreviation,
                        'yards_to_endzone': play.get('start', {}).get('yardsToEndzone', 0),
                        'home_score': play.get('homeScore', 0),
                        'away_score': play.get('awayScore', 0),
                        'day_time': play.get('modified', 'Unknown')
                    }
                    all_cleaned_data.append(play_data)
    else:
        print(f"File not found: {file_path}")

df = pd.DataFrame(all_cleaned_data)

print("Data extraction complete. Displaying head of the consolidated DataFrame:")
print(df.head())

latest_year = df['year'].max()          

df.to_csv(f'pbp/pbp_data_{latest_year}.csv', index=False)  


