#!/usr/bin/env python3

import os
import subprocess
import re

class VerilogVerifier:
    def __init__(self):
        self.verilog_dir = "verilog_files"
        self.testbench_dir = "testbenches"
        self.synthesis_dir = "synthesis_results"
        os.makedirs(self.testbench_dir, exist_ok=True)
        os.makedirs(self.synthesis_dir, exist_ok=True)

    def parse_module_ports(self, verilog_file):
        """Parse the module ports from Verilog file"""
        with open(os.path.join(self.verilog_dir, verilog_file), 'r') as f:
            content = f.read()
            
        # Extract module name and ports
        module_match = re.search(r'module\s+(\w+)\s*\(([\s\S]*?)\);', content)
        if not module_match:
            return None, []
            
        module_name = module_match.group(1)
        ports_text = module_match.group(2)
        
        # Parse ports
        ports = []
        for line in ports_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            # Match port declarations
            port_match = re.search(r'(input|output)\s+wire|reg\s*(\[\d+:\d+\])?\s*(\w+)', line)
            if port_match:
                ports.append(line.split()[-1].rstrip(','))
                
        return module_name, ports

    def generate_testbench(self, verilog_file):
        """Generate a testbench for a given Verilog file"""
        module_name, ports = self.parse_module_ports(verilog_file)
        if not module_name:
            return None
            
        has_reset = 'rst' in ' '.join(ports)
        has_enable = 'en' in ' '.join(ports)
        
        # Find the data width
        with open(os.path.join(self.verilog_dir, verilog_file), 'r') as f:
            content = f.read()
        width_match = re.search(r'\[(\d+):0\]', content)
        width = int(width_match.group(1)) + 1 if width_match else 8

        testbench = f"""
`timescale 1ns/1ps

module {module_name}_tb;
    // Parameters
    parameter WIDTH = {width};
    
    // Signals
    reg clk;
    {"reg rst_n;" if has_reset else ""}
    {"reg en;" if has_enable else ""}
    reg [WIDTH-1:0] data_in;
    wire [WIDTH-1:0] data_out;
    
    // Instantiate the module under test
    {module_name} uut (
        .clk(clk),
        {".rst_n(rst_n)," if has_reset else ""}
        {".en(en)," if has_enable else ""}
        .data_in(data_in),
        .data_out(data_out)
    );
    
    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    // Test stimulus
    initial begin
        // Initialize
        data_in = 0;
        {"rst_n = 1;" if has_reset else ""}
        {"en = 0;" if has_enable else ""}
        
        #100;
        
        {"// Test reset" if has_reset else ""}
        {"rst_n = 0; #20; rst_n = 1;" if has_reset else ""}
        #20;
        
        {"// Test with enable" if has_enable else ""}
        {"en = 1;" if has_enable else ""}
        data_in = {width}'h5;
        #20;
        
        data_in = {width}'hA;
        #20;
        
        {"// Test with enable off" if has_enable else ""}
        {"en = 0;" if has_enable else ""}
        data_in = {width}'h3;
        #20;
        
        #100;
        $finish;
    end
    
    // Monitor changes
    initial begin
        $monitor("Time=%0t data_in=%h data_out=%h",
                 $time, data_in, data_out);
    end
endmodule
"""
        
        testbench_file = os.path.join(self.testbench_dir, f"{module_name}_tb.v")
        with open(testbench_file, 'w') as f:
            f.write(testbench)
        return testbench_file

    def verify_with_icarus(self, verilog_file):
        """Verify using Icarus Verilog"""
        try:
            testbench_file = self.generate_testbench(verilog_file)
            if not testbench_file:
                print(f"Failed to generate testbench for {verilog_file}")
                return False
                
            module_name = os.path.splitext(os.path.basename(verilog_file))[0]
            output_path = os.path.join(self.synthesis_dir, f'{module_name}.vvp')
            
            cmd = ['iverilog', '-o', output_path,
                   os.path.join(self.verilog_dir, verilog_file),
                   testbench_file]
            print(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Compilation failed for {verilog_file}")
                print(result.stderr)
                return False
            
            # Run simulation
            result = subprocess.run(['vvp', output_path], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Simulation failed for {verilog_file}")
                print(result.stderr)
                return False
                
            print(f"✓ Verification passed for {verilog_file}")
            return True
            
        except Exception as e:
            print(f"Error verifying {verilog_file}: {e}")
            return False

    def run_synthesis(self, verilog_file):
        """Run synthesis using Yosys"""
        try:
            module_name = os.path.splitext(os.path.basename(verilog_file))[0]
            log_file = os.path.join(self.synthesis_dir, f"{module_name}_synthesis.log")
            
            yosys_script = f"""
                read_verilog {os.path.join(self.verilog_dir, verilog_file)};
                synth -top {module_name};
                write_json {os.path.join(self.synthesis_dir, module_name)}.json;
                stat;
            """
            
            result = subprocess.run(['yosys', '-p', yosys_script], 
                                  capture_output=True, text=True)
            
            with open(log_file, 'w') as f:
                f.write(result.stdout)
            
            if result.returncode != 0:
                print(f"Synthesis failed for {verilog_file}")
                print(result.stderr)
                return False
            
            print(f"✓ Synthesis passed for {verilog_file}")
            print(f"  Log saved to {log_file}")
            return True
            
        except Exception as e:
            print(f"Error in synthesis for {verilog_file}: {e}")
            return False

def main():
    verifier = VerilogVerifier()
    
    verilog_files = [f for f in os.listdir("verilog_files") 
                     if f.endswith('.v')]
    
    print("\n=== Starting Verification Process ===")
    for vfile in sorted(verilog_files):
        print(f"\nProcessing: {vfile}")
        print("1. Running Icarus Verilog verification...")
        verifier.verify_with_icarus(vfile)
        
        print("\n2. Running Yosys synthesis...")
        verifier.run_synthesis(vfile)

if __name__ == "__main__":
    main()
