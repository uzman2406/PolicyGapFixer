import json
from typing import List, Dict, Any
from embedding_system import VectorStore
from llm_handler import LocalLLMHandler

class GapAnalyzer:
    def __init__(self, vector_store: VectorStore, llm_handler: LocalLLMHandler):
        self.vector_store = vector_store
        self.llm = llm_handler
        self.nist_functions = ["Identify", "Protect", "Detect", "Respond", "Recover"]
    
    def extract_policy_sections(self, policy_text: str) -> Dict[str, str]:
        """Extract sections from policy text"""
        sections = {}
        lines = policy_text.split('\n')
        current_section = "Header"
        current_content = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('##') or line.startswith('**')):
                if current_content:
                    sections[current_section] = ' '.join(current_content)
                current_section = line.replace('#', '').replace('*', '').strip()
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = ' '.join(current_content)
        
        return sections
    
    def find_relevant_standards(self, policy_section: str, top_k: int = 3) -> List[str]:
        """Find relevant CIS/NIST standards for a policy section"""
        results = self.vector_store.search(policy_section, k=top_k)
        return [result['chunk']['text'] for result in results]
    
    def analyze_gaps(self, policy_text: str) -> Dict[str, Any]:
        """Main gap analysis function"""
        
     
        sections = self.extract_policy_sections(policy_text)
        
        all_gaps = []
        
        for section_name, section_content in sections.items():
           
            relevant_standards = self.find_relevant_standards(section_content)
            
        
            prompt = f"""Analyze the following policy section against cybersecurity standards:

Policy Section Title: {section_name}
Policy Section Content: {section_content}

Relevant Standards/Requirements:
{chr(10).join(relevant_standards)}

Identify specific gaps where the policy is missing or insufficient compared to best practices.
For each gap, specify:
1. Gap Description
2. Severity (High/Medium/Low)
3. Relevant NIST CSF Function
4. Recommended improvement

Provide the analysis in structured format."""
            
            
            output_format = {
                "section": section_name,
                "gaps": [
                    {
                        "gap_description": "Description of the gap",
                        "severity": "High/Medium/Low",
                        "nist_function": "Identify/Protect/Detect/Respond/Recover",
                        "recommendation": "Specific recommendation to address gap"
                    }
                ]
            }
            
            
            analysis = self.llm.generate_structured(prompt, output_format)
            all_gaps.append(analysis)
        
        return {
            "policy_analysis": all_gaps,
            "summary": {
                "total_gaps": sum(len(item.get('gaps', [])) for item in all_gaps),
                "high_priority_gaps": sum(1 for item in all_gaps for gap in item.get('gaps', []) if gap.get('severity') == 'High')
            }
        }