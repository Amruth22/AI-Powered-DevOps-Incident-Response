#!/usr/bin/env python3
"""
Remediation Agent
AI-powered auto-remediation with safety protocols
"""

import asyncio
import time
import random
from typing import Dict, Any, List
from .base_agent import BaseIncidentAgent
from services.gemini.client import get_remediation_llm

class RemediationAgent(BaseIncidentAgent):
    """AI-powered auto-remediation with safety protocols"""
    
    def __init__(self):
        super().__init__(
            role="Senior Auto-Remediation Engineer",
            goal="Plan safe remediation with AI safety analysis",
            backstory="Expert remediation engineer with AI safety protocols and automated resolution capabilities",
            llm=get_remediation_llm()
        )
    
    def _get_agent_name(self) -> str:
        return "remediation"
    
    async def analyze_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Plan safe auto-remediation"""
        
        # Combine all previous analyses if available
        combined_analysis = self._combine_analyses(incident_data)
        
        # AI Analysis
        prompt = f"""
        AUTO-REMEDIATION PLANNING - {incident_data.get('incident_id', 'unknown')}
        
        INCIDENT SUMMARY:
        - Service: {incident_data.get('service', 'unknown')}
        - Type: {incident_data.get('type', 'unknown')}
        - Severity: {incident_data.get('severity', 'unknown')}
        - Overall Confidence: {incident_data.get('overall_confidence', 0.0):.2f}
        
        COMBINED AGENT ANALYSES:
        {combined_analysis}
        
        SAFETY REQUIREMENTS:
        - Only recommend actions with >80% success rate
        - All actions must be reversible
        - Provide detailed rollback procedures
        - Never risk production stability
        - Conservative approach for P0/P1 incidents
        
        As a senior auto-remediation engineer, provide:
        1. REMEDIATION CONFIDENCE (0.0-1.0): Confidence in auto-remediation
        2. RECOMMENDED ACTIONS: Step-by-step remediation plan
        3. SAFETY ASSESSMENT: Risk level of each action (LOW/MEDIUM/HIGH)
        4. ROLLBACK PLAN: Detailed rollback procedures
        5. SUCCESS PROBABILITY: Estimated success rate
        6. EXECUTION TIME: Expected time to complete
        7. MONITORING PLAN: How to verify success
        
        Be conservative - if unsure, recommend human intervention.
        """
        
        # Run AI analysis in executor to avoid blocking
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, self.llm._call, prompt)
        
        # Extract remediation confidence
        remediation_confidence = self._extract_remediation_confidence(analysis)
        
        return {
            "analysis": analysis,
            "remediation_confidence": remediation_confidence
        }
    
    def _combine_analyses(self, incident_data: Dict[str, Any]) -> str:
        """Combine all previous agent analyses"""
        combined = []
        
        # Get agent analyses from incident data
        agent_analyses = incident_data.get("agent_analyses", {})
        
        for agent_name, analysis in agent_analyses.items():
            if isinstance(analysis, dict) and "analysis" in analysis:
                combined.append(f"\n{agent_name.upper()} ANALYSIS:\n{analysis['analysis'][:300]}...")
        
        return "\n".join(combined) if combined else "No previous analyses available"
    
    async def execute_remediation(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute remediation actions (simulated)"""
        incident_type = incident_data.get('type', 'unknown')
        
        self.logger.info(f"Executing remediation for {incident_type}...")
        
        # Simulate different success rates based on incident type
        success_rates = {
            "database_timeout": 0.85,
            "memory_leak": 0.80,
            "service_crash": 0.90,
            "high_cpu": 0.75,
            "network_issue": 0.70,
            "disk_full": 0.85
        }
        
        success_rate = success_rates.get(incident_type, 0.80)
        
        # Simulate execution time
        execution_time = random.uniform(1.0, 3.0)
        await asyncio.sleep(execution_time)
        
        # Determine success
        success = random.random() < success_rate
        
        if success:
            self.logger.info(f"SUCCESS: Remediation successful for {incident_type}")
            return {
                "success": True,
                "execution_time": execution_time,
                "actions_taken": self._get_remediation_actions(incident_type),
                "verification": "System health checks passed"
            }
        else:
            self.logger.warning(f"ERROR: Remediation failed for {incident_type}")
            return {
                "success": False,
                "execution_time": execution_time,
                "failure_reason": "Remediation actions did not resolve the issue",
                "rollback_performed": True
            }
    
    def _get_remediation_actions(self, incident_type: str) -> List[str]:
        """Get remediation actions based on incident type"""
        actions_map = {
            "database_timeout": [
                "Increased database connection pool size",
                "Optimized slow queries",
                "Restarted database connection manager"
            ],
            "memory_leak": [
                "Restarted affected service instances",
                "Increased memory limits",
                "Enabled garbage collection optimization"
            ],
            "service_crash": [
                "Restarted crashed service",
                "Updated health check configuration",
                "Scaled service replicas"
            ],
            "high_cpu": [
                "Scaled service horizontally",
                "Optimized CPU-intensive processes",
                "Load balanced traffic distribution"
            ],
            "network_issue": [
                "Restarted network components",
                "Updated routing configuration",
                "Failover to backup network path"
            ],
            "disk_full": [
                "Cleaned up temporary files",
                "Increased disk space allocation",
                "Archived old log files"
            ]
        }
        
        return actions_map.get(incident_type, ["Generic remediation actions performed"])