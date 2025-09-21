#!/usr/bin/env python3
"""
Detective Agent
AI-powered incident detective with API integration for investigation
"""

import asyncio
from typing import Dict, Any
from .base_agent import BaseIncidentAgent
from services.gemini.client import get_detective_llm
from services.mock.client import get_investigation_data

class DetectiveAgent(BaseIncidentAgent):
    """AI-powered incident detective with API integration"""
    
    def __init__(self):
        super().__init__(
            role="Senior Incident Detective",
            goal="Detect and analyze incidents with AI-powered intelligence",
            backstory="Expert incident detective with advanced AI analysis capabilities and access to system logs and metrics",
            llm=get_detective_llm()
        )
    
    def _get_agent_name(self) -> str:
        return "detective"
    
    async def analyze_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Investigate incident with API data analysis"""
        
        # Gather investigation data from APIs
        investigation_data = await self._gather_investigation_data_async(incident_data)
        
        # AI Analysis
        prompt = f"""
        INCIDENT INVESTIGATION - {incident_data.get('incident_id', 'unknown')}
        
        BASIC INCIDENT DATA:
        - Service: {incident_data.get('service', 'unknown')}
        - Type: {incident_data.get('type', 'unknown')}
        - Severity: {incident_data.get('severity', 'unknown')}
        - Description: {incident_data.get('description', 'Unknown incident')}
        - Symptoms: {', '.join(incident_data.get('symptoms', []))}
        
        INVESTIGATION DATA GATHERED:
        {self._format_investigation_data(investigation_data)}
        
        As a senior incident detective, provide:
        1. CONFIDENCE SCORE (0.0-1.0): How confident are you this is a genuine incident?
        2. ROOT CAUSE ANALYSIS: What is the most likely root cause?
        3. SEVERITY ASSESSMENT: Is the current severity appropriate?
        4. IMPACT ANALYSIS: What systems/users are affected?
        5. URGENCY LEVEL: How quickly must this be resolved?
        6. KEY EVIDENCE: What evidence supports your conclusions?
        
        Be decisive and provide specific confidence scores.
        """
        
        # Run AI analysis in executor to avoid blocking
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, self.llm._call, prompt)
        
        # Extract confidence score
        confidence = self._extract_confidence_score(analysis)
        
        return {
            "analysis": analysis,
            "confidence": confidence,
            "investigation_data": investigation_data
        }
    
    async def _gather_investigation_data_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gather investigation data from APIs asynchronously"""
        service = incident_data.get('service', 'unknown')
        incident_type = incident_data.get('type', 'unknown')
        
        # Run API calls in executor to avoid blocking
        loop = asyncio.get_event_loop()
        investigation_data = await loop.run_in_executor(
            None, get_investigation_data, service, incident_type
        )
        
        return investigation_data
    
    def _format_investigation_data(self, data: Dict[str, Any]) -> str:
        """Format investigation data for AI analysis"""
        formatted = []
        
        # Format logs data
        if "logs" in data and "error" not in data["logs"]:
            logs = data["logs"]
            formatted.append(f"LOGS ANALYSIS:")
            formatted.append(f"- Total logs: {logs.get('total_logs', 0)}")
            formatted.append(f"- Error count: {logs.get('summary', {}).get('error_count', 0)}")
            formatted.append(f"- Warning count: {logs.get('summary', {}).get('warning_count', 0)}")
            
            # Add top errors
            top_errors = logs.get('top_errors', [])
            if top_errors:
                formatted.append("- Top errors:")
                for error in top_errors[:2]:
                    formatted.append(f"  • {error.get('message', 'Unknown')}: {error.get('count', 0)} occurrences")
        
        # Format metrics data
        if "metrics" in data and "error" not in data["metrics"]:
            metrics = data["metrics"]
            formatted.append(f"METRICS ANALYSIS:")
            formatted.append(f"- Service health: {metrics.get('health_score', 'Unknown')}")
            formatted.append(f"- CPU usage: {metrics.get('cpu_usage', 'Unknown')}")
            formatted.append(f"- Memory usage: {metrics.get('memory_usage', 'Unknown')}")
            formatted.append(f"- Request rate: {metrics.get('request_rate', 'Unknown')}")
        
        return "\n".join(formatted) if formatted else "No investigation data available"