#!/usr/bin/env python3
"""
Configuration module for Blog Generator AI Agent
"""

import os
from typing import List

class Config:
    """Configuration class for the application"""
    
    # Groq API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    # Application Configuration
    APP_NAME = "Blog Generator AI Agent"
    APP_VERSION = "1.0.0"
    
    # Processing Configuration
    DEFAULT_MAX_LENGTH = 800
    DEFAULT_STYLE = "informative"
    DEFAULT_PROCESSING_INTENSITY = "heavy"
    
    # Available writing styles
    AVAILABLE_STYLES = [
        "informative",
        "casual", 
        "professional",
        "engaging"
    ]
    
    # Available processing intensities
    AVAILABLE_INTENSITIES = [
        "light",
        "medium", 
        "heavy",
        "balanced",
        "plagiarism_focused",
        "ai_focused"
    ]
    
    def validate_required_keys(self) -> None:
        """Validate that required configuration keys are set"""
        required_keys = ["GROQ_API_KEY"]
        missing_keys = []
        
        for key in required_keys:
            if not getattr(self, key):
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")

# Create global config instance
config = Config() 