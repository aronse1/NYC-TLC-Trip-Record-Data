import pandas as pd
import os
import glob

def merge_parquet_files():
    output_dir = 'data/processed'
    os.makedirs(output_dir, exist_ok=True)
    
    all_files = glob.glob('data/raw/yellow_tripdata_2024-*.parquet')
    
    if not all_files:
        print("No files found in data/raw/. Checking current directory...")
        all_files = glob.glob('yellow_tripdata_2024-*.parquet')
    
    if not all_files:
        raise FileNotFoundError("No parquet files found")
    
    print(f"Found {len(all_files)} files")
    
    dfs = []
    for file in all_files:
        df = pd.read_parquet(file)
        dfs.append(df)
    
    merged_df = pd.concat(dfs, ignore_index=True)
    print(f"Merged dataframe shape: {merged_df.shape}")
    
    merged_df = clean_data(merged_df)
    
    merged_df.to_parquet(f'{output_dir}/yellow_tripdata_2024_merged.parquet', index=False)
    print(f"Merged and cleaned data saved to {output_dir}/yellow_tripdata_2024_merged.parquet")

def clean_data(df):
    df = df.dropna(subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
    df = df[df['fare_amount'] > 0]
    df = df[df['trip_distance'] > 0]
    return df

if __name__ == "__main__":
    merge_parquet_files()
