# 🚀 Mock DevOps APIs Server

**AI-Optimized Mock API Ecosystem for Incident Response Testing**

A comprehensive mock server that simulates all major DevOps APIs with AI-friendly features, realistic data patterns, and advanced chaos engineering capabilities.

## 🌟 **Key Features**

### **🤖 AI-Optimized Design**
- **Parallel Agent Support** - Optimized for concurrent AI agent requests
- **Confidence Scoring** - Built-in confidence metrics for AI decision making
- **Realistic Data Patterns** - Production-like complexity without overwhelming AI systems
- **Performance Benchmarking** - Built-in metrics for AI system evaluation

### **📊 Comprehensive API Coverage**
- **8 Major DevOps APIs** - Complete ecosystem simulation
- **Advanced Chaos Engineering** - AI-testable incident generation
- **Historical Data Simulation** - Pattern matching and learning capabilities
- **Real-time Metrics** - Dynamic data generation with time-based patterns

## 🏗️ **Architecture**

```
mock_server/
├── main.py                     # FastAPI server with all endpoints
├── start_server.py            # Easy startup script with options
├── apis/                      # Individual mock API implementations
│   ├── elasticsearch_mock.py  # Log analysis & search
│   ├── kubernetes_mock.py     # Container orchestration
│   ├── jira_mock.py          # Historical incident analysis
│   ├── slack_mock.py         # Team communication
│   ├── prometheus_mock.py    # Metrics & monitoring
│   ├── aws_mock.py           # Cloud infrastructure
│   ├── datadog_mock.py       # Comprehensive monitoring
│   └── pagerduty_mock.py     # Incident escalation
├── scenarios/                 # Chaos engineering
│   └── incident_generator.py # Advanced incident generation
└── README.md                 # This file
```

## 🚀 **Quick Start**

### **Installation**
```bash
# Navigate to mock server directory
cd mock_server

# Install dependencies (if not already installed)
pip install fastapi uvicorn faker

# Start server with defaults
python start_server.py
```

### **Custom Configuration**
```bash
# Custom port and host
python start_server.py --host 0.0.0.0 --port 8080

# Development mode with auto-reload
python start_server.py --reload

# Production mode with multiple workers
python start_server.py --workers 4 --log-level info

# Enable access logging
python start_server.py --access-log
```

### **Alternative Startup**
```bash
# Direct uvicorn startup
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or using Python module
python -m uvicorn main:app --reload
```

## 📋 **API Endpoints**

### **🔍 Core Information**
- `GET /` - Server info and available endpoints
- `GET /health` - Health check with service status
- `GET /metrics` - Server metrics and statistics

### **🔍 Elasticsearch Mock**
- `GET /elasticsearch/search` - Search logs with AI-friendly filters
- `GET /elasticsearch/logs/{service}` - Service-specific logs with analysis

### **☸️ Kubernetes Mock**
- `GET /kubernetes/pods` - Pod status with health metrics
- `GET /kubernetes/pods/{pod}/logs` - Pod logs for AI analysis
- `GET /kubernetes/nodes` - Node health for diagnostics
- `POST /kubernetes/pods/{pod}/restart` - Restart pod (remediation)

### **🎫 Jira Mock**
- `GET /jira/incidents` - Historical incidents for pattern matching
- `GET /jira/incidents/similar` - AI-powered similar incident matching
- `POST /jira/incidents` - Create incident (AI-generated)

### **💬 Slack Mock**
- `POST /slack/notify` - Send AI-generated notifications
- `POST /slack/create-incident-channel` - Create incident coordination channel

### **📊 Prometheus Mock**
- `GET /prometheus/query` - Query metrics with AI context
- `GET /prometheus/metrics/{service}` - Service metrics for analysis
- `GET /prometheus/alerts` - Active alerts for AI processing

### **☁️ AWS Mock**
- `GET /aws/cloudwatch/logs` - CloudWatch logs for analysis
- `GET /aws/ec2/instances` - EC2 instances for diagnostics
- `POST /aws/ec2/instances/{id}/restart` - Restart instance (remediation)

