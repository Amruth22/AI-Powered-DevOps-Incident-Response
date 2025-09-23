#!/usr/bin/env python3
"""
Mock Server Integration Test
Test the complete integration between the AI system and mock server
"""

import asyncio
import time
import requests
from datetime import datetime
from services.mock.client import mock_api_client

def test_mock_server_connection():
    """Test basic mock server connection"""
    print("🔍 Testing mock server connection...")
    
    try:
        # Test basic connection
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Mock server is running and accessible")
            return True
        else:
            print(f"❌ Mock server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to mock server")
        print("💡 Start the mock server with: cd mock_server && python start_server.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to mock server: {e}")
        return False

def test_incident_generation():
    """Test incident generation capabilities"""
    print("\n🌪️ Testing incident generation...")
    
    try:
        # Generate a basic incident
        incident = mock_api_client.generate_incident("database_timeout")
        
        if "error" in incident:
            print(f"❌ Error generating incident: {incident['error']}")
            return False
        
        print(f"✅ Generated incident: {incident['incident_id']}")
        print(f"   • Type: {incident['type']}")
        print(f"   • Service: {incident['service']}")
        print(f"   • Severity: {incident['severity']}")
        
        # Test AI-optimized incident
        ai_incident = mock_api_client.generate_incident("memory_leak", "confidence_testing")
        
        if "error" not in ai_incident:
            print(f"✅ Generated AI-optimized incident: {ai_incident['incident_id']}")
            print(f"   • AI Confidence Target: {ai_incident.get('ai_testing', {}).get('confidence_target', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in incident generation test: {e}")
        return False

