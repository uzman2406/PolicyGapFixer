import subprocess
import json
import re
from typing import Optional, Dict, Any
import os
import time

class LocalLLMHandler:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        self.temperature = 0.1  
        
    def _clean_output(self, text: str) -> str:
        """Clean LLM output"""
        
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        return text
    
    def generate_direct(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response using Ollama directly"""
        try:
            import ollama
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt[:800],  
                options={
                    'num_predict': max_tokens,
                    'temperature': self.temperature
                }
            )
            return self._clean_output(response['response'])
        except Exception as e:
            print(f"Direct generation error: {e}")
            
            return self._generate_subprocess(prompt, max_tokens)
    
    def _generate_subprocess(self, prompt: str, max_tokens: int = 500) -> str:
        """Fallback: Generate using subprocess"""
        try:
            
            request = {
                "model": self.model_name,
                "prompt": prompt[:500], 
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": max_tokens
                }
            }
            
           
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt[:500]],
                capture_output=True,
                text=True,
                timeout=300  
            )
            
            if result.returncode == 0:
                return self._clean_output(result.stdout)
            else:
                print(f"Error running Ollama: {result.stderr}")
                return ""
                
        except subprocess.TimeoutExpired:
            print(" Generation timed out after 300 seconds")
            return "Generation timed out"
        except Exception as e:
            print(f"Error in LLM generation: {e}")
            return ""
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Main generation method"""
        return self.generate_direct(prompt, max_tokens)
    
    def generate_with_retry(self, prompt: str, max_tokens: int = 500, retries: int = 2) -> str:
        """Generate with retry logic"""
        for attempt in range(retries):
            try:
                response = self.generate(prompt, max_tokens)
                if response and len(response) > 10 and not response.startswith("Error"):
                    return response
                elif attempt < retries - 1:
                    print(f"Empty response, retry {attempt + 1}...")
                    time.sleep(2)
            except Exception as e:
                if attempt < retries - 1:
                    print(f" Attempt {attempt + 1} failed, retrying... ({e})")
                    time.sleep(3)
                else:
                    print(f"All retries failed: {e}")
                    return f"Error: {str(e)[:100]}"
        return ""
    
    def generate_structured(self, prompt: str, output_format: Dict) -> Dict:
        """Generate structured output"""
        structured_prompt = f"""{prompt}

Please respond in the following JSON format:
{json.dumps(output_format, indent=2)}

Ensure your response is valid JSON."""
        
        response = self.generate_with_retry(structured_prompt, max_tokens=800)
        
        try:
            
            return json.loads(response)
        except json.JSONDecodeError:
            
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    return {"error": "Could not parse JSON", "raw_response": response}
            return {"error": "No JSON found", "raw_response": response}