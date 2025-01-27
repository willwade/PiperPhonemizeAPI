# Product Requirements Document (PRD)

## Project Name: Phonemizer API

### Overview
The Phonemizer API is a Python-based web application that converts input text into phonemes in multiple phonetic representations (IPA, SAMPA, and eSpeak ASCII). It uses the Piper Phonemization Library for primary phoneme generation and Gruut-IPA for phoneme format conversion. The application is designed to support multiple languages and will be deployed on a *nix environment, running on a DigitalOcean App Platform.

The API will also provide a Swagger interface for ease of testing and demonstration, along with robust error handling and setup capabilities for managing dependencies like `espeak-ng`.

---

## Features
### Core Features:
1. **Phoneme Conversion**:
   - Input text is converted into phonemes using the Piper Phonemization Library.
   - Supported output formats: IPA, SAMPA, and eSpeak ASCII.
   - Uses Gruut-IPA for format conversions.

2. **Multi-language Support**:
   - Supports multiple languages, selectable via a `language` parameter.
   - Error handling for unsupported languages or invalid input.

3. **Swagger Interface**:
   - Provides a user-friendly interface to test the API.
   - Includes detailed documentation and example requests/responses.

4. **Error Handling**:
   - Gracefully handles errors such as missing dependencies, unsupported languages, or invalid input text.
   - Returns meaningful error messages and HTTP status codes.

5. **Setup and Configuration**:
   - Automated build and installation of `espeak-ng` using `make` and `make install`.
   - Configuration of the Piper Phonemization Library during application startup.

---

## API Endpoints

### 1. `/phonemize`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "text": "This is a test.",
    "language": "en-us"
  }
  ```
- **Response Body**:
  ```json
  {
    "ipa": "ðɪs ɪz ə tɛst.",
    "sampa": "DIs Iz @ tEst.",
    "espeak_ascii": "[[D,Is Iz @ t\'Est.]]"
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Invalid input format.
  - `500 Internal Server Error`: Dependency issues or unexpected runtime errors.

---

## Technical Details

### Dependencies
1. **Piper Phonemization Library**
   - Converts text to phonemes using `lib/piper_phonemize`.
   - Requires the `espeak-ng` fork for generating phoneme data.

2. **Gruut-IPA**
   - Converts phonemes between formats (IPA, SAMPA, eSpeak ASCII).
   - Runs as a Python module (`gruut_ipa`).

3. **FastAPI**
   - Provides the web framework for the API.
   - Handles routing, input validation, and documentation generation (Swagger).

4. **Uvicorn**
   - ASGI server for running the application in production.

5. **DigitalOcean App Platform**
   - Deployment target for hosting the application.
   - Supports automated builds from a Git repository.

### Directory Structure
```
project-root/
|-- app.py                  # Main application file
|-- espeak-ng/              # Espeak-ng source directory
|-- lib/
|   |-- piper_phonemize     # Piper phonemization binary
|-- requirements.txt        # Python dependencies
|-- pyproject.toml          # Poetry configuration
|-- Dockerfile              # Containerization setup
```

---

## Installation and Setup

### Local Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project-root
   ```

2. Install Python dependencies:
   ```bash
   poetry install
   ```

3. Build and install `espeak-ng`:
   ```bash
   cd espeak-ng
   make
   make install
   cd ..
   ```

4. Run the application locally:
   ```bash
   poetry run uvicorn app:app --host 0.0.0.0 --port 8000
   ```

### Deployment on DigitalOcean
1. Push the repository to a GitHub/Bitbucket repository.
2. Configure the DigitalOcean App Platform to build the application using the provided Dockerfile.
3. Ensure the `espeak-ng` directory is included in the deployment.
4. Set the environment variables and deploy.

---

## Error Handling
1. **Missing Dependencies**:
   - If required binaries (`lib/piper_phonemize` or `espeak-ng`) are missing, the application fails gracefully with a detailed error message.

2. **Invalid Input**:
   - Input validation is performed using Pydantic models. Invalid input raises a `400 Bad Request`.

3. **Language Support**:
   - If an unsupported language is requested, the API returns a `400 Bad Request` with a list of supported languages.

---

## Swagger Documentation Examples

### Example Request
- **Text**: "Hello world!"
- **Language**: `en-us`

### Example Response
- **IPA**: `hɛloʊ wɜːld`
- **SAMPA**: `"hel@U "w3:ld`
- **eSpeak ASCII**: `[[h'E,l@U w'3:l,d]]`

---

## Future Enhancements
1. Add support for additional phoneme formats.
2. Improve error messages with detailed suggestions.
3. Add caching for frequently used text-language combinations.
4. Extend language support with community contributions.
5. Provide a web-based UI for users unfamiliar with Swagger.

---

## Glossary
- **IPA**: International Phonetic Alphabet.
- **SAMPA**: Speech Assessment Methods Phonetic Alphabet.
- **eSpeak ASCII**: ASCII representation of phonemes used by eSpeak.

