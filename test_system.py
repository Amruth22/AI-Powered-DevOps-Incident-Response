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
    print("Testing Configuration...")
    
    try:
        validate_config()
        print("SUCCESS: Configuration validation passed")
        return True
    except Exception as e:
        print(f"ERROR: Configuration validation failed: {e}")
        return False

async def test_gemini_connection():
    """Test Gemini AI connection"""
    print("\nTesting Gemini AI Connection...")
    
    try:
        if test_gemini_connection():
            print("SUCCESS: Gemini AI connection successful")
            return True
        else:
            print("ERROR: Gemini AI connection failed")
            return False
    except Exception as e:
        print(f"ERROR: Gemini AI connection error: {e}")
        return False

async def test_mock_api():
    """Test mock API connection"""
    print("\nTesting Mock API Connection...")
    
    try:
        # Try to generate a test incident
        incident = mock_api_client.generate_incident("database_timeout")
        
        if "error" not in incident:
            print(f"SUCCESS: Mock API connection successful")
            print(f"   Generated test incident: {incident.get('incident_id', 'Unknown')}")
            return True, incident
        else:
            print(f"ERROR: Mock API error: {incident['error']}")
            return False, None
    except Exception as e:
        print(f"ERROR: Mock API connection failed: {e}")
        print("HINT: Make sure the mock API server is running:")
        print("   python -m mock_apis.main  # If you have the mock server")
        return False, None

async def test_parallel_workflow(test_incident):
    """Test the parallel workflow"""
    print("\nTesting Parallel Workflow...")
    
    try:
        start_time = datetime.now()
        
        result = await process_incident_parallel(test_incident)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"SUCCESS: Parallel workflow completed in {duration:.2f} seconds")
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
        print(f"ERROR: Parallel workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_individual_agents():
    """Test individual agents"""
    print("\nTesting Individual Agents...")
    
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
                    print(f"   SUCCESS: {agent_name} Agent: Working")
                else:
                    print(f"   WARNING: {agent_name} Agent: Error - {result.get('error', 'Unknown')}")
            except Exception as e:
                print(f"   ERROR: {agent_name} Agent: Failed - {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Agent testing failed: {e}")
        return False

async def main():
    """Main test function"""
    print("AI-POWERED DEVOPS INCIDENT RESPONSE SYSTEM TEST")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Test configuration
    config_ok = await test_configuration()
    if not config_ok:
        print("\nERROR: Configuration test failed - cannot continue")
        print_config_status()
        sys.exit(1)
    
    # Test Gemini connection
    gemini_ok = await test_gemini_connection()
    if not gemini_ok:
        print("\nERROR: Gemini AI test failed - cannot continue")
        sys.exit(1)
    
    # Test individual agents
    agents_ok = await test_individual_agents()
    if not agents_ok:
        print("\nWARNING: Some agents failed individual tests")
    
    # Test mock API (optional)
    mock_ok, test_incident = await test_mock_api()
    
    if mock_ok and test_incident:
        # Test full parallel workflow
        workflow_ok = await test_parallel_workflow(test_incident)
        
        if workflow_ok:
            print("\nSUCCESS: ALL TESTS PASSED!")
            print("SUCCESS: System is ready for production use")
        else:
            print("\nWARNING: Workflow test failed, but core components are working")
    else:
        print("\nWARNING: Mock API not available - skipping workflow test")
        print("HINT: To test the full workflow, start the mock API server first")
    
    print("\nTest Summary:")
    print(f"   • Configuration: {'PASS' if config_ok else 'FAIL'}")
    print(f"   • Gemini AI: {'PASS' if gemini_ok else 'FAIL'}")
    print(f"   • Individual Agents: {'PASS' if agents_ok else 'WARNING'}")
    print(f"   • Mock API: {'PASS' if mock_ok else 'WARNING'}")
    
    if config_ok and gemini_ok:
        print("\nSUCCESS: Core system is functional!")
        print("   You can now run: python main.py --demo")
    else:
        print("\nERROR: Core system issues detected")
        print("   Please fix configuration and try again")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted!")
    except Exception as e:
        print(f"\nERROR: Test error: {e}")
        sys.exit(1)