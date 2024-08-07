import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def load_data(directory, year=None):
    # file pattern
    if year:
        file_pattern = os.path.join(directory, f"Streaming_History_Audio_{year}_*.json")
    else:
        file_pattern = os.path.join(directory, "Streaming_History_Audio_*.json")
    
    # list files matching the pattern
    files = glob.glob(file_pattern)
    
    # load and concatenate data from all files
    data = []
    for file in files:
        with open(file, 'r') as f:
            data.extend(json.load(f))
    
    df = pd.json_normalize(data)
    return df

def clean_data(df):
    # convert timestamp to datetime
    df['ts'] = pd.to_datetime(df['ts'])
    # fill missing values
    df = df.fillna({'episode_name': '', 'episode_show_name': '', 'spotify_episode_uri': ''})
    return df

def top_artists(df, top_n=10):
    top_artists = df['master_metadata_album_artist_name'].value_counts().head(top_n)
    return top_artists

def top_tracks(df, top_n=10):
    top_tracks = df['master_metadata_track_name'].value_counts().head(top_n)
    return top_tracks

def listening_trends(df):
    df['date'] = df['ts'].dt.date
    daily_trends = df.groupby('date').size()
    return daily_trends

def plot_data(data, title, xlabel, ylabel, kind='bar', rotation=45):
    plt.figure(figsize=(10, 6))
    ax = data.plot(kind=kind, color='#39FF14', edgecolor='white')
    plt.title(title, fontsize=16, color='white')
    plt.xlabel(xlabel, fontsize=14, color='white')
    plt.ylabel(ylabel, fontsize=14, color='white')
    plt.xticks(rotation=rotation, ha='right', color='white')
    plt.yticks(color='white')
    plt.ylim(bottom=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_facecolor('black')
    plt.gcf().patch.set_facecolor('black')
    plt.show()

def plot_top_artists(df, top_n=10):
    top_artists_df = top_artists(df, top_n)
    plot_data(top_artists_df, 'Top Artists', 'Artists', 'Play Count')

def plot_top_tracks(df, top_n=10):
    top_tracks_df = top_tracks(df, top_n)
    plot_data(top_tracks_df, 'Top Tracks', 'Tracks', 'Play Count')

def plot_listening_trends(df):
    trends = listening_trends(df)
    plt.figure(figsize=(14, 7))
    ax = trends.plot(kind='line', color='#39FF14', linewidth=2)
    plt.title('Listening Trends', fontsize=16, color='white')
    plt.xlabel('Date', fontsize=14, color='white')
    plt.ylabel('Number of Plays', fontsize=14, color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.ylim(bottom=0)  # Ensure y-axis starts at 0
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    ax.set_facecolor('black')
    plt.gcf().patch.set_facecolor('black')
    plt.tight_layout()
    plt.show()

def main():
    print("\n\nWelcome to Spotify Unwrapped\n")
    directory = "Spotify_Extended_Streaming_History"
    year = input("Enter the year to filter by (or press Enter to process all years): ")
    year = year.strip() if year else None
    
    df = load_data(directory, year)
    df = clean_data(df)
    
    while True:
        print("\nOptions:")
        print("1. Top Artists")
        print("2. Top Tracks")
        print("3. Listening Trends")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            plot_top_artists(df)
        elif choice == '2':
            plot_top_tracks(df)
        elif choice == '3':
            plot_listening_trends(df)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
