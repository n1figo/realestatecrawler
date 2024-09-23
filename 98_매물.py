import pandas as pd
import pickle
import os

def excel_to_pickle(excel_path, pickle_path):
    excel_file = pd.ExcelFile(excel_path)
    df = excel_file.parse(excel_file.sheet_names[1])
    with open(pickle_path, 'wb') as f:
        pickle.dump(df, f)
    print(f"데이터가 {pickle_path}에 저장되었습니다.")
    return df

def load_pickle(pickle_path):
    with open(pickle_path, 'rb') as f:
        df = pickle.load(f)
    print(f"{pickle_path}에서 데이터를 로드했습니다.")
    return df

def print_column_list(df):
    print("\n컬럼 리스트:")
    for column in df.columns:
        print(column)

def filter_data(df):
    df['min(매매) - MAX(전세)'] = pd.to_numeric(df['min(매매) - MAX(전세)'].str.replace(',', ''), errors='coerce')
    df = df.dropna(subset=['min(매매) - MAX(전세)'])
    filtered_df = df[df['min(매매) - MAX(전세)'] <= 600000000]
    return filtered_df

def save_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"필터링된 데이터가 {csv_path}에 저장되었습니다.")

if __name__ == "__main__":
    excel_path = '/workspaces/realestatecrawler/서울시 아파트_2024-09-18.xlsx'
    pickle_path = 'second_sheet_data.pkl'
    csv_path = 'filtered_real_estate_data.csv'
    
    try:
        df = load_pickle(pickle_path)
    except FileNotFoundError:
        df = excel_to_pickle(excel_path, pickle_path)
    
    print_column_list(df)
    print(f"\n원본 데이터 shape: {df.shape}")
    
    filtered_df = filter_data(df)
    
    print(f"\n필터링된 데이터 shape: {filtered_df.shape}")
    print(f"'min(매매) - MAX(전세)' 값이 600,000,000 이하인 데이터 수: {len(filtered_df)}")
    
    print("\n필터링된 데이터의 처음 5행:")
    print(filtered_df.head())
    
    print("\n'min(매매) - MAX(전세)' 컬럼의 데이터 타입:")
    print(filtered_df['min(매매) - MAX(전세)'].dtype)
    
    # 필터링된 데이터를 CSV 파일로 저장
    save_to_csv(filtered_df, csv_path)
    
    # CSV 파일의 크기 출력
    csv_size = os.path.getsize(csv_path) / (1024 * 1024)  # MB 단위로 변환
    print(f"\nCSV 파일 크기: {csv_size:.2f} MB")