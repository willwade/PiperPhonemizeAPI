from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gruut_ipa
from piper_phonemize import Phonemizer


app = FastAPI(
    title="Phonemizer API",
    description="Convert text to various phoneme formats",
    version="0.1.0"
)


class PhonemeRequest(BaseModel):
    text: str
    language: str


class PhonemeResponse(BaseModel):
    ipa: str
    sampa: str
    espeak_ascii: str


@app.post("/phonemize", response_model=PhonemeResponse)
async def phonemize_text(request: PhonemeRequest) -> PhonemeResponse:
    try:
        # Initialize phonemizer with the requested language
        phonemizer = Phonemizer(request.language)
        
        # Get eSpeak ASCII phonemes
        espeak_ascii = phonemizer.phonemize(request.text)
        
        # Convert to IPA using gruut-ipa
        ipa = gruut_ipa.convert("espeak", "ipa", espeak_ascii)
        
        # Convert to SAMPA using gruut-ipa
        sampa = gruut_ipa.convert("ipa", "sampa", ipa)
        
        return PhonemeResponse(
            ipa=ipa,
            sampa=sampa,
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