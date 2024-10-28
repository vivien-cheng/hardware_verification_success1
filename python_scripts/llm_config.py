"""Configuration for LLM integration"""

LLM_SETTINGS = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "model": "claude-3-opus-20240229"  # or your chosen model
}

VERILOG_CONSTRAINTS = {
    "use_posedge": True,
    "require_registers": True,
    "synchronous_design": True,
    "max_width": 32
}

# Template for prompting LLM
VERILOG_PROMPT_TEMPLATE = """
Create a Verilog module that meets these requirements:
- Uses positive edge-triggered registers
- Follows synchronous design principles
- Implements the following specification:
{specification}

Additional constraints:
- Must use only posedge clock triggering
- Must use registers for all outputs
- Must be purely digital logic (no analog components)
- Must follow CMOS-compatible design

Return only the Verilog code without any explanations.
"""
