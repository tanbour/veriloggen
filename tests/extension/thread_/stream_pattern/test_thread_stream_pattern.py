from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import thread_stream_pattern

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  wire [32-1:0] myaxi_awaddr;
  wire [8-1:0] myaxi_awlen;
  wire myaxi_awvalid;
  reg myaxi_awready;
  wire [32-1:0] myaxi_wdata;
  wire [4-1:0] myaxi_wstrb;
  wire myaxi_wlast;
  wire myaxi_wvalid;
  reg myaxi_wready;
  wire [32-1:0] myaxi_araddr;
  wire [8-1:0] myaxi_arlen;
  wire myaxi_arvalid;
  reg myaxi_arready;
  reg [32-1:0] myaxi_rdata;
  reg myaxi_rlast;
  reg myaxi_rvalid;
  wire myaxi_rready;
  wire [32-1:0] memory_awaddr;
  wire [8-1:0] memory_awlen;
  wire memory_awvalid;
  reg memory_awready;
  wire [32-1:0] memory_wdata;
  wire [4-1:0] memory_wstrb;
  wire memory_wlast;
  wire memory_wvalid;
  reg memory_wready;
  wire [32-1:0] memory_araddr;
  wire [8-1:0] memory_arlen;
  wire memory_arvalid;
  reg memory_arready;
  reg [32-1:0] memory_rdata;
  reg memory_rlast;
  reg memory_rvalid;
  wire memory_rready;
  reg [8-1:0] _memory_mem [0:2**20-1];

  initial begin
    $readmemh("_memory_memimg_.out", _memory_mem);
  end

  reg [32-1:0] _memory_fsm;
  localparam _memory_fsm_init = 0;
  reg [33-1:0] _write_count;
  reg [32-1:0] _write_addr;
  reg [33-1:0] _read_count;
  reg [32-1:0] _read_addr;
  reg [33-1:0] _sleep_count;
  reg [32-1:0] _d1__memory_fsm;
  reg __memory_fsm_cond_100_0_1;
  reg __memory_fsm_cond_200_1_1;
  reg __memory_fsm_cond_211_2_1;
  assign memory_awaddr = myaxi_awaddr;
  assign memory_awlen = myaxi_awlen;
  assign memory_awvalid = myaxi_awvalid;
  wire _tmp_0;
  assign _tmp_0 = memory_awready;

  always @(*) begin
    myaxi_awready = _tmp_0;
  end

  assign memory_wdata = myaxi_wdata;
  assign memory_wstrb = myaxi_wstrb;
  assign memory_wlast = myaxi_wlast;
  assign memory_wvalid = myaxi_wvalid;
  wire _tmp_1;
  assign _tmp_1 = memory_wready;

  always @(*) begin
    myaxi_wready = _tmp_1;
  end

  assign memory_araddr = myaxi_araddr;
  assign memory_arlen = myaxi_arlen;
  assign memory_arvalid = myaxi_arvalid;
  wire _tmp_2;
  assign _tmp_2 = memory_arready;

  always @(*) begin
    myaxi_arready = _tmp_2;
  end


  always @(*) begin
    myaxi_rdata <= memory_rdata;
  end

  wire _tmp_3;
  assign _tmp_3 = memory_rlast;

  always @(*) begin
    myaxi_rlast = _tmp_3;
  end

  wire _tmp_4;
  assign _tmp_4 = memory_rvalid;

  always @(*) begin
    myaxi_rvalid = _tmp_4;
  end

  assign memory_rready = myaxi_rready;

  blinkled
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .myaxi_awaddr(myaxi_awaddr),
    .myaxi_awlen(myaxi_awlen),
    .myaxi_awvalid(myaxi_awvalid),
    .myaxi_awready(myaxi_awready),
    .myaxi_wdata(myaxi_wdata),
    .myaxi_wstrb(myaxi_wstrb),
    .myaxi_wlast(myaxi_wlast),
    .myaxi_wvalid(myaxi_wvalid),
    .myaxi_wready(myaxi_wready),
    .myaxi_araddr(myaxi_araddr),
    .myaxi_arlen(myaxi_arlen),
    .myaxi_arvalid(myaxi_arvalid),
    .myaxi_arready(myaxi_arready),
    .myaxi_rdata(myaxi_rdata),
    .myaxi_rlast(myaxi_rlast),
    .myaxi_rvalid(myaxi_rvalid),
    .myaxi_rready(myaxi_rready)
  );


  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut);
  end


  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end


  initial begin
    RST = 0;
    memory_awready = 0;
    memory_wready = 0;
    memory_arready = 0;
    memory_rdata = 0;
    memory_rlast = 0;
    memory_rvalid = 0;
    _memory_fsm = _memory_fsm_init;
    _write_count = 0;
    _write_addr = 0;
    _read_count = 0;
    _read_addr = 0;
    _sleep_count = 0;
    _d1__memory_fsm = _memory_fsm_init;
    __memory_fsm_cond_100_0_1 = 0;
    __memory_fsm_cond_200_1_1 = 0;
    __memory_fsm_cond_211_2_1 = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #100000;
    $finish;
  end

  localparam _memory_fsm_200 = 200;
  localparam _memory_fsm_201 = 201;
  localparam _memory_fsm_202 = 202;
  localparam _memory_fsm_203 = 203;
  localparam _memory_fsm_204 = 204;
  localparam _memory_fsm_205 = 205;
  localparam _memory_fsm_206 = 206;
  localparam _memory_fsm_207 = 207;
  localparam _memory_fsm_208 = 208;
  localparam _memory_fsm_209 = 209;
  localparam _memory_fsm_210 = 210;
  localparam _memory_fsm_211 = 211;
  localparam _memory_fsm_100 = 100;
  localparam _memory_fsm_101 = 101;
  localparam _memory_fsm_102 = 102;
  localparam _memory_fsm_103 = 103;
  localparam _memory_fsm_104 = 104;
  localparam _memory_fsm_105 = 105;
  localparam _memory_fsm_106 = 106;
  localparam _memory_fsm_107 = 107;
  localparam _memory_fsm_108 = 108;
  localparam _memory_fsm_109 = 109;
  localparam _memory_fsm_110 = 110;
  localparam _memory_fsm_111 = 111;
  localparam _memory_fsm_112 = 112;

  always @(posedge CLK) begin
    if(RST) begin
      _memory_fsm <= _memory_fsm_init;
      _d1__memory_fsm <= _memory_fsm_init;
      memory_awready <= 0;
      _write_addr <= 0;
      _write_count <= 0;
      __memory_fsm_cond_100_0_1 <= 0;
      memory_wready <= 0;
      memory_arready <= 0;
      _read_addr <= 0;
      _read_count <= 0;
      __memory_fsm_cond_200_1_1 <= 0;
      memory_rdata[7:0] <= (0 >> 0) & { 8{ 1'd1 } };
      memory_rdata[15:8] <= (0 >> 8) & { 8{ 1'd1 } };
      memory_rdata[23:16] <= (0 >> 16) & { 8{ 1'd1 } };
      memory_rdata[31:24] <= (0 >> 24) & { 8{ 1'd1 } };
      memory_rvalid <= 0;
      memory_rlast <= 0;
      __memory_fsm_cond_211_2_1 <= 0;
      memory_rdata <= 0;
      _sleep_count <= 0;
    end else begin
      _sleep_count <= _sleep_count + 1;
      if(_sleep_count == 3) begin
        _sleep_count <= 0;
      end 
      _d1__memory_fsm <= _memory_fsm;
      case(_d1__memory_fsm)
        _memory_fsm_100: begin
          if(__memory_fsm_cond_100_0_1) begin
            memory_awready <= 0;
          end 
        end
        _memory_fsm_200: begin
          if(__memory_fsm_cond_200_1_1) begin
            memory_arready <= 0;
          end 
        end
        _memory_fsm_211: begin
          if(__memory_fsm_cond_211_2_1) begin
            memory_rvalid <= 0;
            memory_rlast <= 0;
          end 
        end
      endcase
      case(_memory_fsm)
        _memory_fsm_init: begin
          if(memory_awvalid) begin
            _memory_fsm <= _memory_fsm_100;
          end 
          if(memory_arvalid) begin
            _memory_fsm <= _memory_fsm_200;
          end 
        end
        _memory_fsm_100: begin
          if(memory_awvalid) begin
            memory_awready <= 1;
            _write_addr <= memory_awaddr;
            _write_count <= memory_awlen + 1;
          end 
          __memory_fsm_cond_100_0_1 <= 1;
          if(!memory_awvalid) begin
            _memory_fsm <= _memory_fsm_init;
          end 
          if(memory_awvalid) begin
            _memory_fsm <= _memory_fsm_101;
          end 
        end
        _memory_fsm_101: begin
          _memory_fsm <= _memory_fsm_102;
        end
        _memory_fsm_102: begin
          _memory_fsm <= _memory_fsm_103;
        end
        _memory_fsm_103: begin
          _memory_fsm <= _memory_fsm_104;
        end
        _memory_fsm_104: begin
          _memory_fsm <= _memory_fsm_105;
        end
        _memory_fsm_105: begin
          _memory_fsm <= _memory_fsm_106;
        end
        _memory_fsm_106: begin
          _memory_fsm <= _memory_fsm_107;
        end
        _memory_fsm_107: begin
          _memory_fsm <= _memory_fsm_108;
        end
        _memory_fsm_108: begin
          _memory_fsm <= _memory_fsm_109;
        end
        _memory_fsm_109: begin
          _memory_fsm <= _memory_fsm_110;
        end
        _memory_fsm_110: begin
          _memory_fsm <= _memory_fsm_111;
        end
        _memory_fsm_111: begin
          memory_wready <= 1;
          _memory_fsm <= _memory_fsm_112;
        end
        _memory_fsm_112: begin
          if(memory_wvalid && memory_wstrb[0]) begin
            _memory_mem[_write_addr + 0] <= memory_wdata[7:0];
          end 
          if(memory_wvalid && memory_wstrb[1]) begin
            _memory_mem[_write_addr + 1] <= memory_wdata[15:8];
          end 
          if(memory_wvalid && memory_wstrb[2]) begin
            _memory_mem[_write_addr + 2] <= memory_wdata[23:16];
          end 
          if(memory_wvalid && memory_wstrb[3]) begin
            _memory_mem[_write_addr + 3] <= memory_wdata[31:24];
          end 
          if(memory_wvalid && memory_wready) begin
            _write_addr <= _write_addr + 4;
            _write_count <= _write_count - 1;
          end 
          if(_sleep_count == 3) begin
            memory_wready <= 0;
          end else begin
            memory_wready <= 1;
          end
          if(memory_wvalid && memory_wready && (_write_count == 1)) begin
            memory_wready <= 0;
          end 
          if(memory_wvalid && memory_wready && (_write_count == 1)) begin
            _memory_fsm <= _memory_fsm_init;
          end 
        end
        _memory_fsm_200: begin
          if(memory_arvalid) begin
            memory_arready <= 1;
            _read_addr <= memory_araddr;
            _read_count <= memory_arlen + 1;
          end 
          __memory_fsm_cond_200_1_1 <= 1;
          if(!memory_arvalid) begin
            _memory_fsm <= _memory_fsm_init;
          end 
          if(memory_arvalid) begin
            _memory_fsm <= _memory_fsm_201;
          end 
        end
        _memory_fsm_201: begin
          _memory_fsm <= _memory_fsm_202;
        end
        _memory_fsm_202: begin
          _memory_fsm <= _memory_fsm_203;
        end
        _memory_fsm_203: begin
          _memory_fsm <= _memory_fsm_204;
        end
        _memory_fsm_204: begin
          _memory_fsm <= _memory_fsm_205;
        end
        _memory_fsm_205: begin
          _memory_fsm <= _memory_fsm_206;
        end
        _memory_fsm_206: begin
          _memory_fsm <= _memory_fsm_207;
        end
        _memory_fsm_207: begin
          _memory_fsm <= _memory_fsm_208;
        end
        _memory_fsm_208: begin
          _memory_fsm <= _memory_fsm_209;
        end
        _memory_fsm_209: begin
          _memory_fsm <= _memory_fsm_210;
        end
        _memory_fsm_210: begin
          _memory_fsm <= _memory_fsm_211;
        end
        _memory_fsm_211: begin
          if(memory_rready | !memory_rvalid) begin
            memory_rdata[7:0] <= _memory_mem[_read_addr + 0];
          end 
          if(memory_rready | !memory_rvalid) begin
            memory_rdata[15:8] <= _memory_mem[_read_addr + 1];
          end 
          if(memory_rready | !memory_rvalid) begin
            memory_rdata[23:16] <= _memory_mem[_read_addr + 2];
          end 
          if(memory_rready | !memory_rvalid) begin
            memory_rdata[31:24] <= _memory_mem[_read_addr + 3];
          end 
          if((_sleep_count < 3) && (_read_count > 0) && memory_rready | !memory_rvalid) begin
            memory_rvalid <= 1;
            _read_addr <= _read_addr + 4;
            _read_count <= _read_count - 1;
          end 
          if((_sleep_count < 3) && (_read_count == 1) && memory_rready | !memory_rvalid) begin
            memory_rlast <= 1;
          end 
          __memory_fsm_cond_211_2_1 <= 1;
          if(memory_rvalid && !memory_rready) begin
            memory_rvalid <= memory_rvalid;
            memory_rdata <= memory_rdata;
            memory_rlast <= memory_rlast;
          end 
          if(memory_rvalid && memory_rready && (_read_count == 0)) begin
            _memory_fsm <= _memory_fsm_init;
          end 
        end
      endcase
    end
  end


endmodule



module blinkled
(
  input CLK,
  input RST,
  output reg [32-1:0] myaxi_awaddr,
  output reg [8-1:0] myaxi_awlen,
  output reg myaxi_awvalid,
  input myaxi_awready,
  output reg [32-1:0] myaxi_wdata,
  output reg [4-1:0] myaxi_wstrb,
  output reg myaxi_wlast,
  output reg myaxi_wvalid,
  input myaxi_wready,
  output reg [32-1:0] myaxi_araddr,
  output reg [8-1:0] myaxi_arlen,
  output reg myaxi_arvalid,
  input myaxi_arready,
  input [32-1:0] myaxi_rdata,
  input myaxi_rlast,
  input myaxi_rvalid,
  output myaxi_rready
);

  reg [10-1:0] ram_a_0_addr;
  wire [32-1:0] ram_a_0_rdata;
  reg [32-1:0] ram_a_0_wdata;
  reg ram_a_0_wenable;

  ram_a
  inst_ram_a
  (
    .CLK(CLK),
    .ram_a_0_addr(ram_a_0_addr),
    .ram_a_0_rdata(ram_a_0_rdata),
    .ram_a_0_wdata(ram_a_0_wdata),
    .ram_a_0_wenable(ram_a_0_wenable)
  );

  reg [10-1:0] ram_b_0_addr;
  wire [32-1:0] ram_b_0_rdata;
  reg [32-1:0] ram_b_0_wdata;
  reg ram_b_0_wenable;

  ram_b
  inst_ram_b
  (
    .CLK(CLK),
    .ram_b_0_addr(ram_b_0_addr),
    .ram_b_0_rdata(ram_b_0_rdata),
    .ram_b_0_wdata(ram_b_0_wdata),
    .ram_b_0_wenable(ram_b_0_wenable)
  );

  reg [10-1:0] ram_c_0_addr;
  wire [32-1:0] ram_c_0_rdata;
  reg [32-1:0] ram_c_0_wdata;
  reg ram_c_0_wenable;

  ram_c
  inst_ram_c
  (
    .CLK(CLK),
    .ram_c_0_addr(ram_c_0_addr),
    .ram_c_0_rdata(ram_c_0_rdata),
    .ram_c_0_wdata(ram_c_0_wdata),
    .ram_c_0_wenable(ram_c_0_wenable)
  );

  reg [32-1:0] th_comp;
  localparam th_comp_init = 0;
  reg signed [32-1:0] _th_comp_offset_0;
  reg [10-1:0] _tmp_0;
  reg [32-1:0] _tmp_1;
  reg [32-1:0] _tmp_2;
  reg [32-1:0] _tmp_3;
  reg [32-1:0] _tmp_fsm_0;
  localparam _tmp_fsm_0_init = 0;
  reg [9-1:0] _tmp_4;
  reg _myaxi_cond_0_1;
  reg [32-1:0] _tmp_5;
  reg _tmp_6;
  reg [33-1:0] _tmp_7;
  reg _tmp_8;
  wire [32-1:0] _tmp_data_9;
  wire _tmp_valid_9;
  wire _tmp_ready_9;
  assign _tmp_ready_9 = (_tmp_7 > 0) && !_tmp_8;
  reg _ram_a_cond_0_1;
  reg [10-1:0] _tmp_10;
  reg [32-1:0] _tmp_11;
  reg [32-1:0] _tmp_12;
  reg [32-1:0] _tmp_13;
  reg [32-1:0] _tmp_fsm_1;
  localparam _tmp_fsm_1_init = 0;
  reg [9-1:0] _tmp_14;
  reg _myaxi_cond_1_1;
  reg [32-1:0] _tmp_15;
  reg _tmp_16;
  reg [33-1:0] _tmp_17;
  reg _tmp_18;
  wire [32-1:0] _tmp_data_19;
  wire _tmp_valid_19;
  wire _tmp_ready_19;
  assign _tmp_ready_19 = (_tmp_17 > 0) && !_tmp_18;
  reg _ram_b_cond_0_1;
  reg _mystream_flag_1;
  reg [32-1:0] _mystream_fsm_2;
  localparam _mystream_fsm_2_init = 0;
  reg _tmp_20;
  reg _tmp_21;
  wire _tmp_22;
  wire _tmp_23;
  assign _tmp_23 = 1;
  localparam _tmp_24 = 1;
  wire [_tmp_24-1:0] _tmp_25;
  assign _tmp_25 = (_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21);
  reg [_tmp_24-1:0] __tmp_25_1;
  wire [32-1:0] _tmp_26;
  reg [32-1:0] __tmp_26_1;
  assign _tmp_26 = (__tmp_25_1)? ram_a_0_rdata : __tmp_26_1;
  reg _tmp_27;
  reg _tmp_28;
  reg _tmp_29;
  reg _tmp_30;
  reg _tmp_31;
  wire [10-1:0] _tmp_32;
  wire [10-1:0] _tmp_33;
  reg [10-1:0] _tmp_34;
  reg [10-1:0] _tmp_35;
  assign _tmp_33 = _tmp_35 + (_tmp_34 + _th_comp_offset_0);
  reg [5-1:0] _tmp_36;
  reg [4-1:0] _tmp_37;
  reg [6-1:0] _tmp_38;
  assign _tmp_32 = ((0 && 0)? _tmp_38 == 0 : _tmp_36 == 0)? _tmp_33 : ram_a_0_addr + ((0 && 0)? 1 : 64);
  reg _mystream_flag_3;
  reg [32-1:0] _mystream_fsm_4;
  localparam _mystream_fsm_4_init = 0;
  reg _tmp_39;
  reg _tmp_40;
  wire _tmp_41;
  wire _tmp_42;
  assign _tmp_42 = 1;
  localparam _tmp_43 = 1;
  wire [_tmp_43-1:0] _tmp_44;
  assign _tmp_44 = (_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40);
  reg [_tmp_43-1:0] __tmp_44_1;
  wire [32-1:0] _tmp_45;
  reg [32-1:0] __tmp_45_1;
  assign _tmp_45 = (__tmp_44_1)? ram_b_0_rdata : __tmp_45_1;
  reg _tmp_46;
  reg _tmp_47;
  reg _tmp_48;
  reg _tmp_49;
  reg _tmp_50;
  wire [10-1:0] _tmp_51;
  wire [10-1:0] _tmp_52;
  reg [10-1:0] _tmp_53;
  reg [10-1:0] _tmp_54;
  assign _tmp_52 = _tmp_54 + (_tmp_53 + _th_comp_offset_0);
  reg [5-1:0] _tmp_55;
  reg [4-1:0] _tmp_56;
  reg [6-1:0] _tmp_57;
  assign _tmp_51 = ((0 && 0)? _tmp_57 == 0 : _tmp_55 == 0)? _tmp_52 : ram_b_0_addr + ((0 && 0)? 1 : 64);
  reg _mystream_flag_5;
  reg [32-1:0] _mystream_fsm_6;
  localparam _mystream_fsm_6_init = 0;
  reg [2-1:0] _tmp_58;
  reg _tmp_59;
  wire _tmp_all_valid_60;
  wire [32-1:0] _tmp_data_61;
  wire _tmp_valid_61;
  wire _tmp_ready_61;
  assign _tmp_ready_61 = (_tmp_58 > 0) && !_tmp_59 && _tmp_all_valid_60;
  wire [1-1:0] _tmp_data_62;
  wire _tmp_valid_62;
  wire _tmp_ready_62;
  assign _tmp_ready_62 = (_tmp_58 > 0) && !_tmp_59 && _tmp_all_valid_60;
  assign _tmp_all_valid_60 = _tmp_valid_61 && _tmp_valid_62;
  reg _ram_c_cond_0_1;
  reg [10-1:0] _tmp_63;
  reg [32-1:0] _tmp_64;
  reg [32-1:0] _tmp_65;
  reg [32-1:0] _tmp_66;
  reg [32-1:0] _tmp_fsm_2;
  localparam _tmp_fsm_2_init = 0;
  reg [9-1:0] _tmp_67;
  reg _myaxi_cond_2_1;
  reg _tmp_68;
  reg _tmp_69;
  wire _tmp_70;
  wire _tmp_71;
  assign _tmp_71 = 1;
  localparam _tmp_72 = 1;
  wire [_tmp_72-1:0] _tmp_73;
  assign _tmp_73 = (_tmp_70 || !_tmp_68) && (_tmp_71 || !_tmp_69);
  reg [_tmp_72-1:0] __tmp_73_1;
  wire [32-1:0] _tmp_74;
  reg [32-1:0] __tmp_74_1;
  assign _tmp_74 = (__tmp_73_1)? ram_c_0_rdata : __tmp_74_1;
  reg _tmp_75;
  reg _tmp_76;
  reg _tmp_77;
  reg _tmp_78;
  reg [33-1:0] _tmp_79;
  reg _tmp_80;
  wire [32-1:0] _tmp_data_81;
  wire _tmp_valid_81;
  wire _tmp_ready_81;
  assign _tmp_ready_81 = (_tmp_fsm_2 == 3) && ((_tmp_67 > 0) && (myaxi_wready || !myaxi_wvalid));
  reg _myaxi_cond_3_1;
  reg [10-1:0] _tmp_82;
  reg [32-1:0] _tmp_83;
  reg [32-1:0] _tmp_84;
  reg [32-1:0] _tmp_85;
  reg [32-1:0] _tmp_fsm_3;
  localparam _tmp_fsm_3_init = 0;
  reg [9-1:0] _tmp_86;
  reg _myaxi_cond_4_1;
  reg [32-1:0] _tmp_87;
  reg _tmp_88;
  reg [33-1:0] _tmp_89;
  reg _tmp_90;
  wire [32-1:0] _tmp_data_91;
  wire _tmp_valid_91;
  wire _tmp_ready_91;
  assign _tmp_ready_91 = (_tmp_89 > 0) && !_tmp_90;
  reg _ram_a_cond_1_1;
  reg [10-1:0] _tmp_92;
  reg [32-1:0] _tmp_93;
  reg [32-1:0] _tmp_94;
  reg [32-1:0] _tmp_95;
  reg [32-1:0] _tmp_fsm_4;
  localparam _tmp_fsm_4_init = 0;
  reg [9-1:0] _tmp_96;
  reg _myaxi_cond_5_1;
  reg [32-1:0] _tmp_97;
  reg _tmp_98;
  reg [33-1:0] _tmp_99;
  reg _tmp_100;
  wire [32-1:0] _tmp_data_101;
  wire _tmp_valid_101;
  wire _tmp_ready_101;
  assign _tmp_ready_101 = (_tmp_99 > 0) && !_tmp_100;
  reg _ram_b_cond_1_1;
  assign myaxi_rready = (_tmp_fsm_0 == 3) || (_tmp_fsm_1 == 3) || (_tmp_fsm_3 == 3) || (_tmp_fsm_4 == 3);
  reg [32-1:0] th_sequential;
  localparam th_sequential_init = 0;
  reg _th_sequential_called;
  reg signed [32-1:0] _th_sequential_offset_7;
  reg signed [32-1:0] _th_sequential_offset_8;
  reg signed [32-1:0] _th_sequential_sum_9;
  reg signed [32-1:0] _th_sequential_i_10;
  reg _tmp_102;
  reg _ram_a_cond_2_1;
  reg _ram_a_cond_3_1;
  reg _ram_a_cond_3_2;
  reg signed [32-1:0] _tmp_103;
  reg signed [32-1:0] _th_sequential_a_11;
  reg _tmp_104;
  reg _ram_b_cond_2_1;
  reg _ram_b_cond_3_1;
  reg _ram_b_cond_3_2;
  reg signed [32-1:0] _tmp_105;
  reg signed [32-1:0] _th_sequential_b_12;
  reg _ram_c_cond_1_1;
  reg [10-1:0] _tmp_106;
  reg [32-1:0] _tmp_107;
  reg [32-1:0] _tmp_108;
  reg [32-1:0] _tmp_109;
  reg [32-1:0] _tmp_fsm_5;
  localparam _tmp_fsm_5_init = 0;
  reg [9-1:0] _tmp_110;
  reg _myaxi_cond_6_1;
  reg _tmp_111;
  reg _tmp_112;
  wire _tmp_113;
  wire _tmp_114;
  assign _tmp_114 = 1;
  localparam _tmp_115 = 1;
  wire [_tmp_115-1:0] _tmp_116;
  assign _tmp_116 = (_tmp_113 || !_tmp_111) && (_tmp_114 || !_tmp_112);
  reg [_tmp_115-1:0] __tmp_116_1;
  wire [32-1:0] _tmp_117;
  reg [32-1:0] __tmp_117_1;
  assign _tmp_117 = (__tmp_116_1)? ram_c_0_rdata : __tmp_117_1;
  reg _tmp_118;
  reg _tmp_119;
  reg _tmp_120;
  reg _tmp_121;
  reg [33-1:0] _tmp_122;
  reg _tmp_123;
  wire [32-1:0] _tmp_data_124;
  wire _tmp_valid_124;
  wire _tmp_ready_124;
  assign _tmp_ready_124 = (_tmp_fsm_5 == 3) && ((_tmp_110 > 0) && (myaxi_wready || !myaxi_wvalid));
  reg _myaxi_cond_7_1;
  reg signed [32-1:0] _th_comp_offset_stream_13;
  reg signed [32-1:0] _th_comp_offset_seq_14;
  reg signed [32-1:0] _th_comp_all_ok_15;
  reg _tmp_125;
  reg _ram_c_cond_2_1;
  reg _ram_c_cond_3_1;
  reg _ram_c_cond_3_2;
  reg signed [32-1:0] _tmp_126;
  reg signed [32-1:0] _th_comp_st_16;
  reg _tmp_127;
  reg _ram_c_cond_4_1;
  reg _ram_c_cond_5_1;
  reg _ram_c_cond_5_2;
  reg signed [32-1:0] _tmp_128;
  reg signed [32-1:0] _th_comp_sq_17;

  always @(posedge CLK) begin
    if(RST) begin
      myaxi_araddr <= 0;
      myaxi_arlen <= 0;
      myaxi_arvalid <= 0;
      _tmp_4 <= 0;
      _myaxi_cond_0_1 <= 0;
      _tmp_14 <= 0;
      _myaxi_cond_1_1 <= 0;
      myaxi_awaddr <= 0;
      myaxi_awlen <= 0;
      myaxi_awvalid <= 0;
      _tmp_67 <= 0;
      _myaxi_cond_2_1 <= 0;
      myaxi_wdata <= 0;
      myaxi_wvalid <= 0;
      myaxi_wlast <= 0;
      myaxi_wstrb <= 0;
      _tmp_80 <= 0;
      _myaxi_cond_3_1 <= 0;
      _tmp_86 <= 0;
      _myaxi_cond_4_1 <= 0;
      _tmp_96 <= 0;
      _myaxi_cond_5_1 <= 0;
      _tmp_110 <= 0;
      _myaxi_cond_6_1 <= 0;
      _tmp_123 <= 0;
      _myaxi_cond_7_1 <= 0;
    end else begin
      if(_myaxi_cond_0_1) begin
        myaxi_arvalid <= 0;
      end 
      if(_myaxi_cond_1_1) begin
        myaxi_arvalid <= 0;
      end 
      if(_myaxi_cond_2_1) begin
        myaxi_awvalid <= 0;
      end 
      if(_myaxi_cond_3_1) begin
        myaxi_wvalid <= 0;
        myaxi_wlast <= 0;
        _tmp_80 <= 0;
      end 
      if(_myaxi_cond_4_1) begin
        myaxi_arvalid <= 0;
      end 
      if(_myaxi_cond_5_1) begin
        myaxi_arvalid <= 0;
      end 
      if(_myaxi_cond_6_1) begin
        myaxi_awvalid <= 0;
      end 
      if(_myaxi_cond_7_1) begin
        myaxi_wvalid <= 0;
        myaxi_wlast <= 0;
        _tmp_123 <= 0;
      end 
      if((_tmp_fsm_0 == 1) && ((myaxi_arready || !myaxi_arvalid) && (_tmp_4 == 0))) begin
        myaxi_araddr <= _tmp_1;
        myaxi_arlen <= _tmp_2 - 1;
        myaxi_arvalid <= 1;
        _tmp_4 <= _tmp_2;
      end 
      _myaxi_cond_0_1 <= 1;
      if(myaxi_arvalid && !myaxi_arready) begin
        myaxi_arvalid <= myaxi_arvalid;
      end 
      if(myaxi_rready && myaxi_rvalid && (_tmp_4 > 0)) begin
        _tmp_4 <= _tmp_4 - 1;
      end 
      if((_tmp_fsm_1 == 1) && ((myaxi_arready || !myaxi_arvalid) && (_tmp_14 == 0))) begin
        myaxi_araddr <= _tmp_11;
        myaxi_arlen <= _tmp_12 - 1;
        myaxi_arvalid <= 1;
        _tmp_14 <= _tmp_12;
      end 
      _myaxi_cond_1_1 <= 1;
      if(myaxi_arvalid && !myaxi_arready) begin
        myaxi_arvalid <= myaxi_arvalid;
      end 
      if(myaxi_rready && myaxi_rvalid && (_tmp_14 > 0)) begin
        _tmp_14 <= _tmp_14 - 1;
      end 
      if((_tmp_fsm_2 == 1) && ((myaxi_awready || !myaxi_awvalid) && (_tmp_67 == 0))) begin
        myaxi_awaddr <= _tmp_64;
        myaxi_awlen <= _tmp_65 - 1;
        myaxi_awvalid <= 1;
        _tmp_67 <= _tmp_65;
      end 
      if((_tmp_fsm_2 == 1) && ((myaxi_awready || !myaxi_awvalid) && (_tmp_67 == 0)) && (_tmp_65 == 0)) begin
        myaxi_awvalid <= 0;
      end 
      _myaxi_cond_2_1 <= 1;
      if(myaxi_awvalid && !myaxi_awready) begin
        myaxi_awvalid <= myaxi_awvalid;
      end 
      if(_tmp_valid_81 && ((_tmp_fsm_2 == 3) && ((_tmp_67 > 0) && (myaxi_wready || !myaxi_wvalid))) && ((_tmp_67 > 0) && (myaxi_wready || !myaxi_wvalid) && (_tmp_67 > 0))) begin
        myaxi_wdata <= _tmp_data_81;
        myaxi_wvalid <= 1;
        myaxi_wlast <= 0;
        myaxi_wstrb <= { 4{ 1'd1 } };
        _tmp_67 <= _tmp_67 - 1;
      end 
      if(_tmp_valid_81 && ((_tmp_fsm_2 == 3) && ((_tmp_67 > 0) && (myaxi_wready || !myaxi_wvalid))) && ((_tmp_67 > 0) && (myaxi_wready || !myaxi_wvalid) && (_tmp_67 > 0)) && (_tmp_67 == 1)) begin
        myaxi_wlast <= 1;
        _tmp_80 <= 1;
      end 
      _myaxi_cond_3_1 <= 1;
      if(myaxi_wvalid && !myaxi_wready) begin
        myaxi_wvalid <= myaxi_wvalid;
        myaxi_wlast <= myaxi_wlast;
        _tmp_80 <= _tmp_80;
      end 
      if((_tmp_fsm_3 == 1) && ((myaxi_arready || !myaxi_arvalid) && (_tmp_86 == 0))) begin
        myaxi_araddr <= _tmp_83;
        myaxi_arlen <= _tmp_84 - 1;
        myaxi_arvalid <= 1;
        _tmp_86 <= _tmp_84;
      end 
      _myaxi_cond_4_1 <= 1;
      if(myaxi_arvalid && !myaxi_arready) begin
        myaxi_arvalid <= myaxi_arvalid;
      end 
      if(myaxi_rready && myaxi_rvalid && (_tmp_86 > 0)) begin
        _tmp_86 <= _tmp_86 - 1;
      end 
      if((_tmp_fsm_4 == 1) && ((myaxi_arready || !myaxi_arvalid) && (_tmp_96 == 0))) begin
        myaxi_araddr <= _tmp_93;
        myaxi_arlen <= _tmp_94 - 1;
        myaxi_arvalid <= 1;
        _tmp_96 <= _tmp_94;
      end 
      _myaxi_cond_5_1 <= 1;
      if(myaxi_arvalid && !myaxi_arready) begin
        myaxi_arvalid <= myaxi_arvalid;
      end 
      if(myaxi_rready && myaxi_rvalid && (_tmp_96 > 0)) begin
        _tmp_96 <= _tmp_96 - 1;
      end 
      if((_tmp_fsm_5 == 1) && ((myaxi_awready || !myaxi_awvalid) && (_tmp_110 == 0))) begin
        myaxi_awaddr <= _tmp_107;
        myaxi_awlen <= _tmp_108 - 1;
        myaxi_awvalid <= 1;
        _tmp_110 <= _tmp_108;
      end 
      if((_tmp_fsm_5 == 1) && ((myaxi_awready || !myaxi_awvalid) && (_tmp_110 == 0)) && (_tmp_108 == 0)) begin
        myaxi_awvalid <= 0;
      end 
      _myaxi_cond_6_1 <= 1;
      if(myaxi_awvalid && !myaxi_awready) begin
        myaxi_awvalid <= myaxi_awvalid;
      end 
      if(_tmp_valid_124 && ((_tmp_fsm_5 == 3) && ((_tmp_110 > 0) && (myaxi_wready || !myaxi_wvalid))) && ((_tmp_110 > 0) && (myaxi_wready || !myaxi_wvalid) && (_tmp_110 > 0))) begin
        myaxi_wdata <= _tmp_data_124;
        myaxi_wvalid <= 1;
        myaxi_wlast <= 0;
        myaxi_wstrb <= { 4{ 1'd1 } };
        _tmp_110 <= _tmp_110 - 1;
      end 
      if(_tmp_valid_124 && ((_tmp_fsm_5 == 3) && ((_tmp_110 > 0) && (myaxi_wready || !myaxi_wvalid))) && ((_tmp_110 > 0) && (myaxi_wready || !myaxi_wvalid) && (_tmp_110 > 0)) && (_tmp_110 == 1)) begin
        myaxi_wlast <= 1;
        _tmp_123 <= 1;
      end 
      _myaxi_cond_7_1 <= 1;
      if(myaxi_wvalid && !myaxi_wready) begin
        myaxi_wvalid <= myaxi_wvalid;
        myaxi_wlast <= myaxi_wlast;
        _tmp_123 <= _tmp_123;
      end 
    end
  end

  assign _tmp_data_9 = _tmp_5;
  assign _tmp_valid_9 = _tmp_6;
  assign _tmp_data_19 = _tmp_15;
  assign _tmp_valid_19 = _tmp_16;
  assign _tmp_data_91 = _tmp_87;
  assign _tmp_valid_91 = _tmp_88;
  assign _tmp_data_101 = _tmp_97;
  assign _tmp_valid_101 = _tmp_98;

  always @(posedge CLK) begin
    if(RST) begin
      ram_a_0_addr <= 0;
      _tmp_7 <= 0;
      ram_a_0_wdata <= 0;
      ram_a_0_wenable <= 0;
      _tmp_8 <= 0;
      _ram_a_cond_0_1 <= 0;
      __tmp_25_1 <= 0;
      __tmp_26_1 <= 0;
      _tmp_30 <= 0;
      _tmp_20 <= 0;
      _tmp_21 <= 0;
      _tmp_28 <= 0;
      _tmp_29 <= 0;
      _tmp_27 <= 0;
      _tmp_31 <= 0;
      _tmp_36 <= 0;
      _tmp_37 <= 0;
      _tmp_34 <= 0;
      _tmp_38 <= 0;
      _tmp_35 <= 0;
      _tmp_89 <= 0;
      _tmp_90 <= 0;
      _ram_a_cond_1_1 <= 0;
      _ram_a_cond_2_1 <= 0;
      _tmp_102 <= 0;
      _ram_a_cond_3_1 <= 0;
      _ram_a_cond_3_2 <= 0;
    end else begin
      if(_ram_a_cond_3_2) begin
        _tmp_102 <= 0;
      end 
      if(_ram_a_cond_0_1) begin
        ram_a_0_wenable <= 0;
        _tmp_8 <= 0;
      end 
      if(_ram_a_cond_1_1) begin
        ram_a_0_wenable <= 0;
        _tmp_90 <= 0;
      end 
      if(_ram_a_cond_2_1) begin
        _tmp_102 <= 1;
      end 
      _ram_a_cond_3_2 <= _ram_a_cond_3_1;
      if((_tmp_fsm_0 == 2) && (_tmp_7 == 0)) begin
        ram_a_0_addr <= _tmp_0 - 1;
        _tmp_7 <= _tmp_2;
      end 
      if(_tmp_valid_9 && ((_tmp_7 > 0) && !_tmp_8) && (_tmp_7 > 0)) begin
        ram_a_0_addr <= ram_a_0_addr + 1;
        ram_a_0_wdata <= _tmp_data_9;
        ram_a_0_wenable <= 1;
        _tmp_7 <= _tmp_7 - 1;
      end 
      if(_tmp_valid_9 && ((_tmp_7 > 0) && !_tmp_8) && (_tmp_7 == 1)) begin
        _tmp_8 <= 1;
      end 
      _ram_a_cond_0_1 <= 1;
      __tmp_25_1 <= _tmp_25;
      __tmp_26_1 <= _tmp_26;
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_28) begin
        _tmp_30 <= 0;
        _tmp_20 <= 0;
        _tmp_21 <= 0;
        _tmp_28 <= 0;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_27) begin
        _tmp_20 <= 1;
        _tmp_21 <= 1;
        _tmp_30 <= _tmp_29;
        _tmp_29 <= 0;
        _tmp_27 <= 0;
        _tmp_28 <= 1;
      end 
      if((_mystream_fsm_2 == 1) && !_tmp_31 && !_tmp_29 && !_tmp_30) begin
        ram_a_0_addr <= _th_comp_offset_0;
        _tmp_31 <= 1;
        _tmp_27 <= 1;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31) begin
        ram_a_0_addr <= _tmp_32;
        _tmp_27 <= 1;
        _tmp_29 <= 0;
      end 
      if((_mystream_fsm_2 == 1) && !_tmp_31 && !_tmp_29 && !_tmp_30) begin
        _tmp_36 <= 7;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31) begin
        _tmp_36 <= _tmp_36 - 1;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && (_tmp_36 == 0)) begin
        _tmp_36 <= 7;
      end 
      if((_mystream_fsm_2 == 1) && !_tmp_31 && !_tmp_29 && !_tmp_30) begin
        _tmp_37 <= 3;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && (_tmp_36 == 0)) begin
        _tmp_37 <= _tmp_37 - 1;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && (_tmp_36 == 0) && (_tmp_37 == 0)) begin
        _tmp_37 <= 3;
      end 
      if((_mystream_fsm_2 == 1) && !_tmp_31 && !_tmp_29 && !_tmp_30) begin
        _tmp_34 <= 0;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && (_tmp_36 == 1) && !0) begin
        _tmp_34 <= _tmp_34 + 16;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && (_tmp_36 == 1) && (_tmp_37 == 0)) begin
        _tmp_34 <= 0;
      end 
      if((_mystream_fsm_2 == 1) && !_tmp_31 && !_tmp_29 && !_tmp_30) begin
        _tmp_38 <= 15;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && ((_tmp_36 == 0) && (_tmp_37 == 0))) begin
        _tmp_38 <= _tmp_38 - 1;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && ((_tmp_36 == 0) && (_tmp_37 == 0)) && (_tmp_38 == 0)) begin
        _tmp_38 <= 15;
      end 
      if((_mystream_fsm_2 == 1) && !_tmp_31 && !_tmp_29 && !_tmp_30) begin
        _tmp_35 <= 0;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && ((_tmp_36 == 1) && (_tmp_37 == 0)) && !(0 && 0)) begin
        _tmp_35 <= _tmp_35 + 1;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && ((_tmp_36 == 1) && (_tmp_37 == 0)) && (_tmp_38 == 0)) begin
        _tmp_35 <= 0;
      end 
      if((_tmp_22 || !_tmp_20) && (_tmp_23 || !_tmp_21) && _tmp_31 && ((_tmp_36 == 0) && (_tmp_37 == 0) && (_tmp_38 == 0))) begin
        _tmp_31 <= 0;
        _tmp_29 <= 1;
      end 
      if((_tmp_fsm_3 == 2) && (_tmp_89 == 0)) begin
        ram_a_0_addr <= _tmp_82 - 1;
        _tmp_89 <= _tmp_84;
      end 
      if(_tmp_valid_91 && ((_tmp_89 > 0) && !_tmp_90) && (_tmp_89 > 0)) begin
        ram_a_0_addr <= ram_a_0_addr + 1;
        ram_a_0_wdata <= _tmp_data_91;
        ram_a_0_wenable <= 1;
        _tmp_89 <= _tmp_89 - 1;
      end 
      if(_tmp_valid_91 && ((_tmp_89 > 0) && !_tmp_90) && (_tmp_89 == 1)) begin
        _tmp_90 <= 1;
      end 
      _ram_a_cond_1_1 <= 1;
      if(th_sequential == 5) begin
        ram_a_0_addr <= _th_sequential_i_10 + _th_sequential_offset_8;
      end 
      _ram_a_cond_2_1 <= th_sequential == 5;
      _ram_a_cond_3_1 <= th_sequential == 5;
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      ram_b_0_addr <= 0;
      _tmp_17 <= 0;
      ram_b_0_wdata <= 0;
      ram_b_0_wenable <= 0;
      _tmp_18 <= 0;
      _ram_b_cond_0_1 <= 0;
      __tmp_44_1 <= 0;
      __tmp_45_1 <= 0;
      _tmp_49 <= 0;
      _tmp_39 <= 0;
      _tmp_40 <= 0;
      _tmp_47 <= 0;
      _tmp_48 <= 0;
      _tmp_46 <= 0;
      _tmp_50 <= 0;
      _tmp_55 <= 0;
      _tmp_56 <= 0;
      _tmp_53 <= 0;
      _tmp_57 <= 0;
      _tmp_54 <= 0;
      _tmp_99 <= 0;
      _tmp_100 <= 0;
      _ram_b_cond_1_1 <= 0;
      _ram_b_cond_2_1 <= 0;
      _tmp_104 <= 0;
      _ram_b_cond_3_1 <= 0;
      _ram_b_cond_3_2 <= 0;
    end else begin
      if(_ram_b_cond_3_2) begin
        _tmp_104 <= 0;
      end 
      if(_ram_b_cond_0_1) begin
        ram_b_0_wenable <= 0;
        _tmp_18 <= 0;
      end 
      if(_ram_b_cond_1_1) begin
        ram_b_0_wenable <= 0;
        _tmp_100 <= 0;
      end 
      if(_ram_b_cond_2_1) begin
        _tmp_104 <= 1;
      end 
      _ram_b_cond_3_2 <= _ram_b_cond_3_1;
      if((_tmp_fsm_1 == 2) && (_tmp_17 == 0)) begin
        ram_b_0_addr <= _tmp_10 - 1;
        _tmp_17 <= _tmp_12;
      end 
      if(_tmp_valid_19 && ((_tmp_17 > 0) && !_tmp_18) && (_tmp_17 > 0)) begin
        ram_b_0_addr <= ram_b_0_addr + 1;
        ram_b_0_wdata <= _tmp_data_19;
        ram_b_0_wenable <= 1;
        _tmp_17 <= _tmp_17 - 1;
      end 
      if(_tmp_valid_19 && ((_tmp_17 > 0) && !_tmp_18) && (_tmp_17 == 1)) begin
        _tmp_18 <= 1;
      end 
      _ram_b_cond_0_1 <= 1;
      __tmp_44_1 <= _tmp_44;
      __tmp_45_1 <= _tmp_45;
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_47) begin
        _tmp_49 <= 0;
        _tmp_39 <= 0;
        _tmp_40 <= 0;
        _tmp_47 <= 0;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_46) begin
        _tmp_39 <= 1;
        _tmp_40 <= 1;
        _tmp_49 <= _tmp_48;
        _tmp_48 <= 0;
        _tmp_46 <= 0;
        _tmp_47 <= 1;
      end 
      if((_mystream_fsm_4 == 1) && !_tmp_50 && !_tmp_48 && !_tmp_49) begin
        ram_b_0_addr <= _th_comp_offset_0;
        _tmp_50 <= 1;
        _tmp_46 <= 1;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50) begin
        ram_b_0_addr <= _tmp_51;
        _tmp_46 <= 1;
        _tmp_48 <= 0;
      end 
      if((_mystream_fsm_4 == 1) && !_tmp_50 && !_tmp_48 && !_tmp_49) begin
        _tmp_55 <= 7;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50) begin
        _tmp_55 <= _tmp_55 - 1;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && (_tmp_55 == 0)) begin
        _tmp_55 <= 7;
      end 
      if((_mystream_fsm_4 == 1) && !_tmp_50 && !_tmp_48 && !_tmp_49) begin
        _tmp_56 <= 3;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && (_tmp_55 == 0)) begin
        _tmp_56 <= _tmp_56 - 1;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && (_tmp_55 == 0) && (_tmp_56 == 0)) begin
        _tmp_56 <= 3;
      end 
      if((_mystream_fsm_4 == 1) && !_tmp_50 && !_tmp_48 && !_tmp_49) begin
        _tmp_53 <= 0;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && (_tmp_55 == 1) && !0) begin
        _tmp_53 <= _tmp_53 + 16;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && (_tmp_55 == 1) && (_tmp_56 == 0)) begin
        _tmp_53 <= 0;
      end 
      if((_mystream_fsm_4 == 1) && !_tmp_50 && !_tmp_48 && !_tmp_49) begin
        _tmp_57 <= 15;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && ((_tmp_55 == 0) && (_tmp_56 == 0))) begin
        _tmp_57 <= _tmp_57 - 1;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && ((_tmp_55 == 0) && (_tmp_56 == 0)) && (_tmp_57 == 0)) begin
        _tmp_57 <= 15;
      end 
      if((_mystream_fsm_4 == 1) && !_tmp_50 && !_tmp_48 && !_tmp_49) begin
        _tmp_54 <= 0;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && ((_tmp_55 == 1) && (_tmp_56 == 0)) && !(0 && 0)) begin
        _tmp_54 <= _tmp_54 + 1;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && ((_tmp_55 == 1) && (_tmp_56 == 0)) && (_tmp_57 == 0)) begin
        _tmp_54 <= 0;
      end 
      if((_tmp_41 || !_tmp_39) && (_tmp_42 || !_tmp_40) && _tmp_50 && ((_tmp_55 == 0) && (_tmp_56 == 0) && (_tmp_57 == 0))) begin
        _tmp_50 <= 0;
        _tmp_48 <= 1;
      end 
      if((_tmp_fsm_4 == 2) && (_tmp_99 == 0)) begin
        ram_b_0_addr <= _tmp_92 - 1;
        _tmp_99 <= _tmp_94;
      end 
      if(_tmp_valid_101 && ((_tmp_99 > 0) && !_tmp_100) && (_tmp_99 > 0)) begin
        ram_b_0_addr <= ram_b_0_addr + 1;
        ram_b_0_wdata <= _tmp_data_101;
        ram_b_0_wenable <= 1;
        _tmp_99 <= _tmp_99 - 1;
      end 
      if(_tmp_valid_101 && ((_tmp_99 > 0) && !_tmp_100) && (_tmp_99 == 1)) begin
        _tmp_100 <= 1;
      end 
      _ram_b_cond_1_1 <= 1;
      if(th_sequential == 7) begin
        ram_b_0_addr <= _th_sequential_i_10 + _th_sequential_offset_8;
      end 
      _ram_b_cond_2_1 <= th_sequential == 7;
      _ram_b_cond_3_1 <= th_sequential == 7;
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      ram_c_0_addr <= 0;
      _tmp_58 <= 0;
      ram_c_0_wdata <= 0;
      ram_c_0_wenable <= 0;
      _tmp_59 <= 0;
      _ram_c_cond_0_1 <= 0;
      __tmp_73_1 <= 0;
      __tmp_74_1 <= 0;
      _tmp_78 <= 0;
      _tmp_68 <= 0;
      _tmp_69 <= 0;
      _tmp_76 <= 0;
      _tmp_77 <= 0;
      _tmp_75 <= 0;
      _tmp_79 <= 0;
      _ram_c_cond_1_1 <= 0;
      __tmp_116_1 <= 0;
      __tmp_117_1 <= 0;
      _tmp_121 <= 0;
      _tmp_111 <= 0;
      _tmp_112 <= 0;
      _tmp_119 <= 0;
      _tmp_120 <= 0;
      _tmp_118 <= 0;
      _tmp_122 <= 0;
      _ram_c_cond_2_1 <= 0;
      _tmp_125 <= 0;
      _ram_c_cond_3_1 <= 0;
      _ram_c_cond_3_2 <= 0;
      _ram_c_cond_4_1 <= 0;
      _tmp_127 <= 0;
      _ram_c_cond_5_1 <= 0;
      _ram_c_cond_5_2 <= 0;
    end else begin
      if(_ram_c_cond_3_2) begin
        _tmp_125 <= 0;
      end 
      if(_ram_c_cond_5_2) begin
        _tmp_127 <= 0;
      end 
      if(_ram_c_cond_0_1) begin
        ram_c_0_wenable <= 0;
        _tmp_59 <= 0;
      end 
      if(_ram_c_cond_1_1) begin
        ram_c_0_wenable <= 0;
      end 
      if(_ram_c_cond_2_1) begin
        _tmp_125 <= 1;
      end 
      _ram_c_cond_3_2 <= _ram_c_cond_3_1;
      if(_ram_c_cond_4_1) begin
        _tmp_127 <= 1;
      end 
      _ram_c_cond_5_2 <= _ram_c_cond_5_1;
      if((_mystream_fsm_6 == 1) && (_tmp_58 == 0)) begin
        ram_c_0_addr <= _th_comp_offset_0 - 1;
        _tmp_58 <= 1;
      end 
      if(_tmp_data_62 && (_tmp_valid_61 && ((_tmp_58 > 0) && !_tmp_59 && _tmp_all_valid_60)) && (_tmp_58 > 0)) begin
        ram_c_0_addr <= ram_c_0_addr + 1;
        ram_c_0_wdata <= _tmp_data_61;
        ram_c_0_wenable <= 1;
        _tmp_58 <= _tmp_58 - 1;
      end 
      if(_tmp_data_62 && (_tmp_valid_61 && ((_tmp_58 > 0) && !_tmp_59 && _tmp_all_valid_60)) && (_tmp_58 == 1)) begin
        _tmp_59 <= 1;
      end 
      _ram_c_cond_0_1 <= 1;
      __tmp_73_1 <= _tmp_73;
      __tmp_74_1 <= _tmp_74;
      if((_tmp_70 || !_tmp_68) && (_tmp_71 || !_tmp_69) && _tmp_76) begin
        _tmp_78 <= 0;
        _tmp_68 <= 0;
        _tmp_69 <= 0;
        _tmp_76 <= 0;
      end 
      if((_tmp_70 || !_tmp_68) && (_tmp_71 || !_tmp_69) && _tmp_75) begin
        _tmp_68 <= 1;
        _tmp_69 <= 1;
        _tmp_78 <= _tmp_77;
        _tmp_77 <= 0;
        _tmp_75 <= 0;
        _tmp_76 <= 1;
      end 
      if((_tmp_fsm_2 == 2) && (_tmp_79 == 0) && !_tmp_77 && !_tmp_78) begin
        ram_c_0_addr <= _tmp_63;
        _tmp_79 <= _tmp_65 - 1;
        _tmp_75 <= 1;
      end 
      if((_tmp_70 || !_tmp_68) && (_tmp_71 || !_tmp_69) && (_tmp_79 > 0)) begin
        ram_c_0_addr <= ram_c_0_addr + 1;
        _tmp_79 <= _tmp_79 - 1;
        _tmp_75 <= 1;
        _tmp_77 <= 0;
      end 
      if((_tmp_70 || !_tmp_68) && (_tmp_71 || !_tmp_69) && (_tmp_79 == 1)) begin
        _tmp_77 <= 1;
      end 
      if(th_sequential == 11) begin
        ram_c_0_addr <= _th_sequential_offset_8;
        ram_c_0_wdata <= _th_sequential_sum_9;
        ram_c_0_wenable <= 1;
      end 
      _ram_c_cond_1_1 <= th_sequential == 11;
      __tmp_116_1 <= _tmp_116;
      __tmp_117_1 <= _tmp_117;
      if((_tmp_113 || !_tmp_111) && (_tmp_114 || !_tmp_112) && _tmp_119) begin
        _tmp_121 <= 0;
        _tmp_111 <= 0;
        _tmp_112 <= 0;
        _tmp_119 <= 0;
      end 
      if((_tmp_113 || !_tmp_111) && (_tmp_114 || !_tmp_112) && _tmp_118) begin
        _tmp_111 <= 1;
        _tmp_112 <= 1;
        _tmp_121 <= _tmp_120;
        _tmp_120 <= 0;
        _tmp_118 <= 0;
        _tmp_119 <= 1;
      end 
      if((_tmp_fsm_5 == 2) && (_tmp_122 == 0) && !_tmp_120 && !_tmp_121) begin
        ram_c_0_addr <= _tmp_106;
        _tmp_122 <= _tmp_108 - 1;
        _tmp_118 <= 1;
      end 
      if((_tmp_113 || !_tmp_111) && (_tmp_114 || !_tmp_112) && (_tmp_122 > 0)) begin
        ram_c_0_addr <= ram_c_0_addr + 1;
        _tmp_122 <= _tmp_122 - 1;
        _tmp_118 <= 1;
        _tmp_120 <= 0;
      end 
      if((_tmp_113 || !_tmp_111) && (_tmp_114 || !_tmp_112) && (_tmp_122 == 1)) begin
        _tmp_120 <= 1;
      end 
      if(th_comp == 27) begin
        ram_c_0_addr <= _th_comp_offset_stream_13;
      end 
      _ram_c_cond_2_1 <= th_comp == 27;
      _ram_c_cond_3_1 <= th_comp == 27;
      if(th_comp == 29) begin
        ram_c_0_addr <= _th_comp_offset_seq_14;
      end 
      _ram_c_cond_4_1 <= th_comp == 29;
      _ram_c_cond_5_1 <= th_comp == 29;
    end
  end

  assign _tmp_data_81 = _tmp_74;
  assign _tmp_valid_81 = _tmp_68;
  assign _tmp_70 = 1 && _tmp_ready_81;
  assign _tmp_data_124 = _tmp_117;
  assign _tmp_valid_124 = _tmp_111;
  assign _tmp_113 = 1 && _tmp_ready_124;
  reg [32-1:0] _tmp_data_129;
  reg _tmp_valid_129;
  wire _tmp_ready_129;
  wire [32-1:0] _tmp_data_130;
  wire _tmp_valid_130;
  wire _tmp_ready_130;
  wire [64-1:0] _tmp_odata_130;
  reg [64-1:0] _tmp_data_reg_130;
  assign _tmp_data_130 = _tmp_data_reg_130;
  wire _tmp_ovalid_130;
  reg _tmp_valid_reg_130;
  assign _tmp_valid_130 = _tmp_valid_reg_130;
  wire _tmp_enable_130;
  wire _tmp_update_130;
  assign _tmp_enable_130 = (_tmp_ready_130 || !_tmp_valid_130) && (_tmp_22 && _tmp_41) && (_tmp_20 && _tmp_39);
  assign _tmp_update_130 = _tmp_ready_130 || !_tmp_valid_130;

  multiplier_0
  mul130
  (
    .CLK(CLK),
    .RST(RST),
    .update(_tmp_update_130),
    .enable(_tmp_enable_130),
    .valid(_tmp_ovalid_130),
    .a(_tmp_26),
    .b(_tmp_45),
    .c(_tmp_odata_130)
  );

  assign _tmp_22 = 1 && ((_tmp_ready_130 || !_tmp_valid_130) && (_tmp_20 && _tmp_39));
  assign _tmp_41 = 1 && ((_tmp_ready_130 || !_tmp_valid_130) && (_tmp_20 && _tmp_39));
  reg [1-1:0] _tmp_data_131;
  reg _tmp_valid_131;
  wire _tmp_ready_131;
  assign _tmp_ready_129 = (_tmp_ready_131 || !_tmp_valid_131) && _tmp_valid_129;
  reg [1-1:0] _tmp_data_132;
  reg [1-1:0] _tmp_data_133;
  reg [1-1:0] _tmp_data_134;
  reg _tmp_valid_134;
  wire _tmp_ready_134;
  reg [1-1:0] _tmp_data_135;
  reg _tmp_valid_135;
  wire _tmp_ready_135;
  assign _tmp_ready_131 = (_tmp_ready_134 || !_tmp_valid_134) && _tmp_valid_131 && ((_tmp_ready_135 || !_tmp_valid_135) && _tmp_valid_131);
  reg [1-1:0] _tmp_data_136;
  reg _tmp_valid_136;
  wire _tmp_ready_136;
  assign _tmp_ready_134 = (_tmp_ready_136 || !_tmp_valid_136) && _tmp_valid_134;
  reg [1-1:0] _tmp_data_137;
  reg _tmp_valid_137;
  wire _tmp_ready_137;
  assign _tmp_ready_135 = (_tmp_ready_137 || !_tmp_valid_137) && _tmp_valid_135;
  reg [1-1:0] _tmp_data_138;
  reg _tmp_valid_138;
  wire _tmp_ready_138;
  assign _tmp_ready_136 = (_tmp_ready_138 || !_tmp_valid_138) && _tmp_valid_136;
  reg [1-1:0] _tmp_data_139;
  reg _tmp_valid_139;
  wire _tmp_ready_139;
  assign _tmp_ready_137 = (_tmp_ready_139 || !_tmp_valid_139) && _tmp_valid_137;
  reg [1-1:0] _tmp_data_140;
  reg _tmp_valid_140;
  wire _tmp_ready_140;
  assign _tmp_ready_138 = (_tmp_ready_140 || !_tmp_valid_140) && _tmp_valid_138;
  reg [1-1:0] _tmp_data_141;
  reg _tmp_valid_141;
  wire _tmp_ready_141;
  assign _tmp_ready_139 = (_tmp_ready_141 || !_tmp_valid_141) && _tmp_valid_139;
  reg [1-1:0] _tmp_data_142;
  reg _tmp_valid_142;
  wire _tmp_ready_142;
  assign _tmp_ready_140 = (_tmp_ready_142 || !_tmp_valid_142) && _tmp_valid_140;
  reg [1-1:0] _tmp_data_143;
  reg _tmp_valid_143;
  wire _tmp_ready_143;
  assign _tmp_ready_141 = (_tmp_ready_143 || !_tmp_valid_143) && _tmp_valid_141;
  reg [1-1:0] _tmp_data_144;
  reg _tmp_valid_144;
  wire _tmp_ready_144;
  assign _tmp_ready_142 = (_tmp_ready_144 || !_tmp_valid_144) && _tmp_valid_142;
  reg [1-1:0] _tmp_data_145;
  reg _tmp_valid_145;
  wire _tmp_ready_145;
  assign _tmp_ready_143 = (_tmp_ready_145 || !_tmp_valid_145) && _tmp_valid_143;
  reg [32-1:0] _tmp_data_146;
  reg _tmp_valid_146;
  wire _tmp_ready_146;
  assign _tmp_ready_130 = (_tmp_ready_146 || !_tmp_valid_146) && (_tmp_valid_130 && _tmp_valid_144);
  assign _tmp_ready_144 = (_tmp_ready_146 || !_tmp_valid_146) && (_tmp_valid_130 && _tmp_valid_144);
  reg [1-1:0] _tmp_data_147;
  reg _tmp_valid_147;
  wire _tmp_ready_147;
  assign _tmp_ready_145 = (_tmp_ready_147 || !_tmp_valid_147) && _tmp_valid_145;
  assign _tmp_data_61 = _tmp_data_146;
  assign _tmp_valid_61 = _tmp_valid_146;
  assign _tmp_ready_146 = _tmp_ready_61;
  assign _tmp_data_62 = _tmp_data_147;
  assign _tmp_valid_62 = _tmp_valid_147;
  assign _tmp_ready_147 = _tmp_ready_62;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_data_129 <= 1'sd0;
      _tmp_valid_129 <= 0;
      _tmp_data_reg_130 <= 0;
      _tmp_valid_reg_130 <= 0;
      _tmp_data_131 <= 0;
      _tmp_valid_131 <= 0;
      _tmp_data_132 <= 0;
      _tmp_data_133 <= 0;
      _tmp_data_134 <= 0;
      _tmp_valid_134 <= 0;
      _tmp_data_135 <= 0;
      _tmp_valid_135 <= 0;
      _tmp_data_136 <= 0;
      _tmp_valid_136 <= 0;
      _tmp_data_137 <= 0;
      _tmp_valid_137 <= 0;
      _tmp_data_138 <= 0;
      _tmp_valid_138 <= 0;
      _tmp_data_139 <= 0;
      _tmp_valid_139 <= 0;
      _tmp_data_140 <= 0;
      _tmp_valid_140 <= 0;
      _tmp_data_141 <= 0;
      _tmp_valid_141 <= 0;
      _tmp_data_142 <= 0;
      _tmp_valid_142 <= 0;
      _tmp_data_143 <= 0;
      _tmp_valid_143 <= 0;
      _tmp_data_144 <= 0;
      _tmp_valid_144 <= 0;
      _tmp_data_145 <= 0;
      _tmp_valid_145 <= 0;
      _tmp_data_146 <= 1'sd0;
      _tmp_valid_146 <= 0;
      _tmp_data_147 <= 0;
      _tmp_valid_147 <= 0;
    end else begin
      if((_tmp_ready_129 || !_tmp_valid_129) && 1 && 1) begin
        _tmp_data_129 <= (_tmp_data_129 >= 511)? 0 : _tmp_data_129 + 2'sd1;
      end 
      if(_tmp_valid_129 && _tmp_ready_129) begin
        _tmp_valid_129 <= 0;
      end 
      if((_tmp_ready_129 || !_tmp_valid_129) && 1) begin
        _tmp_valid_129 <= 1;
      end 
      if(_tmp_ready_130 || !_tmp_valid_130) begin
        _tmp_data_reg_130 <= _tmp_odata_130;
      end 
      if(_tmp_ready_130 || !_tmp_valid_130) begin
        _tmp_valid_reg_130 <= _tmp_ovalid_130;
      end 
      if((_tmp_ready_131 || !_tmp_valid_131) && _tmp_ready_129 && _tmp_valid_129) begin
        _tmp_data_131 <= _tmp_data_129 == 10'sd511;
      end 
      if(_tmp_valid_131 && _tmp_ready_131) begin
        _tmp_valid_131 <= 0;
      end 
      if((_tmp_ready_131 || !_tmp_valid_131) && _tmp_ready_129) begin
        _tmp_valid_131 <= _tmp_valid_129;
      end 
      if(_tmp_valid_131 && _tmp_ready_131) begin
        _tmp_data_132 <= _tmp_data_131;
      end 
      if(_tmp_valid_131 && _tmp_ready_131) begin
        _tmp_data_133 <= _tmp_data_132;
      end 
      if((_tmp_ready_134 || !_tmp_valid_134) && _tmp_ready_131 && _tmp_valid_131) begin
        _tmp_data_134 <= _tmp_data_133;
      end 
      if(_tmp_valid_134 && _tmp_ready_134) begin
        _tmp_valid_134 <= 0;
      end 
      if((_tmp_ready_134 || !_tmp_valid_134) && _tmp_ready_131) begin
        _tmp_valid_134 <= _tmp_valid_131;
      end 
      if((_tmp_ready_135 || !_tmp_valid_135) && _tmp_ready_131 && _tmp_valid_131) begin
        _tmp_data_135 <= _tmp_data_132;
      end 
      if(_tmp_valid_135 && _tmp_ready_135) begin
        _tmp_valid_135 <= 0;
      end 
      if((_tmp_ready_135 || !_tmp_valid_135) && _tmp_ready_131) begin
        _tmp_valid_135 <= _tmp_valid_131;
      end 
      if((_tmp_ready_136 || !_tmp_valid_136) && _tmp_ready_134 && _tmp_valid_134) begin
        _tmp_data_136 <= _tmp_data_134;
      end 
      if(_tmp_valid_136 && _tmp_ready_136) begin
        _tmp_valid_136 <= 0;
      end 
      if((_tmp_ready_136 || !_tmp_valid_136) && _tmp_ready_134) begin
        _tmp_valid_136 <= _tmp_valid_134;
      end 
      if((_tmp_ready_137 || !_tmp_valid_137) && _tmp_ready_135 && _tmp_valid_135) begin
        _tmp_data_137 <= _tmp_data_135;
      end 
      if(_tmp_valid_137 && _tmp_ready_137) begin
        _tmp_valid_137 <= 0;
      end 
      if((_tmp_ready_137 || !_tmp_valid_137) && _tmp_ready_135) begin
        _tmp_valid_137 <= _tmp_valid_135;
      end 
      if((_tmp_ready_138 || !_tmp_valid_138) && _tmp_ready_136 && _tmp_valid_136) begin
        _tmp_data_138 <= _tmp_data_136;
      end 
      if(_tmp_valid_138 && _tmp_ready_138) begin
        _tmp_valid_138 <= 0;
      end 
      if((_tmp_ready_138 || !_tmp_valid_138) && _tmp_ready_136) begin
        _tmp_valid_138 <= _tmp_valid_136;
      end 
      if((_tmp_ready_139 || !_tmp_valid_139) && _tmp_ready_137 && _tmp_valid_137) begin
        _tmp_data_139 <= _tmp_data_137;
      end 
      if(_tmp_valid_139 && _tmp_ready_139) begin
        _tmp_valid_139 <= 0;
      end 
      if((_tmp_ready_139 || !_tmp_valid_139) && _tmp_ready_137) begin
        _tmp_valid_139 <= _tmp_valid_137;
      end 
      if((_tmp_ready_140 || !_tmp_valid_140) && _tmp_ready_138 && _tmp_valid_138) begin
        _tmp_data_140 <= _tmp_data_138;
      end 
      if(_tmp_valid_140 && _tmp_ready_140) begin
        _tmp_valid_140 <= 0;
      end 
      if((_tmp_ready_140 || !_tmp_valid_140) && _tmp_ready_138) begin
        _tmp_valid_140 <= _tmp_valid_138;
      end 
      if((_tmp_ready_141 || !_tmp_valid_141) && _tmp_ready_139 && _tmp_valid_139) begin
        _tmp_data_141 <= _tmp_data_139;
      end 
      if(_tmp_valid_141 && _tmp_ready_141) begin
        _tmp_valid_141 <= 0;
      end 
      if((_tmp_ready_141 || !_tmp_valid_141) && _tmp_ready_139) begin
        _tmp_valid_141 <= _tmp_valid_139;
      end 
      if((_tmp_ready_142 || !_tmp_valid_142) && _tmp_ready_140 && _tmp_valid_140) begin
        _tmp_data_142 <= _tmp_data_140;
      end 
      if(_tmp_valid_142 && _tmp_ready_142) begin
        _tmp_valid_142 <= 0;
      end 
      if((_tmp_ready_142 || !_tmp_valid_142) && _tmp_ready_140) begin
        _tmp_valid_142 <= _tmp_valid_140;
      end 
      if((_tmp_ready_143 || !_tmp_valid_143) && _tmp_ready_141 && _tmp_valid_141) begin
        _tmp_data_143 <= _tmp_data_141;
      end 
      if(_tmp_valid_143 && _tmp_ready_143) begin
        _tmp_valid_143 <= 0;
      end 
      if((_tmp_ready_143 || !_tmp_valid_143) && _tmp_ready_141) begin
        _tmp_valid_143 <= _tmp_valid_141;
      end 
      if((_tmp_ready_144 || !_tmp_valid_144) && _tmp_ready_142 && _tmp_valid_142) begin
        _tmp_data_144 <= _tmp_data_142;
      end 
      if(_tmp_valid_144 && _tmp_ready_144) begin
        _tmp_valid_144 <= 0;
      end 
      if((_tmp_ready_144 || !_tmp_valid_144) && _tmp_ready_142) begin
        _tmp_valid_144 <= _tmp_valid_142;
      end 
      if((_tmp_ready_145 || !_tmp_valid_145) && _tmp_ready_143 && _tmp_valid_143) begin
        _tmp_data_145 <= _tmp_data_143;
      end 
      if(_tmp_valid_145 && _tmp_ready_145) begin
        _tmp_valid_145 <= 0;
      end 
      if((_tmp_ready_145 || !_tmp_valid_145) && _tmp_ready_143) begin
        _tmp_valid_145 <= _tmp_valid_143;
      end 
      if((_tmp_ready_146 || !_tmp_valid_146) && (_tmp_ready_130 && _tmp_ready_144) && (_tmp_valid_130 && _tmp_valid_144)) begin
        _tmp_data_146 <= _tmp_data_146 + _tmp_data_130;
      end 
      if(_tmp_valid_146 && _tmp_ready_146) begin
        _tmp_valid_146 <= 0;
      end 
      if((_tmp_ready_146 || !_tmp_valid_146) && (_tmp_ready_130 && _tmp_ready_144)) begin
        _tmp_valid_146 <= _tmp_valid_130 && _tmp_valid_144;
      end 
      if((_tmp_ready_146 || !_tmp_valid_146) && (_tmp_ready_130 && _tmp_ready_144) && (_tmp_valid_130 && _tmp_valid_144) && _tmp_data_144) begin
        _tmp_data_146 <= 1'sd0 + _tmp_data_130;
      end 
      if((_tmp_ready_147 || !_tmp_valid_147) && _tmp_ready_145 && _tmp_valid_145) begin
        _tmp_data_147 <= _tmp_data_145;
      end 
      if(_tmp_valid_147 && _tmp_ready_147) begin
        _tmp_valid_147 <= 0;
      end 
      if((_tmp_ready_147 || !_tmp_valid_147) && _tmp_ready_145) begin
        _tmp_valid_147 <= _tmp_valid_145;
      end 
    end
  end

  localparam th_comp_1 = 1;
  localparam th_comp_2 = 2;
  localparam th_comp_3 = 3;
  localparam th_comp_4 = 4;
  localparam th_comp_5 = 5;
  localparam th_comp_6 = 6;
  localparam th_comp_7 = 7;
  localparam th_comp_8 = 8;
  localparam th_comp_9 = 9;
  localparam th_comp_10 = 10;
  localparam th_comp_11 = 11;
  localparam th_comp_12 = 12;
  localparam th_comp_13 = 13;
  localparam th_comp_14 = 14;
  localparam th_comp_15 = 15;
  localparam th_comp_16 = 16;
  localparam th_comp_17 = 17;
  localparam th_comp_18 = 18;
  localparam th_comp_19 = 19;
  localparam th_comp_20 = 20;
  localparam th_comp_21 = 21;
  localparam th_comp_22 = 22;
  localparam th_comp_23 = 23;
  localparam th_comp_24 = 24;
  localparam th_comp_25 = 25;
  localparam th_comp_26 = 26;
  localparam th_comp_27 = 27;
  localparam th_comp_28 = 28;
  localparam th_comp_29 = 29;
  localparam th_comp_30 = 30;
  localparam th_comp_31 = 31;
  localparam th_comp_32 = 32;
  localparam th_comp_33 = 33;
  localparam th_comp_34 = 34;
  localparam th_comp_35 = 35;
  localparam th_comp_36 = 36;
  localparam th_comp_37 = 37;

  always @(posedge CLK) begin
    if(RST) begin
      th_comp <= th_comp_init;
      _th_comp_offset_0 <= 0;
      _tmp_0 <= 0;
      _tmp_1 <= 0;
      _tmp_3 <= 0;
      _tmp_2 <= 0;
      _tmp_10 <= 0;
      _tmp_11 <= 0;
      _tmp_13 <= 0;
      _tmp_12 <= 0;
      _tmp_63 <= 0;
      _tmp_64 <= 0;
      _tmp_66 <= 0;
      _tmp_65 <= 0;
      _tmp_82 <= 0;
      _tmp_83 <= 0;
      _tmp_85 <= 0;
      _tmp_84 <= 0;
      _tmp_92 <= 0;
      _tmp_93 <= 0;
      _tmp_95 <= 0;
      _tmp_94 <= 0;
      _tmp_106 <= 0;
      _tmp_107 <= 0;
      _tmp_109 <= 0;
      _tmp_108 <= 0;
      _th_comp_offset_stream_13 <= 0;
      _th_comp_offset_seq_14 <= 0;
      _th_comp_all_ok_15 <= 0;
      _tmp_126 <= 0;
      _th_comp_st_16 <= 0;
      _tmp_128 <= 0;
      _th_comp_sq_17 <= 0;
    end else begin
      case(th_comp)
        th_comp_init: begin
          th_comp <= th_comp_1;
        end
        th_comp_1: begin
          _th_comp_offset_0 <= 0;
          th_comp <= th_comp_2;
        end
        th_comp_2: begin
          _tmp_0 <= _th_comp_offset_0;
          _tmp_1 <= 0;
          _tmp_3 <= 512;
          th_comp <= th_comp_3;
        end
        th_comp_3: begin
          if(_tmp_3 <= 256) begin
            _tmp_2 <= _tmp_3;
            _tmp_3 <= 0;
          end else begin
            _tmp_2 <= 256;
            _tmp_3 <= _tmp_3 - 256;
          end
          th_comp <= th_comp_4;
        end
        th_comp_4: begin
          if(_tmp_8) begin
            _tmp_0 <= _tmp_0 + _tmp_2;
            _tmp_1 <= _tmp_1 + (_tmp_2 << 2);
          end 
          if(_tmp_8 && (_tmp_3 > 0)) begin
            th_comp <= th_comp_3;
          end 
          if(_tmp_8 && (_tmp_3 == 0)) begin
            th_comp <= th_comp_5;
          end 
        end
        th_comp_5: begin
          _tmp_10 <= _th_comp_offset_0;
          _tmp_11 <= 0;
          _tmp_13 <= 512;
          th_comp <= th_comp_6;
        end
        th_comp_6: begin
          if(_tmp_13 <= 256) begin
            _tmp_12 <= _tmp_13;
            _tmp_13 <= 0;
          end else begin
            _tmp_12 <= 256;
            _tmp_13 <= _tmp_13 - 256;
          end
          th_comp <= th_comp_7;
        end
        th_comp_7: begin
          if(_tmp_18) begin
            _tmp_10 <= _tmp_10 + _tmp_12;
            _tmp_11 <= _tmp_11 + (_tmp_12 << 2);
          end 
          if(_tmp_18 && (_tmp_13 > 0)) begin
            th_comp <= th_comp_6;
          end 
          if(_tmp_18 && (_tmp_13 == 0)) begin
            th_comp <= th_comp_8;
          end 
        end
        th_comp_8: begin
          th_comp <= th_comp_9;
        end
        th_comp_9: begin
          if(_mystream_flag_1 && _mystream_flag_3 && _mystream_flag_5) begin
            th_comp <= th_comp_10;
          end 
        end
        th_comp_10: begin
          _tmp_63 <= _th_comp_offset_0;
          _tmp_64 <= 4096;
          _tmp_66 <= 1;
          th_comp <= th_comp_11;
        end
        th_comp_11: begin
          if(_tmp_66 <= 256) begin
            _tmp_65 <= _tmp_66;
            _tmp_66 <= 0;
          end else begin
            _tmp_65 <= 256;
            _tmp_66 <= _tmp_66 - 256;
          end
          th_comp <= th_comp_12;
        end
        th_comp_12: begin
          if(_tmp_80) begin
            _tmp_63 <= _tmp_63 + _tmp_65;
            _tmp_64 <= _tmp_64 + (_tmp_65 << 2);
          end 
          if(_tmp_80 && (_tmp_66 > 0)) begin
            th_comp <= th_comp_11;
          end 
          if(_tmp_80 && (_tmp_66 == 0)) begin
            th_comp <= th_comp_13;
          end 
        end
        th_comp_13: begin
          _th_comp_offset_0 <= 512;
          th_comp <= th_comp_14;
        end
        th_comp_14: begin
          _tmp_82 <= _th_comp_offset_0;
          _tmp_83 <= 0;
          _tmp_85 <= 512;
          th_comp <= th_comp_15;
        end
        th_comp_15: begin
          if(_tmp_85 <= 256) begin
            _tmp_84 <= _tmp_85;
            _tmp_85 <= 0;
          end else begin
            _tmp_84 <= 256;
            _tmp_85 <= _tmp_85 - 256;
          end
          th_comp <= th_comp_16;
        end
        th_comp_16: begin
          if(_tmp_90) begin
            _tmp_82 <= _tmp_82 + _tmp_84;
            _tmp_83 <= _tmp_83 + (_tmp_84 << 2);
          end 
          if(_tmp_90 && (_tmp_85 > 0)) begin
            th_comp <= th_comp_15;
          end 
          if(_tmp_90 && (_tmp_85 == 0)) begin
            th_comp <= th_comp_17;
          end 
        end
        th_comp_17: begin
          _tmp_92 <= _th_comp_offset_0;
          _tmp_93 <= 0;
          _tmp_95 <= 512;
          th_comp <= th_comp_18;
        end
        th_comp_18: begin
          if(_tmp_95 <= 256) begin
            _tmp_94 <= _tmp_95;
            _tmp_95 <= 0;
          end else begin
            _tmp_94 <= 256;
            _tmp_95 <= _tmp_95 - 256;
          end
          th_comp <= th_comp_19;
        end
        th_comp_19: begin
          if(_tmp_100) begin
            _tmp_92 <= _tmp_92 + _tmp_94;
            _tmp_93 <= _tmp_93 + (_tmp_94 << 2);
          end 
          if(_tmp_100 && (_tmp_95 > 0)) begin
            th_comp <= th_comp_18;
          end 
          if(_tmp_100 && (_tmp_95 == 0)) begin
            th_comp <= th_comp_20;
          end 
        end
        th_comp_20: begin
          th_comp <= th_comp_21;
        end
        th_comp_21: begin
          if(th_sequential == 12) begin
            th_comp <= th_comp_22;
          end 
        end
        th_comp_22: begin
          _tmp_106 <= _th_comp_offset_0;
          _tmp_107 <= 8192;
          _tmp_109 <= 1;
          th_comp <= th_comp_23;
        end
        th_comp_23: begin
          if(_tmp_109 <= 256) begin
            _tmp_108 <= _tmp_109;
            _tmp_109 <= 0;
          end else begin
            _tmp_108 <= 256;
            _tmp_109 <= _tmp_109 - 256;
          end
          th_comp <= th_comp_24;
        end
        th_comp_24: begin
          if(_tmp_123) begin
            _tmp_106 <= _tmp_106 + _tmp_108;
            _tmp_107 <= _tmp_107 + (_tmp_108 << 2);
          end 
          if(_tmp_123 && (_tmp_109 > 0)) begin
            th_comp <= th_comp_23;
          end 
          if(_tmp_123 && (_tmp_109 == 0)) begin
            th_comp <= th_comp_25;
          end 
        end
        th_comp_25: begin
          _th_comp_offset_stream_13 <= 0;
          _th_comp_offset_seq_14 <= _th_comp_offset_0;
          th_comp <= th_comp_26;
        end
        th_comp_26: begin
          _th_comp_all_ok_15 <= 1;
          th_comp <= th_comp_27;
        end
        th_comp_27: begin
          if(_tmp_125) begin
            _tmp_126 <= ram_c_0_rdata;
          end 
          if(_tmp_125) begin
            th_comp <= th_comp_28;
          end 
        end
        th_comp_28: begin
          _th_comp_st_16 <= _tmp_126;
          th_comp <= th_comp_29;
        end
        th_comp_29: begin
          if(_tmp_127) begin
            _tmp_128 <= ram_c_0_rdata;
          end 
          if(_tmp_127) begin
            th_comp <= th_comp_30;
          end 
        end
        th_comp_30: begin
          _th_comp_sq_17 <= _tmp_128;
          th_comp <= th_comp_31;
        end
        th_comp_31: begin
          if(_th_comp_st_16 !== _th_comp_sq_17) begin
            th_comp <= th_comp_32;
          end else begin
            th_comp <= th_comp_33;
          end
        end
        th_comp_32: begin
          _th_comp_all_ok_15 <= 0;
          th_comp <= th_comp_33;
        end
        th_comp_33: begin
          if(_th_comp_all_ok_15) begin
            th_comp <= th_comp_34;
          end else begin
            th_comp <= th_comp_36;
          end
        end
        th_comp_34: begin
          $display("OK");
          th_comp <= th_comp_35;
        end
        th_comp_35: begin
          th_comp <= th_comp_37;
        end
        th_comp_36: begin
          $display("NG");
          th_comp <= th_comp_37;
        end
      endcase
    end
  end

  localparam _tmp_fsm_0_1 = 1;
  localparam _tmp_fsm_0_2 = 2;
  localparam _tmp_fsm_0_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_0 <= _tmp_fsm_0_init;
      _tmp_6 <= 0;
      _tmp_5 <= 0;
    end else begin
      case(_tmp_fsm_0)
        _tmp_fsm_0_init: begin
          if(th_comp == 4) begin
            _tmp_fsm_0 <= _tmp_fsm_0_1;
          end 
        end
        _tmp_fsm_0_1: begin
          if(myaxi_arready || !myaxi_arvalid) begin
            _tmp_fsm_0 <= _tmp_fsm_0_2;
          end 
        end
        _tmp_fsm_0_2: begin
          _tmp_fsm_0 <= _tmp_fsm_0_3;
        end
        _tmp_fsm_0_3: begin
          _tmp_6 <= 0;
          if(myaxi_rready && myaxi_rvalid) begin
            _tmp_5 <= myaxi_rdata;
            _tmp_6 <= 1;
          end 
          if(_tmp_8) begin
            _tmp_fsm_0 <= _tmp_fsm_0_init;
          end 
        end
      endcase
    end
  end

  localparam _tmp_fsm_1_1 = 1;
  localparam _tmp_fsm_1_2 = 2;
  localparam _tmp_fsm_1_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_1 <= _tmp_fsm_1_init;
      _tmp_16 <= 0;
      _tmp_15 <= 0;
    end else begin
      case(_tmp_fsm_1)
        _tmp_fsm_1_init: begin
          if(th_comp == 7) begin
            _tmp_fsm_1 <= _tmp_fsm_1_1;
          end 
        end
        _tmp_fsm_1_1: begin
          if(myaxi_arready || !myaxi_arvalid) begin
            _tmp_fsm_1 <= _tmp_fsm_1_2;
          end 
        end
        _tmp_fsm_1_2: begin
          _tmp_fsm_1 <= _tmp_fsm_1_3;
        end
        _tmp_fsm_1_3: begin
          _tmp_16 <= 0;
          if(myaxi_rready && myaxi_rvalid) begin
            _tmp_15 <= myaxi_rdata;
            _tmp_16 <= 1;
          end 
          if(_tmp_18) begin
            _tmp_fsm_1 <= _tmp_fsm_1_init;
          end 
        end
      endcase
    end
  end

  localparam _mystream_fsm_2_1 = 1;
  localparam _mystream_fsm_2_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      _mystream_fsm_2 <= _mystream_fsm_2_init;
      _mystream_flag_1 <= 0;
    end else begin
      case(_mystream_fsm_2)
        _mystream_fsm_2_init: begin
          if(th_comp == 8) begin
            _mystream_flag_1 <= 0;
          end 
          if(th_comp == 8) begin
            _mystream_fsm_2 <= _mystream_fsm_2_1;
          end 
        end
        _mystream_fsm_2_1: begin
          _mystream_fsm_2 <= _mystream_fsm_2_2;
        end
        _mystream_fsm_2_2: begin
          if(_tmp_30) begin
            _mystream_flag_1 <= 1;
          end 
          if(_tmp_30) begin
            _mystream_fsm_2 <= _mystream_fsm_2_init;
          end 
        end
      endcase
    end
  end

  localparam _mystream_fsm_4_1 = 1;
  localparam _mystream_fsm_4_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      _mystream_fsm_4 <= _mystream_fsm_4_init;
      _mystream_flag_3 <= 0;
    end else begin
      case(_mystream_fsm_4)
        _mystream_fsm_4_init: begin
          if(th_comp == 8) begin
            _mystream_flag_3 <= 0;
          end 
          if(th_comp == 8) begin
            _mystream_fsm_4 <= _mystream_fsm_4_1;
          end 
        end
        _mystream_fsm_4_1: begin
          _mystream_fsm_4 <= _mystream_fsm_4_2;
        end
        _mystream_fsm_4_2: begin
          if(_tmp_49) begin
            _mystream_flag_3 <= 1;
          end 
          if(_tmp_49) begin
            _mystream_fsm_4 <= _mystream_fsm_4_init;
          end 
        end
      endcase
    end
  end

  localparam _mystream_fsm_6_1 = 1;
  localparam _mystream_fsm_6_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      _mystream_fsm_6 <= _mystream_fsm_6_init;
      _mystream_flag_5 <= 0;
    end else begin
      case(_mystream_fsm_6)
        _mystream_fsm_6_init: begin
          if(th_comp == 8) begin
            _mystream_flag_5 <= 0;
          end 
          if(th_comp == 8) begin
            _mystream_fsm_6 <= _mystream_fsm_6_1;
          end 
        end
        _mystream_fsm_6_1: begin
          _mystream_fsm_6 <= _mystream_fsm_6_2;
        end
        _mystream_fsm_6_2: begin
          if(_tmp_59) begin
            _mystream_flag_5 <= 1;
          end 
          if(_tmp_59) begin
            _mystream_fsm_6 <= _mystream_fsm_6_init;
          end 
        end
      endcase
    end
  end

  localparam _tmp_fsm_2_1 = 1;
  localparam _tmp_fsm_2_2 = 2;
  localparam _tmp_fsm_2_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_2 <= _tmp_fsm_2_init;
    end else begin
      case(_tmp_fsm_2)
        _tmp_fsm_2_init: begin
          if(th_comp == 12) begin
            _tmp_fsm_2 <= _tmp_fsm_2_1;
          end 
        end
        _tmp_fsm_2_1: begin
          if(myaxi_awready || !myaxi_awvalid) begin
            _tmp_fsm_2 <= _tmp_fsm_2_2;
          end 
        end
        _tmp_fsm_2_2: begin
          _tmp_fsm_2 <= _tmp_fsm_2_3;
        end
        _tmp_fsm_2_3: begin
          if(_tmp_80) begin
            _tmp_fsm_2 <= _tmp_fsm_2_init;
          end 
        end
      endcase
    end
  end

  localparam _tmp_fsm_3_1 = 1;
  localparam _tmp_fsm_3_2 = 2;
  localparam _tmp_fsm_3_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_3 <= _tmp_fsm_3_init;
      _tmp_88 <= 0;
      _tmp_87 <= 0;
    end else begin
      case(_tmp_fsm_3)
        _tmp_fsm_3_init: begin
          if(th_comp == 16) begin
            _tmp_fsm_3 <= _tmp_fsm_3_1;
          end 
        end
        _tmp_fsm_3_1: begin
          if(myaxi_arready || !myaxi_arvalid) begin
            _tmp_fsm_3 <= _tmp_fsm_3_2;
          end 
        end
        _tmp_fsm_3_2: begin
          _tmp_fsm_3 <= _tmp_fsm_3_3;
        end
        _tmp_fsm_3_3: begin
          _tmp_88 <= 0;
          if(myaxi_rready && myaxi_rvalid) begin
            _tmp_87 <= myaxi_rdata;
            _tmp_88 <= 1;
          end 
          if(_tmp_90) begin
            _tmp_fsm_3 <= _tmp_fsm_3_init;
          end 
        end
      endcase
    end
  end

  localparam _tmp_fsm_4_1 = 1;
  localparam _tmp_fsm_4_2 = 2;
  localparam _tmp_fsm_4_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_4 <= _tmp_fsm_4_init;
      _tmp_98 <= 0;
      _tmp_97 <= 0;
    end else begin
      case(_tmp_fsm_4)
        _tmp_fsm_4_init: begin
          if(th_comp == 19) begin
            _tmp_fsm_4 <= _tmp_fsm_4_1;
          end 
        end
        _tmp_fsm_4_1: begin
          if(myaxi_arready || !myaxi_arvalid) begin
            _tmp_fsm_4 <= _tmp_fsm_4_2;
          end 
        end
        _tmp_fsm_4_2: begin
          _tmp_fsm_4 <= _tmp_fsm_4_3;
        end
        _tmp_fsm_4_3: begin
          _tmp_98 <= 0;
          if(myaxi_rready && myaxi_rvalid) begin
            _tmp_97 <= myaxi_rdata;
            _tmp_98 <= 1;
          end 
          if(_tmp_100) begin
            _tmp_fsm_4 <= _tmp_fsm_4_init;
          end 
        end
      endcase
    end
  end

  localparam th_sequential_1 = 1;
  localparam th_sequential_2 = 2;
  localparam th_sequential_3 = 3;
  localparam th_sequential_4 = 4;
  localparam th_sequential_5 = 5;
  localparam th_sequential_6 = 6;
  localparam th_sequential_7 = 7;
  localparam th_sequential_8 = 8;
  localparam th_sequential_9 = 9;
  localparam th_sequential_10 = 10;
  localparam th_sequential_11 = 11;
  localparam th_sequential_12 = 12;

  always @(posedge CLK) begin
    if(RST) begin
      th_sequential <= th_sequential_init;
      _th_sequential_called <= 0;
      _th_sequential_offset_7 <= 0;
      _th_sequential_offset_8 <= 0;
      _th_sequential_sum_9 <= 0;
      _th_sequential_i_10 <= 0;
      _tmp_103 <= 0;
      _th_sequential_a_11 <= 0;
      _tmp_105 <= 0;
      _th_sequential_b_12 <= 0;
    end else begin
      case(th_sequential)
        th_sequential_init: begin
          if(th_comp == 20) begin
            _th_sequential_called <= 1;
          end 
          if(th_comp == 20) begin
            _th_sequential_offset_7 <= _th_comp_offset_0;
          end 
          if(th_comp == 20) begin
            th_sequential <= th_sequential_1;
          end 
        end
        th_sequential_1: begin
          _th_sequential_offset_8 <= _th_sequential_offset_7;
          th_sequential <= th_sequential_2;
        end
        th_sequential_2: begin
          _th_sequential_sum_9 <= 0;
          th_sequential <= th_sequential_3;
        end
        th_sequential_3: begin
          _th_sequential_i_10 <= 0;
          th_sequential <= th_sequential_4;
        end
        th_sequential_4: begin
          if(_th_sequential_i_10 < 512) begin
            th_sequential <= th_sequential_5;
          end else begin
            th_sequential <= th_sequential_11;
          end
        end
        th_sequential_5: begin
          if(_tmp_102) begin
            _tmp_103 <= ram_a_0_rdata;
          end 
          if(_tmp_102) begin
            th_sequential <= th_sequential_6;
          end 
        end
        th_sequential_6: begin
          _th_sequential_a_11 <= _tmp_103;
          th_sequential <= th_sequential_7;
        end
        th_sequential_7: begin
          if(_tmp_104) begin
            _tmp_105 <= ram_b_0_rdata;
          end 
          if(_tmp_104) begin
            th_sequential <= th_sequential_8;
          end 
        end
        th_sequential_8: begin
          _th_sequential_b_12 <= _tmp_105;
          th_sequential <= th_sequential_9;
        end
        th_sequential_9: begin
          _th_sequential_sum_9 <= _th_sequential_sum_9 + _th_sequential_a_11 * _th_sequential_b_12;
          th_sequential <= th_sequential_10;
        end
        th_sequential_10: begin
          _th_sequential_i_10 <= _th_sequential_i_10 + 1;
          th_sequential <= th_sequential_4;
        end
        th_sequential_11: begin
          th_sequential <= th_sequential_12;
        end
      endcase
    end
  end

  localparam _tmp_fsm_5_1 = 1;
  localparam _tmp_fsm_5_2 = 2;
  localparam _tmp_fsm_5_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_5 <= _tmp_fsm_5_init;
    end else begin
      case(_tmp_fsm_5)
        _tmp_fsm_5_init: begin
          if(th_comp == 24) begin
            _tmp_fsm_5 <= _tmp_fsm_5_1;
          end 
        end
        _tmp_fsm_5_1: begin
          if(myaxi_awready || !myaxi_awvalid) begin
            _tmp_fsm_5 <= _tmp_fsm_5_2;
          end 
        end
        _tmp_fsm_5_2: begin
          _tmp_fsm_5 <= _tmp_fsm_5_3;
        end
        _tmp_fsm_5_3: begin
          if(_tmp_123) begin
            _tmp_fsm_5 <= _tmp_fsm_5_init;
          end 
        end
      endcase
    end
  end


