#!/usr/bin/env python3
"""
Mock DevOps APIs Server Startup Script
Easy startup with configuration options for AI-powered incident response testing
"""

import os
import sys
import argparse
import uvicorn
from pathlib import Path

def main():
    """Main startup function with configuration options"""
    
    parser = argparse.ArgumentParser(
        description="Mock DevOps APIs Server for AI-Powered Incident Response",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_server.py                    # Start with defaults
  python start_server.py --port 8080       # Custom port
  python start_server.py --host 0.0.0.0    # Bind to all interfaces
  python start_server.py --reload          # Enable auto-reload for development
  python start_server.py --workers 4       # Multiple workers for production
        """
    )
    
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    
    parser.add_argument(
        "--reload", 
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    parser.add_argument(
        "--workers", 
        type=int, 
        default=1,
        help="Number of worker processes (default: 1)"
    )
    
    parser.add_argument(
        "--log-level", 
        choices=["critical", "error", "warning", "info", "debug"],
        default="info",
        help="Log level (default: info)"
    )
    
    parser.add_argument(
        "--access-log", 
        action="store_true",
        help="Enable access logging"
    )
    
    args = parser.parse_args()
    
    # Print startup banner
    print_startup_banner(args)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Start server
    try:
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers if not args.reload else 1,  # Reload doesn't work with multiple workers
            log_level=args.log_level,
            access_log=args.access_log
        )
    except KeyboardInterrupt:
        print("\n👋 Mock DevOps APIs Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

def print_startup_banner(args):
    """Print startup banner with configuration info"""
    
    print("🚀 Mock DevOps APIs Server for AI-Powered Incident Response")
    print("=" * 70)
    print("🤖 AI-Optimized Features:")
    print("   • Parallel agent request support")
    print("   • Realistic data simulation with confidence scoring")
    print("   • Advanced chaos engineering with AI test patterns")
    print("   • Comprehensive mock API ecosystem (8 services)")
    print("   • Performance benchmarking and metrics")
    print()
    print("🔧 Server Configuration:")
    print(f"   • Host: {args.host}")
    print(f"   • Port: {args.port}")
    print(f"   • Workers: {args.workers}")
    print(f"   • Log Level: {args.log_level}")
    print(f"   • Auto-reload: {'Enabled' if args.reload else 'Disabled'}")
    print(f"   • Access Log: {'Enabled' if args.access_log else 'Disabled'}")
    print()
    print("📊 Available APIs:")
    print("   • Elasticsearch - Log analysis and search")
    print("   • Kubernetes - Container orchestration")
    print("   • Jira - Historical incident analysis")
    print("   • Slack - Team communication")
    print("   • Prometheus - Metrics and monitoring")
    print("   • AWS - Cloud infrastructure")
    print("   • Datadog - Comprehensive monitoring")
    print("   • PagerDuty - Incident escalation")
    print("   • Chaos Engineering - Advanced incident generation")
    print()
    print("🌐 Quick Access URLs:")
    print(f"   • API Documentation: http://{args.host}:{args.port}/docs")
    print(f"   • Health Check: http://{args.host}:{args.port}/health")
    print(f"   • Generate Incident: POST http://{args.host}:{args.port}/chaos/generate-incident")
    print("=" * 70)
    print("🎯 Ready for AI-powered incident response testing!")
    print()

def validate_environment():
    """Validate environment and dependencies"""
    
    print("🔍 Validating environment...")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Please run from the mock_server directory.")
        return False
    
    # Check required directories
    required_dirs = ["apis", "scenarios"]
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            print(f"❌ Required directory '{dir_name}' not found.")
            return False
    
    # Check required files
    required_files = [
        "apis/__init__.py",
        "apis/elasticsearch_mock.py",
        "apis/kubernetes_mock.py",
        "apis/jira_mock.py",
        "apis/slack_mock.py",
        "apis/prometheus_mock.py",
        "apis/aws_mock.py",
        "apis/datadog_mock.py",
        "apis/pagerduty_mock.py",
        "scenarios/__init__.py",
        "scenarios/incident_generator.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Required file '{file_path}' not found.")
            return False
    
    # Try importing required modules
    try:
        import fastapi
        import uvicorn
        import faker
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install fastapi uvicorn faker")
        return False
    
    print("✅ Environment validation passed")
    return True

def check_port_availability(host: str, port: int) -> bool:
    """Check if port is available"""
    
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            return True
    except OSError:
        return False

if __name__ == "__main__":
    main()