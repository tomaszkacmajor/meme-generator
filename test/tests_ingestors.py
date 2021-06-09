import os
import unittest
from QuoteEngine.ingestors import simple_parse_lines, DocxIngestor, TextIngestor, CSVIngestor, PDFIngestor

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class IngestorsTests(unittest.TestCase):

    def test_simple_line_parsing(self):
        lines = [" \"Quote 1\" - Author 1 \n\r",
                 "  \" Quote 2 \"  -  Author 2"]
        quotes = simple_parse_lines(lines)
        self.make_asserts(quotes)

    def test_docx_ingestor(self):
        self.ingest(DocxIngestor, 'DocxTestFile.docx')

    def test_txt_ingestor(self):
        self.ingest(TextIngestor, 'TxtTestFile.txt')

    def test_csv_ingestor(self):
        self.ingest(CSVIngestor, 'CSVTestFile.csv')

    def test_pdf_ingestor(self):
        self.ingest(PDFIngestor, 'PDFTestFile.pdf')

    def ingest(self, importer, path):
        test_data_path = os.path.join(THIS_DIR, 'test_data', path)
        quotes = importer.parse(test_data_path)
        self.make_asserts(quotes)

    def make_asserts(self, quotes):
        self.assertEqual(quotes[0].body, "Quote 1")
        self.assertEqual(quotes[0].author, "Author 1")
        self.assertEqual(quotes[1].body, "Quote 2")
        self.assertEqual(quotes[1].author, "Author 2")


if __name__ == '__main__':
    unittest.main()
