module register_w4_rst_en(
    input wire clk,
    input wire rst_n,
    input wire en,
    input wire [3:0] data_in,
    output reg [3:0] data_out
);

    always @(posedge clk) begin
        if (!rst_n) begin
            data_out <= 4'd0;
        end else begin
            if (en) begin
                data_out <= data_in;
            end
        end
    end

endmodule