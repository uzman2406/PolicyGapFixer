import sys
import os
import time


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print("=" * 60)
print("POLICYGAPFIXER - QUICK TEST")
print("=" * 60)

print(f"Current directory: {current_dir}")
print(f"Added to path: {parent_dir}")

try:
    
    from main import PolicyGapFixer
    print("Successfully imported PolicyGapFixer")
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import method...")
    
   
    import importlib.util
    spec = importlib.util.spec_from_file_location("main", "main.py")
    main_module = importlib.util.module_from_spec(spec)
    sys.modules["main"] = main_module
    spec.loader.exec_module(main_module)
    PolicyGapFixer = main_module.PolicyGapFixer
    print("Loaded PolicyGapFixer using alternative method")

def test_simple():
    """Simple test function"""
    
    try:
        import requests
        response = requests.get("http://localhost:11434", timeout=5)
        if "Ollama is running" not in response.text:
            print("Ollama may not be running properly")
    except:
        print("Cannot connect to Ollama. Is it running?")
        print("   Try: ollama serve &")
        return False
    
    # Test with a simple policy
    test_policy = """INFORMATION SECURITY POLICY

1.0 PURPOSE
Protect company data and systems.

2.0 SCOPE
All employees and systems.

3.0 BASIC RULES
- Use strong passwords
- Lock computers when away
- Report suspicious emails

END OF POLICY"""
    
    print(f"\nTesting with simple policy...")
    print(f"Policy length: {len(test_policy)} characters")
    
    # Initialize
    print("\nInitializing PolicyGapFixer...")
    start_time = time.time()
    
    try:
        fixer = PolicyGapFixer()
        init_time = time.time() - start_time
        print(f"Initialized in {init_time:.1f}s")
        
        # Process policy
        print("\nProcessing policy...")
        process_start = time.time()
        
        results = fixer.process_policy(test_policy, "quick_test")
        
        process_time = time.time() - process_start
        total_time = time.time() - start_time
        
        print(f"\nProcessing completed in {process_time:.1f}s")
        print(f"⏱Total time: {total_time:.1f}s")
        
        # Check results
        if isinstance(results, dict):
            print(f"\nResults structure:")
            for key in results.keys():
                print(f"  - {key}")
            
            if 'analysis' in results:
                analysis = results['analysis']
                if isinstance(analysis, dict):
                    print(f"\nAnalysis keys: {list(analysis.keys())}")
                    if 'strengths' in analysis:
                        print(f"  Strengths found: {len(analysis['strengths'])}")
                    if 'recommendations' in analysis:
                        print(f"  Recommendations: {len(analysis['recommendations'])}")
        
        print("\n" + "=" * 60)
        print("QUICK TEST PASSED!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Starting quick test...")
    
   
    success1 = test_simple()
    
    
    success2 = False
    if success1:
        success2 = test_with_file()
    
    if success1 and success2:
        
        print("ALL TESTS PASSED!")
       
        print("\nYou can now run the full system:")
        print("  python src/main.py")
        print("  python src/main.py ../test_policies/dummy_policy_isms.txt")
    else:
    
        print("SOME TESTS FAILED")
    
        sys.exit(1)