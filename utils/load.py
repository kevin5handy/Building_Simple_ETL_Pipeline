import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

def upload_to_csv(data):
    """Fungsi untuk menyimpan data ke dalam format CSV."""
    try:
        data.to_csv('products.csv', index=False)
        print("Data CSV berhasil ditambahkan!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def upload_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL."""
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as con:
            data.to_sql('bookstoscrape', con=con, if_exists='append', index=False)
            print("Data PSQL berhasil ditambahkan!")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")


def upload_to_gsheet(data):
    """Fungsi untuk menyimpan data ke dalam Google Sheet."""
    SERVICE_ACCOUNT_FILE = './google-sheet-api.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '14QKzLTiF_2fSCx5My_5riiD3Utoir4Nc-svyhp_JwfA'
    RANGE_NAME = 'Sheet1!A2'  # mulai dari A2

    try:
        
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        values = data.values.tolist()

        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("Data Google Sheet berhasil ditambahkan!")
    except Exception as e:
        print(f"Terjadi error: {e}")
