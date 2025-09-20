# GRC SDK

A Python SDK for GRC company file services. This library provides file hashing operations using SHA256, offering a simple and efficient way to compute SHA256 hashes of files, byte data, and file-like objects.

## Features

- **SHA256 Hashing**: Compute SHA256 hashes for files, bytes, and streams
- **File Support**: Hash files directly from disk
- **Stream Support**: Hash file-like objects (e.g., FastAPI UploadFile.file)
- **Memory Efficient**: Chunked reading for large files
- **Type Safe**: Full type hints support
- **Well Tested**: Comprehensive test coverage
- **GRC Company**: Built specifically for GRC company file operations

## Installation

### From PyPI (when published)
```bash
pip install grc-sdk
```

### From Source
```bash
git clone https://github.com/grc-sdk/grc-sdk.git
cd grc-sdk
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/grc-sdk/grc-sdk.git
cd grc-sdk
pip install -e ".[dev]"
```

## Quick Start

```python
from grc import FileHasher

# Initialize the hasher
hasher = FileHasher()

# Hash a file on disk
file_hash = hasher.hash_file("example.pdf")
print(f"File hash: {file_hash}")

# Hash raw bytes
data = b"hello world"
bytes_hash = hasher.hash_bytes(data)
print(f"Bytes hash: {bytes_hash}")

# Hash a file-like object
from io import BytesIO
stream = BytesIO(b"hello world")
stream_hash = hasher.hash_stream(stream)
print(f"Stream hash: {stream_hash}")
```

## API Reference

### FileHasher Class

The main class for computing SHA256 hashes.

#### Methods

##### `hash_file(file_path: str) -> str`

Computes the SHA256 hash of a file on disk.

**Parameters:**
- `file_path` (str): Path to the file to hash

**Returns:**
- `str`: SHA256 hex digest (64 characters)

**Raises:**
- `FileNotFoundError`: If the file path is invalid

**Example:**
```python
hasher = FileHasher()
hash_value = hasher.hash_file("document.pdf")
print(hash_value)  # e.g., "a1b2c3d4e5f6..."
```

##### `hash_bytes(data: bytes) -> str`

Computes the SHA256 hash of raw bytes.

**Parameters:**
- `data` (bytes): Bytes to hash

**Returns:**
- `str`: SHA256 hex digest (64 characters)

**Example:**
```python
hasher = FileHasher()
data = b"hello world"
hash_value = hasher.hash_bytes(data)
print(hash_value)  # "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
```

##### `hash_stream(file_obj) -> str`

Computes the SHA256 hash of a file-like object.

**Parameters:**
- `file_obj`: File-like object to hash (must support `read()` and `seek()`)

**Returns:**
- `str`: SHA256 hex digest (64 characters)

**Note:**
The file pointer will be reset to its original position after hashing.

**Example:**
```python
from io import BytesIO

hasher = FileHasher()
stream = BytesIO(b"hello world")
hash_value = hasher.hash_stream(stream)
print(hash_value)  # "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
```

## Usage Examples

### Hashing Files

```python
from grc import FileHasher

hasher = FileHasher()

# Hash a PDF file
pdf_hash = hasher.hash_file("document.pdf")
print(f"PDF hash: {pdf_hash}")

# Hash an image file
image_hash = hasher.hash_file("image.jpg")
print(f"Image hash: {image_hash}")

# Hash a text file
text_hash = hasher.hash_file("readme.txt")
print(f"Text hash: {text_hash}")
```

### Hashing Bytes

```python
from grc import FileHasher

hasher = FileHasher()

# Hash string data
text_data = "Hello, World!".encode('utf-8')
text_hash = hasher.hash_bytes(text_data)
print(f"Text hash: {text_hash}")

# Hash binary data
binary_data = b'\x00\x01\x02\x03\x04\x05'
binary_hash = hasher.hash_bytes(binary_data)
print(f"Binary hash: {binary_hash}")

# Hash empty bytes
empty_hash = hasher.hash_bytes(b"")
print(f"Empty hash: {empty_hash}")
```

### Hashing Streams

```python
from grc import FileHasher
from io import BytesIO

hasher = FileHasher()

# Hash a BytesIO stream
stream = BytesIO(b"hello world")
stream_hash = hasher.hash_stream(stream)
print(f"Stream hash: {stream_hash}")

# Hash with preserved position
stream = BytesIO(b"hello world")
stream.seek(5)  # Move to middle
original_pos = stream.tell()
hash_value = hasher.hash_stream(stream)
print(f"Position after hash: {stream.tell()}")  # Should be 5
```

### FastAPI Integration

```python
from fastapi import FastAPI, UploadFile
from grc import FileHasher

app = FastAPI()
hasher = FileHasher()

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Hash the uploaded file
    file_hash = hasher.hash_stream(file.file)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "hash": file_hash
    }
```

## Error Handling

```python
from grc import FileHasher

hasher = FileHasher()

try:
    hash_value = hasher.hash_file("nonexistent_file.txt")
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

## Performance Considerations

- The library uses chunked reading (4KB chunks) for efficient memory usage with large files
- All methods return consistent 64-character SHA256 hex digests
- File streams are automatically reset to their original position after hashing

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=grc

# Run specific test file
python -m pytest tests/test_hasher.py
```

### Code Quality

```bash
# Format code
black grc/ tests/

# Sort imports
isort grc/ tests/

# Lint code
flake8 grc/ tests/

# Type checking
mypy grc/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

### 1.0.0
- Initial release
- SHA256 hashing for files, bytes, and streams
- Comprehensive test coverage
- Type hints support
