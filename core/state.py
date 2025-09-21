#!/usr/bin/env python3
"""
State Management Functions
Handles incident state creation and updates for the workflow
"""

from datetime import datetime
from typing import Dict, Any, List
import uuid

def create_incident_state(incident_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create initial incident state for workflow processing"""
    
    # Generate incident ID if not provided
    incident_id = incident_data.get("incident_id")
    if not incident_id:
        timestamp = datetime.now().strftime("%Y%m%d")
        random_id = str(uuid.uuid4())[:8].upper()
        incident_id = f"INC-{timestamp}-{random_id}"
    
    # Create initial state
    state = {
        # Core incident information
        "incident_id": incident_id,
        "affected_service": incident_data.get("service", "unknown"),
        "incident_type": incident_data.get("type", "unknown"),
        "description": incident_data.get("description", "Unknown incident"),
        "symptoms": incident_data.get("symptoms", []),
        "severity": incident_data.get("severity", "P3"),
        "metrics": incident_data.get("metrics", {}),
        
        # Timestamps
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        
        # Agent results (will be populated by agents)
        "agent_analyses": {},
        "overall_confidence": 0.0,
        "remediation_plan": {},
        
        # Workflow state
        "status": "active",
        "stage": "initialized",
        "workflow_complete": False,
        
        # Resolution tracking
        "resolved_at": None,
        "resolution_method": None,
        "resolution_time_minutes": None,
        
        # Error tracking
        "errors": [],
        "retry_count": 0
    }
    
    return state

def update_incident_state(state: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update incident state with new information"""
    
    # Update timestamp
    updates["updated_at"] = datetime.now().isoformat()
    
    # Merge updates into state
    state.update(updates)
    
    return state

def add_agent_result(state: Dict[str, Any], agent_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
    """Add agent analysis result to state"""
    
    if "agent_analyses" not in state:
        state["agent_analyses"] = {}
    
    # Add timestamp to result
    result["timestamp"] = datetime.now().isoformat()
    result["agent"] = agent_name
    
    # Store result
    state["agent_analyses"][agent_name] = result
    
    # Update overall state
    state["updated_at"] = datetime.now().isoformat()
    
    return state

def calculate_overall_confidence(state: Dict[str, Any]) -> float:
    """Calculate overall confidence from agent results"""
    
    agent_analyses = state.get("agent_analyses", {})
    
    if not agent_analyses:
        return 0.0
    
    # Extract confidence scores from different agents
    detective_confidence = agent_analyses.get("detective", {}).get("confidence", 0.0)
    diagnostics_health = agent_analyses.get("diagnostics", {}).get("health_score", 0.0)
    historical_pattern = agent_analyses.get("historical", {}).get("pattern_confidence", 0.0)
    
    # Calculate weighted average
    confidences = []
    if detective_confidence > 0:
        confidences.append(detective_confidence)
    if diagnostics_health > 0:
        confidences.append(diagnostics_health)
    if historical_pattern > 0:
        confidences.append(historical_pattern)
    
    if not confidences:
        return 0.0
    
    overall_confidence = sum(confidences) / len(confidences)
    
    # Update state
    state["overall_confidence"] = overall_confidence
    
    return overall_confidence

def mark_incident_resolved(state: Dict[str, Any], resolution_method: str) -> Dict[str, Any]:
    """Mark incident as resolved"""
    
    now = datetime.now()
    created_at = datetime.fromisoformat(state["created_at"])
    resolution_time = int((now - created_at).total_seconds() / 60)
    
    updates = {
        "status": "resolved",
        "stage": "resolved",
        "resolved_at": now.isoformat(),
        "resolution_method": resolution_method,
        "resolution_time_minutes": resolution_time,
        "workflow_complete": True
    }
    
    return update_incident_state(state, updates)

def mark_incident_escalated(state: Dict[str, Any], escalation_reason: str) -> Dict[str, Any]:
    """Mark incident as escalated to human"""
    
    updates = {
        "status": "escalated",
        "stage": "escalated",
        "escalation_reason": escalation_reason,
        "workflow_complete": True
    }
    
    return update_incident_state(state, updates)

def add_error(state: Dict[str, Any], error_message: str, agent_name: str = None) -> Dict[str, Any]:
    """Add error to incident state"""
    
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "message": error_message,
        "agent": agent_name
    }
    
    if "errors" not in state:
        state["errors"] = []
    
    state["errors"].append(error_entry)
    state["updated_at"] = datetime.now().isoformat()
    
    return state