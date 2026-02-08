import unittest
import os
import json
from main import PolicyGapFixer

class TestPolicyGapFixer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize once for all tests"""
        cls.fixer = PolicyGapFixer()
    
    def test_isms_policy(self):
        """Test ISMS policy processing"""
        test_policy = """POLICY: INFORMATION SECURITY MANAGEMENT SYSTEM
        
1.0 Purpose
This policy establishes guidelines for protecting organizational information assets.
        
2.0 Scope
Applies to all employees and systems.
        
3.0 Policy Statements
3.1 Information security roles and responsibilities shall be defined.
3.2 All users must complete annual security awareness training.
3.3 Security incidents must be reported to IT department.
        
4.0 Compliance
This policy shall be reviewed annually."""
        
        results = self.fixer.process_policy(test_policy, "test_isms")
        
      
        self.assertIn("gap_analysis", results)
        self.assertIn("revised_policy", results)
        self.assertIn("roadmap", results)
        
       
        gap_analysis = results["gap_analysis"]
        self.assertIn("policy_analysis", gap_analysis)
        self.assertIn("summary", gap_analysis)
        
        print("\nISMS Policy Test Complete")
        print(f"Total gaps found: {gap_analysis['summary'].get('total_gaps', 0)}")
    
    def test_file_processing(self):
        """Test processing from file"""
        test_file = "test_policies/dummy_policy_isms.txt"
        if os.path.exists(test_file):
            results = self.fixer.process_file(test_file)
            self.assertIsNotNone(results)
            print(f"\nFile processing test complete for: {test_file}")

def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    run_tests()