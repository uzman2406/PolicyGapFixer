
import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

def run_ollama(prompt, model="llama3.2:3b", timeout=90):
    """Run Ollama via CLI with better error handling"""
    try:
      
        clean_prompt = prompt[:250].strip()
        
        print(f"    Prompt: {clean_prompt[:50]}...")
        
        result = subprocess.run(
            ["ollama", "run", model, clean_prompt],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            
            import re
            output = re.sub(r'\s+', ' ', output) 
            return output[:500]  
        else:
            error_msg = result.stderr[:100] if result.stderr else "Unknown error"
            return f"Error: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return "Timeout: Model took too long to respond"
    except Exception as e:
        return f"Exception: {str(e)[:100]}"

def main():
    print(" Simple PolicyGapFixer (CLI Version)")
    
    if len(sys.argv) < 2:
        print("Usage: python simple_main.py <policy_file>")
        return
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r') as f:
        policy = f.read()
    
    policy_name = Path(file_path).stem
    
    print(f"\n Processing: {policy_name}")
    print(f" Size: {len(policy)} chars")
    
    
    print("\n🔍 Analyzing...")
    analysis_prompt = f"List 2 strengths and 2 weaknesses of this policy: {policy[:150]}"
    analysis = run_ollama(analysis_prompt, timeout=60)
    print(f" Analysis: {analysis[:50]}...")
    
    
    print("\n  Revising...")
    revision_prompt = f"Suggest 3 specific improvements for: {policy[:100]}"
    revision = run_ollama(revision_prompt, timeout=60)
    print(f" Revision: {revision[:50]}...")
    
 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"outputs/{policy_name}_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "analysis.txt", 'w') as f:
        f.write(analysis)
    
    with open(output_dir / "revision.txt", 'w') as f:
        f.write(revision)
    
    with open(output_dir / "original.txt", 'w') as f:
        f.write(policy)
    
    print(f"\n Saved to: {output_dir}")
    print(f"\nAnalysis preview: {analysis[:100]}...")
    print(f"Revision preview: {revision[:100]}...")

if __name__ == "__main__":
    main()