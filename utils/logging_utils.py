#!/usr/bin/env python3
"""
Logging Utilities
Centralized logging configuration for the incident response system
"""

import logging
import os
from datetime import datetime
from core.config import config

def setup_logging(log_level: str = None, log_file: str = None):
    """Setup centralized logging configuration"""
    
    # Use config values if not provided
    if log_level is None:
        log_level = config.log_level
    if log_file is None:
        log_file = config.log_file
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("agent").setLevel(logging.INFO)
    logging.getLogger("workflow").setLevel(logging.INFO)
    logging.getLogger("service").setLevel(logging.INFO)
    
    # Reduce noise from external libraries
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    
    logging.info(f"✅ Logging configured - Level: {log_level}, File: {log_file}")

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)