#!/usr/bin/env python3

import os
import json
import anthropic
from datetime import datetime
from llm_config import LLM_SETTINGS, VERILOG_PROMPT_TEMPLATE  # Changed this line

class VerilogGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.output_dir = "verilog_files"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_variations(self, base_specification, num_variations=5):
        """Generate multiple variations of a Verilog design"""
        variations = []
        
        for i in range(num_variations):
            try:
                # Create prompt for this variation
                prompt = VERILOG_PROMPT_TEMPLATE.format(
                    specification=base_specification + f"\nCreate variation {i+1} with unique implementation."
                )
                
                # Generate using Claude
                response = self.client.messages.create(
                    model=LLM_SETTINGS["model"],
                    max_tokens=LLM_SETTINGS["max_tokens"],
                    temperature=LLM_SETTINGS["temperature"],
                    messages=[{"role": "user", "content": prompt}]
                )
                
                verilog_code = response.content[0].text
                
                # Save variation to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/variant_{i+1}_{timestamp}.v"
                
                with open(filename, 'w') as f:
                    f.write(verilog_code)
                
                variations.append({
                    'filename': filename,
                    'code': verilog_code
                })
                
                print(f"✓ Generated variation {i+1}, saved to {filename}")
                
            except Exception as e:
                print(f"Error generating variation {i+1}: {e}")
                continue
        
        return variations

    def generate_with_constraints(self, specification, constraints):
        """Generate Verilog with specific constraints"""
        constraint_str = "\n".join([f"- {c}" for c in constraints])
        prompt = VERILOG_PROMPT_TEMPLATE.format(
            specification=specification + f"\nAdditional constraints:\n{constraint_str}"
        )
        
        try:
            response = self.client.messages.create(
                model=LLM_SETTINGS["model"],
                max_tokens=LLM_SETTINGS["max_tokens"],
                temperature=LLM_SETTINGS["temperature"],
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except Exception as e:
            print(f"Error in generation: {e}")
            return None

def main():
    generator = VerilogGenerator()
    
    # Example usage
    specification = """
    Create an 8-bit register with:
    - Clock input
    - Reset input
    - Enable input
    - 8-bit data input
    - 8-bit data output
    """
    
    print("Generating Verilog variations...")
    variations = generator.generate_variations(specification, num_variations=3)
    
    print(f"\nGenerated {len(variations)} variations")
    
    # Additional constraints example
    constraints = [
        "Maximum fan-out of 4",
        "Use synchronous reset",
        "Include output buffering"
    ]
    
    print("\nGenerating with specific constraints...")
    constrained_design = generator.generate_with_constraints(specification, constraints)
    
    if constrained_design:
        filename = f"{generator.output_dir}/constrained_design_{datetime.now().strftime('%Y%m%d_%H%M%S')}.v"
        with open(filename, 'w') as f:
            f.write(constrained_design)
        print(f"✓ Generated constrained design, saved to {filename}")

if __name__ == "__main__":
    main()
