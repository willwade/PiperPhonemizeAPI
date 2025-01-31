from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from enum import Enum
import gruut
from piper_phonemize import phonemize_espeak
from pathlib import Path
import os
from openai import AzureOpenAI, APIError
from typing import Optional
import logging
from dotenv import load_dotenv


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    api_version="2023-03-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "")
)
ENGINE_NAME = os.getenv("AZURE_OPENAI_ENGINE", "")


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
    Also supports converting IPA back to text using Azure OpenAI.
    
    Use the /languages endpoint to see all supported languages.
    """,
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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
            },
            "ipa-to-text": {
                "path": "/ipa-to-text",
                "method": "POST",
                "description": "Convert IPA to text"
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


class IPAToTextRequest(BaseModel):
    ipa: str = Field(
        ...,
        description="IPA phonemes to convert to text (with or without slashes)",
        examples=["kæt", "/kæt/", "həˈloʊ"]
    )

    @validator('ipa')
    def clean_ipa(cls, v):
        """Clean IPA input by removing slashes and extra whitespace."""
        # Remove leading/trailing slashes and whitespace
        cleaned = v.strip().strip('/')
        if not cleaned:
            raise ValueError('IPA text cannot be empty')
        return cleaned


class IPAToTextResponse(BaseModel):
    text: str = Field(
        ...,
        description="Predicted text from IPA",
        examples=["cat", "hello"]
    )
    confidence: Optional[float] = Field(
        None,
        description="Confidence score of the prediction",
        examples=[0.95]
    )


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


@app.post(
    "/ipa-to-text",
    response_model=IPAToTextResponse,
    summary="Convert IPA to text",
    description="""
    Convert IPA phonemes to the most likely English word spelling using Azure OpenAI.
    
    Examples:
    ```json
    {
        "ipa": "kæt"
    }
    ```
    or
    ```json
    {
        "ipa": "/kæt/"
    }
    ```
    """
)
async def ipa_to_text(request: IPAToTextRequest) -> IPAToTextResponse:
    """Convert IPA phonemes to text using Azure OpenAI."""
    try:
        # Check if Azure OpenAI is configured
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        if not all([endpoint, api_key, ENGINE_NAME]):
            logger.error(f"Missing configuration: endpoint={bool(endpoint)}, api_key={bool(api_key)}, engine={bool(ENGINE_NAME)}")
            raise HTTPException(
                status_code=503,
                detail="Azure OpenAI not configured. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_ENGINE environment variables."
            )

        # Create a new client for each request to ensure fresh configuration
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-05-15",  # Updated API version
            azure_endpoint=endpoint
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that converts IPA symbols "
                    "into English words. Output only the spelled-out English "
                    "word(s), no extra commentary. If multiple words are "
                    "possible, pick the most common."
                ),
            },
            {
                "role": "user",
                "content": f"IPA: {request.ipa}",
            },
        ]

        try:
            response = client.chat.completions.create(
                model=ENGINE_NAME,
                messages=messages,
                temperature=0.0,
                max_tokens=50
            )
            
            predicted_text = response.choices[0].message.content.strip()
            
            return IPAToTextResponse(
                text=predicted_text,
                confidence=response.choices[0].finish_reason == "stop"
            )
        except APIError as e:
            logger.error(f"Azure OpenAI API error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Azure OpenAI API error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error during API call: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error during API call: {str(e)}"
            )
            
    except Exception as e:
        logger.error(f"Error in ipa_to_text: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error converting IPA to text: {str(e)}"
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to check configuration."""
    return {
        "endpoint_set": bool(os.getenv("AZURE_OPENAI_ENDPOINT")),
        "api_key_set": bool(os.getenv("AZURE_OPENAI_API_KEY")),
        "engine_set": bool(os.getenv("AZURE_OPENAI_ENGINE")),
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "").replace(os.getenv("AZURE_OPENAI_API_KEY", ""), "REDACTED"),
        "engine": os.getenv("AZURE_OPENAI_ENGINE", "")
    } 