"""
Jira Mock API
AI-optimized historical incident analysis and pattern matching
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from faker import Faker

fake = Faker()

class JiraMock:
    """Mock Jira API for AI-powered historical incident analysis"""
    
    def __init__(self):
        self.services = ["user-service", "payment-service", "auth-service", "notification-service", "order-service"]
        self.incident_types = ["database_timeout", "memory_leak", "service_crash", "high_cpu", "network_issue", "disk_full"]
        self.severities = ["P0", "P1", "P2", "P3"]
        self.statuses = ["Open", "In Progress", "Resolved", "Closed", "Reopened"]
        self.resolution_methods = ["auto-remediation", "manual-fix", "service-restart", "configuration-change", "scaling"]
        
        # Generate historical incidents database
        self.historical_incidents = self._generate_historical_incidents(100)
    
    def get_incidents(self, status: str = "open", limit: int = 50) -> Dict[str, Any]:
        """Get incident tickets for AI historical analysis"""
        
        # Filter incidents by status
        if status.lower() == "open":
            filtered_incidents = [inc for inc in self.historical_incidents if inc["status"] in ["Open", "In Progress"]]
        elif status.lower() == "closed":
            filtered_incidents = [inc for inc in self.historical_incidents if inc["status"] in ["Resolved", "Closed"]]
        else:
            filtered_incidents = self.historical_incidents
        
        # Limit results
        incidents = random.sample(filtered_incidents, min(limit, len(filtered_incidents)))
        
        return {
            "total": len(filtered_incidents),
            "maxResults": limit,
            "startAt": 0,
            "issues": [
                {
                    "id": incident["id"],
                    "key": incident["key"],
                    "fields": {
                        "summary": incident["summary"],
                        "description": incident["description"],
                        "status": {"name": incident["status"]},
                        "priority": {"name": incident["severity"]},
                        "issuetype": {"name": "Incident"},
                        "created": incident["created"],
                        "updated": incident["updated"],
                        "resolved": incident.get("resolved"),
                        "assignee": {"displayName": incident["assignee"]},
                        "reporter": {"displayName": incident["reporter"]},
                        "labels": incident["labels"],
                        "components": [{"name": incident["service"]}],
                        "customfield_service": incident["service"],
                        "customfield_incident_type": incident["type"],
                        "customfield_resolution_time": incident.get("resolution_time_minutes"),
                        "customfield_customer_impact": incident.get("customer_impact"),
                        "customfield_root_cause": incident.get("root_cause")
                    },
                    "ai_metadata": {
                        "confidence_score": incident["ai_confidence"],
                        "pattern_similarity": incident["pattern_similarity"],
                        "resolution_success_rate": incident["resolution_success_rate"],
                        "automation_potential": incident["automation_potential"]
                    }
                } for incident in incidents
            ],
            "ai_analysis": {
                "total_incidents_analyzed": len(filtered_incidents),
                "pattern_distribution": self._analyze_pattern_distribution(filtered_incidents),
                "resolution_trends": self._analyze_resolution_trends(filtered_incidents),
                "service_impact_analysis": self._analyze_service_impact(filtered_incidents),
                "confidence": random.uniform(0.85, 0.95)
            }
        }
    
    def find_similar_incidents(self, error_type: str, service: str = None) -> Dict[str, Any]:
        """AI-powered similar incident matching"""
        
        # Find incidents with similar characteristics
        similar_incidents = []
        
        for incident in self.historical_incidents:
            similarity_score = self._calculate_similarity(incident, error_type, service)
            
            if similarity_score > 0.6:  # Threshold for similarity
                similar_incident = {
                    "incident_id": incident["key"],
                    "summary": incident["summary"],
                    "service": incident["service"],
                    "type": incident["type"],
                    "severity": incident["severity"],
                    "status": incident["status"],
                    "created": incident["created"],
                    "resolved": incident.get("resolved"),
                    "resolution_time_minutes": incident.get("resolution_time_minutes"),
                    "resolution_method": incident.get("resolution_method"),
                    "root_cause": incident.get("root_cause"),
                    "customer_impact": incident.get("customer_impact"),
                    "similarity_score": round(similarity_score, 3),
                    "confidence": incident["ai_confidence"],
                    "success_rate": incident["resolution_success_rate"],
                    "lessons_learned": incident.get("lessons_learned", []),
                    "prevention_measures": incident.get("prevention_measures", [])
                }
                similar_incidents.append(similar_incident)
        
        # Sort by similarity score (highest first)
        similar_incidents.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        # Limit to top 10 most similar
        similar_incidents = similar_incidents[:10]
        
        return {
            "query": {
                "error_type": error_type,
                "service": service,
                "search_timestamp": datetime.now().isoformat()
            },
            "total_matches": len(similar_incidents),
            "similar_incidents": similar_incidents,
            "ai_recommendations": {
                "best_match": similar_incidents[0] if similar_incidents else None,
                "recommended_solution": self._get_recommended_solution(similar_incidents),
                "success_probability": self._calculate_success_probability(similar_incidents),
                "estimated_resolution_time": self._estimate_resolution_time(similar_incidents),
                "risk_assessment": self._assess_resolution_risk(similar_incidents),
                "automation_feasibility": self._assess_automation_feasibility(similar_incidents)
            },
            "pattern_analysis": {
                "common_root_causes": self._extract_common_root_causes(similar_incidents),
                "resolution_patterns": self._extract_resolution_patterns(similar_incidents),
                "service_correlations": self._extract_service_correlations(similar_incidents),
                "time_patterns": self._extract_time_patterns(similar_incidents)
            },
            "confidence_metrics": {
                "pattern_match_confidence": random.uniform(0.75, 0.95),
                "solution_confidence": random.uniform(0.70, 0.90),
                "data_quality_score": random.uniform(0.80, 0.95)
            }
        }
    
    def create_incident(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create incident ticket (AI-generated)"""
        
        incident_key = f"INC-{random.randint(10000, 99999)}"
        
        new_incident = {
            "id": str(random.randint(100000, 999999)),
            "key": incident_key,
            "summary": incident_data.get("summary", "AI-Generated Incident"),
            "description": incident_data.get("description", "Incident detected by AI system"),
            "service": incident_data.get("service", "unknown-service"),
            "type": incident_data.get("type", "unknown"),
            "severity": incident_data.get("severity", "P3"),
            "status": "Open",
            "created": datetime.now().isoformat(),
            "assignee": "AI-System",
            "reporter": "AI-Agent",
            "labels": incident_data.get("labels", ["ai-generated", "auto-detected"]),
            "ai_confidence": incident_data.get("confidence", random.uniform(0.7, 0.9))
        }
        
        # Add to historical incidents for future matching
        self.historical_incidents.append(new_incident)
        
        return {
            "id": new_incident["id"],
            "key": incident_key,
            "self": f"https://company.atlassian.net/rest/api/2/issue/{incident_key}",
            "fields": {
                "summary": new_incident["summary"],
                "description": new_incident["description"],
                "status": {"name": "Open"},
                "priority": {"name": new_incident["severity"]},
                "created": new_incident["created"],
                "assignee": {"displayName": new_incident["assignee"]},
                "reporter": {"displayName": new_incident["reporter"]}
            },
            "ai_metadata": {
                "auto_generated": True,
                "confidence": new_incident["ai_confidence"],
                "detection_method": "ai_agent_analysis",
                "recommended_actions": self._get_incident_recommendations(new_incident)
            },
            "success": True,
            "message": f"Incident {incident_key} created successfully by AI system"
        }
    
    def _generate_historical_incidents(self, count: int) -> List[Dict[str, Any]]:
        """Generate historical incidents database"""
        incidents = []
        
        for i in range(count):
            incident_type = random.choice(self.incident_types)
            service = random.choice(self.services)
            severity = random.choices(self.severities, weights=[0.1, 0.3, 0.4, 0.2])[0]
            status = random.choices(self.statuses, weights=[0.1, 0.1, 0.6, 0.15, 0.05])[0]
            
            created_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            # Generate resolution data for resolved incidents
            resolution_data = {}
            if status in ["Resolved", "Closed"]:
                resolution_time = random.randint(15, 480)  # 15 minutes to 8 hours
                resolution_data = {
                    "resolved": (created_date + timedelta(minutes=resolution_time)).isoformat(),
                    "resolution_time_minutes": resolution_time,
                    "resolution_method": random.choice(self.resolution_methods),
                    "root_cause": self._generate_root_cause(incident_type),
                    "customer_impact": self._generate_customer_impact(severity),
                    "lessons_learned": self._generate_lessons_learned(incident_type),
                    "prevention_measures": self._generate_prevention_measures(incident_type)
                }
            
            incident = {
                "id": str(random.randint(100000, 999999)),
                "key": f"INC-{random.randint(10000, 99999)}",
                "summary": self._generate_incident_summary(incident_type, service),
                "description": self._generate_incident_description(incident_type, service),
                "service": service,
                "type": incident_type,
                "severity": severity,
                "status": status,
                "created": created_date.isoformat(),
                "updated": (created_date + timedelta(hours=random.randint(1, 48))).isoformat(),
                "assignee": fake.name(),
                "reporter": fake.name(),
                "labels": self._generate_labels(incident_type, service),
                "ai_confidence": random.uniform(0.7, 0.95),
                "pattern_similarity": random.uniform(0.6, 0.9),
                "resolution_success_rate": random.uniform(0.75, 0.95),
                "automation_potential": random.uniform(0.5, 0.9),
                **resolution_data
            }
            incidents.append(incident)
        
        return incidents
    
    def _calculate_similarity(self, incident: Dict[str, Any], error_type: str, service: str = None) -> float:
        """Calculate similarity score between incidents"""
        score = 0.0
        
        # Type similarity (40% weight)
        if incident["type"] == error_type:
            score += 0.4
        elif error_type in incident["type"] or incident["type"] in error_type:
            score += 0.2
        
        # Service similarity (30% weight)
        if service and incident["service"] == service:
            score += 0.3
        elif service and service in incident["service"]:
            score += 0.15
        elif not service:
            score += 0.1  # Partial credit if no service specified
        
        # Resolution success rate (20% weight)
        score += incident["resolution_success_rate"] * 0.2
        
        # Recency bonus (10% weight)
        days_ago = (datetime.now() - datetime.fromisoformat(incident["created"])).days
        recency_score = max(0, 1 - (days_ago / 365))  # Newer incidents get higher score
        score += recency_score * 0.1
        
        return min(score, 1.0)
    
    def _generate_incident_summary(self, incident_type: str, service: str) -> str:
        """Generate realistic incident summary"""
        templates = {
            "database_timeout": f"{service} experiencing database connection timeouts",
            "memory_leak": f"Memory leak detected in {service}",
            "service_crash": f"{service} container crashed unexpectedly",
            "high_cpu": f"High CPU usage in {service}",
            "network_issue": f"Network connectivity issues affecting {service}",
            "disk_full": f"Disk space exhaustion on {service} nodes"
        }
        return templates.get(incident_type, f"Issue with {service}")
    
    def _generate_incident_description(self, incident_type: str, service: str) -> str:
        """Generate detailed incident description"""
        descriptions = {
            "database_timeout": f"The {service} is experiencing database connection timeouts. Connection pool appears to be exhausted with queries taking longer than expected to complete.",
            "memory_leak": f"Memory usage in {service} has been steadily increasing over the past few hours. GC frequency has increased and OutOfMemoryError exceptions are being thrown.",
            "service_crash": f"The {service} container has crashed multiple times. Health checks are failing and the service is not responding to requests.",
            "high_cpu": f"CPU usage in {service} has spiked to over 90% and is sustained. Response times have increased significantly.",
            "network_issue": f"Network connectivity issues are affecting {service}. DNS resolution failures and connection timeouts are being reported.",
            "disk_full": f"Disk space on {service} nodes has reached critical levels. Log files and temporary data are consuming available space."
        }
        return descriptions.get(incident_type, f"Technical issue affecting {service}")
    
    def _generate_labels(self, incident_type: str, service: str) -> List[str]:
        """Generate relevant labels"""
        base_labels = [incident_type, service.replace("-service", "")]
        
        additional_labels = {
            "database_timeout": ["database", "performance", "timeout"],
            "memory_leak": ["memory", "performance", "resource"],
            "service_crash": ["availability", "crash", "container"],
            "high_cpu": ["cpu", "performance", "resource"],
            "network_issue": ["network", "connectivity", "infrastructure"],
            "disk_full": ["disk", "storage", "resource"]
        }
        
        base_labels.extend(additional_labels.get(incident_type, []))
        return base_labels
    
    def _generate_root_cause(self, incident_type: str) -> str:
        """Generate root cause analysis"""
        root_causes = {
            "database_timeout": "Database connection pool misconfiguration and high query load",
            "memory_leak": "Unclosed resources in application code causing memory accumulation",
            "service_crash": "Unhandled exception in request processing logic",
            "high_cpu": "Inefficient algorithm in data processing pipeline",
            "network_issue": "DNS server configuration error and network latency",
            "disk_full": "Log rotation policy not configured properly"
        }
        return root_causes.get(incident_type, "Root cause analysis pending")
    
    def _generate_customer_impact(self, severity: str) -> Dict[str, Any]:
        """Generate customer impact assessment"""
        impact_levels = {
            "P0": {"users_affected": random.randint(10000, 50000), "revenue_impact": random.randint(50000, 200000)},
            "P1": {"users_affected": random.randint(1000, 10000), "revenue_impact": random.randint(10000, 50000)},
            "P2": {"users_affected": random.randint(100, 1000), "revenue_impact": random.randint(1000, 10000)},
            "P3": {"users_affected": random.randint(10, 100), "revenue_impact": random.randint(100, 1000)}
        }
        
        base_impact = impact_levels[severity]
        return {
            "estimated_users_affected": base_impact["users_affected"],
            "estimated_revenue_impact_usd": base_impact["revenue_impact"],
            "customer_complaints": random.randint(0, base_impact["users_affected"] // 100),
            "sla_breach": severity in ["P0", "P1"]
        }
    
    def _generate_lessons_learned(self, incident_type: str) -> List[str]:
        """Generate lessons learned"""
        lessons = {
            "database_timeout": [
                "Connection pool monitoring needs improvement",
                "Query performance optimization required",
                "Database scaling strategy needs review"
            ],
            "memory_leak": [
                "Code review process should include memory management checks",
                "Memory profiling should be part of CI/CD pipeline",
                "Resource cleanup patterns need standardization"
            ],
            "service_crash": [
                "Error handling needs improvement",
                "Health check implementation requires enhancement",
                "Graceful shutdown procedures need implementation"
            ]
        }
        return lessons.get(incident_type, ["Standard incident response procedures followed"])
    
    def _generate_prevention_measures(self, incident_type: str) -> List[str]:
        """Generate prevention measures"""
        measures = {
            "database_timeout": [
                "Implement connection pool monitoring",
                "Add database performance alerts",
                "Regular database maintenance schedule"
            ],
            "memory_leak": [
                "Add memory leak detection to monitoring",
                "Implement automated memory profiling",
                "Regular code reviews for resource management"
            ],
            "service_crash": [
                "Improve application error handling",
                "Add comprehensive health checks",
                "Implement circuit breaker patterns"
            ]
        }
        return measures.get(incident_type, ["Regular system monitoring and maintenance"])
    
    def _analyze_pattern_distribution(self, incidents: List[Dict]) -> Dict[str, Any]:
        """Analyze incident pattern distribution"""
        types = [inc["type"] for inc in incidents]
        services = [inc["service"] for inc in incidents]
        severities = [inc["severity"] for inc in incidents]
        
        return {
            "most_common_type": max(set(types), key=types.count),
            "most_affected_service": max(set(services), key=services.count),
            "severity_distribution": {sev: severities.count(sev) for sev in set(severities)},
            "type_distribution": {typ: types.count(typ) for typ in set(types)}
        }
    
    def _analyze_resolution_trends(self, incidents: List[Dict]) -> Dict[str, Any]:
        """Analyze resolution trends"""
        resolved_incidents = [inc for inc in incidents if inc.get("resolution_time_minutes")]
        
        if not resolved_incidents:
            return {"message": "No resolved incidents to analyze"}
        
        resolution_times = [inc["resolution_time_minutes"] for inc in resolved_incidents]
        
        return {
            "avg_resolution_time_minutes": sum(resolution_times) / len(resolution_times),
            "fastest_resolution_minutes": min(resolution_times),
            "slowest_resolution_minutes": max(resolution_times),
            "resolution_trend": "improving" if random.random() > 0.5 else "stable"
        }
    
    def _analyze_service_impact(self, incidents: List[Dict]) -> Dict[str, Any]:
        """Analyze service impact patterns"""
        service_incidents = {}
        for inc in incidents:
            service = inc["service"]
            if service not in service_incidents:
                service_incidents[service] = []
            service_incidents[service].append(inc)
        
        return {
            "service_incident_counts": {svc: len(incs) for svc, incs in service_incidents.items()},
            "highest_impact_service": max(service_incidents.keys(), key=lambda x: len(service_incidents[x])),
            "service_reliability_scores": {
                svc: random.uniform(0.85, 0.98) for svc in service_incidents.keys()
            }
        }
    
    def _get_recommended_solution(self, similar_incidents: List[Dict]) -> Dict[str, Any]:
        """Get recommended solution based on similar incidents"""
        if not similar_incidents:
            return {"message": "No similar incidents found"}
        
        # Find most successful resolution method
        resolution_methods = [inc.get("resolution_method") for inc in similar_incidents if inc.get("resolution_method")]
        
        if resolution_methods:
            most_common_method = max(set(resolution_methods), key=resolution_methods.count)
            return {
                "recommended_method": most_common_method,
                "success_rate": random.uniform(0.8, 0.95),
                "based_on_incidents": len([inc for inc in similar_incidents if inc.get("resolution_method") == most_common_method])
            }
        
        return {"message": "No resolution data available"}
    
    def _calculate_success_probability(self, similar_incidents: List[Dict]) -> float:
        """Calculate success probability based on historical data"""
        if not similar_incidents:
            return 0.5
        
        success_rates = [inc["success_rate"] for inc in similar_incidents]
        return sum(success_rates) / len(success_rates)
    
    def _estimate_resolution_time(self, similar_incidents: List[Dict]) -> Dict[str, Any]:
        """Estimate resolution time based on similar incidents"""
        resolution_times = [inc.get("resolution_time_minutes") for inc in similar_incidents if inc.get("resolution_time_minutes")]
        
        if not resolution_times:
            return {"estimated_minutes": 120, "confidence": "low"}
        
        avg_time = sum(resolution_times) / len(resolution_times)
        return {
            "estimated_minutes": int(avg_time),
            "range_minutes": {"min": min(resolution_times), "max": max(resolution_times)},
            "confidence": "high" if len(resolution_times) > 5 else "medium"
        }
    
    def _assess_resolution_risk(self, similar_incidents: List[Dict]) -> Dict[str, Any]:
        """Assess risk of resolution attempts"""
        if not similar_incidents:
            return {"risk_level": "unknown", "confidence": 0.5}
        
        success_rates = [inc["success_rate"] for inc in similar_incidents]
        avg_success = sum(success_rates) / len(success_rates)
        
        if avg_success > 0.9:
            risk_level = "low"
        elif avg_success > 0.7:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return {
            "risk_level": risk_level,
            "success_probability": avg_success,
            "confidence": random.uniform(0.7, 0.9)
        }
    
    def _assess_automation_feasibility(self, similar_incidents: List[Dict]) -> Dict[str, Any]:
        """Assess automation feasibility"""
        if not similar_incidents:
            return {"feasible": False, "confidence": 0.5}
        
        automation_scores = [inc["automation_potential"] for inc in similar_incidents]
        avg_automation = sum(automation_scores) / len(automation_scores)
        
        return {
            "feasible": avg_automation > 0.7,
            "automation_score": avg_automation,
            "confidence": random.uniform(0.75, 0.9)
        }
    
    def _extract_common_root_causes(self, similar_incidents: List[Dict]) -> List[str]:
        """Extract common root causes"""
        root_causes = [inc.get("root_cause") for inc in similar_incidents if inc.get("root_cause")]
        
        # Simple frequency analysis
        cause_counts = {}
        for cause in root_causes:
            if cause:
                cause_counts[cause] = cause_counts.get(cause, 0) + 1
        
        return sorted(cause_counts.keys(), key=lambda x: cause_counts[x], reverse=True)[:3]
    
    def _extract_resolution_patterns(self, similar_incidents: List[Dict]) -> List[str]:
        """Extract resolution patterns"""
        methods = [inc.get("resolution_method") for inc in similar_incidents if inc.get("resolution_method")]
        return list(set(methods))
    
    def _extract_service_correlations(self, similar_incidents: List[Dict]) -> List[str]:
        """Extract service correlations"""
        services = [inc["service"] for inc in similar_incidents]
        return list(set(services))
    
    def _extract_time_patterns(self, similar_incidents: List[Dict]) -> Dict[str, Any]:
        """Extract time-based patterns"""
        created_times = [datetime.fromisoformat(inc["created"]) for inc in similar_incidents]
        
        if not created_times:
            return {}
        
        hours = [dt.hour for dt in created_times]
        days = [dt.weekday() for dt in created_times]
        
        return {
            "peak_hour": max(set(hours), key=hours.count) if hours else None,
            "peak_day": max(set(days), key=days.count) if days else None,
            "pattern_detected": len(set(hours)) < 8  # If incidents cluster in specific hours
        }
    
    def _get_incident_recommendations(self, incident: Dict[str, Any]) -> List[str]:
        """Get recommendations for new incident"""
        recommendations = [
            f"Assign to {incident['service']} team",
            f"Check similar {incident['type']} incidents",
            "Monitor system metrics closely",
            "Prepare rollback plan if needed"
        ]
        
        if incident["severity"] in ["P0", "P1"]:
            recommendations.insert(0, "Escalate to on-call engineer immediately")
        
        return recommendations