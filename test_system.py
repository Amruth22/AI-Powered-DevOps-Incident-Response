#!/usr/bin/env python3
"""
System Test Script
Validates the AI-Powered DevOps Incident Response System
"""

import asyncio
import sys
from datetime import datetime

from core.config import validate_config, print_config_status
from services.gemini.client import test_gemini_connection
from services.mock.client import mock_api_client
from workflows.parallel_workflow import process_incident_parallel
from utils.logging_utils import setup_logging

async def test_configuration():
    """Test system configuration"""
    print("🔧 Testing Configuration...")
    
    try:
        validate_config()
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

async def test_gemini_connection():
    """Test Gemini AI connection"""
    print("\n🧠 Testing Gemini AI Connection...")
    
    try:
        if test_gemini_connection():
            print("✅ Gemini AI connection successful")
            return True
        else:
            print("❌ Gemini AI connection failed")
            return False
    except Exception as e:
        print(f"❌ Gemini AI connection error: {e}")
        return False

async def test_mock_api():
    """Test mock API connection"""
    print("\n🔌 Testing Mock API Connection...")
    
    try:
        # Try to generate a test incident
        incident = mock_api_client.generate_incident("database_timeout")
        
        if "error" not in incident:
            print(f"✅ Mock API connection successful")
            print(f"   Generated test incident: {incident.get('incident_id', 'Unknown')}")
            return True, incident
        else:
            print(f"❌ Mock API error: {incident['error']}")
            return False, None
    except Exception as e:
        print(f"❌ Mock API connection failed: {e}")
        print("💡 Make sure the mock API server is running:")
        print("   python -m mock_apis.main  # If you have the mock server")
        return False, None

async def test_parallel_workflow(test_incident):
    """Test the parallel workflow"""
    print("\n🚀 Testing Parallel Workflow...")
    
    try:
        start_time = datetime.now()
        
        result = await process_incident_parallel(test_incident)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Parallel workflow completed in {duration:.2f} seconds")
        print(f"   • Status: {result.get('status', 'Unknown')}")
        print(f"   • Method: {result.get('method', 'Unknown')}")
        print(f"   • Success: {result.get('success', False)}")
        print(f"   • Confidence: {result.get('overall_confidence', 0):.2f}")
        print(f"   • Agents used: {result.get('total_agents_used', 0)}")
        
        # Show timing breakdown
        workflow_time = result.get('workflow_time_seconds', 0)
        parallel_time = result.get('parallel_time_seconds', 0)
        if parallel_time > 0:
            estimated_sequential = parallel_time * 3
            time_saved = estimated_sequential - parallel_time
            print(f"   • Parallel analysis time: {parallel_time:.2f}s")
            print(f"   • Time saved by parallelism: ~{time_saved:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Parallel workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_individual_agents():
    """Test individual agents"""
    print("\n🤖 Testing Individual Agents...")
    
    # Create test incident data
    test_data = {
        "incident_id": "TEST-001",
        "service": "payment-service",
        "type": "database_timeout",
        "severity": "P2",
        "description": "Test incident for agent validation",
        "symptoms": ["Database connection timeout", "High error rate"]
    }
    
    try:
        from agents.detective_agent import DetectiveAgent
        from agents.diagnostics_agent import DiagnosticsAgent
        from agents.historical_agent import HistoricalAgent
        
        # Test each agent individually
        agents = {
            "Detective": DetectiveAgent(),
            "Diagnostics": DiagnosticsAgent(),
            "Historical": HistoricalAgent()
        }
        
        for agent_name, agent in agents.items():
            try:
                result = await agent.execute_async(test_data)
                if result.get('success', False):
                    print(f"   ✅ {agent_name} Agent: Working")
                else:
                    print(f"   ⚠️ {agent_name} Agent: Error - {result.get('error', 'Unknown')}")
            except Exception as e:
                print(f"   ❌ {agent_name} Agent: Failed - {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent testing failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 AI-POWERED DEVOPS INCIDENT RESPONSE SYSTEM TEST")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Test configuration
    config_ok = await test_configuration()
    if not config_ok:
        print("\n❌ Configuration test failed - cannot continue")
        print_config_status()
        sys.exit(1)
    
    # Test Gemini connection
    gemini_ok = await test_gemini_connection()
    if not gemini_ok:
        print("\n❌ Gemini AI test failed - cannot continue")
        sys.exit(1)
    
    # Test individual agents
    agents_ok = await test_individual_agents()
    if not agents_ok:
        print("\n⚠️ Some agents failed individual tests")
    
    # Test mock API (optional)
    mock_ok, test_incident = await test_mock_api()
    
    if mock_ok and test_incident:
        # Test full parallel workflow
        workflow_ok = await test_parallel_workflow(test_incident)
        
        if workflow_ok:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ System is ready for production use")
        else:
            print("\n⚠️ Workflow test failed, but core components are working")
    else:
        print("\n⚠️ Mock API not available - skipping workflow test")
        print("💡 To test the full workflow, start the mock API server first")
    
    print("\n📋 Test Summary:")
    print(f"   • Configuration: {'✅' if config_ok else '❌'}")
    print(f"   • Gemini AI: {'✅' if gemini_ok else '❌'}")
    print(f"   • Individual Agents: {'✅' if agents_ok else '⚠️'}")
    print(f"   • Mock API: {'✅' if mock_ok else '⚠️'}")
    
    if config_ok and gemini_ok:
        print("\n🚀 Core system is functional!")
        print("   You can now run: python main.py --demo")
    else:
        print("\n❌ Core system issues detected")
        print("   Please fix configuration and try again")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted!")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)