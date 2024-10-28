module register_w16(
    input wire clk,
    input wire [15:0] data_in,
    output reg [15:0] data_out
);

    always @(posedge clk) begin
        begin
            data_out <= data_in;
        end
    end

endmodule