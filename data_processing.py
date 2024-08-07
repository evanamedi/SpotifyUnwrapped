import json
import pandas as pd
import os
import glob

def load_data(directory, year=None):
    if year:
        file_pattern = os.path.join(directory, f"Streaming_History_Audio_{year}_*.json")
    else:
        file_pattern = os.path.join(directory, "Streaming_History_Audio_*.json")
    
    files = glob.glob(file_pattern)
    
    data = []
    for file in files:
        with open(file, 'r') as f:
            data.extend(json.load(f))
    
    df = pd.json_normalize(data)
    return df

def clean_data(df):
    print(f"Columns before cleaning: {df.columns}")  
    if 'ts' in df.columns:
        df['ts'] = pd.to_datetime(df['ts'])
    else:
        print("Column 'ts' not found in DataFrame.")
        raise KeyError("Column 'ts' not found in DataFrame.")
    
    df = df.fillna({'episode_name': '', 'episode_show_name': '', 'spotify_episode_uri': ''})
    print(f"Columns after cleaning: {df.columns}")  
    return df

def save_clean_data(df, output_file):
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    directory = "Spotify_Extended_Streaming_History"
    year = input("Enter the year to filter by (or press Enter to process all years): ").strip()
    year = year if year else None
    
    df = load_data(directory, year)
    df = clean_data(df)
    
    output_file = "cleaned_data.csv"
    save_clean_data(df, output_file)
    print(f"Data saved to {output_file}")