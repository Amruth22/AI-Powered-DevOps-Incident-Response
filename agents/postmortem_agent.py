#!/usr/bin/env python3
"""
Post-Mortem Agent
AI-powered post-mortem analysis and documentation
"""

import asyncio
from typing import Dict, Any
from .base_agent import BaseIncidentAgent
from services.gemini.client import get_postmortem_llm

class PostMortemAgent(BaseIncidentAgent):
    """AI-powered post-mortem analysis and documentation"""
    
    def __init__(self):
        super().__init__(
            role="Senior Post-Mortem Analyst",
            goal="Generate comprehensive post-mortems with AI analysis",
            backstory="Expert incident analyst with AI-powered documentation and comprehensive post-mortem analysis capabilities",
            llm=get_postmortem_llm()
        )
    
    def _get_agent_name(self) -> str:
        return "postmortem"
    
    async def analyze_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive post-mortem analysis"""
        
        # Combine all analyses and resolution data
        combined_analysis = self._combine_all_analyses(incident_data)
        resolution_summary = self._get_resolution_summary(incident_data)
        
        # AI Analysis
        prompt = f"""
        POST-MORTEM ANALYSIS - {incident_data.get('incident_id', 'unknown')}
        
        INCIDENT SUMMARY:
        - Service: {incident_data.get('service', 'unknown')}
        - Type: {incident_data.get('type', 'unknown')}
        - Severity: {incident_data.get('severity', 'unknown')}
        - Duration: {incident_data.get('resolution_time_minutes', 'Unknown')} minutes
        - Resolution: {incident_data.get('resolution_method', 'Unknown')}
        - Success: {incident_data.get('status', 'Unknown') == 'resolved'}
        
        RESOLUTION SUMMARY:
        {resolution_summary}
        
        ALL AGENT ANALYSES:
        {combined_analysis}
        
        As a post-mortem expert, provide:
        1. DOCUMENTATION CONFIDENCE (0.0-1.0): Confidence in analysis completeness
        2. ROOT CAUSE SUMMARY: Final root cause determination
        3. LESSONS LEARNED: Key insights from this incident
        4. PREVENTION MEASURES: How to prevent similar incidents
        5. PROCESS IMPROVEMENTS: How to improve incident response
        6. TIMELINE ANALYSIS: Key events and decision points
        7. RECOMMENDATIONS: Specific actionable recommendations
        
        Include a specific documentation confidence score.
        """
        
        # Run AI analysis in executor to avoid blocking
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, self.llm._call, prompt)
        
        # Extract documentation confidence
        doc_confidence = self._extract_confidence_score(analysis)
        
        return {
            "analysis": analysis,
            "documentation_confidence": doc_confidence
        }
    
    def _combine_all_analyses(self, incident_data: Dict[str, Any]) -> str:
        """Combine all agent analyses for post-mortem"""
        combined = []
        
        # Get agent analyses from incident data
        agent_analyses = incident_data.get("agent_analyses", {})
        
        for agent_name, analysis in agent_analyses.items():
            if isinstance(analysis, dict) and "analysis" in analysis:
                combined.append(f"\n{agent_name.upper()}: {analysis['analysis'][:200]}...")
        
        return "\n".join(combined) if combined else "No analyses available for post-mortem"
    
    def _get_resolution_summary(self, incident_data: Dict[str, Any]) -> str:
        """Get resolution summary for post-mortem"""
        status = incident_data.get('status', 'unknown')
        resolution_method = incident_data.get('resolution_method', 'Unknown')
        resolution_time = incident_data.get('resolution_time_minutes', 'Unknown')
        
        if status == 'resolved':
            return f"Incident resolved via {resolution_method} in {resolution_time} minutes"
        elif status == 'escalated':
            escalation_reason = incident_data.get('escalation_reason', 'Unknown reason')
            return f"Incident escalated to human intervention. Reason: {escalation_reason}"
        else:
            return f"Incident status: {status}"