### **🐕 Datadog Mock**
- `GET /datadog/metrics` - Comprehensive metrics for AI analysis
- `GET /datadog/service-summary/{service}` - Service health summary
- `GET /datadog/dashboards` - Dashboard information
- `GET /datadog/alerts` - Alert management
- `GET /datadog/logs` - Log analysis with AI insights

### **📟 PagerDuty Mock**
- `GET /pagerduty/incidents` - Incident management for AI analysis
- `POST /pagerduty/incidents` - Create incident (AI-generated)
- `POST /pagerduty/incidents/{id}/resolve` - Resolve incident
- `GET /pagerduty/oncall-users` - On-call information for escalation

### **🌪️ Chaos Engineering**
- `POST /chaos/generate-incident` - Generate AI-testable incidents
- `POST /chaos/generate-multi-service-incident` - Complex multi-service incidents
- `GET /chaos/active-incidents` - Active incidents for AI processing
- `POST /chaos/resolve-incident/{id}` - Resolve with AI performance tracking

## 🤖 **AI Optimization Features**

### **Confidence Scoring**
Every API response includes AI confidence metrics:
```json
{
  "data": "...",
  "ai_analysis": {
    "confidence": 0.85,
    "pattern_detected": true,
    "anomaly_score": 0.3,
    "recommended_action": "investigate_further"
  }
}
```

### **Parallel Processing Support**
- **Concurrent Request Handling** - Optimized for multiple AI agents
- **Stateless Design** - No conflicts between parallel requests
- **Performance Metrics** - Built-in timing and efficiency tracking

### **Realistic Data Patterns**
- **Time-based Variations** - Daily/hourly patterns in metrics
- **Service Dependencies** - Realistic inter-service relationships
- **Failure Correlations** - Cascading effects and root cause chains

## 🌪️ **Advanced Chaos Engineering**

### **Incident Types**
- `database_timeout` - Connection and query timeouts
- `memory_leak` - Gradual memory exhaustion
- `service_crash` - Container crashes and restarts
- `high_cpu` - CPU saturation and performance issues
- `network_issue` - Connectivity and DNS problems
- `disk_full` - Storage exhaustion

### **AI Testing Modes**
```bash
# Generate incidents for confidence testing
curl -X POST "http://localhost:8000/chaos/generate-incident" \
  -H "Content-Type: application/json" \
  -d '{"scenario_type": "database_timeout", "ai_test_mode": "confidence_testing"}'

# Generate complex multi-service incidents
curl -X POST "http://localhost:8000/chaos/generate-multi-service-incident"

# Get active incidents for AI processing
curl "http://localhost:8000/chaos/active-incidents"
```

### **Incident Complexity Levels**
- **Simple** - Single service, clear symptoms, high confidence
- **Medium** - Multiple symptoms, moderate complexity
- **Complex** - Multi-factor issues, noise, lower confidence
- **Multi-Service** - Cascading effects, coordination required

## 📊 **Example Usage**

### **Basic Incident Generation**
```bash
# Generate a database timeout incident
curl -X POST "http://localhost:8000/chaos/generate-incident" \
  -H "Content-Type: application/json" \
  -d '{"scenario_type": "database_timeout"}'

# Response includes AI-optimized data
{
  "incident_id": "INC-1234",
  "type": "database_timeout",
  "service": "payment-service",
  "severity": "P2",
  "ai_testing": {
    "confidence_target": 0.85,
    "complexity_level": "medium",
    "expected_agent_responses": {...},
    "performance_benchmarks": {...}
  }
}
```

### **Search Logs for AI Analysis**
```bash
# Search for error logs
curl "http://localhost:8000/elasticsearch/search?q=error&severity=error"

# Get service-specific logs
curl "http://localhost:8000/elasticsearch/logs/payment-service?hours=2"
```

### **Get Service Metrics**
```bash
# Get comprehensive service metrics
curl "http://localhost:8000/prometheus/metrics/payment-service?duration=1h"

# Get Datadog service summary
curl "http://localhost:8000/datadog/service-summary/payment-service"
```

