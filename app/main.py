from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from enum import Enum
import gruut
from piper_phonemize import phonemize_espeak
from pathlib import Path


# Define available languages from gruut's documentation
SUPPORTED_LANGUAGES = {
    "ar": "Arabic",
    "cs": "Czech",
    "cs-cz": "Czech (CZ)",
    "de": "German",
    "de-de": "German (DE)",
    "en": "English",
    "en-us": "English (US)",
    "es": "Spanish",
    "es-es": "Spanish (ES)",
    "fa": "Persian",
    "fr": "French",
    "fr-fr": "French (FR)",
    "it": "Italian",
    "it-it": "Italian (IT)",
    "lb": "Luxembourgish",
    "nl": "Dutch",
    "ru": "Russian",
    "ru-ru": "Russian (RU)",
    "sv": "Swedish",
    "sv-se": "Swedish (SE)",
    "sw": "Swahili"
}


app = FastAPI(
    title="Phonemizer API",
    description="""
    Convert text to various phoneme formats including IPA, SAMPA, and eSpeak ASCII.
    
    Use the /languages endpoint to see all supported languages.
    """,
    version="0.1.0"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Phonemizer API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "phonemize": {
                "path": "/phonemize",
                "method": "POST",
                "description": "Convert text to phonemes"
            },
            "languages": {
                "path": "/languages",
                "method": "GET",
                "description": "List supported languages"
            }
        }
    }


class PhonemeRequest(BaseModel):
    text: str = Field(
        ...,
        description="The text to convert to phonemes",
        example="hello world"
    )
    language: str = Field(
        ...,
        description="The language code for phonemization (e.g., 'en-us', 'fr', 'de')",
        example="en-us"
    )

    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()

    @validator('language')
    def language_must_be_supported(cls, v):
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f'Language "{v}" not supported. Available languages: {", ".join(SUPPORTED_LANGUAGES.keys())}'
            )
        return v

    class Config:
        schema_extra = {
            "example": {
                "text": "hello world",
                "language": "en-us"
            }
        }


class PhonemeResponse(BaseModel):
    ipa: str = Field(
        ...,
        description="International Phonetic Alphabet representation (currently same as espeak)",
        example="həˈloʊ ˈwɜːld"
    )
    sampa: str = Field(
        ...,
        description="SAMPA phonetic representation (currently same as espeak)",
        example="h@\"loU \"w3:ld"
    )
    espeak_ascii: str = Field(
        ...,
        description="eSpeak ASCII phoneme representation",
        example="h@l'oU w3:ld"
    )
    note: str = Field(
        default="Format conversion between IPA and SAMPA is pending implementation",
        description="Additional information about the response"
    )

    class Config:
        schema_extra = {
            "example": {
                "ipa": "həˈloʊ ˈwɜːld",
                "sampa": "h@\"loU \"w3:ld",
                "espeak_ascii": "h@l'oU w3:ld",
                "note": "Format conversion between IPA and SAMPA is pending implementation"
            }
        }


@app.get("/languages", 
    summary="List supported languages",
    description="Returns a list of all supported language codes and their descriptions")
async def get_languages():
    """Get a list of all supported languages and their codes."""
    return {
        "languages": [
            {
                "code": code,
                "name": name,
                "description": f"Language code: {code}"
            } for code, name in SUPPORTED_LANGUAGES.items()
        ]
    }


@app.post("/phonemize",
    response_model=PhonemeResponse,
    summary="Convert text to phonemes",
    description="""
    Converts input text to phonetic representations.
    Note: Currently all formats return the eSpeak phonemes. Proper conversion is pending.
    """)
async def phonemize_text(request: PhonemeRequest) -> PhonemeResponse:
    try:
        # Get eSpeak ASCII phonemes
        phonemes = phonemize_espeak(request.text, request.language)
        # phonemize_espeak returns List[List[str]], join them
        espeak_ascii = " ".join("".join(p) for p in phonemes)
        
        return PhonemeResponse(
            ipa=espeak_ascii,
            sampa=espeak_ascii,
            espeak_ascii=espeak_ascii
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during phonemization: {str(e)}"
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 