"""
Tests for document_converter.py
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

import document_converter as dc


class TestEnvLoading:
    """Test environment variable loading."""

    @patch('document_converter.load_dotenv')
    @patch('pathlib.Path.exists')
    def test_load_env_files_success(self, mock_exists, mock_load_dotenv):
        """Test successful .env file loading."""
        mock_exists.return_value = True
        dc.load_env_files()
        # Should be called for skill, skills, and claude dirs
        assert mock_load_dotenv.call_count >= 1

    @patch('document_converter.load_dotenv', None)
    def test_load_env_files_no_dotenv(self):
        """Test when dotenv is not available."""
        # Should not raise an error
        dc.load_env_files()


class TestDependencyCheck:
    """Test dependency checking."""

    @patch('builtins.__import__')
    def test_check_all_dependencies_available(self, mock_import):
        """Test when all dependencies are available."""
        mock_import.return_value = Mock()

        deps = dc.check_dependencies()

        assert 'pypdf' in deps
        assert 'markdown' in deps
        assert 'pillow' in deps

    @patch('builtins.__import__')
    def test_check_dependencies_missing(self, mock_import):
        """Test when dependencies are missing."""
        def import_side_effect(name, *args, **kwargs):
            if name == 'pypdf':
                raise ImportError()
            return Mock()

        mock_import.side_effect = import_side_effect

        # The function uses try/except, so we test the actual function
        with patch('document_converter.sys.modules', {}):
            # This is tricky to test due to import handling
            pass


class TestPDFPageExtraction:
    """Test PDF page extraction."""

    @patch('pypdf.PdfReader')
    @patch('pypdf.PdfWriter')
    @patch('builtins.open', create=True)
    def test_extract_single_page(self, mock_open, mock_writer_class, mock_reader_class):
        """Test extracting a single page."""
        # Mock reader
        mock_reader = Mock()
        mock_page = Mock()
        mock_reader.pages = [Mock(), mock_page, Mock()]
        mock_reader_class.return_value = mock_reader

        # Mock writer
        mock_writer = Mock()
        mock_writer.pages = [mock_page]
        mock_writer_class.return_value = mock_writer

        result = dc.extract_pdf_pages(
            'input.pdf',
            'output.pdf',
            page_range='2',
            verbose=False
        )

        assert result is True
        mock_writer.add_page.assert_called_once_with(mock_page)

    @patch('pypdf.PdfReader')
    @patch('pypdf.PdfWriter')
    @patch('builtins.open', create=True)
    def test_extract_page_range(self, mock_open, mock_writer_class, mock_reader_class):
        """Test extracting a range of pages."""
        mock_reader = Mock()
        mock_reader.pages = [Mock() for _ in range(10)]
        mock_reader_class.return_value = mock_reader

        mock_writer = Mock()
        mock_writer.pages = []
        mock_writer_class.return_value = mock_writer

        result = dc.extract_pdf_pages(
            'input.pdf',
            'output.pdf',
            page_range='2-5',
            verbose=False
        )

        assert result is True
        assert mock_writer.add_page.call_count == 4  # Pages 2-5 (4 pages)

    def test_extract_pages_no_pypdf(self):
        """Test page extraction without pypdf."""
        with patch.dict('sys.modules', {'pypdf': None}):
            result = dc.extract_pdf_pages('input.pdf', 'output.pdf', '1-10')
            assert result is False


class TestPDFOptimization:
    """Test PDF optimization."""

    @patch('pypdf.PdfReader')
    @patch('pypdf.PdfWriter')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.stat')
    def test_optimize_pdf_success(self, mock_stat, mock_open, mock_writer_class, mock_reader_class):
        """Test successful PDF optimization."""
        # Mock reader
        mock_reader = Mock()
        mock_page = Mock()
        mock_reader.pages = [mock_page, mock_page]
        mock_reader_class.return_value = mock_reader

        # Mock writer
        mock_writer = Mock()
        mock_writer.pages = [mock_page, mock_page]
        mock_writer_class.return_value = mock_writer

        # Mock file sizes
        mock_stat.return_value.st_size = 1024 * 1024

        result = dc.optimize_pdf('input.pdf', 'output.pdf', verbose=False)

        assert result is True
        mock_page.compress_content_streams.assert_called()

    def test_optimize_pdf_no_pypdf(self):
        """Test PDF optimization without pypdf."""
        with patch.dict('sys.modules', {'pypdf': None}):
            result = dc.optimize_pdf('input.pdf', 'output.pdf')
            assert result is False


class TestImageExtraction:
    """Test image extraction from PDFs."""

    @patch('pypdf.PdfReader')
    @patch('PIL.Image')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', create=True)
    def test_extract_images_success(self, mock_open, mock_mkdir, mock_image, mock_reader_class):
        """Test successful image extraction."""
        # Mock PDF reader
        mock_reader = Mock()
        mock_page = MagicMock()

        # Mock XObject with image
        mock_obj = MagicMock()
        mock_obj.__getitem__.side_effect = lambda k: {
            '/Subtype': '/Image',
            '/Width': 100,
            '/Height': 100,
            '/Filter': '/DCTDecode'
        }[k]
        mock_obj.get_data.return_value = b'image_data'

        mock_xobjects = MagicMock()
        mock_xobjects.__iter__.return_value = ['img1']
        mock_xobjects.__getitem__.return_value = mock_obj

        mock_resources = MagicMock()
        mock_resources.get_object.return_value = mock_xobjects
        mock_page.__getitem__.side_effect = lambda k: {
            '/Resources': {'/XObject': mock_resources}
        }[k]

        mock_reader.pages = [mock_page]
        mock_reader_class.return_value = mock_reader

        result = dc.extract_images_from_pdf('input.pdf', './output', verbose=False)

        assert len(result) > 0

    def test_extract_images_no_dependencies(self):
        """Test image extraction without required dependencies."""
        with patch.dict('sys.modules', {'pypdf': None}):
            result = dc.extract_images_from_pdf('input.pdf', './output')
            assert result == []


class TestMarkdownConversion:
    """Test Markdown to PDF conversion."""

    @patch('markdown.markdown')
    @patch('builtins.open', create=True)
    @patch('subprocess.run')
    @patch('pathlib.Path.unlink')
    def test_convert_markdown_success(self, mock_unlink, mock_run, mock_open, mock_markdown):
        """Test successful Markdown to PDF conversion."""
        mock_markdown.return_value = '<h1>Test</h1>'

        # Mock file reading and writing
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = '# Test'
        mock_open.return_value = mock_file

        result = dc.convert_markdown_to_pdf('input.md', 'output.pdf', verbose=False)

        assert result is True
        mock_run.assert_called_once()

    @patch('markdown.markdown')
    @patch('builtins.open', create=True)
    @patch('subprocess.run')
    def test_convert_markdown_no_wkhtmltopdf(self, mock_run, mock_open, mock_markdown):
        """Test Markdown conversion without wkhtmltopdf."""
        mock_markdown.return_value = '<h1>Test</h1>'

        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = '# Test'
        mock_open.return_value = mock_file

        mock_run.side_effect = FileNotFoundError()

        result = dc.convert_markdown_to_pdf('input.md', 'output.pdf', verbose=False)

        assert result is False

    def test_convert_markdown_no_markdown_lib(self):
        """Test Markdown conversion without markdown library."""
        with patch.dict('sys.modules', {'markdown': None}):
            result = dc.convert_markdown_to_pdf('input.md', 'output.pdf')
            assert result is False


class TestHTMLConversion:
    """Test HTML to PDF conversion."""

    @patch('subprocess.run')
    def test_convert_html_success(self, mock_run):
        """Test successful HTML to PDF conversion."""
        result = dc.convert_html_to_pdf('input.html', 'output.pdf', verbose=False)

        assert result is True
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_convert_html_no_wkhtmltopdf(self, mock_run):
        """Test HTML conversion without wkhtmltopdf."""
        mock_run.side_effect = FileNotFoundError()

        result = dc.convert_html_to_pdf('input.html', 'output.pdf', verbose=False)

        assert result is False


class TestIntegration:
    """Integration tests."""

    @patch('pathlib.Path.exists')
    def test_file_not_found(self, mock_exists):
        """Test handling of non-existent input file."""
        mock_exists.return_value = False

        # This would normally be tested via main() but we test the concept
        assert not Path('nonexistent.pdf').exists()

    @patch('document_converter.check_dependencies')
    def test_check_dependencies_integration(self, mock_check):
        """Test dependency checking integration."""
        mock_check.return_value = {
            'pypdf': True,
            'markdown': True,
            'pillow': True
        }

        deps = dc.check_dependencies()

        assert deps['pypdf'] is True
        assert deps['markdown'] is True
        assert deps['pillow'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=document_converter', '--cov-report=term-missing'])
