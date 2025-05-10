import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from load import upload_to_csv, upload_to_postgre, upload_to_gsheet


class TestLoadFunctions(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame([{
            'Title': 'Produk X',
            'Price': 160000.0,
            'Rating': 4.6,
            'Colors': 3,
            'Size': 'L',
            'Gender': 'Male'
        }])

    @patch("pandas.DataFrame.to_csv")
    def test_upload_to_csv(self, mock_to_csv):
        """Melakukan test penyimpanan ke file CSV"""
        upload_to_csv(self.df)
        mock_to_csv.assert_called_once_with('products.csv', index=False)

    @patch("load.create_engine")
    def test_upload_to_postgre(self, mock_create_engine):
        """Melakukan test koneksi dan upload ke PostgreSQL dengan mock"""
        mock_engine = MagicMock()
        mock_con = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_con

        upload_to_postgre(self.df, "postgresql://dummy:dummy@localhost:5432/fake_db")

        mock_con.to_sql.assert_called_once_with(
            'bookstoscrape',
            con=mock_con,
            if_exists='append',
            index=False
        )

    @patch("load.Credentials.from_service_account_file")
    @patch("load.build")
    def test_upload_to_gsheet(self, mock_build, mock_creds):
        """Melakukan test upload ke Google Sheets dengan mock API"""
        mock_service = MagicMock()
        mock_sheet = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_sheet
        mock_values = MagicMock()
        mock_sheet.values.return_value = mock_values
        mock_values.update.return_value.execute.return_value = {}

        upload_to_gsheet(self.df)

        mock_values.update.assert_called_once()
        mock_creds.from_service_account_file.assert_called_once()


if __name__ == '__main__':
    unittest.main()
