import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Starting PolicyGapFixer...")

try:
   
    from main import main as run_main
    
    
    run_main()
    
except ImportError as e:
    print(f"Import error: {e}")
    print("\nTrying alternative import...")
    
    # Alternative import method
    import importlib.util
    spec = importlib.util.spec_from_file_location("main", "src/main.py")
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    main_module.main()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()