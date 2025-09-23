#!/usr/bin/env python3
"""
Mock API Client Service
Handles communication with mock DevOps APIs for testing and development
"""

import requests
import logging
from typing import Dict, List, Any, Optional
from core.config import config

logger = logging.getLogger(__name__)

class MockAPIClient:
    """Client for interacting with mock DevOps APIs"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.mock_api_base_url
        self.timeout = 10
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        """Make request to mock API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, params=data, timeout=self.timeout)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Mock API request failed: {e}")
            return {"error": str(e), "success": False}
    
    # ============================================================================
    # INCIDENT GENERATION
    # ============================================================================
    
    def generate_incident(self, scenario_type: str = None, ai_test_mode: str = None) -> Dict[str, Any]:
        """Generate a test incident with AI optimization"""
        data = {}
        if scenario_type:
            data["scenario_type"] = scenario_type
        if ai_test_mode:
            data["ai_test_mode"] = ai_test_mode
        return self._make_request("/chaos/generate-incident", method="POST", data=data)
    
    def get_active_incidents(self) -> List[Dict[str, Any]]:
        """Get active incidents from chaos engineering with AI analysis"""
        try:
            result = self._make_request("/chaos/active-incidents")
            if "error" not in result:
                return result.get("active_incidents", [])
            else:
                return []
        except Exception as e:
            logger.error(f"❌ Error getting incidents: {e}")
            return []
    
    # ============================================================================
    # LOG ANALYSIS
    # ============================================================================
    
    def search_logs(self, query: str = "*", size: int = 10, severity: str = None) -> Dict[str, Any]:
        """Search logs using Elasticsearch mock"""
        params = {"q": query, "size": size}
        if severity:
            params["severity"] = severity
        return self._make_request("/elasticsearch/search", data=params)
    
    def get_service_logs(self, service_name: str, hours: int = 1) -> Dict[str, Any]:
        """Get logs for specific service"""
        return self._make_request(f"/elasticsearch/logs/{service_name}", data={"hours": hours})
    
    # ============================================================================
    # SYSTEM DIAGNOSTICS
    # ============================================================================
    
    def get_pods(self, namespace: str = "default") -> Dict[str, Any]:
        """Get Kubernetes pod status"""
        return self._make_request("/kubernetes/pods", data={"namespace": namespace})
    
    def get_pod_logs(self, pod_name: str, lines: int = 100) -> Dict[str, Any]:
        """Get logs for specific pod"""
        return self._make_request(f"/kubernetes/pods/{pod_name}/logs", data={"lines": lines})
    
    def get_prometheus_alerts(self, state: str = "active") -> Dict[str, Any]:
        """Get Prometheus alerts"""
        return self._make_request("/prometheus/alerts", data={"state": state})
    
    def get_service_metrics(self, service_name: str, duration: str = "1h") -> Dict[str, Any]:
        """Get metrics for specific service"""
        return self._make_request(f"/prometheus/metrics/{service_name}", data={"duration": duration})
    
    # ============================================================================
    # HISTORICAL ANALYSIS
    # ============================================================================
    
    def find_similar_incidents(self, error_type: str, service: str = None) -> Dict[str, Any]:
        """Find similar incidents from Jira"""
        data = {"error_type": error_type}
        if service:
            data["service"] = service
        return self._make_request("/jira/incidents/similar", data=data)
    
    def get_pagerduty_incidents(self, status: str = "open") -> Dict[str, Any]:
        """Get PagerDuty incident history"""
        return self._make_request("/pagerduty/incidents", data={"status": status})
    
    # ============================================================================
    # COMMUNICATION
    # ============================================================================
    
    def send_slack_notification(self, channel: str, message: str, severity: str = "info") -> Dict[str, Any]:
        """Send Slack notification"""
        data = {
            "channel": channel,
            "message": message,
            "severity": severity
        }
        return self._make_request("/slack/notify", method="POST", data=data)
    
    def create_incident_channel(self, incident_id: str) -> Dict[str, Any]:
        """Create incident-specific Slack channel"""
        data = {"incident_id": incident_id}
        return self._make_request("/slack/create-incident-channel", method="POST", data=data)

    def resolve_incident(self, incident_id: str, resolution_method: str = "auto", ai_performance_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Resolve incident with AI performance tracking"""
        data = {
            "resolution_method": resolution_method
        }
        if ai_performance_data:
            data["ai_performance_data"] = ai_performance_data
        return self._make_request(f"/chaos/resolve-incident/{incident_id}", method="POST", data=data)
    
    def generate_multi_service_incident(self, ai_test_mode: str = None) -> Dict[str, Any]:
        """Generate complex multi-service incident"""
        data = {}
        if ai_test_mode:
            data["ai_test_mode"] = ai_test_mode
        return self._make_request("/chaos/generate-multi-service-incident", method="POST", data=data)

# Global client instance
mock_api_client = MockAPIClient()

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_investigation_data(service: str, incident_type: str) -> Dict[str, Any]:
    """Gather investigation data from multiple APIs"""
    data = {}
    
    # Get logs from Elasticsearch
    try:
        logs_result = mock_api_client.get_service_logs(service, hours=1)
        data["logs"] = logs_result
    except:
        data["logs"] = {"error": "Could not retrieve logs"}
    
    # Get metrics from Prometheus
    try:
        metrics_result = mock_api_client.get_service_metrics(service, duration="1h")
        data["metrics"] = metrics_result
    except:
        data["metrics"] = {"error": "Could not retrieve metrics"}
    
    return data

def get_system_health_data(service: str) -> Dict[str, Any]:
    """Gather system health data"""
    data = {}
    
    # Get Kubernetes pod status
    try:
        pods_result = mock_api_client.get_pods()
        data["kubernetes"] = pods_result
    except:
        data["kubernetes"] = {"error": "Could not retrieve pod data"}
    
    # Get Prometheus alerts
    try:
        alerts_result = mock_api_client.get_prometheus_alerts()
        data["alerts"] = alerts_result
    except:
        data["alerts"] = {"error": "Could not retrieve alerts"}
    
    return data

def get_historical_incident_data(incident_type: str, service: str) -> Dict[str, Any]:
    """Gather historical incident data"""
    data = {}
    
    # Get similar incidents from Jira
    try:
        similar_result = mock_api_client.find_similar_incidents(incident_type, service)
        data["similar_incidents"] = similar_result
    except:
        data["similar_incidents"] = {"error": "Could not retrieve similar incidents"}
    
    # Get PagerDuty incident history
    try:
        pagerduty_result = mock_api_client.get_pagerduty_incidents()
        data["pagerduty_history"] = pagerduty_result
    except:
        data["pagerduty_history"] = {"error": "Could not retrieve PagerDuty data"}
    
    return data