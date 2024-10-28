module register_w16_rst(
    input wire clk,
    input wire rst_n,
    input wire [15:0] data_in,
    output reg [15:0] data_out
);

    always @(posedge clk) begin
        if (!rst_n) begin
            data_out <= 16'd0;
        end else begin
            data_out <= data_in;
        end
    end

endmodule