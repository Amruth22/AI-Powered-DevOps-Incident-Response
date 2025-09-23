"""
Prometheus Mock API
AI-optimized metrics collection and alerting system
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from faker import Faker
import math

fake = Faker()

class PrometheusMock:
    """Mock Prometheus API for AI-powered metrics analysis"""
    
    def __init__(self):
        self.services = ["user-service", "payment-service", "auth-service", "notification-service", "order-service"]
        self.metrics = [
            "cpu_usage_percent", "memory_usage_percent", "request_rate_rps", 
            "error_rate_percent", "response_time_ms", "disk_usage_percent",
            "network_rx_bytes", "network_tx_bytes", "active_connections"
        ]
        self.alert_rules = self._generate_alert_rules()
    
    def query_metrics(self, query: str, time: str = None) -> Dict[str, Any]:
        """Query metrics with AI-friendly structure"""
        
        # Parse query to determine metric type and service
        metric_info = self._parse_query(query)
        
        # Generate time series data
        if time:
            # Single point in time
            timestamp = self._parse_time(time)
            data_points = [self._generate_metric_value(metric_info, timestamp)]
        else:
            # Time range (last hour by default)
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)
            data_points = self._generate_time_series(metric_info, start_time, end_time)
        
        return {
            "status": "success",
            "data": {
                "resultType": "matrix" if len(data_points) > 1 else "vector",
                "result": [
                    {
                        "metric": {
                            "__name__": metric_info["metric"],
                            "job": metric_info["service"],
                            "instance": f"{metric_info['service']}-{random.randint(1, 3)}:8080",
                            "service": metric_info["service"]
                        },
                        "values" if len(data_points) > 1 else "value": data_points
                    }
                ]
            },
            "ai_analysis": {
                "metric_health": self._analyze_metric_health(metric_info, data_points),
                "trend_analysis": self._analyze_trend(data_points),
                "anomaly_detection": self._detect_anomalies(data_points),
                "forecasting": self._forecast_metrics(data_points),
                "confidence": random.uniform(0.80, 0.95)
            },
            "query_metadata": {
                "query": query,
                "execution_time_ms": random.randint(10, 100),
                "data_points": len(data_points),
                "time_range_hours": 1 if not time else 0,
                "ai_optimized": True
            }
        }
    
    def get_service_metrics(self, service_name: str, duration: str = "1h") -> Dict[str, Any]:
        """Get comprehensive service metrics for AI analysis"""
        
        # Parse duration
        hours = self._parse_duration(duration)
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        # Generate metrics for all key indicators
        service_metrics = {}
        
        for metric in self.metrics:
            metric_info = {"metric": metric, "service": service_name}
            time_series = self._generate_time_series(metric_info, start_time, end_time)
            
            service_metrics[metric] = {
                "current_value": time_series[-1][1] if time_series else 0,
                "avg_value": sum([float(point[1]) for point in time_series]) / len(time_series) if time_series else 0,
                "max_value": max([float(point[1]) for point in time_series]) if time_series else 0,
                "min_value": min([float(point[1]) for point in time_series]) if time_series else 0,
                "time_series": time_series,
                "health_score": self._calculate_metric_health_score(metric, time_series)
            }
        
        # Calculate overall service health
        health_scores = [metrics["health_score"] for metrics in service_metrics.values()]
        overall_health = sum(health_scores) / len(health_scores) if health_scores else 0.5
        
        return {
            "service": service_name,
            "time_range": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "duration_hours": hours
            },
            "metrics": service_metrics,
            "service_health": {
                "overall_score": overall_health,
                "status": self._get_health_status(overall_health),
                "critical_metrics": self._identify_critical_metrics(service_metrics),
                "recommendations": self._get_health_recommendations(service_metrics)
            },
            "ai_insights": {
                "performance_grade": self._calculate_performance_grade(overall_health),
                "capacity_utilization": self._analyze_capacity_utilization(service_metrics),
                "scaling_recommendation": self._get_scaling_recommendation(service_metrics),
                "alert_likelihood": self._predict_alert_likelihood(service_metrics),
                "maintenance_needed": overall_health < 0.7,
                "confidence": random.uniform(0.85, 0.95)
            },
            "sla_metrics": {
                "availability_percent": random.uniform(99.0, 99.99),
                "error_budget_remaining": random.uniform(0.1, 0.9),
                "mttr_minutes": random.randint(5, 45),
                "mtbf_hours": random.randint(24, 720)
            }
        }
    
    def get_alerts(self, state: str = "active") -> Dict[str, Any]:
        """Get alerts for AI processing"""
        
        # Generate active alerts
        active_alerts = []
        alert_count = random.randint(0, 8)  # 0-8 active alerts
        
        for i in range(alert_count):
            service = random.choice(self.services)
            alert_rule = random.choice(self.alert_rules)
            
            # Determine alert severity based on rule
            severity = self._determine_alert_severity(alert_rule)
            
            alert = {
                "labels": {
                    "alertname": alert_rule["name"],
                    "service": service,
                    "severity": severity,
                    "instance": f"{service}-{random.randint(1, 3)}:8080",
                    "job": service
                },
                "annotations": {
                    "summary": alert_rule["summary"].format(service=service),
                    "description": alert_rule["description"].format(service=service),
                    "runbook_url": f"https://runbooks.company.com/{alert_rule['name'].lower()}",
                    "dashboard_url": f"https://grafana.company.com/d/{service}"
                },
                "state": state,
                "activeAt": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                "value": str(random.uniform(alert_rule["threshold"] * 1.1, alert_rule["threshold"] * 2.0)),
                "ai_metadata": {
                    "confidence": random.uniform(0.75, 0.95),
                    "false_positive_probability": random.uniform(0.05, 0.25),
                    "urgency_score": self._calculate_alert_urgency(severity, alert_rule),
                    "auto_resolution_possible": alert_rule.get("auto_resolvable", False),
                    "escalation_recommended": severity in ["critical", "warning"] and random.random() > 0.6
                }
            }
            active_alerts.append(alert)
        
        return {
            "status": "success",
            "data": {
                "alerts": active_alerts
            },
            "alert_summary": {
                "total_alerts": len(active_alerts),
                "critical_alerts": len([a for a in active_alerts if a["labels"]["severity"] == "critical"]),
                "warning_alerts": len([a for a in active_alerts if a["labels"]["severity"] == "warning"]),
                "info_alerts": len([a for a in active_alerts if a["labels"]["severity"] == "info"]),
                "services_affected": len(set([a["labels"]["service"] for a in active_alerts])),
                "avg_alert_age_minutes": sum([
                    (datetime.now() - datetime.fromisoformat(a["activeAt"])).total_seconds() / 60
                    for a in active_alerts
                ]) / len(active_alerts) if active_alerts else 0
            },
            "ai_alert_analysis": {
                "alert_storm_detected": len(active_alerts) > 5,
                "correlation_patterns": self._analyze_alert_correlations(active_alerts),
                "root_cause_candidates": self._identify_root_cause_candidates(active_alerts),
                "resolution_priority": self._prioritize_alert_resolution(active_alerts),
                "auto_resolution_candidates": [
                    a["labels"]["alertname"] for a in active_alerts 
                    if a["ai_metadata"]["auto_resolution_possible"]
                ],
                "confidence": random.uniform(0.80, 0.92)
            }
        }
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """Parse Prometheus query to extract metric and service info"""
        
        # Simple query parsing (in real implementation, this would be more sophisticated)
        metric = "cpu_usage_percent"  # Default
        service = "unknown-service"
        
        # Extract metric name
        for m in self.metrics:
            if m in query:
                metric = m
                break
        
        # Extract service name
        for s in self.services:
            if s in query:
                service = s
                break
        
        return {"metric": metric, "service": service, "query": query}
    
    def _parse_time(self, time_str: str) -> datetime:
        """Parse time string to datetime"""
        try:
            return datetime.fromisoformat(time_str)
        except:
            return datetime.now()
    
    def _parse_duration(self, duration: str) -> int:
        """Parse duration string to hours"""
        duration_map = {
            "5m": 0.083, "15m": 0.25, "30m": 0.5, "1h": 1, "2h": 2, 
            "6h": 6, "12h": 12, "24h": 24, "1d": 24, "7d": 168
        }
        return duration_map.get(duration, 1)
    
    def _generate_time_series(self, metric_info: Dict, start_time: datetime, end_time: datetime) -> List[List]:
        """Generate realistic time series data"""
        
        points = []
        current_time = start_time
        interval = timedelta(minutes=5)  # 5-minute intervals
        
        # Base value for the metric
        base_value = self._get_base_metric_value(metric_info["metric"])
        
        while current_time <= end_time:
            # Add some realistic variation
            variation = self._get_metric_variation(metric_info["metric"], current_time)
            value = max(0, base_value + variation)
            
            # Format as Prometheus expects: [timestamp, "value"]
            timestamp = int(current_time.timestamp())
            points.append([timestamp, str(round(value, 2))])
            
            current_time += interval
        
        return points
    
    def _generate_metric_value(self, metric_info: Dict, timestamp: datetime) -> List:
        """Generate single metric value"""
        
        base_value = self._get_base_metric_value(metric_info["metric"])
        variation = self._get_metric_variation(metric_info["metric"], timestamp)
        value = max(0, base_value + variation)
        
        return [int(timestamp.timestamp()), str(round(value, 2))]
    
    def _get_base_metric_value(self, metric: str) -> float:
        """Get base value for metric type"""
        
        base_values = {
            "cpu_usage_percent": random.uniform(20, 70),
            "memory_usage_percent": random.uniform(30, 80),
            "request_rate_rps": random.uniform(10, 100),
            "error_rate_percent": random.uniform(0.1, 5.0),
            "response_time_ms": random.uniform(50, 500),
            "disk_usage_percent": random.uniform(20, 60),
            "network_rx_bytes": random.uniform(1000000, 10000000),
            "network_tx_bytes": random.uniform(1000000, 10000000),
            "active_connections": random.uniform(10, 100)
        }
        
        return base_values.get(metric, random.uniform(10, 100))
    
    def _get_metric_variation(self, metric: str, timestamp: datetime) -> float:
        """Get realistic variation for metric"""
        
        # Time-based patterns (daily cycles, etc.)
        hour = timestamp.hour
        
        # Business hours pattern (9 AM - 5 PM higher load)
        if 9 <= hour <= 17:
            time_multiplier = 1.2
        elif 22 <= hour or hour <= 6:
            time_multiplier = 0.7
        else:
            time_multiplier = 1.0
        
        # Random variation
        base_variation = random.uniform(-10, 10)
        
        # Metric-specific patterns
        if metric in ["cpu_usage_percent", "memory_usage_percent"]:
            # Resource metrics tend to have spikes
            if random.random() > 0.9:  # 10% chance of spike
                base_variation += random.uniform(20, 40)
        elif metric == "error_rate_percent":
            # Error rates usually low but can spike
            if random.random() > 0.95:  # 5% chance of error spike
                base_variation += random.uniform(5, 20)
        elif metric == "response_time_ms":
            # Response time correlates with load
            base_variation *= time_multiplier
        
        return base_variation * time_multiplier
    
    def _analyze_metric_health(self, metric_info: Dict, data_points: List) -> Dict[str, Any]:
        """Analyze metric health for AI"""
        
        if not data_points:
            return {"status": "no_data", "health_score": 0.5}
        
        values = [float(point[1]) for point in data_points]
        current_value = values[-1]
        avg_value = sum(values) / len(values)
        
        # Determine health based on metric type and values
        health_score = self._calculate_metric_health_score(metric_info["metric"], data_points)
        
        return {
            "status": self._get_health_status(health_score),
            "health_score": health_score,
            "current_value": current_value,
            "average_value": avg_value,
            "trend": "increasing" if current_value > avg_value * 1.1 else "decreasing" if current_value < avg_value * 0.9 else "stable",
            "threshold_breaches": self._count_threshold_breaches(metric_info["metric"], values)
        }
    
    def _analyze_trend(self, data_points: List) -> Dict[str, Any]:
        """Analyze trend in time series data"""
        
        if len(data_points) < 2:
            return {"trend": "insufficient_data"}
        
        values = [float(point[1]) for point in data_points]
        
        # Simple linear trend analysis
        first_half_avg = sum(values[:len(values)//2]) / (len(values)//2)
        second_half_avg = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        trend_strength = abs(second_half_avg - first_half_avg) / first_half_avg if first_half_avg > 0 else 0
        
        if second_half_avg > first_half_avg * 1.1:
            trend = "increasing"
        elif second_half_avg < first_half_avg * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "trend_strength": trend_strength,
            "confidence": min(0.9, trend_strength * 2),  # Higher strength = higher confidence
            "prediction": self._predict_next_value(values)
        }
    
    def _detect_anomalies(self, data_points: List) -> Dict[str, Any]:
        """Detect anomalies in time series data"""
        
        if len(data_points) < 5:
            return {"anomalies_detected": False, "anomaly_count": 0}
        
        values = [float(point[1]) for point in data_points]
        mean_val = sum(values) / len(values)
        std_dev = math.sqrt(sum([(x - mean_val) ** 2 for x in values]) / len(values))
        
        # Detect outliers (values beyond 2 standard deviations)
        anomalies = []
        for i, value in enumerate(values):
            if abs(value - mean_val) > 2 * std_dev:
                anomalies.append({
                    "index": i,
                    "timestamp": data_points[i][0],
                    "value": value,
                    "deviation": abs(value - mean_val) / std_dev
                })
        
        return {
            "anomalies_detected": len(anomalies) > 0,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "anomaly_score": len(anomalies) / len(values),
            "confidence": random.uniform(0.75, 0.90)
        }
    
    def _forecast_metrics(self, data_points: List) -> Dict[str, Any]:
        """Forecast future metric values"""
        
        if len(data_points) < 3:
            return {"forecast_available": False}
        
        values = [float(point[1]) for point in data_points]
        
        # Simple linear extrapolation
        recent_trend = (values[-1] - values[-3]) / 2  # Trend over last 2 points
        
        # Forecast next 3 points
        forecast = []
        for i in range(1, 4):
            predicted_value = max(0, values[-1] + (recent_trend * i))
            forecast.append({
                "minutes_ahead": i * 5,  # 5-minute intervals
                "predicted_value": round(predicted_value, 2),
                "confidence": max(0.3, 0.9 - (i * 0.2))  # Decreasing confidence
            })
        
        return {
            "forecast_available": True,
            "forecast_points": forecast,
            "trend_direction": "increasing" if recent_trend > 0 else "decreasing" if recent_trend < 0 else "stable",
            "forecast_confidence": random.uniform(0.60, 0.85)
        }
    
    def _calculate_metric_health_score(self, metric: str, data_points: List) -> float:
        """Calculate health score for specific metric"""
        
        if not data_points:
            return 0.5
        
        values = [float(point[1]) for point in data_points]
        current_value = values[-1]
        
        # Health thresholds by metric type
        health_thresholds = {
            "cpu_usage_percent": {"good": 70, "warning": 85, "critical": 95},
            "memory_usage_percent": {"good": 80, "warning": 90, "critical": 95},
            "error_rate_percent": {"good": 1, "warning": 5, "critical": 10},
            "response_time_ms": {"good": 200, "warning": 500, "critical": 1000},
            "disk_usage_percent": {"good": 70, "warning": 85, "critical": 95}
        }
        
        thresholds = health_thresholds.get(metric, {"good": 50, "warning": 75, "critical": 90})
        
        if current_value <= thresholds["good"]:
            return random.uniform(0.8, 1.0)
        elif current_value <= thresholds["warning"]:
            return random.uniform(0.5, 0.8)
        elif current_value <= thresholds["critical"]:
            return random.uniform(0.2, 0.5)
        else:
            return random.uniform(0.0, 0.2)
    
    def _get_health_status(self, health_score: float) -> str:
        """Convert health score to status"""
        if health_score >= 0.8:
            return "healthy"
        elif health_score >= 0.6:
            return "warning"
        elif health_score >= 0.3:
            return "critical"
        else:
            return "unhealthy"
    
    def _count_threshold_breaches(self, metric: str, values: List[float]) -> int:
        """Count threshold breaches"""
        thresholds = {
            "cpu_usage_percent": 85,
            "memory_usage_percent": 90,
            "error_rate_percent": 5,
            "response_time_ms": 500
        }
        
        threshold = thresholds.get(metric, 80)
        return len([v for v in values if v > threshold])
    
    def _predict_next_value(self, values: List[float]) -> Dict[str, Any]:
        """Predict next value in series"""
        if len(values) < 2:
            return {"prediction": values[0] if values else 0, "confidence": 0.3}
        
        # Simple linear prediction
        trend = values[-1] - values[-2]
        prediction = max(0, values[-1] + trend)
        
        return {
            "prediction": round(prediction, 2),
            "confidence": random.uniform(0.6, 0.8)
        }
    
    def _generate_alert_rules(self) -> List[Dict[str, Any]]:
        """Generate realistic alert rules"""
        return [
            {
                "name": "HighCPUUsage",
                "summary": "High CPU usage detected on {service}",
                "description": "CPU usage has been above 85% for more than 5 minutes on {service}",
                "threshold": 85,
                "auto_resolvable": True
            },
            {
                "name": "HighMemoryUsage", 
                "summary": "High memory usage detected on {service}",
                "description": "Memory usage has been above 90% for more than 5 minutes on {service}",
                "threshold": 90,
                "auto_resolvable": False
            },
            {
                "name": "HighErrorRate",
                "summary": "High error rate detected on {service}",
                "description": "Error rate has been above 5% for more than 2 minutes on {service}",
                "threshold": 5,
                "auto_resolvable": True
            },
            {
                "name": "SlowResponseTime",
                "summary": "Slow response time detected on {service}",
                "description": "Response time has been above 500ms for more than 3 minutes on {service}",
                "threshold": 500,
                "auto_resolvable": True
            },
            {
                "name": "ServiceDown",
                "summary": "Service {service} is down",
                "description": "Service {service} is not responding to health checks",
                "threshold": 0,
                "auto_resolvable": True
            }
        ]
    
    def _determine_alert_severity(self, alert_rule: Dict) -> str:
        """Determine alert severity"""
        severity_map = {
            "ServiceDown": "critical",
            "HighErrorRate": "critical", 
            "HighCPUUsage": "warning",
            "HighMemoryUsage": "warning",
            "SlowResponseTime": "warning"
        }
        return severity_map.get(alert_rule["name"], "info")
    
    def _calculate_alert_urgency(self, severity: str, alert_rule: Dict) -> float:
        """Calculate alert urgency score"""
        base_scores = {"critical": 0.9, "warning": 0.6, "info": 0.3}
        base_score = base_scores.get(severity, 0.5)
        
        # Adjust based on auto-resolvability
        if alert_rule.get("auto_resolvable", False):
            base_score *= 1.2  # Higher urgency for auto-resolvable alerts
        
        return min(1.0, base_score)
    
    def _analyze_alert_correlations(self, alerts: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze correlations between alerts"""
        correlations = []
        
        # Group alerts by service
        service_alerts = {}
        for alert in alerts:
            service = alert["labels"]["service"]
            if service not in service_alerts:
                service_alerts[service] = []
            service_alerts[service].append(alert)
        
        # Find services with multiple alerts (potential correlation)
        for service, service_alert_list in service_alerts.items():
            if len(service_alert_list) > 1:
                correlations.append({
                    "type": "service_correlation",
                    "service": service,
                    "alert_count": len(service_alert_list),
                    "alerts": [a["labels"]["alertname"] for a in service_alert_list],
                    "correlation_strength": min(1.0, len(service_alert_list) / 3)
                })
        
        return correlations
    
    def _identify_root_cause_candidates(self, alerts: List[Dict]) -> List[str]:
        """Identify potential root cause alerts"""
        
        # Prioritize certain alert types as potential root causes
        root_cause_priorities = {
            "ServiceDown": 1.0,
            "HighErrorRate": 0.9,
            "HighCPUUsage": 0.7,
            "HighMemoryUsage": 0.7,
            "SlowResponseTime": 0.5
        }
        
        candidates = []
        for alert in alerts:
            alert_name = alert["labels"]["alertname"]
            priority = root_cause_priorities.get(alert_name, 0.3)
            
            if priority >= 0.7:
                candidates.append(alert_name)
        
        return candidates
    
    def _prioritize_alert_resolution(self, alerts: List[Dict]) -> List[Dict[str, Any]]:
        """Prioritize alerts for resolution"""
        
        prioritized = []
        for alert in alerts:
            priority_score = 0.5
            
            # Severity weight
            if alert["labels"]["severity"] == "critical":
                priority_score += 0.4
            elif alert["labels"]["severity"] == "warning":
                priority_score += 0.2
            
            # Auto-resolution capability
            if alert["ai_metadata"]["auto_resolution_possible"]:
                priority_score += 0.2
            
            # Urgency score
            priority_score += alert["ai_metadata"]["urgency_score"] * 0.3
            
            prioritized.append({
                "alert": alert["labels"]["alertname"],
                "service": alert["labels"]["service"],
                "priority_score": min(1.0, priority_score),
                "recommended_action": "auto_resolve" if alert["ai_metadata"]["auto_resolution_possible"] else "manual_investigation"
            })
        
        # Sort by priority score (highest first)
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return prioritized
    
    def _identify_critical_metrics(self, service_metrics: Dict) -> List[str]:
        """Identify critical metrics that need attention"""
        critical = []
        
        for metric, data in service_metrics.items():
            if data["health_score"] < 0.6:
                critical.append(metric)
        
        return critical
    
    def _get_health_recommendations(self, service_metrics: Dict) -> List[str]:
        """Get health improvement recommendations"""
        recommendations = []
        
        for metric, data in service_metrics.items():
            if data["health_score"] < 0.6:
                if metric == "cpu_usage_percent":
                    recommendations.append("Consider CPU optimization or horizontal scaling")
                elif metric == "memory_usage_percent":
                    recommendations.append("Investigate memory leaks or increase memory allocation")
                elif metric == "error_rate_percent":
                    recommendations.append("Investigate error patterns and fix underlying issues")
                elif metric == "response_time_ms":
                    recommendations.append("Optimize response time through caching or code optimization")
        
        return recommendations if recommendations else ["Service metrics appear healthy"]
    
    def _calculate_performance_grade(self, health_score: float) -> str:
        """Calculate performance grade"""
        if health_score >= 0.9:
            return "A"
        elif health_score >= 0.8:
            return "B"
        elif health_score >= 0.7:
            return "C"
        elif health_score >= 0.6:
            return "D"
        else:
            return "F"
    
    def _analyze_capacity_utilization(self, service_metrics: Dict) -> Dict[str, Any]:
        """Analyze capacity utilization"""
        cpu_util = service_metrics.get("cpu_usage_percent", {}).get("current_value", 0)
        memory_util = service_metrics.get("memory_usage_percent", {}).get("current_value", 0)
        
        return {
            "cpu_utilization": cpu_util,
            "memory_utilization": memory_util,
            "overall_utilization": (cpu_util + memory_util) / 2,
            "capacity_status": "high" if (cpu_util + memory_util) / 2 > 70 else "normal"
        }
    
    def _get_scaling_recommendation(self, service_metrics: Dict) -> str:
        """Get scaling recommendation"""
        cpu_util = service_metrics.get("cpu_usage_percent", {}).get("current_value", 0)
        memory_util = service_metrics.get("memory_usage_percent", {}).get("current_value", 0)
        
        if cpu_util > 80 or memory_util > 80:
            return "scale_up"
        elif cpu_util < 30 and memory_util < 40:
            return "scale_down"
        else:
            return "optimal"
    
    def _predict_alert_likelihood(self, service_metrics: Dict) -> Dict[str, Any]:
        """Predict likelihood of alerts"""
        
        risk_factors = []
        overall_risk = 0.0
        
        for metric, data in service_metrics.items():
            if data["health_score"] < 0.7:
                risk_factors.append(metric)
                overall_risk += (1 - data["health_score"]) * 0.2
        
        return {
            "alert_likelihood": min(1.0, overall_risk),
            "risk_level": "high" if overall_risk > 0.6 else "medium" if overall_risk > 0.3 else "low",
            "risk_factors": risk_factors,
            "time_to_alert_estimate": f"{random.randint(10, 60)} minutes" if overall_risk > 0.5 else "low risk"
        }