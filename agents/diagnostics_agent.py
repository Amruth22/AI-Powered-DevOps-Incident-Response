#!/usr/bin/env python3
"""
Diagnostics Agent
AI-powered system diagnostics with infrastructure analysis
"""

import asyncio
from typing import Dict, Any
from .base_agent import BaseIncidentAgent
from services.gemini.client import get_diagnostics_llm
from services.mock.client import get_system_health_data

class DiagnosticsAgent(BaseIncidentAgent):
    """AI-powered system diagnostics with infrastructure analysis"""
    
    def __init__(self):
        super().__init__(
            role="Senior System Diagnostics Engineer",
            goal="Assess system health with AI-powered diagnostics",
            backstory="Expert system diagnostics engineer with AI analysis capabilities and deep infrastructure knowledge",
            llm=get_diagnostics_llm()
        )
    
    def _get_agent_name(self) -> str:
        return "diagnostics"
    
    async def analyze_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete system health diagnosis"""
        
        # Gather system data
        system_data = await self._gather_system_data_async(incident_data)
        
        # AI Analysis
        prompt = f"""
        SYSTEM DIAGNOSTICS - {incident_data.get('incident_id', 'unknown')}
        
        INCIDENT CONTEXT:
        - Service: {incident_data.get('service', 'unknown')}
        - Type: {incident_data.get('type', 'unknown')}
        - Current Status: {incident_data.get('status', 'active')}
        
        SYSTEM DATA COLLECTED:
        {self._format_system_data(system_data)}
        
        As a senior system diagnostics engineer, provide:
        1. SYSTEM HEALTH SCORE (0.0-1.0): Overall system health
        2. RESOURCE ANALYSIS: CPU, memory, disk, network status
        3. COMPONENT HEALTH: Status of all system components
        4. BOTTLENECK IDENTIFICATION: Where are the constraints?
        5. STABILITY ASSESSMENT: How stable is the system?
        6. INFRASTRUCTURE vs APPLICATION: Root cause location
        7. SCALING RECOMMENDATIONS: Should we scale resources?
        
        Provide specific technical recommendations.
        """
        
        # Run AI analysis in executor to avoid blocking
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, self.llm._call, prompt)
        
        # Extract health score
        health_score = self._extract_health_score(analysis)
        
        return {
            "analysis": analysis,
            "health_score": health_score,
            "system_data": system_data
        }
    
    async def _gather_system_data_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gather system health data asynchronously"""
        service = incident_data.get('service', 'unknown')
        
        # Run API calls in executor to avoid blocking
        loop = asyncio.get_event_loop()
        system_data = await loop.run_in_executor(
            None, get_system_health_data, service
        )
        
        return system_data
    
    def _format_system_data(self, data: Dict[str, Any]) -> str:
        """Format system data for AI analysis"""
        formatted = []
        
        # Format Kubernetes data
        if "kubernetes" in data and "error" not in data["kubernetes"]:
            k8s = data["kubernetes"]
            formatted.append(f"KUBERNETES STATUS:")
            
            pods = k8s.get('pods', [])
            if pods:
                running_pods = len([p for p in pods if p.get('status') == 'Running'])
                total_pods = len(pods)
                formatted.append(f"- Pods: {running_pods}/{total_pods} running")
                
                # Add problematic pods
                problem_pods = [p for p in pods if p.get('status') != 'Running']
                if problem_pods:
                    formatted.append("- Problem pods:")
                    for pod in problem_pods[:3]:
                        formatted.append(f"  • {pod.get('name', 'Unknown')}: {pod.get('status', 'Unknown')}")
        
        # Format alerts data
        if "alerts" in data and "error" not in data["alerts"]:
            alerts = data["alerts"]
            formatted.append(f"PROMETHEUS ALERTS:")
            
            active_alerts = alerts.get('alerts', [])
            if active_alerts:
                formatted.append(f"- Active alerts: {len(active_alerts)}")
                for alert in active_alerts[:3]:
                    formatted.append(f"  • {alert.get('alertname', 'Unknown')}: {alert.get('severity', 'Unknown')}")
            else:
                formatted.append("- No active alerts")
        
        return "\n".join(formatted) if formatted else "No system data available"