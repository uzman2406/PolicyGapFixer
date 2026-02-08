from typing import Dict, List, Any
from llm_handler import LocalLLMHandler

class PolicyReviser:
    def __init__(self, llm_handler: LocalLLMHandler):
        self.llm = llm_handler
    
    def revise_policy(self, original_policy: str, gap_analysis: Dict) -> Dict[str, Any]:
        """Revise policy based on gap analysis"""
        
        # Prepare gap summary for prompt
        gap_summary = []
        for analysis in gap_analysis.get('policy_analysis', []):
            for gap in analysis.get('gaps', []):
                gap_summary.append({
                    "issue": gap.get('gap_description', ''),
                    "recommendation": gap.get('recommendation', '')
                })
        
        # Create revision prompt
        prompt = f"""Revise the following cybersecurity policy to address identified gaps:

ORIGINAL POLICY:
{original_policy}

IDENTIFIED GAPS TO ADDRESS:
{chr(10).join([f"- {gap['issue']}: {gap['recommendation']}" for gap in gap_summary])}

Please provide:
1. A revised version of the policy with all gaps addressed
2. Track changes showing what was added or modified
3. Explanation of how each gap was addressed

Structure your response accordingly."""

        output_format = {
            "revised_policy": "Full text of revised policy",
            "track_changes": [
                {
                    "section": "Section name",
                    "original": "Original text",
                    "revised": "Revised text",
                    "rationale": "Why this change was made"
                }
            ],
            "gap_addressing_summary": "Summary of how gaps were addressed"
        }
        
        revision = self.llm.generate_structured(prompt, output_format)
        
        return revision
    
    def create_roadmap(self, gap_analysis: Dict) -> Dict[str, Any]:
        """Create implementation roadmap"""
        
        nist_gaps = {"Identify": [], "Protect": [], "Detect": [], "Respond": [], "Recover": []}
        
        for analysis in gap_analysis.get('policy_analysis', []):
            for gap in analysis.get('gaps', []):
                nist_function = gap.get('nist_function', 'Identify')
                if nist_function in nist_gaps:
                    nist_gaps[nist_function].append(gap)
        
        
        prompt = f"""Based on the following gap analysis, create a 6-month implementation roadmap aligned with NIST CSF:

GAP ANALYSIS SUMMARY:
Total Gaps: {gap_analysis.get('summary', {}).get('total_gaps', 0)}
High Priority Gaps: {gap_analysis.get('summary', {}).get('high_priority_gaps', 0)}

Gaps by NIST Function:
Identify: {len(nist_gaps['Identify'])} gaps
Protect: {len(nist_gaps['Protect'])} gaps
Detect: {len(nist_gaps['Detect'])} gaps
Respond: {len(nist_gaps['Respond'])} gaps
Recover: {len(nist_gaps['Recover'])} gaps

Create a phased implementation plan with timeline, priority, and resources needed."""

        output_format = {
            "roadmap": {
                "phases": [
                    {
                        "phase": "Phase 1 (Month 1-2)",
                        "objectives": ["Objective 1", "Objective 2"],
                        "key_activities": ["Activity 1", "Activity 2"],
                        "success_metrics": ["Metric 1", "Metric 2"],
                        "resources_needed": ["Resource 1", "Resource 2"]
                    }
                ],
                "timeline": "Gantt chart or timeline description",
                "success_criteria": ["Criteria 1", "Criteria 2"]
            }
        }
        
        roadmap = self.llm.generate_structured(prompt, output_format)
        return roadmap