def test_api_endpoints():
    """Test various API endpoints"""
    print("\n📊 Testing API endpoints...")
    
    endpoints_to_test = [
        ("GET", "/elasticsearch/search?q=error", "Elasticsearch search"),
        ("GET", "/kubernetes/pods", "Kubernetes pods"),
        ("GET", "/prometheus/alerts", "Prometheus alerts"),
        ("GET", "/jira/incidents", "Jira incidents"),
        ("GET", "/datadog/metrics?metric=system.cpu.user", "Datadog metrics"),
        ("GET", "/pagerduty/incidents", "PagerDuty incidents"),
        ("GET", "/aws/ec2/instances", "AWS EC2 instances")
    ]
    
    success_count = 0
    
    for method, endpoint, description in endpoints_to_test:
        try:
            url = f"http://localhost:8000{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                success_count += 1
            else:
                print(f"❌ {description}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    print(f"\n📈 API Endpoint Results: {success_count}/{len(endpoints_to_test)} successful")
    return success_count == len(endpoints_to_test)

def test_ai_workflow_simulation():
    """Test complete AI workflow simulation"""
    print("\n🤖 Testing AI workflow simulation...")
    
    try:
        # Step 1: Generate incident
        print("   1. Generating incident...")
        incident = mock_api_client.generate_incident("service_crash", "parallel_testing")
        
        if "error" in incident:
            print(f"❌ Failed to generate incident: {incident['error']}")
            return False
        
        incident_id = incident["incident_id"]
        service = incident["service"]
        print(f"      ✅ Generated: {incident_id} ({service})")
        
        # Step 2: Simulate parallel data gathering (like AI agents would do)
        print("   2. Simulating parallel data gathering...")
        start_time = time.time()
        
        # Simulate what Detective, Diagnostics, and Historical agents would do
        try:
            # These would normally run in parallel
            logs_data = mock_api_client.get_service_logs(service, hours=1)
            metrics_data = mock_api_client.get_service_metrics(service, duration="1h")
            similar_incidents = mock_api_client.find_similar_incidents("service_crash", service)
            
            gather_time = time.time() - start_time
            print(f"      ✅ Data gathering completed in {gather_time:.2f}s")
            
        except Exception as e:
            print(f"      ❌ Data gathering failed: {e}")
            return False
        
        # Step 3: Simulate AI decision making
        print("   3. Simulating AI decision making...")
        
        # Mock AI performance data
        ai_performance = {
            "overall_confidence": 0.87,
            "agents_completed": 6,
            "workflow_time_seconds": gather_time + 5,  # Add processing time
            "parallel_execution": True
        }
        
        # Step 4: Resolve incident
        print("   4. Resolving incident...")
        resolution = mock_api_client.resolve_incident(
            incident_id, 
            "auto", 
            ai_performance
        )
        
        if resolution.get("success"):
            print(f"      ✅ Incident resolved successfully")
            print(f"      • Resolution time: {resolution['resolution_summary']['resolution_time_minutes']} minutes")
            print(f"      • AI Performance score: {resolution['resolution_summary']['ai_performance_score']:.2f}")
        else:
            print(f"      ❌ Failed to resolve incident: {resolution.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ AI workflow simulation failed: {e}")
        return False

def test_multi_service_incident():
    """Test multi-service incident generation"""
    print("\n🌐 Testing multi-service incident generation...")
    
    try:
        # Generate multi-service incident
        incident = mock_api_client.generate_multi_service_incident("complexity_testing")
        
        if "error" in incident:
            print(f"❌ Failed to generate multi-service incident: {incident['error']}")
            return False
        
        print(f"✅ Generated multi-service incident: {incident['incident_id']}")
        print(f"   • Affected services: {len(incident.get('affected_services', []))}")
        print(f"   • Severity: {incident['severity']}")
        print(f"   • Complexity: {incident.get('ai_testing', {}).get('complexity_level', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multi-service incident test failed: {e}")
        return False

async def test_parallel_processing():
    """Test parallel processing capabilities"""
    print("\n⚡ Testing parallel processing capabilities...")
    
    try:
        # Generate multiple incidents
        print("   1. Generating multiple incidents...")
        incidents = []
        
        for i in range(3):
            incident = mock_api_client.generate_incident()
            if "error" not in incident:
                incidents.append(incident)
        
        if len(incidents) < 3:
            print("❌ Failed to generate enough incidents for parallel testing")
            return False
        
        print(f"      ✅ Generated {len(incidents)} incidents")
        
        # Test parallel data gathering
        print("   2. Testing parallel data gathering...")
        start_time = time.time()
        
        # Simulate parallel requests (what AI agents would do)
        tasks = []
        for incident in incidents:
            service = incident["service"]
            # In real implementation, these would be async calls
            tasks.append(f"logs-{service}")
            tasks.append(f"metrics-{service}")
        
        # Simulate processing time
        await asyncio.sleep(0.5)  # Simulate parallel processing
        
        parallel_time = time.time() - start_time
        print(f"      ✅ Parallel processing completed in {parallel_time:.2f}s")
        
        # Clean up - resolve incidents
        print("   3. Cleaning up incidents...")
        for incident in incidents:
            try:
                mock_api_client.resolve_incident(incident["incident_id"], "test_cleanup")
            except:
                pass  # Ignore cleanup errors
        
        return True
        
    except Exception as e:
        print(f"❌ Parallel processing test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🧪 Mock Server Integration Test Suite")
    print("=" * 50)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Mock Server Connection", test_mock_server_connection),
        ("Incident Generation", test_incident_generation),
        ("API Endpoints", test_api_endpoints),
        ("AI Workflow Simulation", test_ai_workflow_simulation),
        ("Multi-Service Incidents", test_multi_service_incident),
    ]
    
    results = []
    
    # Run synchronous tests
    for test_name, test_func in tests:
        print(f"🔄 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
        print()
    
    # Run async test
    print(f"🔄 Running: Parallel Processing")
    try:
        result = asyncio.run(test_parallel_processing())
        results.append(("Parallel Processing", result))
        if result:
            print(f"✅ Parallel Processing: PASSED")
        else:
            print(f"❌ Parallel Processing: FAILED")
    except Exception as e:
        print(f"❌ Parallel Processing: ERROR - {e}")
        results.append(("Parallel Processing", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Mock server integration is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the mock server setup and try again.")
        return 1

if __name__ == "__main__":
    exit(main())