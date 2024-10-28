#!/usr/bin/env python3

import os
from datetime import datetime
import random

class VerilogGenerator:
    def __init__(self):
        self.output_dir = "verilog_files"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_register_variant(self, width=8, use_reset=True, use_enable=True):
        """Generate a register variant with specified parameters"""
        # Create base module name
        module_name = f"register_w{width}"
        if use_reset:
            module_name += "_rst"
        if use_enable:
            module_name += "_en"
        
        # Create Verilog code
        code = []
        code.append(f"module {module_name}(")
        code.append("    input wire clk,")
        if use_reset:
            code.append("    input wire rst_n,")
        if use_enable:
            code.append("    input wire en,")
        code.append(f"    input wire [{width-1}:0] data_in,")
        code.append(f"    output reg [{width-1}:0] data_out")
        code.append(");")
        code.append("")
        code.append("    always @(posedge clk) begin")
        
        if use_reset:
            code.append("        if (!rst_n) begin")
            code.append(f"            data_out <= {width}'d0;")
            code.append("        end else begin")
            indent = "            "
        else:
            code.append("        begin")
            indent = "            "
        
        if use_enable:
            code.append(f"{indent}if (en) begin")
            code.append(f"{indent}    data_out <= data_in;")
            code.append(f"{indent}end")
        else:
            code.append(f"{indent}data_out <= data_in;")
        
        code.append("        end")
        code.append("    end")
        code.append("")
        code.append("endmodule")
        
        return module_name, "\n".join(code)

    def generate_variations(self, num_variations=3):
        variations = []
        
        for i in range(num_variations):
            width = random.choice([4, 8, 16, 32])
            use_reset = random.choice([True, False])
            use_enable = random.choice([True, False])
            
            module_name, verilog_code = self.generate_register_variant(
                width=width,
                use_reset=use_reset,
                use_enable=use_enable
            )
            
            # Use module name for the file name
            filename = f"{module_name}.v"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(verilog_code)
            
            variations.append({
                'filename': filename,
                'code': verilog_code,
                'parameters': {
                    'width': width,
                    'use_reset': use_reset,
                    'enable': use_enable
                }
            })
            
            print(f"✓ Generated variation {i+1}:")
            print(f"  - Module: {module_name}")
            print(f"  - Width: {width} bits")
            print(f"  - Reset: {'Yes' if use_reset else 'No'}")
            print(f"  - Enable: {'Yes' if use_enable else 'No'}")
            print(f"  - Saved to: {filepath}\n")
        
        return variations

def main():
    generator = VerilogGenerator()
    print("Generating Verilog variations...")
    variations = generator.generate_variations(num_variations=3)
    
    print("\n=== Generated Variations Summary ===")
    for i, var in enumerate(variations, 1):
        print(f"\nVariation {i}:")
        print(f"File: {var['filename']}")
        print(f"Parameters: {var['parameters']}")

if __name__ == "__main__":
    main()
