#!/usr/bin/env python3
"""
Teste Groq API direkt
"""
import asyncio
import sys
import os
sys.path.append('.')

from toobix.core.ai_handler import AIHandler
from toobix.config.settings import Settings

async def test_groq():
    print("🧪 Teste Groq API...")
    
    settings = Settings()
    ai = AIHandler(settings)
    
    # Einfache Test-Anfrage
    response = await ai.get_response("Sage nur 'Hallo' auf Deutsch.")
    print(f"🤖 Antwort: '{response}'")
    
    # Zweite Test-Anfrage
    response2 = await ai.get_response("Wie spät ist es?")
    print(f"🤖 Antwort 2: '{response2}'")

if __name__ == "__main__":
    asyncio.run(test_groq())
