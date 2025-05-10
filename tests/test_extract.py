import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests
from extract import fetching_content, extract_book_data, scrape_book

class TestExtractFunctions(unittest.TestCase):

    def setUp(self):
        self.sample_html = """
        <div class="product-details">
            <h3 class="product-title">Rok</h3>
            <div class="price-container">
                <span class="price">$99.99</span>
            </div>
            <p>Rating: ⭐ 4.6 / 5</p>
            <p>2 Colors</p>
            <p>Size: M</p>
            <p>Gender: Female</p>
        </div>
        """

    @patch("extract.requests.Session.get")
    def test_fetching_content_success(self, mock_get):
        """Melakukan test fetching_content ketika request berhasil"""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<html>OK</html>"
        mock_get.return_value = mock_response

        result = fetching_content("http://example.com")
        self.assertEqual(result, b"<html>OK</html>")

    @patch("extract.requests.Session.get")
    def test_fetching_content_failure(self, mock_get):
        """Melakukan test fetching_content ketika request gagal"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        mock_get.return_value = mock_response

        result = fetching_content("http://example.com")
        self.assertIsNone(result)

    def test_extract_book_data(self):
        """Melakukan test extract_book_data dari potongan HTML"""
        soup = BeautifulSoup(self.sample_html, "html.parser")
        article = soup.find("div", class_="product-details")

        expected = {
            "Title": "Rok",
            "Price": "$99.99",
            "Rating": "⭐ 4.6 / 5",
            "Colors": "2 Colors",
            "Size": "M",
            "Gender": "Female"
        }

        result = extract_book_data(article)
        self.assertEqual(result, expected)

    @patch("extract.fetching_content")
    def test_scrape_book_single_page(self, mock_fetching_content):
        """Melakukan test scrape_book pada satu halaman"""
        html = f"""
        <html>
        <body>
            {self.sample_html}
        </body>
        </html>
        """
        mock_fetching_content.return_value = html.encode("utf-8")

        result = scrape_book("http://fake-url.com/", start_page=1, delay=0)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn("Title", result[0])
        self.assertIn("Timestamp", result[0])

if __name__ == '__main__':
    unittest.main()
