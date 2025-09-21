#!/usr/bin/env python3
"""
Core Configuration Management
Environment-based configuration for the AI-Powered DevOps Incident Response System
"""

import os
from dataclasses import dataclass
from typing import Optional

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
        """Load configuration from environment variables"""
        # Override with environment variables if available
        self.mock_api_base_url = os.getenv("MOCK_API_BASE_URL", self.mock_api_base_url)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", self.gemini_api_key)
        self.gemini_model = os.getenv("GEMINI_MODEL", self.gemini_model)
        
        # Numeric configurations
        self.auto_remediation_confidence_threshold = float(
            os.getenv("AUTO_REMEDIATION_THRESHOLD", str(self.auto_remediation_confidence_threshold))
        )
        self.max_retries = int(os.getenv("MAX_RETRIES", str(self.max_retries)))
        self.max_parallel_incidents = int(os.getenv("MAX_PARALLEL_INCIDENTS", str(self.max_parallel_incidents)))
        self.escalation_timeout_minutes = int(os.getenv("ESCALATION_TIMEOUT", str(self.escalation_timeout_minutes)))
        
        # Logging
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
    if not config.gemini_api_key or config.gemini_api_key == "AIzaSyCNPiCpybxrw5q67zkpd2LQy-5HBTlnDo4":
        raise ValueError(
            "GEMINI_API_KEY is required. Set the GEMINI_API_KEY environment variable "
            "or update the configuration with your actual API key."
        )
    
    # Validate thresholds
    if not (0.0 <= config.auto_remediation_confidence_threshold <= 1.0):
        raise ValueError("AUTO_REMEDIATION_THRESHOLD must be between 0.0 and 1.0")
    
    if config.max_retries < 1:
        raise ValueError("MAX_RETRIES must be at least 1")
    
    return True

# Global configuration instance
config = get_config()