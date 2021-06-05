"""Module providing ingestors for quotes."""

import os
from abc import ABC, abstractmethod
from typing import List
from .quote_model import QuoteModel
import subprocess
import pandas
import docx


class IngestorInterface(ABC):
    """Interface for all ingestors ingesting quotes."""

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Perform a test if the object can ingest the specified file."""
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Abstract method for parsing a file."""
        pass


class DocxIngestor(IngestorInterface):
    """Ingestor parsing .docx files."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a .docx file."""
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        doc = docx.Document(path)
        quotes = simple_parse_lines([line.text for line in doc.paragraphs])
        return quotes


class CSVIngestor(IngestorInterface):
    """Ingestor parsing CSV files."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a CSV file."""
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        df = pandas.read_csv(path, header=0)

        for index, row in df.iterrows():
            new_quote = QuoteModel(row['body'], row['author'])
            quotes.append(new_quote)

        return quotes


class TextIngestor(IngestorInterface):
    """Ingestor parsing .txt files."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a .txt file."""
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        with open(path) as f:
            quotes = simple_parse_lines(f.readlines())

        return quotes


class PDFIngestor(IngestorInterface):
    """Ingestor parsing PDF files."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a PDF file."""
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        tmp = './tmp/tmp.txt'
        subprocess.call(['pdftotext', "-layout", path, tmp])

        f = open(tmp, "r")
        quotes = simple_parse_lines(f.readlines())

        f.close()
        os.remove(tmp)
        return quotes


class Ingestor(IngestorInterface):
    """Class for parsing a file with quotes."""

    importers = [DocxIngestor, CSVIngestor, TextIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Appropriate ingestor is selected based on file type."""
        for importer in cls.importers:
            if importer.can_ingest(path):
                return importer.parse(path)


def simple_parse_lines(lines: List[str]) -> List[QuoteModel]:
    """Help function for simple lines parsing.

    @param lines: List of lines to be parsed.
    @return: List of extracted QuoteModel objects.
    """
    quotes = []

    for line in lines:
        line = line.strip('\n\r').strip()
        if len(line) > 0:
            parse = line.split('-')
            new_quote = QuoteModel(parse[0].strip(" \""),
                                   parse[1].strip(" \""))
            quotes.append(new_quote)

    return quotes