endmodule



module ram_a
(
  input CLK,
  input [10-1:0] ram_a_0_addr,
  output [32-1:0] ram_a_0_rdata,
  input [32-1:0] ram_a_0_wdata,
  input ram_a_0_wenable
);

  reg [10-1:0] ram_a_0_daddr;
  reg [32-1:0] mem [0:1024-1];

  always @(posedge CLK) begin
    if(ram_a_0_wenable) begin
      mem[ram_a_0_addr] <= ram_a_0_wdata;
    end 
    ram_a_0_daddr <= ram_a_0_addr;
  end

  assign ram_a_0_rdata = mem[ram_a_0_daddr];

endmodule



module ram_b
(
  input CLK,
  input [10-1:0] ram_b_0_addr,
  output [32-1:0] ram_b_0_rdata,
  input [32-1:0] ram_b_0_wdata,
  input ram_b_0_wenable
);

  reg [10-1:0] ram_b_0_daddr;
  reg [32-1:0] mem [0:1024-1];

  always @(posedge CLK) begin
    if(ram_b_0_wenable) begin
      mem[ram_b_0_addr] <= ram_b_0_wdata;
    end 
    ram_b_0_daddr <= ram_b_0_addr;
  end

  assign ram_b_0_rdata = mem[ram_b_0_daddr];

