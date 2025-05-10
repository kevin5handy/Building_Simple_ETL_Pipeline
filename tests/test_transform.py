import unittest
import pandas as pd
from transform import transform_to_df, clean_dirty_data, transform_data

class TestTransformFunctions(unittest.TestCase):

    def setUp(self):
        self.raw_data = [
            {
            "Title": "Rok",
            "Price": "$99.99",
            "Rating": "⭐ 4.6 / 5",
            "Colors": "2 Colors",
            "Size": "M",
            "Gender": "Female"
            },
            {
                "Title": "Unknown Product",
                "Price": "Price Unavailable",
                "Rating": "Invalid Rating / 5",
                "Colors": "0 Colors",
                "Size": "L",
                "Gender": "Female"
            }
        ]

    def test_transform_to_df(self):
        data = transform_to_df(self.raw_data)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)

    def test_clean_dirty_data(self):
        data = transform_to_df(self.raw_data)
        cleaned_df = clean_dirty_data(data)
        self.assertEqual(len(cleaned_df), 1)
        self.assertNotIn("Unknown Product", cleaned_df["Title"].values)

    def test_transform_data(self):
        data = transform_to_df([self.raw_data[0]])  # hanya yang valid
        data = clean_dirty_data(data)
        transformed_df = transform_data(data, exchange_rupiah=16000)
        
        self.assertEqual(transformed_df.shape[0], 1)
        self.assertIn("Price", transformed_df.columns)
        self.assertIsInstance(transformed_df["Price"].iloc[0], float)
        self.assertAlmostEqual(transformed_df["Price"].iloc[0], 160000.0)

if __name__ == '__main__':
    unittest.main()