### **AI Agent Workflow Simulation**
```bash
# 1. Generate incident
INCIDENT=$(curl -s -X POST "http://localhost:8000/chaos/generate-incident")
INCIDENT_ID=$(echo $INCIDENT | jq -r '.incident_id')

# 2. Gather investigation data (parallel)
curl "http://localhost:8000/elasticsearch/logs/payment-service" &
curl "http://localhost:8000/prometheus/metrics/payment-service" &
curl "http://localhost:8000/kubernetes/pods" &
wait

# 3. Get historical matches
curl "http://localhost:8000/jira/incidents/similar?error_type=database_timeout&service=payment-service"

# 4. Resolve incident
curl -X POST "http://localhost:8000/chaos/resolve-incident/$INCIDENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"resolution_method": "auto", "ai_performance_data": {"overall_confidence": 0.87}}'
```

## 🔧 **Configuration Options**

### **Server Configuration**
```bash
# Basic options
python start_server.py --host 0.0.0.0 --port 8080

# Development
python start_server.py --reload --log-level debug

# Production
python start_server.py --workers 4 --log-level info --access-log
```

### **Environment Variables**
```bash
# Optional environment configuration
export MOCK_SERVER_HOST=0.0.0.0
export MOCK_SERVER_PORT=8000
export MOCK_SERVER_LOG_LEVEL=info
```

## 📈 **Performance & Monitoring**

### **Built-in Metrics**
- Request/response times
- Concurrent request handling
- AI confidence score distributions
- Incident generation statistics

### **Health Monitoring**
```bash
# Check server health
curl "http://localhost:8000/health"

# Get server metrics
curl "http://localhost:8000/metrics"
```

## 🧪 **Testing & Validation**

### **API Testing**
```bash
# Test all endpoints
python -m pytest tests/ -v

# Test specific API
curl "http://localhost:8000/" | jq '.'
```

### **AI System Integration**
```python
# Python client example
import requests

# Generate test incident
response = requests.post("http://localhost:8000/chaos/generate-incident", 
                        json={"scenario_type": "service_crash"})
incident = response.json()

# Process with AI agents (your implementation)
ai_result = process_with_ai_agents(incident)

# Report performance
requests.post(f"http://localhost:8000/chaos/resolve-incident/{incident['incident_id']}", 
              json={"resolution_method": "auto", "ai_performance_data": ai_result})
```

## 🔍 **Troubleshooting**

### **Common Issues**

**Port Already in Use**
```bash
# Check what's using the port
lsof -i :8000

# Use different port
python start_server.py --port 8080
```

**Missing Dependencies**
```bash
# Install required packages
pip install fastapi uvicorn faker

# Or install from requirements.txt (if available)
pip install -r requirements.txt
```

**Import Errors**
```bash
# Make sure you're in the mock_server directory
cd mock_server
python start_server.py
```

### **Validation**
```bash
# Validate environment
python start_server.py --help

# Check API documentation
open http://localhost:8000/docs
```

## 🚀 **Integration with AI Systems**

### **Compatible with:**
- **CrewAI Multi-Agent Systems** - Optimized for parallel agent workflows
- **LangChain Applications** - Structured data for LLM processing
- **Custom AI Frameworks** - RESTful API with JSON responses
- **Monitoring Integrations** - Real-time metrics and health checks

### **AI-Friendly Features:**
- **Structured JSON Responses** - Consistent, parseable data formats
- **Confidence Scoring** - Built-in uncertainty quantification
- **Performance Benchmarking** - Automated AI system evaluation
- **Realistic Complexity** - Production-like scenarios without overwhelming complexity

## 📄 **API Documentation**

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🤝 **Contributing**

This mock server is designed to support AI-powered incident response systems. Contributions welcome for:
- Additional API endpoints
- Enhanced AI testing scenarios
- Performance optimizations
- Documentation improvements

## 📞 **Support**

For issues or questions:
1. Check the interactive API documentation at `/docs`
2. Validate your environment with the startup script
3. Review the comprehensive logging output
4. Test individual endpoints with curl or your HTTP client

---

**🎯 Ready to power your AI-driven incident response system with realistic, comprehensive mock data!** 🚀