#!/usr/bin/env python3
"""
Gemini LLM Client Service
Custom LangChain wrapper for Google Gemini LLM with specialized configurations
"""

import os
import logging
from typing import Any, List, Optional, Dict
from google import genai
from google.genai import types

try:
    from langchain.llms.base import LLM
    from langchain.callbacks.manager import CallbackManagerForLLMRun
except ImportError:
    # Fallback for newer LangChain versions
    from langchain_core.language_models.llms import LLM
    from langchain_core.callbacks.manager import CallbackManagerForLLMRun

from pydantic import Field
from core.config import config

# Configure logging
logger = logging.getLogger(__name__)

class GeminiLLM(LLM):
    """Custom LangChain wrapper for Google Gemini LLM"""
    
    client: Any = Field(default=None, exclude=True)
    model: str = Field(default="gemini-2.0-flash")
    api_key: str = Field(default="")
    temperature: float = Field(default=0.1)
    max_tokens: int = Field(default=2048)
    
    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        
        # Use provided API key or from config
        self.api_key = api_key or config.gemini_api_key
        
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
        
        # Initialize Gemini client
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"✅ Gemini LLM initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            raise
    
    @property
    def _llm_type(self) -> str:
        """Return identifier for this LLM."""
        return "gemini"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Gemini LLM with the given prompt."""
        try:
            logger.debug(f"🔍 Sending prompt to Gemini (length: {len(prompt)} chars)")
            
            # Prepare content for Gemini
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt),
                    ],
                ),
            ]
            
            # Configure generation settings
            generate_content_config = types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )
            
            # Generate response
            response_chunks = []
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    response_chunks.append(chunk.text)
            
            # Combine all chunks
            full_response = "".join(response_chunks)
            
            if not full_response.strip():
                logger.warning("⚠️ Gemini returned empty response")
                return "I apologize, but I couldn't generate a response. Please try again."
            
            logger.debug(f"✅ Gemini response received (length: {len(full_response)} chars)")
            return full_response.strip()
            
        except Exception as e:
            logger.error(f"❌ Error calling Gemini LLM: {e}")
            # Return a fallback response instead of raising exception
            return f"Error occurred while processing request: {str(e)}"

# ============================================================================
# SPECIALIZED LLM CONFIGURATIONS FOR DIFFERENT AGENT TYPES
# ============================================================================

def get_detective_llm() -> GeminiLLM:
    """Get LLM optimized for incident detection and analysis"""
    return GeminiLLM(
        temperature=0.1,  # Low temperature for precise analysis
        max_tokens=1500,
        model=config.gemini_model
    )

def get_diagnostics_llm() -> GeminiLLM:
    """Get LLM optimized for system diagnostics"""
    return GeminiLLM(
        temperature=0.05,  # Very low temperature for technical accuracy
        max_tokens=1200,
        model=config.gemini_model
    )

def get_historical_llm() -> GeminiLLM:
    """Get LLM optimized for historical analysis"""
    return GeminiLLM(
        temperature=0.2,  # Slightly higher for pattern matching
        max_tokens=1800,
        model=config.gemini_model
    )

def get_remediation_llm() -> GeminiLLM:
    """Get LLM optimized for safe remediation planning"""
    return GeminiLLM(
        temperature=0.0,  # Minimum temperature for safety-critical decisions
        max_tokens=1000,
        model=config.gemini_model
    )

def get_communication_llm() -> GeminiLLM:
    """Get LLM optimized for stakeholder communication"""
    return GeminiLLM(
        temperature=0.3,  # Higher temperature for natural communication
        max_tokens=800,
        model=config.gemini_model
    )

def get_postmortem_llm() -> GeminiLLM:
    """Get LLM optimized for post-mortem analysis and documentation"""
    return GeminiLLM(
        temperature=0.2,  # Balanced for analysis and creativity
        max_tokens=2048,
        model=config.gemini_model
    )

# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_gemini_connection(api_key: str = None) -> bool:
    """
    Test Gemini LLM connection and basic functionality
    
    Args:
        api_key: API key to test (optional)
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        logger.info("🧪 Testing Gemini LLM connection...")
        
        llm = get_detective_llm()
        
        # Simple test prompt
        test_prompt = """
        You are an expert DevOps incident analyst. 
        
        Analyze this simple scenario:
        - Service: user-service
        - Error: Database connection timeout
        - CPU: 85%
        - Memory: 90%
        
        Provide a brief analysis with confidence score (0-1).
        """
        
        response = llm._call(test_prompt)
        
        if response and len(response) > 50:
            logger.info("✅ Gemini LLM connection test successful")
            logger.info(f"📝 Sample response: {response[:100]}...")
            return True
        else:
            logger.error("❌ Gemini LLM returned insufficient response")
            return False
            
    except Exception as e:
        logger.error(f"❌ Gemini LLM connection test failed: {e}")
        return False