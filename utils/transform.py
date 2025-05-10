import pandas as pd

def transform_to_df(data):
    """Data to Dataframe."""
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"[ERROR] Gagal transform data ke DataFrame: {e}")
        return pd.DataFrame() 

def clean_dirty_data(data):
    """Menghapus baris data yang memuat data di bawah."""
    dirty_patterns = {
        "Title": ["Unknown Product"],
        "Rating": ["Invalid Rating / 5", "Not Rated"],
        "Price": ["Price Unavailable", None]
    }

    for column, patterns in dirty_patterns.items():
        data = data[~data[column].isin(patterns)]
    return data

def transform_data(data, exchange_rupiah):
    """Transformasi data sesuai format yang ditentukan."""
    data["Price"] = data["Price"].replace('[\$,]', '', regex=True)
    data["Price"] = pd.to_numeric(data["Price"], errors='coerce') * exchange_rupiah

    data['Rating'] = data['Rating'].str.extract(r'(\d+(\.\d+)?)')[0]
    data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')

    data['Colors'] = data['Colors'].str.extract(r'(\d+)')[0]
    data['Colors'] = pd.to_numeric(data['Colors'], errors='coerce')

    data['Size'] = data['Size'].astype('string')
    data['Gender'] = data['Gender'].astype('string')

    data = data.dropna(subset=['Price', 'Rating', 'Colors'])
    return data
