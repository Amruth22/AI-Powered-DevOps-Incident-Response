#!/usr/bin/env python3
"""
AI-Powered DevOps Incident Response System
Professional parallel multi-agent system with CrewAI and Gemini LLM
"""

import sys
import argparse
import asyncio
import os
from datetime import datetime

from workflows.parallel_workflow import process_incident_parallel
from services.mock.client import mock_api_client
from utils.logging_utils import setup_logging
from core.config import config, validate_config, print_config_status

def main():
    """Main application entry point"""
    
    parser = argparse.ArgumentParser(
        description="AI-Powered DevOps Incident Response System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Payment API database timeout"
  python main.py --demo
  python main.py --test
  python main.py --config  # Show configuration status
        """
    )
    
    # Demo option
    parser.add_argument(
        "--demo", "-d", 
        action="store_true",
        help="Run interactive demo with sample scenarios"
    )
    
    # Test option
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run system test with generated incident"
    )
    
    # Config option
    parser.add_argument(
        "--config", "-c",
        action="store_true",
        help="Show current configuration status"
    )
    
    # Alert text (positional argument)
    parser.add_argument(
        "alert", 
        nargs="*", 
        help="Incident alert text to process"
    )
    
    args = parser.parse_args()
    
    # Show configuration status if requested
    if args.config:
        print_config_status()
        return
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("WARNING: .env file not found!")
        print("\nSetup Instructions:")
        print("1. Copy the example file: cp .env.example .env")
        print("2. Edit .env and update GEMINI_API_KEY with your actual key")
        print("3. Get your API key from: https://makersuite.google.com/app/apikey")
        print("4. Run the application again")
        sys.exit(1)
    
    # Validate configuration
    try:
        validate_config()
        print("SUCCESS: Configuration validated successfully")
    except ValueError as e:
        print(f"ERROR: Configuration Error: {e}")
        print("\nCurrent Configuration Status:")
        print_config_status()
        sys.exit(1)
    
    # Setup logging
    setup_logging()
    
    # Handle different modes
    if args.demo:
        asyncio.run(run_demo())
    elif args.test:
        asyncio.run(run_test())
    elif args.alert:
        alert_text = " ".join(args.alert)
        asyncio.run(run_incident_response(alert_text))
    else:
        # Interactive mode
        asyncio.run(run_interactive_mode())

async def run_incident_response(alert_text: str):
    """Run the parallel multi-agent workflow"""
    print("PARALLEL MULTI-AGENT INCIDENT RESPONSE")
    print("=" * 50)
    start_time = datetime.now()
    
    try:
        # Create incident data from alert text
        incident_data = {
            "description": alert_text,
            "service": extract_service_from_alert(alert_text),
            "type": extract_type_from_alert(alert_text),
            "severity": "P2",  # Default severity
            "symptoms": [alert_text]
        }
        
        result = await process_incident_parallel(incident_data)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\nWorkflow completed in {duration:.2f} seconds")
        print_workflow_summary(result)
        
    except Exception as e:
        print(f"ERROR: Workflow error: {e}")
        import traceback
        traceback.print_exc()

async def run_test():
    """Run system test with generated incident"""
    print("SYSTEM TEST - Parallel Multi-Agent Processing")
    print("=" * 50)
    
    try:
        # Generate test incident
        incident = mock_api_client.generate_incident("database_timeout")
        
        if "error" not in incident:
            print(f"SUCCESS: Test incident generated: {incident['incident_id']}")
            
            # Process with parallel workflow
            result = await process_incident_parallel(incident)
            
            print(f"\nTEST RESULTS:")
            print(f"   • Success: {result.get('success', False)}")
            print(f"   • Method: {result.get('method', 'unknown')}")
            print(f"   • Confidence: {result.get('overall_confidence', 0):.2f}")
            print(f"   • Total workflow time: {result.get('workflow_time_seconds', 0):.2f}s")
            print(f"   • Parallel analysis time: {result.get('parallel_time_seconds', 0):.2f}s")
            
            # Calculate time savings
            parallel_time = result.get('parallel_time_seconds', 0)
            estimated_sequential_time = parallel_time * 3  # 3 agents in parallel
            time_saved = estimated_sequential_time - parallel_time
            print(f"   Time saved by parallel execution: ~{time_saved:.2f}s")
            
        else:
            print("ERROR: Could not generate test incident")
            print("HINT: Make sure the mock API server is running:")
            print("   python -m mock_apis.main  # If you have the mock server")
            
    except Exception as e:
        print(f"ERROR: Test error: {e}")

async def run_demo():
    """Run interactive demo with sample scenarios"""
    print("INTERACTIVE DEMO - Parallel AI-Powered Incident Response")
    print("=" * 55)
    
    scenarios = [
        {
            "name": "Database Timeout",
            "alert": "Payment API experiencing database connection timeouts and high error rates",
            "description": "High confidence scenario - should auto-resolve"
        },
        {
            "name": "Memory Leak",
            "alert": "Auth Service showing memory leak patterns and degraded performance",
            "description": "Medium confidence scenario - may require escalation"
        },
        {
            "name": "Network Issues",
            "alert": "Load balancer reporting uneven traffic distribution and connection failures",
            "description": "Complex scenario - likely escalation"
        },
        {
            "name": "Service Crash",
            "alert": "Order service crashed with high CPU usage and memory exhaustion",
            "description": "High confidence scenario - should auto-resolve"
        }
    ]
    
    print("Available Demo Scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario['name']} - {scenario['description']}")
    
    print("  5. Custom Alert - Enter your own incident")
    print("  0. Exit")
    
    while True:
        try:
            choice = input("\nSelect scenario (0-5): ").strip()
            
            if choice == "0":
                print("Demo completed!")
                break
            elif choice in ["1", "2", "3", "4"]:
                scenario = scenarios[int(choice) - 1]
                print(f"\nRunning scenario: {scenario['name']}")
                print(f"Alert: {scenario['alert']}")
                print("-" * 50)
                await run_incident_response(scenario['alert'])
                    
            elif choice == "5":
                custom_alert = input("Enter custom incident alert: ").strip()
                if custom_alert:
                    await run_incident_response(custom_alert)
                else:
                    print("ERROR: No alert provided")
                    
            else:
                print("ERROR: Invalid choice. Please select 0-5.")
                
        except KeyboardInterrupt:
            print("\nDemo interrupted!")
            break
        except Exception as e:
            print(f"ERROR: Demo error: {e}")

async def run_interactive_mode():
    """Interactive mode for single incident processing"""
    print("Parallel AI-Powered Incident Response System")
    print("=" * 45)
    print("Options:")
    print("  1. Process Incident Alert")
    print("  2. Interactive Demo")
    print("  3. System Test")
    print("  4. Show Configuration")
    print("  0. Exit")
    
    choice = input("\nSelect option (0-4): ").strip()
    
    if choice == "0":
        print("Goodbye!")
        return
    elif choice == "1":
        alert = input("Enter incident alert: ").strip()
        if alert:
            await run_incident_response(alert)
        else:
            print("ERROR: No alert provided")
    elif choice == "2":
        await run_demo()
    elif choice == "3":
        await run_test()
    elif choice == "4":
        print_config_status()
    else:
        print("ERROR: Invalid choice")

def extract_service_from_alert(alert: str) -> str:
    """Extract service name from alert text"""
    alert_lower = alert.lower()
    services = ["payment", "auth", "user", "order", "notification"]
    
    for service in services:
        if service in alert_lower:
            return f"{service}-service"
    
    return "unknown-service"

def extract_type_from_alert(alert: str) -> str:
    """Extract incident type from alert text"""
    alert_lower = alert.lower()
    
    if "database" in alert_lower or "timeout" in alert_lower:
        return "database_timeout"
    elif "memory" in alert_lower or "leak" in alert_lower:
        return "memory_leak"
    elif "crash" in alert_lower or "down" in alert_lower:
        return "service_crash"
    elif "cpu" in alert_lower or "high" in alert_lower:
        return "high_cpu"
    elif "network" in alert_lower or "connection" in alert_lower:
        return "network_issue"
    elif "disk" in alert_lower or "space" in alert_lower:
        return "disk_full"
    else:
        return "unknown_issue"

def print_workflow_summary(result: dict):
    """Print a summary of workflow results"""
    print(f"\nWORKFLOW SUMMARY")
    print("-" * 40)
    print(f"Incident ID: {result.get('incident_id', 'Unknown')}")
    print(f"Final Status: {result.get('status', 'Unknown').upper()}")
    print(f"Method: {result.get('method', 'Unknown')}")
    print(f"Success: {result.get('success', False)}")
    print(f"Overall Confidence: {result.get('overall_confidence', 0):.2f}")
    
    if result.get('reason'):
        print(f"Reason: {result['reason']}")
    
    # Show agent results
    agent_results = result.get('agent_results', {})
    if agent_results:
        print(f"Agents Completed: {len(agent_results)}")
    
    # Show timing information
    workflow_time = result.get('workflow_time_seconds', 0)
    parallel_time = result.get('parallel_time_seconds', 0)
    if workflow_time > 0:
        print(f"Workflow Time: {workflow_time:.2f}s")
    if parallel_time > 0:
        print(f"Parallel Analysis Time: {parallel_time:.2f}s")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication interrupted!")
    except Exception as e:
        print(f"ERROR: Application error: {e}")
        sys.exit(1)