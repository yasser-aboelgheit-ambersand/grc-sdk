"""
Tests for the FileHasher class.
"""

import os
import tempfile
import unittest
from io import BytesIO
from grc import FileHasher


class TestFileHasher(unittest.TestCase):
    """Test cases for FileHasher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hasher = FileHasher()
        self.test_data = b"hello world"
        self.expected_hash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    
    def test_hash_bytes(self):
        """Test hashing raw bytes."""
        result = self.hasher.hash_bytes(self.test_data)
        
        # Assert SHA256 digest length is 64 hex characters
        self.assertEqual(len(result), 64)
        self.assertEqual(result, self.expected_hash)
        
        # Test with empty bytes
        empty_hash = self.hasher.hash_bytes(b"")
        self.assertEqual(len(empty_hash), 64)
        self.assertEqual(empty_hash, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    
    def test_hash_file(self):
        """Test hashing a file on disk."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            temp_file.write(self.test_data)
            temp_file_path = temp_file.name
        
        try:
            result = self.hasher.hash_file(temp_file_path)
            
            # Assert SHA256 digest length is 64 hex characters
            self.assertEqual(len(result), 64)
            self.assertEqual(result, self.expected_hash)
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
    
    def test_hash_file_not_found(self):
        """Test that FileNotFoundError is raised for invalid file paths."""
        with self.assertRaises(FileNotFoundError):
            self.hasher.hash_file("nonexistent_file.txt")
    
    def test_hash_stream(self):
        """Test hashing a file-like object (BytesIO stream)."""
        # Create a BytesIO stream
        stream = BytesIO(self.test_data)
        
        # Test that file pointer is at beginning
        self.assertEqual(stream.tell(), 0)
        
        result = self.hasher.hash_stream(stream)
        
        # Assert SHA256 digest length is 64 hex characters
        self.assertEqual(len(result), 64)
        self.assertEqual(result, self.expected_hash)
        
        # Assert that file pointer is reset to beginning
        self.assertEqual(stream.tell(), 0)
    
    def test_hash_stream_preserves_position(self):
        """Test that hash_stream preserves the original file position."""
        stream = BytesIO(b"hello world")
        
        # Move to middle of stream
        stream.seek(5)
        original_position = stream.tell()
        
        # Hash the stream
        result = self.hasher.hash_stream(stream)
        
        # Assert that position is preserved
        self.assertEqual(stream.tell(), original_position)
        self.assertEqual(len(result), 64)
    
    def test_hash_stream_empty(self):
        """Test hashing an empty stream."""
        stream = BytesIO(b"")
        result = self.hasher.hash_stream(stream)
        
        # Assert SHA256 digest length is 64 hex characters
        self.assertEqual(len(result), 64)
        self.assertEqual(result, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    
    def test_hash_large_data(self):
        """Test hashing larger data to ensure chunked reading works."""
        # Create large test data (1MB)
        large_data = b"x" * (1024 * 1024)
        
        # Test with bytes
        result_bytes = self.hasher.hash_bytes(large_data)
        self.assertEqual(len(result_bytes), 64)
        
        # Test with stream
        stream = BytesIO(large_data)
        result_stream = self.hasher.hash_stream(stream)
        self.assertEqual(len(result_stream), 64)
        
        # Results should be the same
        self.assertEqual(result_bytes, result_stream)
    
    def test_consistency_across_methods(self):
        """Test that all three methods produce the same hash for the same data."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            temp_file.write(self.test_data)
            temp_file_path = temp_file.name
        
        try:
            # Hash using all three methods
            hash_file = self.hasher.hash_file(temp_file_path)
            hash_bytes = self.hasher.hash_bytes(self.test_data)
            
            stream = BytesIO(self.test_data)
            hash_stream = self.hasher.hash_stream(stream)
            
            # All hashes should be identical
            self.assertEqual(hash_file, hash_bytes)
            self.assertEqual(hash_bytes, hash_stream)
            self.assertEqual(hash_file, hash_stream)
            
            # All should be 64 characters
            self.assertEqual(len(hash_file), 64)
            self.assertEqual(len(hash_bytes), 64)
            self.assertEqual(len(hash_stream), 64)
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()
