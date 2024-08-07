import pandas as pd
import matplotlib.pyplot as plt
import sys

import matplotlib
matplotlib.use('Agg')

def plot_top_artists(df, output_file, top_n=10):
    top_artists = df['master_metadata_album_artist_name'].value_counts().head(top_n)
    plt.figure(figsize=(12, 8))
    ax = top_artists.plot(kind='bar', color='#39FF14')
    plt.title('Most Played Artists', fontsize=24, color='white')
    plt.xlabel('Artists', fontsize=14, color='white')
    plt.ylabel('Play Count', fontsize=14, color='white')
    plt.xticks(rotation=30, ha='right', color='white')
    plt.yticks(color='white')
    plt.ylim(bottom=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for i in range(len(top_artists)):
        ax.text(i, top_artists.iloc[i], str(top_artists.iloc[i]), ha='center', va='bottom', color='white', fontsize=12)
        
    ax.set_facecolor('black')
    plt.gcf().patch.set_facecolor('black')
    plt.tight_layout(pad=2.0)
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved to {output_file}")

def plot_top_tracks(df, output_file, top_n=10):
    top_tracks = df['master_metadata_track_name'].value_counts().head(top_n)
    plt.figure(figsize=(12, 8))
    ax = top_tracks.plot(kind='bar', color='#39FF14')
    plt.title('Most Played Tracks', fontsize=24, color='white')
    plt.xlabel('Tracks', fontsize=14, color='white')
    plt.ylabel('Play Count', fontsize=14, color='white')
    plt.xticks(rotation=30, ha='right', color='white')
    plt.yticks(color='white')
    plt.ylim(bottom=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for i in range(len(top_tracks)):
        ax.text(i, top_tracks.iloc[i], str(top_tracks.iloc[i]), ha='center', va='bottom', color='white', fontsize=12)
        
    ax.set_facecolor('black')
    plt.gcf().patch.set_facecolor('black')
    plt.tight_layout(pad=2.0)
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved to {output_file}")

def plot_listening_trends(df, output_file):
    df['date'] = df['ts'].dt.date
    daily_trends = df.groupby('date').size()
    plt.figure(figsize=(14, 7))
    ax = daily_trends.plot(kind='line', color='#39FF14', linewidth=2)
    plt.title('Listening Trends', fontsize=16, color='white')
    plt.xlabel('Date', fontsize=14, color='white')
    plt.ylabel('Number of Plays', fontsize=14, color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.ylim(bottom=0)
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    ax.set_facecolor('black')
    plt.gcf().patch.set_facecolor('black')
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved to {output_file}")


if __name__ == "__main__":
    input_file = sys.argv[1]
    plot_type = sys.argv[2]
    output_file = sys.argv[3]
    
    df = pd.read_csv(input_file, parse_dates=['ts'], low_memory=False)
    
    if plot_type == 'top_artists':
        plot_top_artists(df, output_file)
    elif plot_type == 'top_tracks':
        plot_top_tracks(df, output_file)
    elif plot_type == 'listening_trends':
        plot_listening_trends(df, output_file)
    else:
        print(f"Unknown plot type: {plot_type}")