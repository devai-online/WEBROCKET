#!/usr/bin/env python3
"""
Startup script for the Blog Generator UI
This will start the Flask UI and provide instructions for the backend
"""

import subprocess
import sys
import time
import requests
from flask_ui import app

def check_backend():
    """Check if the FastAPI backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 Blog Generator UI Startup")
    print("=" * 50)
    
    # Check if backend is running
    print("🔍 Checking backend connection...")
    if check_backend():
        print("✅ Backend is running and accessible!")
    else:
        print("⚠️  Backend is not running!")
        print("\n📋 To start the backend, run in a separate terminal:")
        print("   cd backend")
        print("   python main.py")
        print("\n⏳ Waiting for backend to start...")
        
        # Wait for backend to start
        for i in range(30):  # Wait up to 30 seconds
            if check_backend():
                print("✅ Backend is now running!")
                break
            time.sleep(1)
            if i % 5 == 0:
                print(f"   Still waiting... ({i+1}/30)")
        else:
            print("❌ Backend did not start. Please start it manually.")
            print("   The UI will still work but blog generation will fail.")
    
    print("\n🌐 Starting Flask UI...")
    print("📱 UI will be available at: http://localhost:5000")
    print("🔧 Backend API: http://localhost:8000")
    print("\n💡 Usage:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Enter a blog topic")
    print("   3. Choose your options")
    print("   4. Click 'Generate Blog'")
    print("\n🛑 Press Ctrl+C to stop the UI")
    print("=" * 50)
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 UI stopped. Goodbye!")
        sys.exit(0) 