#!/usr/bin/env python3
"""
Parallel Multi-Agent Incident Response Workflow
Orchestrates parallel execution of analysis agents for faster incident processing
"""

import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum

from agents.detective_agent import DetectiveAgent
from agents.diagnostics_agent import DiagnosticsAgent
from agents.historical_agent import HistoricalAgent
from agents.remediation_agent import RemediationAgent
from agents.communication_agent import CommunicationAgent
from agents.postmortem_agent import PostMortemAgent
from core.config import config
from core.state import (
    create_incident_state, add_agent_result, calculate_overall_confidence,
    mark_incident_resolved, mark_incident_escalated
)

logger = logging.getLogger(__name__)

class IncidentStatus(Enum):
    ACTIVE = "active"
    INVESTIGATING = "investigating"
    MITIGATING = "mitigating"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    ERROR = "error"

class ParallelIncidentWorkflow:
    """Parallel multi-agent incident response workflow"""
    
    def __init__(self):
        # Initialize all agents
        self.agents = {
            "detective": DetectiveAgent(),
            "diagnostics": DiagnosticsAgent(),
            "historical": HistoricalAgent(),
            "remediation": RemediationAgent(),
            "communication": CommunicationAgent(),
            "postmortem": PostMortemAgent()
        }
        
        self.metrics = {
            "total_incidents_handled": 0,
            "auto_remediated_count": 0,
            "escalated_count": 0,
            "success_rate": 0.0,
            "avg_workflow_time": 0.0
        }
        
        logger.info("Parallel Incident Workflow initialized with 6 agents")
    
    async def process_incident(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incident using parallel multi-agent workflow"""
        incident_id = incident_data.get("incident_id", "unknown")
        
        logger.info(f"PARALLEL PROCESSING: {incident_id}")
        logger.info(f"   Type: {incident_data.get('type', 'unknown')}")
        logger.info(f"   Service: {incident_data.get('service', 'unknown')}")
        logger.info(f"   Severity: {incident_data.get('severity', 'unknown')}")
        
        workflow_start = time.time()
        
        # Create incident state
        state = create_incident_state(incident_data)
        
        try:
            # Phase 1: PARALLEL ANALYSIS - Run Detective, Diagnostics, Historical concurrently
            logger.info(f"PHASE 1: PARALLEL ANALYSIS (Detective + Diagnostics + Historical)")
            
            parallel_start = time.time()
            
            # Execute all 3 analysis agents in parallel using asyncio.gather
            # Use return_exceptions=True to handle individual agent failures gracefully
            results = await asyncio.gather(
                self.agents["detective"].execute_async(state),
                self.agents["diagnostics"].execute_async(state),
                self.agents["historical"].execute_async(state),
                return_exceptions=True
            )
            
            # Process results and handle any exceptions
            detective_result = results[0] if not isinstance(results[0], Exception) else {
                "agent": "detective", "error": str(results[0]), "success": False, "confidence": 0.5
            }
            diagnostics_result = results[1] if not isinstance(results[1], Exception) else {
                "agent": "diagnostics", "error": str(results[1]), "success": False, "health_score": 0.5
            }
            historical_result = results[2] if not isinstance(results[2], Exception) else {
                "agent": "historical", "error": str(results[2]), "success": False, "pattern_confidence": 0.5
            }
            
            parallel_time = time.time() - parallel_start
            
            # Add results to state
            add_agent_result(state, "detective", detective_result)
            add_agent_result(state, "diagnostics", diagnostics_result)
            add_agent_result(state, "historical", historical_result)
            
            logger.info(f"   PARALLEL EXECUTION COMPLETE in {parallel_time:.2f}s")
            logger.info(f"   Detective: {detective_result.get('confidence', 0):.2f} confidence")
            logger.info(f"   Diagnostics: {diagnostics_result.get('health_score', 0):.2f} health score")
            logger.info(f"   Historical: {historical_result.get('pattern_confidence', 0):.2f} pattern confidence")
            
            # Log any agent errors
            for result in [detective_result, diagnostics_result, historical_result]:
                if not result.get('success', True):
                    logger.warning(f"   WARNING: {result.get('agent', 'Unknown')} agent had errors: {result.get('error', 'Unknown error')}")
            
            # Calculate overall confidence
            overall_confidence = calculate_overall_confidence(state)
            logger.info(f"OVERALL CONFIDENCE: {overall_confidence:.2f}")
            
            # Phase 2: REMEDIATION PLANNING
            logger.info(f"PHASE 2: REMEDIATION PLANNING")
            
            try:
                remediation_result = await self.agents["remediation"].execute_async(state)
            except Exception as e:
                logger.error(f"Remediation agent error: {e}")
                remediation_result = {
                    "agent": "remediation", "error": str(e), "success": False, "remediation_confidence": 0.3
                }
            
            add_agent_result(state, "remediation", remediation_result)
            
            logger.info(f"   Remediation: {remediation_result.get('remediation_confidence', 0):.2f} remediation confidence")
            
            # Phase 3: COMMUNICATION PLANNING
            logger.info(f"PHASE 3: COMMUNICATION PLANNING")
            
            try:
                communication_result = await self.agents["communication"].execute_async(state)
            except Exception as e:
                logger.error(f"Communication agent error: {e}")
                communication_result = {
                    "agent": "communication", "error": str(e), "success": False, "communication_confidence": 0.5
                }
            
            add_agent_result(state, "communication", communication_result)
            
            logger.info(f"   Communication: {communication_result.get('communication_confidence', 0):.2f} communication confidence")
            
            # Phase 4: EXECUTION DECISION
            logger.info(f"PHASE 4: EXECUTION DECISION")
            
            should_auto_remediate = self._should_auto_remediate(
                overall_confidence,
                remediation_result.get('remediation_confidence', 0),
                state.get('severity', 'P3')
            )
            
            if should_auto_remediate:
                logger.info(f"   PARALLEL AUTO-REMEDIATION APPROVED")
                
                # Execute remediation
                try:
                    remediation_execution = await self.agents["remediation"].execute_remediation(state)
                except Exception as e:
                    logger.error(f"Remediation execution error: {e}")
                    remediation_execution = {"success": False, "error": str(e)}
                
                if remediation_execution.get('success', False):
                    self.metrics["auto_remediated_count"] += 1
                    logger.info(f"   PARALLEL AUTO-REMEDIATION SUCCESSFUL!")
                    
                    # Mark as resolved
                    mark_incident_resolved(state, "parallel_auto_remediation")
                    
                    # Phase 5: Post-Mortem Analysis (for successful resolutions)
                    logger.info(f"PHASE 5: POST-MORTEM ANALYSIS")
                    
                    try:
                        postmortem_result = await self.agents["postmortem"].execute_async(state)
                    except Exception as e:
                        logger.error(f"Post-mortem agent error: {e}")
                        postmortem_result = {
                            "agent": "postmortem", "error": str(e), "success": False, "documentation_confidence": 0.5
                        }
                    
                    add_agent_result(state, "postmortem", postmortem_result)
                    
                    logger.info(f"   Post-Mortem: {postmortem_result.get('documentation_confidence', 0):.2f} documentation confidence")
                    
                    workflow_time = time.time() - workflow_start
                    
                    result = {
                        "incident_id": incident_id,
                        "status": "resolved",
                        "method": "parallel_auto_remediation",
                        "success": True,
                        "overall_confidence": overall_confidence,
                        "workflow_time_seconds": workflow_time,
                        "parallel_time_seconds": parallel_time,
                        "agent_results": state.get("agent_analyses", {}),
                        "total_agents_used": len(state.get("agent_analyses", {}))
                    }
                else:
                    self.metrics["escalated_count"] += 1
                    logger.info(f"   REMEDIATION FAILED - ESCALATING")
                    
                    # Mark as escalated
                    mark_incident_escalated(state, "Remediation execution failed")
                    
                    workflow_time = time.time() - workflow_start
                    
                    result = {
                        "incident_id": incident_id,
                        "status": "escalated",
                        "method": "failed_remediation",
                        "success": False,
                        "overall_confidence": overall_confidence,
                        "workflow_time_seconds": workflow_time,
                        "parallel_time_seconds": parallel_time,
                        "agent_results": state.get("agent_analyses", {})
                    }
            else:
                logger.info(f"   PARALLEL ESCALATING TO HUMAN")
                logger.info(f"      • Overall confidence: {overall_confidence:.2f}")
                logger.info(f"      • Remediation confidence: {remediation_result.get('remediation_confidence', 0):.2f}")
                
                self.metrics["escalated_count"] += 1
                
                # Determine escalation reason
                escalation_reason = self._get_escalation_reason(
                    overall_confidence,
                    remediation_result.get('remediation_confidence', 0),
                    state.get('severity', 'P3')
                )
                
                # Mark as escalated
                mark_incident_escalated(state, escalation_reason)
                
                workflow_time = time.time() - workflow_start
                
                result = {
                    "incident_id": incident_id,
                    "status": "escalated",
                    "method": "parallel_escalation",
                    "success": False,
                    "reason": escalation_reason,
                    "overall_confidence": overall_confidence,
                    "workflow_time_seconds": workflow_time,
                    "parallel_time_seconds": parallel_time,
                    "agent_results": state.get("agent_analyses", {})
                }
            
            # Update metrics
            self._update_metrics(workflow_time)
            
            return result
            
        except Exception as e:
            logger.error(f"   ERROR: PARALLEL WORKFLOW ERROR: {e}")
            workflow_time = time.time() - workflow_start
            return {
                "incident_id": incident_id,
                "status": "error",
                "success": False,
                "error": str(e),
                "workflow_time_seconds": workflow_time
            }
    
    def _should_auto_remediate(self, overall_confidence: float, remediation_confidence: float, severity: str) -> bool:
        """Determine if incident should be auto-remediated"""
        return (
            overall_confidence >= config.auto_remediation_confidence_threshold and
            remediation_confidence >= 0.7 and
            severity != 'P0'  # Never auto-remediate P0 incidents
        )
    
    def _get_escalation_reason(self, overall_confidence: float, remediation_confidence: float, severity: str) -> str:
        """Get reason for escalation"""
        if severity == 'P0':
            return "P0 severity - requires human oversight"
        elif overall_confidence < config.auto_remediation_confidence_threshold:
            return f"Low overall confidence ({overall_confidence:.2f})"
        elif remediation_confidence < 0.7:
            return f"Low remediation confidence ({remediation_confidence:.2f})"
        else:
            return "Unknown escalation reason"
    
    def _update_metrics(self, workflow_time: float):
        """Update workflow metrics"""
        self.metrics["total_incidents_handled"] += 1
        
        if self.metrics["total_incidents_handled"] > 0:
            self.metrics["success_rate"] = (
                self.metrics["auto_remediated_count"] / self.metrics["total_incidents_handled"]
            ) * 100
            
            # Update average workflow time
            current_avg = self.metrics["avg_workflow_time"]
            total_incidents = self.metrics["total_incidents_handled"]
            self.metrics["avg_workflow_time"] = (
                (current_avg * (total_incidents - 1) + workflow_time) / total_incidents
            )

# Global workflow instance
parallel_workflow = ParallelIncidentWorkflow()

async def process_incident_parallel(incident_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process an incident through the parallel workflow"""
    return await parallel_workflow.process_incident(incident_data)