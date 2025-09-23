"""
Elasticsearch Mock API
AI-optimized log analysis and search functionality
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from faker import Faker

fake = Faker()

class ElasticsearchMock:
    """Mock Elasticsearch API for AI-powered log analysis"""
    
    def __init__(self):
        self.services = ["user-service", "payment-service", "auth-service", "notification-service", "order-service"]
        self.log_levels = ["ERROR", "WARN", "INFO", "DEBUG", "FATAL"]
        self.error_patterns = {
            "database_timeout": [
                "Connection timeout after 5000ms",
                "Unable to acquire connection from pool",
                "Database connection pool exhausted",
                "Query execution timeout"
            ],
            "memory_leak": [
                "OutOfMemoryError: Java heap space",
                "GC overhead limit exceeded", 
                "Memory usage at 95% of heap",
                "Unable to allocate memory"
            ],
            "service_crash": [
                "Application terminated unexpectedly",
                "Segmentation fault detected",
                "Container exited with code 137",
                "Health check failed"
            ],
            "high_cpu": [
                "CPU usage sustained at 95%",
                "High load average detected",
                "Thread pool exhausted",
                "Performance degradation"
            ],
            "network_issue": [
                "DNS resolution failed",
                "Connection reset by peer", 
                "Network timeout after 10000ms",
                "Packet loss detected"
            ],
            "disk_full": [
                "No space left on device",
                "Unable to write log file",
                "Disk usage at 98%",
                "Failed to extend database"
            ]
        }
    
    def search_logs(self, query: str = "*", size: int = 10, severity: str = None) -> Dict[str, Any]:
        """Search logs with AI-friendly structure"""
        
        # Generate realistic log entries
        logs = []
        for i in range(size):
            timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))
            service = random.choice(self.services)
            level = severity.upper() if severity else random.choice(self.log_levels)
            
            # Generate contextual message based on query
            if query != "*" and query.lower() in ["error", "timeout", "crash", "memory", "cpu", "network", "disk"]:
                error_type = self._map_query_to_error_type(query.lower())
                message = random.choice(self.error_patterns.get(error_type, ["Generic error message"]))
            else:
                message = fake.sentence()
            
            log_entry = {
                "timestamp": timestamp.isoformat(),
                "service": service,
                "level": level,
                "message": message,
                "host": f"{service}-{random.randint(1, 5)}",
                "thread": f"thread-{random.randint(1, 20)}",
                "request_id": fake.uuid4(),
                "user_id": fake.uuid4() if random.random() > 0.3 else None,
                "correlation_id": fake.uuid4(),
                "stack_trace": self._generate_stack_trace() if level in ["ERROR", "FATAL"] else None,
                "ai_confidence": random.uniform(0.7, 0.95)  # AI confidence in log relevance
            }
            logs.append(log_entry)
        
        # Sort by timestamp (newest first)
        logs.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "took": random.randint(5, 50),
            "timed_out": False,
            "hits": {
                "total": {"value": random.randint(100, 10000), "relation": "eq"},
                "max_score": random.uniform(1.0, 10.0),
                "hits": [
                    {
                        "_index": f"logs-{log['service']}-{datetime.now().strftime('%Y.%m.%d')}",
                        "_type": "_doc",
                        "_id": fake.uuid4(),
                        "_score": random.uniform(1.0, 10.0),
                        "_source": log
                    } for log in logs
                ]
            },
            "aggregations": self._generate_aggregations(logs),
            "ai_analysis": {
                "pattern_detected": query != "*",
                "severity_distribution": self._analyze_severity_distribution(logs),
                "time_pattern": self._analyze_time_pattern(logs),
                "service_correlation": self._analyze_service_correlation(logs),
                "confidence_score": random.uniform(0.75, 0.95)
            }
        }
    
    def get_service_logs(self, service_name: str, hours: int = 1) -> Dict[str, Any]:
        """Get service-specific logs for AI analysis"""
        
        # Generate service-specific logs
        log_count = random.randint(20, 100)
        logs = []
        
        for i in range(log_count):
            timestamp = datetime.now() - timedelta(minutes=random.randint(1, hours * 60))
            level = random.choices(
                self.log_levels,
                weights=[0.1, 0.2, 0.5, 0.15, 0.05]  # More INFO, less FATAL
            )[0]
            
            # Generate service-specific messages
            if "payment" in service_name.lower():
                messages = [
                    "Payment processed successfully",
                    "Credit card validation failed",
                    "Transaction timeout occurred",
                    "Payment gateway connection error"
                ]
            elif "auth" in service_name.lower():
                messages = [
                    "User authentication successful",
                    "Invalid credentials provided",
                    "JWT token expired",
                    "OAuth callback failed"
                ]
            elif "user" in service_name.lower():
                messages = [
                    "User profile updated",
                    "Database connection timeout",
                    "User registration completed",
                    "Profile validation error"
                ]
            else:
                messages = [
                    "Service operation completed",
                    "Request processing error",
                    "Health check passed",
                    "Configuration loaded"
                ]
            
            log_entry = {
                "timestamp": timestamp.isoformat(),
                "service": service_name,
                "level": level,
                "message": random.choice(messages),
                "host": f"{service_name}-{random.randint(1, 3)}",
                "thread": f"thread-{random.randint(1, 10)}",
                "request_id": fake.uuid4(),
                "response_time_ms": random.randint(10, 2000),
                "memory_usage_mb": random.randint(100, 1000),
                "cpu_usage_percent": random.randint(10, 90)
            }
            logs.append(log_entry)
        
        # Sort by timestamp
        logs.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "service": service_name,
            "time_range": f"last_{hours}_hours",
            "total_logs": len(logs),
            "logs": logs,
            "summary": {
                "error_count": len([l for l in logs if l["level"] in ["ERROR", "FATAL"]]),
                "warning_count": len([l for l in logs if l["level"] == "WARN"]),
                "info_count": len([l for l in logs if l["level"] == "INFO"]),
                "avg_response_time_ms": sum([l.get("response_time_ms", 0) for l in logs]) / len(logs),
                "peak_memory_mb": max([l.get("memory_usage_mb", 0) for l in logs]),
                "peak_cpu_percent": max([l.get("cpu_usage_percent", 0) for l in logs])
            },
            "ai_insights": {
                "health_score": random.uniform(0.6, 0.95),
                "anomaly_detected": random.random() > 0.7,
                "trend_analysis": "stable" if random.random() > 0.3 else "degrading",
                "recommended_action": self._get_recommended_action(service_name, logs),
                "confidence": random.uniform(0.8, 0.95)
            }
        }
    
    def _map_query_to_error_type(self, query: str) -> str:
        """Map search query to error type"""
        mapping = {
            "error": "service_crash",
            "timeout": "database_timeout", 
            "crash": "service_crash",
            "memory": "memory_leak",
            "cpu": "high_cpu",
            "network": "network_issue",
            "disk": "disk_full"
        }
        return mapping.get(query, "service_crash")
    
    def _generate_stack_trace(self) -> List[str]:
        """Generate realistic stack trace"""
        traces = [
            "at com.company.service.PaymentService.processPayment(PaymentService.java:142)",
            "at com.company.controller.PaymentController.handlePayment(PaymentController.java:67)",
            "at java.base/java.lang.Thread.run(Thread.java:834)",
            "at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1040)"
        ]
        return random.sample(traces, random.randint(2, 4))
    
    def _generate_aggregations(self, logs: List[Dict]) -> Dict[str, Any]:
        """Generate aggregations for AI analysis"""
        return {
            "services": {
                "buckets": [
                    {"key": service, "doc_count": random.randint(1, 20)}
                    for service in set([log["service"] for log in logs])
                ]
            },
            "levels": {
                "buckets": [
                    {"key": level, "doc_count": random.randint(1, 15)}
                    for level in set([log["level"] for log in logs])
                ]
            },
            "time_histogram": {
                "buckets": [
                    {
                        "key_as_string": (datetime.now() - timedelta(minutes=i*10)).isoformat(),
                        "doc_count": random.randint(0, 10)
                    } for i in range(6)
                ]
            }
        }
    
    def _analyze_severity_distribution(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analyze severity distribution for AI"""
        levels = [log["level"] for log in logs]
        return {
            "error_percentage": (levels.count("ERROR") + levels.count("FATAL")) / len(levels) * 100,
            "warning_percentage": levels.count("WARN") / len(levels) * 100,
            "info_percentage": levels.count("INFO") / len(levels) * 100,
            "severity_trend": "increasing" if random.random() > 0.6 else "stable"
        }
    
    def _analyze_time_pattern(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analyze time patterns for AI"""
        return {
            "peak_hour": random.randint(9, 17),
            "frequency_trend": "increasing" if random.random() > 0.5 else "decreasing",
            "burst_detected": random.random() > 0.7,
            "pattern_confidence": random.uniform(0.7, 0.9)
        }
    
    def _analyze_service_correlation(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analyze service correlations for AI"""
        services = list(set([log["service"] for log in logs]))
        return {
            "correlated_services": random.sample(services, min(2, len(services))),
            "correlation_strength": random.uniform(0.3, 0.8),
            "cascade_probability": random.uniform(0.1, 0.6)
        }
    
    def _get_recommended_action(self, service_name: str, logs: List[Dict]) -> str:
        """Get AI-recommended action"""
        error_count = len([l for l in logs if l["level"] in ["ERROR", "FATAL"]])
        
        if error_count > 10:
            return f"Investigate {service_name} - high error rate detected"
        elif error_count > 5:
            return f"Monitor {service_name} - elevated error rate"
        else:
            return f"{service_name} appears healthy - continue monitoring"