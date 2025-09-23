"""
Kubernetes Mock API
AI-optimized container orchestration and health monitoring
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from faker import Faker

fake = Faker()

class KubernetesMock:
    """Mock Kubernetes API for AI-powered container diagnostics"""
    
    def __init__(self):
        self.services = ["user-service", "payment-service", "auth-service", "notification-service", "order-service"]
        self.namespaces = ["default", "production", "staging", "monitoring"]
        self.pod_statuses = ["Running", "Pending", "Failed", "Succeeded", "Unknown"]
        self.node_conditions = ["Ready", "MemoryPressure", "DiskPressure", "PIDPressure", "NetworkUnavailable"]
    
    def get_pods(self, namespace: str = "default") -> Dict[str, Any]:
        """Get pod status with AI-friendly health metrics"""
        
        pods = []
        pod_count = random.randint(8, 15)
        
        for i in range(pod_count):
            service = random.choice(self.services)
            pod_name = f"{service}-{fake.uuid4()[:8]}"
            
            # 80% healthy, 20% with issues for realistic simulation
            is_healthy = random.random() > 0.2
            status = "Running" if is_healthy else random.choice(["Pending", "Failed", "Unknown"])
            
            # Generate realistic resource usage
            cpu_usage = random.uniform(10, 90) if is_healthy else random.uniform(80, 100)
            memory_usage = random.uniform(20, 80) if is_healthy else random.uniform(85, 98)
            
            pod = {
                "metadata": {
                    "name": pod_name,
                    "namespace": namespace,
                    "labels": {
                        "app": service,
                        "version": f"v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                        "environment": namespace
                    },
                    "creationTimestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                    "uid": fake.uuid4()
                },
                "spec": {
                    "containers": [
                        {
                            "name": service,
                            "image": f"{service}:latest",
                            "resources": {
                                "requests": {"cpu": "100m", "memory": "128Mi"},
                                "limits": {"cpu": "500m", "memory": "512Mi"}
                            }
                        }
                    ],
                    "nodeName": f"node-{random.randint(1, 5)}"
                },
                "status": {
                    "phase": status,
                    "conditions": self._generate_pod_conditions(is_healthy),
                    "containerStatuses": [
                        {
                            "name": service,
                            "ready": is_healthy,
                            "restartCount": 0 if is_healthy else random.randint(1, 10),
                            "state": {
                                "running": {
                                    "startedAt": (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat()
                                } if is_healthy else None,
                                "waiting": {
                                    "reason": "ImagePullBackOff" if not is_healthy else None
                                } if not is_healthy else None
                            }
                        }
                    ],
                    "podIP": fake.ipv4_private(),
                    "hostIP": fake.ipv4_private(),
                    "startTime": (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat()
                },
                "metrics": {
                    "cpu_usage_percent": round(cpu_usage, 2),
                    "memory_usage_percent": round(memory_usage, 2),
                    "network_rx_bytes": random.randint(1000000, 100000000),
                    "network_tx_bytes": random.randint(1000000, 100000000),
                    "disk_usage_percent": random.uniform(10, 70),
                    "uptime_seconds": random.randint(3600, 86400)
                },
                "ai_health_score": self._calculate_health_score(cpu_usage, memory_usage, is_healthy),
                "ai_insights": {
                    "status_confidence": random.uniform(0.85, 0.98),
                    "performance_trend": "stable" if is_healthy else "degrading",
                    "anomaly_detected": not is_healthy,
                    "recommended_action": self._get_pod_recommendation(status, cpu_usage, memory_usage)
                }
            }
            pods.append(pod)
        
        return {
            "apiVersion": "v1",
            "kind": "PodList",
            "metadata": {
                "namespace": namespace,
                "resourceVersion": str(random.randint(100000, 999999))
            },
            "items": pods,
            "summary": {
                "total_pods": len(pods),
                "running_pods": len([p for p in pods if p["status"]["phase"] == "Running"]),
                "failed_pods": len([p for p in pods if p["status"]["phase"] == "Failed"]),
                "pending_pods": len([p for p in pods if p["status"]["phase"] == "Pending"]),
                "avg_cpu_usage": sum([p["metrics"]["cpu_usage_percent"] for p in pods]) / len(pods),
                "avg_memory_usage": sum([p["metrics"]["memory_usage_percent"] for p in pods]) / len(pods),
                "health_score": sum([p["ai_health_score"] for p in pods]) / len(pods)
            },
            "ai_cluster_analysis": {
                "overall_health": "healthy" if len([p for p in pods if p["status"]["phase"] == "Running"]) / len(pods) > 0.8 else "degraded",
                "resource_pressure": "high" if sum([p["metrics"]["cpu_usage_percent"] for p in pods]) / len(pods) > 70 else "normal",
                "scaling_recommendation": self._get_scaling_recommendation(pods),
                "confidence": random.uniform(0.8, 0.95)
            }
        }
    
    def get_pod_logs(self, pod_name: str, lines: int = 100) -> Dict[str, Any]:
        """Get pod logs for AI analysis"""
        
        logs = []
        for i in range(min(lines, random.randint(20, 100))):
            timestamp = datetime.now() - timedelta(seconds=random.randint(1, 3600))
            level = random.choices(
                ["INFO", "WARN", "ERROR", "DEBUG"],
                weights=[0.6, 0.2, 0.15, 0.05]
            )[0]
            
            # Generate contextual log messages
            messages = [
                "Application started successfully",
                "Health check endpoint responding",
                "Database connection established",
                "Processing incoming request",
                "Request completed successfully",
                "Memory usage within normal limits",
                "CPU utilization stable"
            ]
            
            if level == "ERROR":
                messages = [
                    "Failed to connect to database",
                    "Request timeout occurred",
                    "Memory allocation failed",
                    "Service unavailable",
                    "Connection refused"
                ]
            elif level == "WARN":
                messages = [
                    "High memory usage detected",
                    "Slow database query",
                    "Connection pool near limit",
                    "Disk space running low"
                ]
            
            log_entry = {
                "timestamp": timestamp.isoformat(),
                "level": level,
                "message": random.choice(messages),
                "pod": pod_name,
                "container": pod_name.split('-')[0] + "-container",
                "thread": f"thread-{random.randint(1, 10)}"
            }
            logs.append(log_entry)
        
        # Sort by timestamp (newest first)
        logs.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "pod_name": pod_name,
            "lines_requested": lines,
            "lines_returned": len(logs),
            "logs": logs,
            "log_analysis": {
                "error_count": len([l for l in logs if l["level"] == "ERROR"]),
                "warning_count": len([l for l in logs if l["level"] == "WARN"]),
                "info_count": len([l for l in logs if l["level"] == "INFO"]),
                "error_rate": len([l for l in logs if l["level"] == "ERROR"]) / len(logs) * 100,
                "health_indicator": "healthy" if len([l for l in logs if l["level"] == "ERROR"]) < 5 else "unhealthy"
            },
            "ai_insights": {
                "log_pattern_confidence": random.uniform(0.75, 0.92),
                "anomaly_score": random.uniform(0.1, 0.8),
                "trend_analysis": "stable" if random.random() > 0.3 else "concerning",
                "recommended_investigation": self._get_log_investigation_recommendation(logs)
            }
        }
    
    def get_nodes(self) -> Dict[str, Any]:
        """Get cluster node health for AI diagnostics"""
        
        nodes = []
        node_count = random.randint(3, 8)
        
        for i in range(node_count):
            node_name = f"node-{i+1}"
            is_healthy = random.random() > 0.1  # 90% healthy nodes
            
            node = {
                "metadata": {
                    "name": node_name,
                    "labels": {
                        "kubernetes.io/hostname": node_name,
                        "node-role.kubernetes.io/worker": "",
                        "kubernetes.io/os": "linux"
                    },
                    "creationTimestamp": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat()
                },
                "spec": {
                    "podCIDR": f"10.244.{i}.0/24",
                    "providerID": f"aws:///us-west-2a/i-{fake.uuid4()[:8]}"
                },
                "status": {
                    "conditions": self._generate_node_conditions(is_healthy),
                    "addresses": [
                        {"type": "InternalIP", "address": fake.ipv4_private()},
                        {"type": "ExternalIP", "address": fake.ipv4_public()},
                        {"type": "Hostname", "address": node_name}
                    ],
                    "capacity": {
                        "cpu": f"{random.randint(2, 16)}",
                        "memory": f"{random.randint(4, 64)}Gi",
                        "pods": "110",
                        "ephemeral-storage": f"{random.randint(50, 500)}Gi"
                    },
                    "allocatable": {
                        "cpu": f"{random.randint(1, 15)}",
                        "memory": f"{random.randint(3, 60)}Gi",
                        "pods": "110",
                        "ephemeral-storage": f"{random.randint(40, 450)}Gi"
                    },
                    "nodeInfo": {
                        "machineID": fake.uuid4(),
                        "systemUUID": fake.uuid4(),
                        "bootID": fake.uuid4(),
                        "kernelVersion": "5.4.0-1043-aws",
                        "osImage": "Ubuntu 20.04.2 LTS",
                        "containerRuntimeVersion": "docker://20.10.7",
                        "kubeletVersion": "v1.21.2",
                        "kubeProxyVersion": "v1.21.2"
                    }
                },
                "metrics": {
                    "cpu_usage_percent": random.uniform(10, 80) if is_healthy else random.uniform(85, 98),
                    "memory_usage_percent": random.uniform(20, 70) if is_healthy else random.uniform(80, 95),
                    "disk_usage_percent": random.uniform(15, 60),
                    "network_utilization_percent": random.uniform(5, 40),
                    "pod_count": random.randint(5, 25),
                    "uptime_hours": random.randint(24, 8760)
                },
                "ai_health_score": random.uniform(0.8, 0.98) if is_healthy else random.uniform(0.3, 0.7),
                "ai_insights": {
                    "performance_grade": "A" if is_healthy else random.choice(["B", "C", "D"]),
                    "resource_pressure": "low" if is_healthy else "high",
                    "maintenance_needed": not is_healthy,
                    "confidence": random.uniform(0.85, 0.95)
                }
            }
            nodes.append(node)
        
        return {
            "apiVersion": "v1",
            "kind": "NodeList",
            "items": nodes,
            "cluster_summary": {
                "total_nodes": len(nodes),
                "ready_nodes": len([n for n in nodes if any(c["type"] == "Ready" and c["status"] == "True" for c in n["status"]["conditions"])]),
                "total_cpu_cores": sum([int(n["status"]["capacity"]["cpu"]) for n in nodes]),
                "total_memory_gb": sum([int(n["status"]["capacity"]["memory"].replace("Gi", "")) for n in nodes]),
                "avg_cpu_usage": sum([n["metrics"]["cpu_usage_percent"] for n in nodes]) / len(nodes),
                "avg_memory_usage": sum([n["metrics"]["memory_usage_percent"] for n in nodes]) / len(nodes),
                "cluster_health_score": sum([n["ai_health_score"] for n in nodes]) / len(nodes)
            },
            "ai_cluster_insights": {
                "scaling_recommendation": "scale_up" if len(nodes) < 5 else "optimal",
                "resource_optimization": self._get_resource_optimization_advice(nodes),
                "maintenance_schedule": self._get_maintenance_recommendations(nodes),
                "confidence": random.uniform(0.8, 0.94)
            }
        }
    
    def restart_pod(self, pod_name: str) -> Dict[str, Any]:
        """Restart pod (AI remediation action)"""
        
        # Simulate restart success/failure
        success = random.random() > 0.1  # 90% success rate
        
        if success:
            return {
                "action": "restart_pod",
                "pod_name": pod_name,
                "status": "success",
                "message": f"Pod {pod_name} restarted successfully",
                "timestamp": datetime.now().isoformat(),
                "new_pod_id": fake.uuid4(),
                "restart_time_seconds": random.randint(10, 60),
                "ai_confidence": random.uniform(0.85, 0.95),
                "expected_recovery_time": f"{random.randint(1, 5)} minutes",
                "monitoring_recommendation": "Monitor pod health for next 10 minutes"
            }
        else:
            return {
                "action": "restart_pod",
                "pod_name": pod_name,
                "status": "failed",
                "message": f"Failed to restart pod {pod_name}",
                "error": "Pod stuck in terminating state",
                "timestamp": datetime.now().isoformat(),
                "ai_confidence": random.uniform(0.6, 0.8),
                "recommended_escalation": "Manual intervention required",
                "alternative_actions": ["Force delete pod", "Check node health", "Review resource constraints"]
            }
    
    def _generate_pod_conditions(self, is_healthy: bool) -> List[Dict[str, Any]]:
        """Generate pod conditions"""
        conditions = [
            {
                "type": "Initialized",
                "status": "True",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
            },
            {
                "type": "Ready",
                "status": "True" if is_healthy else "False",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 30))).isoformat()
            },
            {
                "type": "ContainersReady",
                "status": "True" if is_healthy else "False",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 30))).isoformat()
            },
            {
                "type": "PodScheduled",
                "status": "True",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
            }
        ]
        return conditions
    
    def _generate_node_conditions(self, is_healthy: bool) -> List[Dict[str, Any]]:
        """Generate node conditions"""
        conditions = [
            {
                "type": "Ready",
                "status": "True" if is_healthy else "False",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                "reason": "KubeletReady" if is_healthy else "KubeletNotReady"
            },
            {
                "type": "MemoryPressure",
                "status": "False" if is_healthy else "True",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
            },
            {
                "type": "DiskPressure",
                "status": "False",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
            },
            {
                "type": "PIDPressure",
                "status": "False",
                "lastTransitionTime": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
            }
        ]
        return conditions
    
    def _calculate_health_score(self, cpu_usage: float, memory_usage: float, is_healthy: bool) -> float:
        """Calculate AI health score"""
        if not is_healthy:
            return random.uniform(0.2, 0.5)
        
        # Base score on resource usage
        cpu_score = max(0, 1 - (cpu_usage / 100))
        memory_score = max(0, 1 - (memory_usage / 100))
        
        return (cpu_score + memory_score) / 2
    
    def _get_pod_recommendation(self, status: str, cpu_usage: float, memory_usage: float) -> str:
        """Get AI recommendation for pod"""
        if status != "Running":
            return f"Investigate pod failure - status: {status}"
        elif cpu_usage > 80:
            return "Consider CPU limit increase or horizontal scaling"
        elif memory_usage > 80:
            return "Consider memory limit increase or investigate memory leaks"
        else:
            return "Pod operating within normal parameters"
    
    def _get_scaling_recommendation(self, pods: List[Dict]) -> str:
        """Get scaling recommendation"""
        avg_cpu = sum([p["metrics"]["cpu_usage_percent"] for p in pods]) / len(pods)
        running_pods = len([p for p in pods if p["status"]["phase"] == "Running"])
        
        if avg_cpu > 70:
            return "Consider horizontal pod autoscaling - high CPU usage detected"
        elif running_pods < 3:
            return "Consider increasing replica count for high availability"
        else:
            return "Current scaling appears optimal"
    
    def _get_log_investigation_recommendation(self, logs: List[Dict]) -> str:
        """Get log investigation recommendation"""
        error_count = len([l for l in logs if l["level"] == "ERROR"])
        
        if error_count > 10:
            return "High error rate - immediate investigation required"
        elif error_count > 5:
            return "Elevated error rate - monitor closely"
        else:
            return "Log patterns appear normal"
    
    def _get_resource_optimization_advice(self, nodes: List[Dict]) -> str:
        """Get resource optimization advice"""
        avg_cpu = sum([n["metrics"]["cpu_usage_percent"] for n in nodes]) / len(nodes)
        avg_memory = sum([n["metrics"]["memory_usage_percent"] for n in nodes]) / len(nodes)
        
        if avg_cpu < 30 and avg_memory < 40:
            return "Cluster may be over-provisioned - consider downsizing"
        elif avg_cpu > 80 or avg_memory > 80:
            return "Cluster under resource pressure - consider adding nodes"
        else:
            return "Resource utilization appears optimal"
    
    def _get_maintenance_recommendations(self, nodes: List[Dict]) -> List[str]:
        """Get maintenance recommendations"""
        recommendations = []
        
        for node in nodes:
            if node["metrics"]["uptime_hours"] > 8760:  # 1 year
                recommendations.append(f"Schedule maintenance for {node['metadata']['name']} - high uptime")
            elif node["ai_health_score"] < 0.7:
                recommendations.append(f"Investigate {node['metadata']['name']} - low health score")
        
        return recommendations if recommendations else ["No immediate maintenance required"]