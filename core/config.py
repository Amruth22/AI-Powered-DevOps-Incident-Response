#!/usr/bin/env python3
"""
Core Configuration Management
Environment-based configuration for the AI-Powered DevOps Incident Response System
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class SystemConfig:
    """System configuration with environment variable support"""
    
    # Mock API Configuration
    mock_api_base_url: str = "http://localhost:8000"
    
    # AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    
    # Decision Making
    auto_remediation_confidence_threshold: float = 0.6
    max_retries: int = 3
    
    # Performance
    max_parallel_incidents: int = 5
    escalation_timeout_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/incident_response.log"
    
    def __post_init__(self):
        """Load configuration from environment variables (.env file)"""
        # Load from .env file using python-dotenv
        self.mock_api_base_url = os.getenv("MOCK_API_BASE_URL", self.mock_api_base_url)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", self.gemini_api_key)
        self.gemini_model = os.getenv("GEMINI_MODEL", self.gemini_model)
        
        # Numeric configurations with type conversion
        self.auto_remediation_confidence_threshold = float(
            os.getenv("AUTO_REMEDIATION_THRESHOLD", str(self.auto_remediation_confidence_threshold))
        )
        self.max_retries = int(os.getenv("MAX_RETRIES", str(self.max_retries)))
        self.max_parallel_incidents = int(os.getenv("MAX_PARALLEL_INCIDENTS", str(self.max_parallel_incidents)))
        self.escalation_timeout_minutes = int(os.getenv("ESCALATION_TIMEOUT", str(self.escalation_timeout_minutes)))
        
        # Logging configuration
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)
        self.log_file = os.getenv("LOG_FILE", self.log_file)

def get_config() -> SystemConfig:
    """Get system configuration instance"""
    return SystemConfig()

def validate_config(config: Optional[SystemConfig] = None) -> bool:
    """Validate system configuration"""
    if config is None:
        config = get_config()
    
    # Check required configurations
    if not config.gemini_api_key or config.gemini_api_key == "your-gemini-api-key-here":
        raise ValueError(
            "GEMINI_API_KEY is required. Please:\n"
            "1. Copy .env.example to .env\n"
            "2. Update GEMINI_API_KEY in .env with your actual API key\n"
            "3. Get your API key from: https://makersuite.google.com/app/apikey"
        )
    
    # Validate thresholds
    if not (0.0 <= config.auto_remediation_confidence_threshold <= 1.0):
        raise ValueError("AUTO_REMEDIATION_THRESHOLD must be between 0.0 and 1.0")
    
    if config.max_retries < 1:
        raise ValueError("MAX_RETRIES must be at least 1")
    
    if config.max_parallel_incidents < 1:
        raise ValueError("MAX_PARALLEL_INCIDENTS must be at least 1")
    
    if config.escalation_timeout_minutes < 1:
        raise ValueError("ESCALATION_TIMEOUT must be at least 1 minute")
    
    return True

def print_config_status():
    """Print current configuration status for debugging"""
    config = get_config()
    
    print("🔧 CONFIGURATION STATUS:")
    print(f"   • Gemini API Key: {'✅ Set' if config.gemini_api_key and config.gemini_api_key != 'your-gemini-api-key-here' else '❌ Missing'}")
    print(f"   • Gemini Model: {config.gemini_model}")
    print(f"   • Mock API URL: {config.mock_api_base_url}")
    print(f"   • Auto-Remediation Threshold: {config.auto_remediation_confidence_threshold}")
    print(f"   • Max Retries: {config.max_retries}")
    print(f"   • Log Level: {config.log_level}")
    print(f"   • Log File: {config.log_file}")

# Global configuration instance
config = get_config()