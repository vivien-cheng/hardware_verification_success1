#!/usr/bin/env python3

import subprocess
import os

class VerilogVerifier:
    def __init__(self):
        self.verilog_dir = "verilog_files"
        self.synthesis_dir = "synthesis_results"
        
    def verify_compilation(self, verilog_file):
        """Verify if the Verilog file compiles using iverilog"""
        try:
            result = subprocess.run(['iverilog', '-o', 'test.out', 
                                   os.path.join(self.verilog_dir, verilog_file)],
                                  capture_output=True, text=True)
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)
    
    def run_synthesis(self, verilog_file):
        """Run synthesis using Yosys"""
        try:
            synthesis_log = os.path.join(self.synthesis_dir, 
                                       f"{os.path.splitext(verilog_file)[0]}_synthesis.log")
            
            yosys_script = f"read_verilog {os.path.join(self.verilog_dir, verilog_file)}; "
            yosys_script += "synth -top test_reg; "
            yosys_script += "write_json synthetic.json"
            
            result = subprocess.run(['yosys', '-p', yosys_script],
                                  capture_output=True, text=True)
            
            with open(synthesis_log, 'w') as f:
                f.write(result.stdout)
                
            return result.returncode == 0, synthesis_log
        except Exception as e:
            return False, str(e)

def main():
    verifier = VerilogVerifier()
    
    # Test with our example file
    test_file = "test_reg.v"
    
    print(f"Testing {test_file}")
    success, message = verifier.verify_compilation(test_file)
    print(f"Compilation: {'Success' if success else 'Failed'}")
    if not success:
        print(f"Error: {message}")
        return
    
    success, log_file = verifier.run_synthesis(test_file)
    print(f"Synthesis: {'Success' if success else 'Failed'}")
    if success:
        print(f"Synthesis log written to: {log_file}")
    else:
        print(f"Error: {log_file}")

if __name__ == "__main__":
    main()
