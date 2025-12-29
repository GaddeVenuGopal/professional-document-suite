#!/usr/bin/env python3
"""
Deployment script for Professional Document Suite on Replicate
"""
import os
import subprocess
import sys


def deploy_to_replicate():
    """
    Deploy the model to Replicate using the cog command
    """
    print("Deploying Professional Document Suite to Replicate...")
    
    # Check if cog is installed
    try:
        result = subprocess.run(["cog", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Cog is not installed. Please install it with: pip install cog")
            return False
    except FileNotFoundError:
        print("Cog is not installed. Please install it with: pip install cog")
        return False
    
    # Check if REPLICATE_API_TOKEN is set
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("REPLICATE_API_TOKEN environment variable is not set.")
        print("Please set it with: export REPLICATE_API_TOKEN=your_token_here")
        return False
    
    # Run the deployment command
    try:
        print("Building and pushing the model to Replicate...")
        result = subprocess.run([
            "cog", "push", "r8.im/your-username/professional-document-suite"
        ], check=True)
        
        print("Successfully deployed to Replicate!")
        print("Your model is now available at: https://replicate.com/your-username/professional-document-suite")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Deployment failed: {e}")
        return False


def main():
    print("Professional Document Suite - Replicate Deployment Tool")
    print("=" * 55)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("\nUsage: python deploy_replicate.py")
        print("\nThis script will deploy the Professional Document Suite to Replicate.")
        print("Before running, make sure you have:")
        print("1. Installed cog: pip install cog")
        print("2. Set your REPLICATE_API_TOKEN environment variable")
        print("3. Updated your username in the deployment command")
        return
    
    deploy_to_replicate()


if __name__ == "__main__":
    main()