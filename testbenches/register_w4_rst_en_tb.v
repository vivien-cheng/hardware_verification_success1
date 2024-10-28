
`timescale 1ns/1ps

module register_w4_rst_en_tb;
    // Parameters
    parameter WIDTH = 4;
    
    // Signals
    reg clk;
    reg rst_n;
    reg en;
    reg [WIDTH-1:0] data_in;
    wire [WIDTH-1:0] data_out;
    
    // Instantiate the module under test
    register_w4_rst_en uut (
        .clk(clk),
        .rst_n(rst_n),
        .en(en),
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
        rst_n = 1;
        en = 0;
        
        #100;
        
        // Test reset
        rst_n = 0; #20; rst_n = 1;
        #20;
        
        // Test with enable
        en = 1;
        data_in = 4'h5;
        #20;
        
        data_in = 4'hA;
        #20;
        
        // Test with enable off
        en = 0;
        data_in = 4'h3;
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
