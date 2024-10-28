#!/usr/bin/env python3

import os
import sys
# Add the python_scripts directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_scripts.verify_design import VerilogVerifier
from python_scripts.llm_generator import VerilogGenerator

def test_all_variations():
    verifier = VerilogVerifier()
    
    # Get all Verilog files in the verilog_files directory
    verilog_files = [f for f in os.listdir('verilog_files') if f.endswith('.v')]
    
    results = []
    for vfile in verilog_files:
        print(f"\nTesting {vfile}...")
        syntax_ok = verifier.verify_syntax(vfile)
        synthesis_ok = verifier.verify_synthesis(vfile)
        
        results.append({
            'file': vfile,
            'syntax_ok': syntax_ok,
            'synthesis_ok': synthesis_ok
        })
    
    return results

def main():
    # First generate some variations
    generator = VerilogGenerator()
    specification = """
    Create an 8-bit register with:
    - Clock input
    - Reset input
    - Enable input
    - 8-bit data input
    - 8-bit data output
    """
    
    print("Generating variations...")
    generator.generate_variations(specification, num_variations=3)
    
    print("\nTesting all generated variations...")
    results = test_all_variations()
    
    # Print summary
    print("\n=== Test Results ===")
    for result in results:
        print(f"\nFile: {result['file']}")
        print(f"Syntax Check: {'✓' if result['syntax_ok'] else '✗'}")
        print(f"Synthesis: {'✓' if result['synthesis_ok'] else '✗'}")

if __name__ == "__main__":
    main()
