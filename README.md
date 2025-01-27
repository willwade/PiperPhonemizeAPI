# Phonemizer API

A Python-based web application that converts input text into phonemes in multiple phonetic representations (IPA, SAMPA, and eSpeak ASCII). Built with FastAPI and powered by the Piper Phonemization Library and Gruut-IPA.

## Features

- Convert text to IPA, SAMPA, and eSpeak ASCII phonetic representations
- Multi-language support
- Swagger UI for easy API testing
- Built with FastAPI and uv for modern Python development
- Docker support

## Prerequisites

- Python 3.9+
- uv (Python package installer)
- git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/phonemizer-api.git
cd phonemizer-api
```

### 2. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies

```bash
uv pip install -e .
```

### 4. Install espeak-ng

```bash
sudo ./scripts/install_espeak.sh
```

## Development

### Running the API locally

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000
Swagger documentation is available at http://localhost:8000/docs

### Running tests

```bash
uv run pytest
```

## Docker Deployment

### Build the Docker image

```bash
docker build -t phonemizer-api .
```

### Run the container

```bash
docker run -p 8000:8000 phonemizer-api
```

## API Usage

### Convert text to phonemes

```bash
curl -X POST http://localhost:8000/phonemize \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world", "language": "en-us"}'
```

Example response:
```json
{
  "ipa": "həˈloʊ ˈwɜːld",
  "sampa": "h@\"loU \"w3:ld",
  "espeak_ascii": "[[h@l'oU w'3:ld]]"
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- [Piper Phonemization Library](https://github.com/rhasspy/piper-phonemize)
- [Gruut-IPA](https://github.com/rhasspy/gruut-ipa)
- [eSpeak-ng (Rhasspy fork)](https://github.com/rhasspy/espeak-ng) 