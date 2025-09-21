#!/usr/bin/env python3
"""
Communication Agent
AI-powered stakeholder communication and notifications
"""

import asyncio
from typing import Dict, Any
from .base_agent import BaseIncidentAgent
from services.gemini.client import get_communication_llm

class CommunicationAgent(BaseIncidentAgent):
    """AI-powered stakeholder communication and notifications"""
    
    def __init__(self):
        super().__init__(
            role="Senior Communication Coordinator",
            goal="Handle stakeholder notifications with AI-powered communication",
            backstory="Expert communication coordinator with AI-powered messaging and stakeholder management expertise",
            llm=get_communication_llm()
        )
    
    def _get_agent_name(self) -> str:
        return "communication"
    
    async def analyze_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle communications and stakeholder notifications"""
        
        # Combine all analyses for communication context
        combined_analysis = self._combine_all_analyses(incident_data)
        
        # AI Analysis
        prompt = f"""
        STAKEHOLDER COMMUNICATION - {incident_data.get('incident_id', 'unknown')}
        
        INCIDENT SUMMARY:
        - Service: {incident_data.get('service', 'unknown')}
        - Type: {incident_data.get('type', 'unknown')}
        - Severity: {incident_data.get('severity', 'unknown')}
        - Status: {incident_data.get('status', 'active')}
        - Resolution Method: {incident_data.get('resolution_method', 'Unknown')}
        
        ALL AGENT ANALYSES:
        {combined_analysis}
        
        As a communication expert, provide:
        1. COMMUNICATION CONFIDENCE (0.0-1.0): Confidence in messaging strategy
        2. STAKEHOLDER NOTIFICATIONS: Who should be notified?
        3. MESSAGE CONTENT: What should be communicated?
        4. ESCALATION STRATEGY: When to escalate communications?
        5. FOLLOW-UP PLAN: What follow-up communications are needed?
        6. TRANSPARENCY LEVEL: How much detail to share?
        
        Include a specific communication confidence score.
        """
        
        # Run AI analysis in executor to avoid blocking
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, self.llm._call, prompt)
        
        # Extract communication confidence
        comm_confidence = self._extract_confidence_score(analysis)
        
        return {
            "analysis": analysis,
            "communication_confidence": comm_confidence
        }
    
    def _combine_all_analyses(self, incident_data: Dict[str, Any]) -> str:
        """Combine all agent analyses for communication context"""
        combined = []
        
        # Get agent analyses from incident data
        agent_analyses = incident_data.get("agent_analyses", {})
        
        for agent_name, analysis in agent_analyses.items():
            if isinstance(analysis, dict) and "analysis" in analysis:
                combined.append(f"\n{agent_name.upper()}: {analysis['analysis'][:200]}...")
        
        return "\n".join(combined) if combined else "No analyses available for communication"