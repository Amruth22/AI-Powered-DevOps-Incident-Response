#!/usr/bin/env python3
"""
Historical Agent
AI-powered historical analysis with pattern matching
"""

import asyncio
from typing import Dict, Any
from .base_agent import BaseIncidentAgent
from services.gemini.client import get_historical_llm
from services.mock.client import get_historical_incident_data

class HistoricalAgent(BaseIncidentAgent):
    """AI-powered historical analysis with pattern matching"""
    
    def __init__(self):
        super().__init__(
            role="Senior Historical Analysis Specialist",
            goal="Find similar incidents with AI pattern matching",
            backstory="Expert historical analyst with AI pattern recognition and access to comprehensive incident databases",
            llm=get_historical_llm()
        )
    
    def _get_agent_name(self) -> str:
        return "historical"
    
    async def analyze_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze historical patterns and recommend solutions"""
        
        # Gather historical data
        historical_data = await self._gather_historical_data_async(incident_data)
        
        # AI Analysis
        prompt = f"""
        HISTORICAL PATTERN ANALYSIS - {incident_data.get('incident_id', 'unknown')}
        
        CURRENT INCIDENT:
        - Service: {incident_data.get('service', 'unknown')}
        - Type: {incident_data.get('type', 'unknown')}
        - Severity: {incident_data.get('severity', 'unknown')}
        - Symptoms: {self._safe_join_symptoms(incident_data.get('symptoms', []))}
        
        HISTORICAL DATA:
        {self._format_historical_data(historical_data)}
        
        As a senior historical analysis specialist, provide:
        1. PATTERN MATCH CONFIDENCE (0.0-1.0): How similar are historical incidents?
        2. SIMILAR INCIDENTS: List of most relevant past incidents
        3. SOLUTION SUCCESS RATES: Historical success rates for each solution
        4. RECOMMENDED SOLUTION: Best solution based on history
        5. RISK ASSESSMENT: Risks of recommended solutions
        6. TIME TO RESOLUTION: Expected resolution time
        7. LESSONS LEARNED: Key insights from past incidents
        
        Focus on actionable recommendations with success probabilities.
        """
        
        # Run AI analysis in executor to avoid blocking
        loop = asyncio.get_event_loop()
        analysis = await loop.run_in_executor(None, self.llm._call, prompt)
        
        # Extract pattern confidence
        pattern_confidence = self._extract_pattern_confidence(analysis)
        
        return {
            "analysis": analysis,
            "pattern_confidence": pattern_confidence,
            "historical_data": historical_data
        }
    
    def _safe_join_symptoms(self, symptoms) -> str:
        """Safely join symptoms list, handling various data types"""
        try:
            if not symptoms:
                return "No symptoms provided"
            
            # Handle list of strings
            if isinstance(symptoms, list):
                return ', '.join(str(symptom) for symptom in symptoms if symptom)
            
            # Handle single string
            if isinstance(symptoms, str):
                return symptoms
            
            # Handle other types
            return str(symptoms)
            
        except Exception:
            return "Unable to process symptoms"
    
    async def _gather_historical_data_async(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gather historical incident data asynchronously"""
        try:
            # Safely extract incident type and service
            incident_type = incident_data.get('type', 'unknown')
            service = incident_data.get('service', 'unknown')
            
            # Ensure we have string values (handle dict or other types)
            if isinstance(incident_type, dict):
                incident_type = incident_type.get('name', 'unknown')
            incident_type = str(incident_type) if incident_type else 'unknown'
            
            if isinstance(service, dict):
                service = service.get('name', 'unknown')
            service = str(service) if service else 'unknown'
            
            # Run API calls in executor to avoid blocking
            loop = asyncio.get_event_loop()
            historical_data = await loop.run_in_executor(
                None, get_historical_incident_data, incident_type, service
            )
            
            return historical_data if historical_data else {}
            
        except Exception as e:
            self.logger.error(f"Error gathering historical data: {e}")
            # Return empty data structure to prevent workflow failure
            return {
                "error": f"Failed to gather historical data: {str(e)}",
                "similar_incidents": {"similar_incidents": []},
                "pagerduty_history": {"incidents": []}
            }
    
    def _format_historical_data(self, data: Dict[str, Any]) -> str:
        """Format historical data for AI analysis - Fixed version"""
        try:
            formatted = []
            
            # Handle error case first
            if "error" in data:
                formatted.append(f"HISTORICAL DATA ERROR: {data['error']}")
                return "\n".join(formatted)
            
            # Format similar incidents - with safe data handling
            if "similar_incidents" in data:
                similar = data["similar_incidents"]
                
                # Handle different data structures safely
                if isinstance(similar, dict) and "error" not in similar:
                    incidents = similar.get('similar_incidents', [])
                    
                    formatted.append(f"SIMILAR INCIDENTS:")
                    if incidents and isinstance(incidents, list):
                        formatted.append(f"- Found {len(incidents)} similar incidents")
                        for i, incident in enumerate(incidents[:3]):
                            try:
                                if isinstance(incident, dict):
                                    summary = str(incident.get('summary', f'Incident {i+1}'))
                                    resolution = str(incident.get('resolution', 'Unknown'))
                                    success_rate = str(incident.get('success_rate', 'Unknown'))
                                    
                                    formatted.append(f"  • {summary}")
                                    formatted.append(f"    Resolution: {resolution}")
                                    formatted.append(f"    Success: {success_rate}")
                                else:
                                    formatted.append(f"  • {str(incident)}")
                            except Exception as e:
                                formatted.append(f"  • Error processing incident: {str(e)}")
                    else:
                        formatted.append("- No similar incidents found")
                else:
                    formatted.append("SIMILAR INCIDENTS: Data unavailable")
            
            # Format PagerDuty history - with safe data handling
            if "pagerduty_history" in data:
                pagerduty = data["pagerduty_history"]
                
                if isinstance(pagerduty, dict) and "error" not in pagerduty:
                    incidents = pagerduty.get('incidents', [])
                    
                    formatted.append(f"PAGERDUTY HISTORY:")
                    if incidents and isinstance(incidents, list):
                        formatted.append(f"- Historical incidents: {len(incidents)}")
                        
                        # Group by service - with safe processing
                        service_incidents = {}
                        for incident in incidents:
                            try:
                                if isinstance(incident, dict):
                                    service_name = str(incident.get('service', 'Unknown'))
                                    # Use string as key to avoid unhashable type error
                                    if service_name not in service_incidents:
                                        service_incidents[service_name] = 0
                                    service_incidents[service_name] += 1
                            except Exception:
                                # Skip problematic incidents silently
                                continue
                        
                        if service_incidents:
                            formatted.append("- By service:")
                            # Convert to list safely to avoid iteration issues
                            try:
                                service_items = list(service_incidents.items())[:3]
                                for service_name, count in service_items:
                                    formatted.append(f"  • {service_name}: {count} incidents")
                            except Exception:
                                formatted.append("  • Error processing service breakdown")
                    else:
                        formatted.append("- No historical incidents found")
                else:
                    formatted.append("PAGERDUTY HISTORY: Data unavailable")
            
            return "\n".join(formatted) if formatted else "No historical data available"
            
        except Exception as e:
            self.logger.error(f"Error formatting historical data: {e}")
            return f"Error formatting historical data: {str(e)}"