endmodule



module ram_c
(
  input CLK,
  input [10-1:0] ram_c_0_addr,
  output [32-1:0] ram_c_0_rdata,
  input [32-1:0] ram_c_0_wdata,
  input ram_c_0_wenable
);

  reg [10-1:0] ram_c_0_daddr;
  reg [32-1:0] mem [0:1024-1];

  always @(posedge CLK) begin
    if(ram_c_0_wenable) begin
      mem[ram_c_0_addr] <= ram_c_0_wdata;
    end 
    ram_c_0_daddr <= ram_c_0_addr;
  end

  assign ram_c_0_rdata = mem[ram_c_0_daddr];

endmodule



module multiplier_0
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [32-1:0] b,
  output [64-1:0] c
);

  reg valid_reg0;
  reg valid_reg1;
  reg valid_reg2;
  reg valid_reg3;
  reg valid_reg4;
  reg valid_reg5;
  assign valid = valid_reg5;

  always @(posedge CLK) begin
    if(RST) begin
      valid_reg0 <= 0;
      valid_reg1 <= 0;
      valid_reg2 <= 0;
      valid_reg3 <= 0;
      valid_reg4 <= 0;
      valid_reg5 <= 0;
    end else begin
      if(update) begin
        valid_reg0 <= enable;
        valid_reg1 <= valid_reg0;
        valid_reg2 <= valid_reg1;
        valid_reg3 <= valid_reg2;
        valid_reg4 <= valid_reg3;
        valid_reg5 <= valid_reg4;
      end 
    end
  end


  multiplier_core_0
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_0
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [32-1:0] b,
  output [64-1:0] c
);

  reg [32-1:0] _a;
  reg [32-1:0] _b;
  reg signed [64-1:0] _tmpval0;
  reg signed [64-1:0] _tmpval1;
  reg signed [64-1:0] _tmpval2;
  reg signed [64-1:0] _tmpval3;
  reg signed [64-1:0] _tmpval4;
  wire signed [64-1:0] rslt;
  assign rslt = $signed({ 1'd0, _a }) * $signed({ 1'd0, _b });
  assign c = _tmpval4;

  always @(posedge CLK) begin
    if(update) begin
      _a <= a;
      _b <= b;
      _tmpval0 <= rslt;
      _tmpval1 <= _tmpval0;
      _tmpval2 <= _tmpval1;
      _tmpval3 <= _tmpval2;
      _tmpval4 <= _tmpval3;
    end 
  end


endmodule
"""


def test():
    veriloggen.reset()
    test_module = thread_stream_pattern.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
