
`timescale 1ns/1ps

module register_tb;
    // Parameters
    parameter WIDTH = 8;
    
    // Signals
    reg clk;
    
    
    reg [WIDTH-1:0] data_in;
    wire [WIDTH-1:0] data_out;
    
    // Instantiate the module under test
    register uut (
        .clk(clk),
        
        
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
        
        
        
        #100;
        
        
        
        #20;
        
        
        
        data_in = 8'h5;
        #20;
        
        data_in = 8'hA;
        #20;
        
        
        
        data_in = 8'h3;
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
