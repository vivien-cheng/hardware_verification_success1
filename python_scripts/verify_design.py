#!/usr/bin/env python3

import subprocess
import os
import sys

class VerilogVerifier:
    def __init__(self):
        self.verilog_dir = "verilog_files"
        self.synthesis_dir = "synthesis_results"

    def verify_syntax(self, verilog_file):
        """Verify Verilog syntax using iverilog"""
        cmd = ['iverilog', '-o', 'temp.out', f"{self.verilog_dir}/{verilog_file}"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Syntax verification passed for {verilog_file}")
                return True
            else:
                print(f"✗ Syntax verification failed for {verilog_file}")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error running verification: {e}")
            return False

    def verify_synthesis(self, verilog_file):
        """Verify synthesis using Yosys"""
        synthesis_log = f"{self.synthesis_dir}/{verilog_file}_synthesis.log"
        
        # Create Yosys script
        yosys_script = f"""
        read_verilog {self.verilog_dir}/{verilog_file}
        synth -top register
        write_json {self.synthesis_dir}/output.json
        """
        
        try:
            result = subprocess.run(['yosys', '-p', yosys_script], 
                                  capture_output=True, text=True)
            
            # Save synthesis log
            os.makedirs(self.synthesis_dir, exist_ok=True)
            with open(synthesis_log, 'w') as f:
                f.write(result.stdout)
            
            if result.returncode == 0:
                print(f"✓ Synthesis successful for {verilog_file}")
                print(f"  Log saved to {synthesis_log}")
                return True
            else:
                print(f"✗ Synthesis failed for {verilog_file}")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error running synthesis: {e}")
            return False

def main():
    verifier = VerilogVerifier()
    
    # Test file to verify
    test_file = "register.v"
    
    print("\n=== Starting Verilog Verification ===")
    
    # Verify syntax
    print("\nStep 1: Syntax Verification")
    if not verifier.verify_syntax(test_file):
        sys.exit(1)
    
    # Verify synthesis
    print("\nStep 2: Synthesis Verification")
    if not verifier.verify_synthesis(test_file):
        sys.exit(1)
    
    print("\n✓ All verifications passed!")

if __name__ == "__main__":
    main()
