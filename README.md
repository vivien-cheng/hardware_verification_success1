# Hardware Verification Framework - Success 1

This project implements a Verilog register verification framework that:
- Generates different register variations (width, reset, enable)
- Creates automated testbenches
- Verifies using Icarus Verilog
- Synthesizes using Yosys

## Directory Structure
- python_scripts/: Python verification framework
- verilog_files/: Verilog source files
- synthesis_results/: Synthesis outputs
- testbenches/: Generated testbenches
- verification/: Verification results

## Successfully Verified Modules
1. register_w16.v (16-bit basic register)
2. register_w16_rst.v (16-bit register with reset)
3. register_w4_rst_en.v (4-bit register with reset and enable)
4. register.v
5. register_basic.v
6. test_reg.v

## Tools Used
- Icarus Verilog for compilation and simulation
- Yosys for synthesis
- Python for automation
