"""
File hashing utilities using SHA256.
"""

import hashlib
from typing import Union, BinaryIO


class FileHasher:
    """
    A utility class for computing SHA256 hashes of files, bytes, and streams.
    """
    
    def __init__(self):
        """Initialize the FileHasher."""
        pass
    
    def hash_file(self, file_path: str) -> str:
        """
        Compute SHA256 hash of a file on disk.
        
        Args:
            file_path: Path to the file to hash
            
        Returns:
            SHA256 hex digest (64 characters)
            
        Raises:
            FileNotFoundError: If the file path is invalid
        """
        try:
            with open(file_path, 'rb') as f:
                return self._compute_hash(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def hash_bytes(self, data: bytes) -> str:
        """
        Compute SHA256 hash of raw bytes.
        
        Args:
            data: Bytes to hash
            
        Returns:
            SHA256 hex digest (64 characters)
        """
        return hashlib.sha256(data).hexdigest()
    
    def hash_stream(self, file_obj: BinaryIO) -> str:
        """
        Compute SHA256 hash of a file-like object.
        
        Args:
            file_obj: File-like object to hash
            
        Returns:
            SHA256 hex digest (64 characters)
            
        Note:
            The file pointer will be reset to position 0 after hashing.
        """
        # Store current position
        current_position = file_obj.tell()
        
        # Reset to beginning
        file_obj.seek(0)
        
        try:
            # Compute hash
            hash_digest = self._compute_hash(file_obj)
            return hash_digest
        finally:
            # Always reset file pointer to original position
            file_obj.seek(current_position)
    
    def _compute_hash(self, file_obj: BinaryIO) -> str:
        """
        Internal method to compute SHA256 hash of a file-like object.
        
        Args:
            file_obj: File-like object to hash
            
        Returns:
            SHA256 hex digest (64 characters)
        """
        sha256_hash = hashlib.sha256()
        
        # Read file in chunks to handle large files efficiently
        for chunk in iter(lambda: file_obj.read(4096), b""):
            sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
