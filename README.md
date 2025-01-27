# Phonemizer API

A FastAPI-based service that converts text to various phoneme formats (IPA, SAMPA, and eSpeak ASCII) using the Rhasspy fork of eSpeak-NG.

## Features

- Convert text to phonetic representations
- Support for multiple languages (Arabic, Czech, English, French, German, etc.)
- RESTful API with Swagger documentation
- Docker support
- Health check endpoint

## Requirements

- Python 3.9+
- eSpeak-NG (Rhasspy fork)
- FastAPI and dependencies

## Installation

### Local Development

1. Install system dependencies (macOS):
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install build dependencies and espeak-ng
./scripts/install_espeak.sh
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API:
```bash
uvicorn app.main:app --reload
```

### Docker Installation

Build and run using Docker:

```bash
# Build the image
docker build -t phonemizer-api .

# Run the container
docker run -p 8000:8000 phonemizer-api
```

## API Usage

The API will be available at http://localhost:8000 with the following endpoints:

### Endpoints

#### POST /phonemize
Convert text to phonemes.

Request body:
```json
{
    "text": "hello world",
    "language": "en-us"
}
```

Response:
```json
{
    "ipa": "həˈloʊ ˈwɜːld",
    "sampa": "h@\"loU \"w3:ld",
    "espeak_ascii": "h@l'oU w3:ld",
    "note": "Format conversion between IPA and SAMPA is pending implementation"
}
```

#### GET /languages
List all supported languages.

#### GET /health
Health check endpoint.

### Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running Tests

```bash
pytest
```

### API Documentation

The API documentation is automatically generated and available at:
- `/docs` - Swagger UI
- `/redoc` - ReDoc interface

## Notes

- Currently, all phonetic formats (IPA, SAMPA) return the eSpeak ASCII format. Proper conversion is pending implementation.
- The API uses the Rhasspy fork of eSpeak-NG for better compatibility and features.

## License

MIT License

## Acknowledgments

- [eSpeak-NG (Rhasspy fork)](https://github.com/rhasspy/espeak-ng)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Piper Phonemize](https://github.com/rhasspy/piper-phonemize) 