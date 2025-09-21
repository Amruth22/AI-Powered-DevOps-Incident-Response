#!/usr/bin/env python3
"""
Base Agent Class
Abstract base class for all incident response agents with standardized interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from crewai import Agent
from services.gemini.client import GeminiLLM

class BaseIncidentAgent(ABC):
    """Abstract base class for all incident response agents"""
    
    def __init__(self, role: str, goal: str, backstory: str, llm: Optional[GeminiLLM] = None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = llm
        self.logger = logging.getLogger(f"agent.{self._get_agent_name()}")
        
        # Create CrewAI agent if LLM is provided
        if self.llm:
            self.crewai_agent = Agent(
                role=self.role,
                goal=self.goal,
                backstory=self.backstory,
                llm=self.llm,
                verbose=False,
                allow_delegation=False,
                max_iter=1
            )
        else:
            self.crewai_agent = None
    
    @abstractmethod
    def _get_agent_name(self) -> str:
        """Get the agent name for logging and identification"""
        pass
    
    @abstractmethod
    async def analyze_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async analysis method to be implemented by subclasses"""
        pass
    
    def _extract_confidence_score(self, analysis: str) -> float:
        """Extract confidence score from analysis text"""
        import re
        
        patterns = [
            r'confidence.*?score.*?(\d+\.?\d*)',
            r'confidence.*?(\d+\.?\d*)',
            r'(\d+\.?\d*).*?confidence',
            r'(0\.[0-9]+)',
            r'([0-9]+)%'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, analysis.lower())
            for match in matches:
                try:
                    confidence = float(match)
                    if confidence > 1.0:
                        confidence = confidence / 100.0
                    if 0.1 <= confidence <= 1.0:
                        return confidence
                except:
                    continue
        
        return 0.75  # Default confidence
    
    def _extract_health_score(self, analysis: str) -> float:
        """Extract health score from analysis text"""
        import re
        
        patterns = [
            r'health.*?score.*?(\d+\.?\d*)',
            r'system.*?health.*?(\d+\.?\d*)',
            r'health.*?(\d+\.?\d*)',
            r'(0\.[0-9]+)',
            r'([0-9]+)%'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, analysis.lower())
            for match in matches:
                try:
                    score = float(match)
                    if score > 1.0:
                        score = score / 100.0
                    if 0.1 <= score <= 1.0:
                        return score
                except:
                    continue
        
        return 0.70  # Default health score
    
    def _extract_pattern_confidence(self, analysis: str) -> float:
        """Extract pattern confidence from analysis text"""
        import re
        
        patterns = [
            r'pattern.*?confidence.*?(\d+\.?\d*)',
            r'match.*?confidence.*?(\d+\.?\d*)',
            r'confidence.*?(\d+\.?\d*)',
            r'(0\.[0-9]+)',
            r'([0-9]+)%'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, analysis.lower())
            for match in matches:
                try:
                    confidence = float(match)
                    if confidence > 1.0:
                        confidence = confidence / 100.0
                    if 0.1 <= confidence <= 1.0:
                        return confidence
                except:
                    continue
        
        return 0.80  # Default pattern confidence
    
    def _extract_remediation_confidence(self, analysis: str) -> float:
        """Extract remediation confidence from analysis text"""
        import re
        
        patterns = [
            r'remediation.*?confidence.*?(\d+\.?\d*)',
            r'auto.*?confidence.*?(\d+\.?\d*)',
            r'confidence.*?(\d+\.?\d*)',
            r'(0\.[0-9]+)',
            r'([0-9]+)%'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, analysis.lower())
            for match in matches:
                try:
                    confidence = float(match)
                    if confidence > 1.0:
                        confidence = confidence / 100.0
                    if 0.1 <= confidence <= 1.0:
                        return confidence
                except:
                    continue
        
        # Check for safety keywords that indicate lower confidence
        if any(word in analysis.lower() for word in ['risky', 'dangerous', 'uncertain', 'complex']):
            return 0.45
        
        return 0.65  # Default remediation confidence
    
    async def execute_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent analysis asynchronously with error handling"""
        agent_name = self._get_agent_name()
        incident_id = incident_data.get("incident_id", "unknown")
        
        self.logger.info(f"🤖 {agent_name.upper()} AGENT: {incident_id}")
        
        try:
            # Execute agent-specific analysis
            result = await self.analyze_async(incident_data)
            
            # Add metadata
            result.update({
                "agent": agent_name,
                "success": True,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.info(f"✅ {agent_name.title()} analysis complete")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ {agent_name.title()} agent error: {e}")
            return {
                "agent": agent_name,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }