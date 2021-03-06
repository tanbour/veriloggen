from __future__ import absolute_import
from __future__ import print_function

import math
import functools
import ast
import inspect
import textwrap
from collections import OrderedDict

import veriloggen.core.vtypes as vtypes
from veriloggen.seq.seq import make_condition
from veriloggen.fsm.fsm import FSM
from veriloggen.seq.seq import Seq
from veriloggen.stream.stream import Stream as BaseStream
from veriloggen.stream.stypes import Substream as BaseSubstream

from . import compiler
from . import thread

mode_width = 3
mode_idle = vtypes.Int(0, mode_width, base=2)
mode_normal = vtypes.Int(1, mode_width, base=2)
mode_pattern = vtypes.Int(2, mode_width, base=2)
mode_multipattern = vtypes.Int(4, mode_width, base=2)


def TmpStream(m, clk, rst,
              datawidth=32, addrwidth=32,
              max_pattern_length=4, ram_sel_width=8,
              fsm_as_module=False):
    name = compiler._tmp_name('_tmp_stream')
    return Stream(m, name, clk, rst,
                  datawidth, addrwidth,
                  max_pattern_length, ram_sel_width,
                  fsm_as_module=False)


class Stream(BaseStream):
    __intrinsics__ = ('set_source', 'set_source_pattern', 'set_source_multidim',
                      'set_source_multipattern',
                      'set_sink', 'set_sink_pattern', 'set_sink_multidim',
                      'set_sink_multipattern',
                      'set_sink_empty', 'set_constant',
                      'run', 'join', 'done')

    def __init__(self, m, name, clk, rst,
                 datawidth=32, addrwidth=32,
                 max_pattern_length=4, max_multipattern_length=2,
                 ram_sel_width=8, fsm_as_module=False):

        BaseStream.__init__(self, module=m, clock=clk, reset=rst,
                            no_hook=True)

        self.name = name
        self.datawidth = datawidth
        self.addrwidth = addrwidth

        self.max_pattern_length = max_pattern_length
        self.max_multipattern_length = max_multipattern_length
        self.ram_sel_width = ram_sel_width

        self.fsm_as_module = fsm_as_module

        self.stream_synthesized = False
        self.fsm_synthesized = False

        self.fsm = FSM(self.module, '_%s_fsm' %
                       self.name, self.clock, self.reset,
                       as_module=self.fsm_as_module)
        self.start_flag = self.module.Wire(
            '_'.join(['', self.name, 'start_flag']))
        self.start = self.module.Reg(
            '_'.join(['', self.name, 'start']), initval=0)
        self.busy = self.module.Reg(
            '_'.join(['', self.name, 'busy']), initval=0)

        self.reduce_reset = None
        self.reduce_reset_var = None

        self.sources = OrderedDict()
        self.sinks = OrderedDict()
        self.constants = OrderedDict()
        self.substreams = []

        self.var_name_map = OrderedDict()
        self.var_id_map = OrderedDict()
        self.var_id_name_map = OrderedDict()
        self.var_name_id_map = OrderedDict()
        self.var_id_count = 0

        self.source_idle_map = OrderedDict()
        self.sink_when_map = OrderedDict()

        self.ram_id_count = 1  # '0' is reserved for idle
        self.ram_id_map = OrderedDict()  # key: ran._id(), value: count

        self.fsm_id_count = 0

        self.ram_delay = 4

    def source(self, name=None, datawidth=None, point=0, signed=True):
        if self.stream_synthesized:
            raise ValueError(
                'cannot modify the stream because already synthesized')

        _id = self.var_id_count
        if name is None:
            name = 'source_%d' % _id

        if name in self.var_name_map:
            raise ValueError("'%s' is already defined in stream '%s'" %
                             (name, self.name))

        prefix = self._prefix(name)

        self.var_id_count += 1

        if datawidth is None:
            datawidth = self.datawidth

        var = self.Variable(self._dataname(name), datawidth, point, signed)

        self.sources[name] = var
        self.var_id_map[_id] = var
        self.var_name_map[name] = var
        self.var_id_name_map[_id] = name
        self.var_name_id_map[name] = _id

        var.source_fsm = None
        var.source_pat_fsm = None
        var.source_multipat_fsm = None

        var.source_idle = self.module.Reg('_%s_idle' % prefix, initval=1)
        self.source_idle_map[name] = var.source_idle

        # 3'b001: set_source, 3'b010: set_source_pattern, 3'b100: set_source_multipattern
        var.source_mode = self.module.Reg('_%s_source_mode' % prefix, mode_width,
                                          initval=mode_idle)

        var.source_offset = self.module.Reg('_%s_source_offset' % prefix,
                                            self.addrwidth, initval=0)
        var.source_size = self.module.Reg('_%s_source_size' % prefix,
                                          self.addrwidth + 1, initval=0)
        var.source_stride = self.module.Reg('_%s_source_stride' % prefix,
                                            self.addrwidth, initval=0)
        var.source_count = self.module.Reg('_%s_source_count' % prefix,
                                           self.addrwidth + 1, initval=0)

        var.source_pat_cur_offsets = None
        var.source_pat_sizes = None
        var.source_pat_strides = None
        var.source_pat_counts = None

        var.source_multipat_num_patterns = None
        var.source_multipat_offsets = None
        var.source_multipat_cur_offsets = None
        var.source_multipat_sizes = None
        var.source_multipat_strides = None

        var.source_ram_id_map = OrderedDict()
        var.source_ram_sel = self.module.Reg('_%s_source_ram_sel' % prefix,
                                             self.ram_sel_width, initval=0)
        var.source_ram_raddr = self.module.Reg('_%s_source_ram_raddr' % prefix,
                                               self.addrwidth, initval=0)
        var.source_ram_renable = self.module.Reg('_%s_source_ram_renable' % prefix,
                                                 initval=0)
        var.source_ram_rdata = self.module.Wire('_%s_source_ram_rdata' % prefix,
                                                datawidth)
        var.source_ram_rvalid = self.module.Reg('_%s_source_ram_rvalid' % prefix,
                                                initval=0)

        return var

    def sink(self, data, name=None, when=None, when_name=None):
        if self.stream_synthesized:
            raise ValueError(
                'cannot modify the stream because already synthesized')

        _id = self.var_id_count
        if name is None:
            name = 'sink_%d' % _id

        if name in self.var_name_map:
            raise ValueError("'%s' is already defined in stream '%s'" %
                             (name, self.name))
        else:
            data.output(self._dataname(name))

        prefix = self._prefix(name)

        self.var_id_count += 1

        self.sinks[name] = data
        self.var_id_map[_id] = data
        self.var_name_map[name] = data
        self.var_id_name_map[_id] = name
        self.var_name_id_map[name] = _id

        data.sink_fsm = None
        data.sink_pat_fsm = None
        data.sink_multipat_fsm = None

        # 3'b001: set_sink, 3'b010: set_sink_pattern, 3'b100: set_sink_multipattern
        data.sink_mode = self.module.Reg('_%s_sink_mode' % prefix, mode_width,
                                         initval=mode_idle)

        data.sink_offset = self.module.Reg('_%s_sink_offset' % prefix,
                                           self.addrwidth, initval=0)
        data.sink_size = self.module.Reg('_%s_sink_size' % prefix,
                                         self.addrwidth + 1, initval=0)
        data.sink_stride = self.module.Reg('_%s_sink_stride' % prefix,
                                           self.addrwidth, initval=0)
        data.sink_count = self.module.Reg('_%s_sink_count' % prefix,
                                          self.addrwidth + 1, initval=0)

        data.sink_pat_cur_offsets = None
        data.sink_pat_sizes = None
        data.sink_pat_strides = None
        data.sink_pat_counts = None

        data.sink_multipat_num_patterns = None
        data.sink_multipat_offsets = None
        data.sink_multipat_cur_offsets = None
        data.sink_multipat_sizes = None
        data.sink_multipat_strides = None

        data.sink_ram_id_map = OrderedDict()
        data.sink_ram_sel = self.module.Reg('_%s_sink_ram_sel' % prefix,
                                            self.ram_sel_width, initval=0)
        data.sink_ram_waddr = self.module.Reg('_%s_sink_waddr' % prefix,
                                              self.addrwidth, initval=0)
        data.sink_ram_wenable = self.module.Reg('_%s_sink_wenable' % prefix,
                                                initval=0)
        data.sink_ram_wdata = self.module.Reg('_%s_sink_wdata' % prefix,
                                              data.width, initval=0)

        if when is not None:
            self.sink(when, when_name)
            self.sink_when_map[name] = when

    def constant(self, name=None, datawidth=None, point=0, signed=True):
        if self.stream_synthesized:
            raise ValueError(
                'cannot modify the stream because already synthesized')

        _id = self.var_id_count
        if name is None:
            name = 'constant_%d' % _id

        if name in self.var_name_map:
            raise ValueError("'%s' is already defined in stream '%s'" %
                             (name, self.name))

        prefix = self._prefix(name)

        self.var_id_count += 1

        if datawidth is None:
            datawidth = self.datawidth

        var = self.ParameterVariable(self._dataname(name), datawidth,
                                     point, signed)

        self.constants[name] = var
        self.var_id_map[_id] = var
        self.var_name_map[name] = var
        self.var_id_name_map[_id] = name
        self.var_name_id_map[name] = _id

        return var

    def substream(self, substrm):
        sub = Substream(self.module, self.clock, self.reset, substrm, self)
        self.substreams.append(sub)
        return sub

    def set_source(self, fsm, name, ram, offset, size, stride=1, port=0):
        """ intrinsic method to assign RAM property to a source stream """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.sources:
            raise NameError("No such stream '%s'" % name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        self.seq.If(set_cond)(
            var.source_mode(mode_normal),
            var.source_offset(offset),
            var.source_size(size),
            var.source_stride(stride)
        )

        port = vtypes.to_int(port)
        self._setup_source_ram(ram, var, port, set_cond)
        self._synthesize_set_source(var, name)

        fsm.goto_next()

    def set_source_pattern(self, fsm, name, ram, offset, pattern, port=0):
        """ intrinsic method to assign RAM property to a source stream """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.sources:
            raise NameError("No such stream '%s'" % name)

        if not isinstance(pattern, (tuple, list)):
            raise TypeError('pattern must be list or tuple.')

        if not pattern:
            raise ValueError(
                'pattern must have one (size, stride) pair at least.')

        if not isinstance(pattern[0], (tuple, list)):
            pattern = (pattern,)

        pattern = tuple(pattern)

        if len(pattern) > self.max_pattern_length:
            raise ValueError(
                "'pattern' length exceeds maximum pattern length.")

        self._make_source_pattern_vars(var, name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        self.seq.If(set_cond)(
            var.source_mode(mode_pattern),
            var.source_offset(offset)
        )

        pad = tuple([(1, 0)
                     for _ in range(self.max_pattern_length - len(pattern))])

        for (source_pat_size, source_pat_stride,
             (size, stride)) in zip(var.source_pat_sizes, var.source_pat_strides,
                                    pattern + pad):
            self.seq.If(set_cond)(
                source_pat_size(size),
                source_pat_stride(stride)
            )

        port = vtypes.to_int(port)
        self._setup_source_ram(ram, var, port, set_cond)
        self._synthesize_set_source_pattern(var, name)

        fsm.goto_next()

    def set_source_multidim(self, fsm, name, ram, offset, shape, order=None, port=0):
        """ intrinsic method to assign RAM property to a source stream """

        if order is None:
            order = list(reversed(range(len(shape))))

        pattern = self._to_pattern(shape, order)
        return self.set_source_pattern(fsm, name, ram, offset, pattern, port)

    def set_source_multipattern(self, fsm, name, ram, offsets, patterns, port=0):
        """ intrinsic method to assign multiple patterns to a RAM """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.sources:
            raise NameError("No such stream '%s'" % name)

        if not isinstance(patterns, (tuple, list)):
            raise TypeError('patterns must be list or tuple.')

        if not patterns:
            raise ValueError(
                'patterns must have one [(size, stride)] list at least.')

        if not isinstance(offsets, (tuple, list)):
            offsets = [offsets] * len(patterns)

        if not offsets:
            raise ValueError('offsets must have one offset value at least.')

        offsets = tuple(offsets)
        patterns = tuple(patterns)

        if len(offsets) != len(patterns):
            raise ValueError(
                "number of offsets must be 1 or equal to the number of patterns.")

        if len(offsets) > self.max_multipattern_length:
            raise ValueError(
                "'offsets' length exceeds maximum multipattern length.")

        if len(patterns) > self.max_multipattern_length:
            raise ValueError(
                "'patterns' length exceeds maximum multipattern length.")

        for pattern in patterns:
            if len(pattern) > self.max_pattern_length:
                raise ValueError(
                    "'pattern' length exceeds maximum pattern length.")

        self._make_source_multipattern_vars(var, name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        self.seq.If(set_cond)(
            var.source_mode(mode_multipattern),
            var.source_multipat_num_patterns(len(patterns))
        )

        offsets_pad = tuple(
            [0 for _ in range(self.max_multipattern_length - len(patterns))])

        for offset, multipat_offset in zip(offsets + offsets_pad,
                                           var.source_multipat_offsets):
            self.seq.If(set_cond)(
                multipat_offset(offset)
            )

        for multipat_sizes, multipat_strides, pattern in zip(
                var.source_multipat_sizes, var.source_multipat_strides, patterns):
            pad = tuple([(1, 0)
                         for _ in range(self.max_pattern_length - len(pattern))])

            for (multipat_size, multipat_stride,
                 (size, stride)) in zip(multipat_sizes, multipat_strides,
                                        pattern + pad):
                self.seq.If(set_cond)(
                    multipat_size(size),
                    multipat_stride(stride)
                )

        port = vtypes.to_int(port)
        self._setup_source_ram(ram, var, port, set_cond)
        self._synthesize_set_source_multipattern(var, name)

        fsm.goto_next()

    def set_sink(self, fsm, name, ram, offset, size, stride=1, port=0):
        """ intrinsic method to assign RAM property to a sink stream """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.sinks:
            raise NameError("No such stream '%s'" % name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        self.seq.If(set_cond)(
            var.sink_mode(mode_normal),
            var.sink_offset(offset),
            var.sink_size(size),
            var.sink_stride(stride)
        )

        port = vtypes.to_int(port)
        self._setup_sink_ram(ram, var, port, set_cond)
        self._synthesize_set_sink(var, name)

        fsm.goto_next()

    def set_sink_pattern(self, fsm, name, ram, offset, pattern, port=0):
        """ intrinsic method to assign RAM property to a sink stream """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.sinks:
            raise NameError("No such stream '%s'" % name)

        if not isinstance(pattern, (tuple, list)):
            raise TypeError('pattern must be list or tuple.')

        if not pattern:
            raise ValueError(
                'pattern must have one (size, stride) pair at least.')

        if not isinstance(pattern[0], (tuple, list)):
            pattern = (pattern,)

        pattern = tuple(pattern)

        if len(pattern) > self.max_pattern_length:
            raise ValueError(
                "'pattern' length exceeds maximum pattern length.")

        self._make_sink_pattern_vars(var, name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        self.seq.If(set_cond)(
            var.sink_mode(mode_pattern),
            var.sink_offset(offset)
        )

        pad = tuple([(1, 0)
                     for _ in range(self.max_pattern_length - len(pattern))])

        for (sink_pat_size, sink_pat_stride,
             (size, stride)) in zip(var.sink_pat_sizes, var.sink_pat_strides,
                                    pattern + pad):
            self.seq.If(set_cond)(
                sink_pat_size(size),
                sink_pat_stride(stride)
            )

        port = vtypes.to_int(port)
        self._setup_sink_ram(ram, var, port, set_cond)
        self._synthesize_set_sink_pattern(var, name)

        fsm.goto_next()

    def set_sink_multidim(self, fsm, name, ram, offset, shape, order=None, port=0):
        """ intrinsic method to assign RAM property to a sink stream """

        if order is None:
            order = list(reversed(range(len(shape))))

        pattern = self._to_pattern(shape, order)
        return self.set_sink_pattern(fsm, name, ram, offset, pattern, port)

    def set_sink_multipattern(self, fsm, name, ram, offsets, patterns, port=0):
        """ intrinsic method to assign multiple patterns to a RAM """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.sinks:
            raise NameError("No such stream '%s'" % name)

        if not isinstance(patterns, (tuple, list)):
            raise TypeError('patterns must be list or tuple.')

        if not patterns:
            raise ValueError(
                'patterns must have one [(size, stride)] list at least.')

        if not isinstance(offsets, (tuple, list)):
            offsets = [offsets] * len(patterns)

        if not offsets:
            raise ValueError('offsets must have one offset value at least.')

        offsets = tuple(offsets)
        patterns = tuple(patterns)

        if len(offsets) != len(patterns):
            raise ValueError(
                "number of offsets must be 1 or equal to the number of patterns.")

        if len(offsets) > self.max_multipattern_length:
            raise ValueError(
                "'offsets' length exceeds maximum multipattern length.")

        if len(patterns) > self.max_multipattern_length:
            raise ValueError(
                "'patterns' length exceeds maximum multipattern length.")

        for pattern in patterns:
            if len(pattern) > self.max_pattern_length:
                raise ValueError(
                    "'pattern' length exceeds maximum pattern length.")

        self._make_sink_multipattern_vars(var, name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        self.seq.If(set_cond)(
            var.sink_mode(mode_multipattern),
            var.sink_multipat_num_patterns(len(patterns))
        )

        offsets_pad = tuple(
            [0 for _ in range(self.max_multipattern_length - len(patterns))])

        for offset, multipat_offset in zip(offsets + offsets_pad,
                                           var.sink_multipat_offsets):
            self.seq.If(set_cond)(
                multipat_offset(offset)
            )

        for multipat_sizes, multipat_strides, pattern in zip(
                var.sink_multipat_sizes, var.sink_multipat_strides, patterns):
            pad = tuple([(1, 0)
                         for _ in range(self.max_pattern_length - len(pattern))])

            for (multipat_size, multipat_stride,
                 (size, stride)) in zip(multipat_sizes, multipat_strides,
                                        pattern + pad):
                self.seq.If(set_cond)(
                    multipat_size(size),
                    multipat_stride(stride)
                )

        port = vtypes.to_int(port)
        self._setup_sink_ram(ram, var, port, set_cond)
        self._synthesize_set_sink_multipattern(var, name)

        fsm.goto_next()

    def set_sink_empty(self, fsm, name):
        """ intrinsic method to assign RAM property to a sink stream """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.sinks:
            raise NameError("No such stream '%s'" % name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        ram_sel = var.sink_ram_sel

        self.seq.If(set_cond)(
            ram_sel(0)  # '0' is reserved for empty
        )

        fsm.goto_next()

    def set_constant(self, fsm, name, value):
        """ intrinsic method to assign constant value to a constant stream """

        if not self.stream_synthesized:
            self._implement_stream()

        if isinstance(name, str):
            var = self.var_name_map[name]
        elif isinstance(name, vtypes.Str):
            name = name.value
            var = self.var_name_map[name]
        elif isinstance(name, int):
            var = self.var_id_map[name]
        elif isinstance(name, vtypes.Int):
            name = name.value
            var = self.var_id_map[name]
        else:
            raise TypeError('Unsupported index name')

        if name not in self.constants:
            raise NameError("No such stream '%s'" % name)

        #set_cond = fsm.here
        set_cond = self._set_flag(fsm)

        wdata = value
        wenable = set_cond
        var.write(wdata, wenable)

        fsm.goto_next()

    def run(self, fsm):
        # entry point
        self.fsm._set_index(0)

        #cond = fsm.here
        cond = self._set_flag(fsm)
        add_mux(self.start_flag, cond, 1)

        # after started
        if self.fsm_synthesized:
            fsm.goto_next()
            fsm.goto_next()
            return

        self.fsm_synthesized = True

        num_wdelay = self._write_delay()

        self.fsm.If(self.start_flag)(
            self.start(1),
            self.busy(1)
        )

        if self.reduce_reset is not None:
            self.fsm.seq.If(self.seq.Prev(self.start_flag, self.ram_delay + 1))(
                self.reduce_reset(0)
            )

        substreams = self._collect_substreams()

        for sub in substreams:
            reset_delay = self.ram_delay + 1 + sub.start_stage + sub.reset_delay
            sub_fsm = sub.substrm.fsm
            sub_fsm._set_index(0)

            if sub.substrm.reduce_reset is not None:
                sub_fsm.seq.If(self.seq.Prev(self.start_flag, reset_delay))(
                    sub.substrm.reduce_reset(0)
                )

            for cond in sub.conds.values():
                sub_fsm.If(self.start_flag)(
                    cond(1)
                )

        self.fsm.If(self.start_flag).goto_next()

        self.fsm(
            self.start(0)
        )
        self.fsm.goto_next()

        done_cond = None
        for key, source_idle in sorted(self.source_idle_map.items(),
                                       key=lambda x: x[0]):
            done_cond = make_condition(done_cond, source_idle)

        done = self.module.Wire('_%s_done' % self.name)
        done.assign(done_cond)

        self.fsm.If(done).goto_next()

        depth = self.pipeline_depth()
        for _ in range(depth):
            self.fsm.goto_next()

        self.fsm.goto_next()

        # reset accumulate pipelines
        if self.reduce_reset is not None:
            self.fsm(
                self.reduce_reset(1)
            )

        end_flag = self.fsm.here

        for sub in substreams:
            sub_fsm = sub.substrm.fsm
            sub_fsm._set_index(0)
            if sub.substrm.reduce_reset is not None:
                sub_fsm.If(end_flag)(
                    sub.substrm.reduce_reset(1)
                )

            for cond in sub.conds.values():
                sub_fsm.If(end_flag)(
                    cond(0)
                )

        self.fsm.goto_next()

        self.fsm(
            self.busy(0)
        )

        self.fsm.goto_init()

        fsm.goto_next()
        fsm.goto_next()

        return 0

    def join(self, fsm):
        fsm.If(vtypes.Not(self.busy)).goto_next()
        return 0

    def done(self, fsm):
        return vtypes.Not(self.busy)

    def _setup_source_ram(self, ram, var, port, set_cond):
        if ram._id() in var.source_ram_id_map:
            ram_id = var.source_ram_id_map[ram._id()]
            self.seq.If(set_cond)(
                var.source_ram_sel(ram_id)
            )
            return

        if ram._id() not in self.ram_id_map:
            ram_id = self.ram_id_count
            self.ram_id_count += 1
            self.ram_id_map[ram._id()] = ram_id
        else:
            ram_id = self.ram_id_map[ram._id()]

        var.source_ram_id_map[ram._id()] = ram_id

        self.seq.If(set_cond)(
            var.source_ram_sel(ram_id)
        )

        ram_cond = (var.source_ram_sel == ram_id)
        renable = vtypes.Ands(var.source_ram_renable, ram_cond)

        d, v = ram.read_rtl(var.source_ram_raddr, port=port, cond=renable)
        add_mux(var.source_ram_rdata, ram_cond, d)

        self.seq(
            var.source_ram_rvalid(self.seq.Prev(renable, 1))
        )

    def _synthesize_set_source(self, var, name):
        if var.source_fsm is not None:
            return

        wdata = var.source_ram_rdata
        wenable = var.source_ram_rvalid
        var.write(wdata, wenable)

        source_start = vtypes.Ands(self.start,
                                   vtypes.And(var.source_mode, mode_normal))

        self.seq.If(source_start)(
            var.source_idle(0)
        )

        fsm_id = self.fsm_id_count
        self.fsm_id_count += 1

        prefix = self._prefix(name)

        fsm_name = '_%s_source_fsm_%d' % (prefix, fsm_id)
        var.source_fsm = FSM(self.module, fsm_name, self.clock, self.reset,
                             as_module=self.fsm_as_module)

        var.source_fsm.If(source_start).goto_next()

        self.seq.If(var.source_fsm.here)(
            var.source_ram_raddr(var.source_offset),
            var.source_ram_renable(1),
            var.source_count(var.source_size)
        )

        var.source_fsm.goto_next()

        self.seq.If(var.source_fsm.here)(
            var.source_ram_raddr.add(var.source_stride),
            var.source_ram_renable(1),
            var.source_count.dec()
        )
        self.seq.If(var.source_fsm.here, var.source_count == 1)(
            var.source_ram_renable(0),
            var.source_idle(1)
        )

        var.source_fsm.If(var.source_count == 1).goto_init()

    def _make_source_pattern_vars(self, var, name):
        if var.source_pat_cur_offsets is not None:
            return

        prefix = self._prefix(name)

        var.source_pat_cur_offsets = [
            self.module.Reg('_source_%s_pat_cur_offset_%d' % (prefix, i),
                            self.addrwidth, initval=0)
            for i in range(self.max_pattern_length)]
        var.source_pat_sizes = [self.module.Reg('_source_%s_pat_size_%d' % (prefix, i),
                                                self.addrwidth + 1, initval=0)
                                for i in range(self.max_pattern_length)]
        var.source_pat_strides = [self.module.Reg('_source_%s_pat_stride_%d' % (prefix, i),
                                                  self.addrwidth, initval=0)
                                  for i in range(self.max_pattern_length)]
        var.source_pat_counts = [self.module.Reg('_source_%s_pat_count_%d' % (prefix, i),
                                                 self.addrwidth + 1, initval=0)
                                 for i in range(self.max_pattern_length)]

    def _synthesize_set_source_pattern(self, var, name):
        if var.source_pat_fsm is not None:
            return

        wdata = var.source_ram_rdata
        wenable = var.source_ram_rvalid
        var.write(wdata, wenable)

        source_start = vtypes.Ands(self.start,
                                   vtypes.And(var.source_mode, mode_pattern))

        self.seq.If(source_start)(
            var.source_idle(0)
        )

        for source_pat_cur_offset in var.source_pat_cur_offsets:
            self.seq.If(source_start)(
                source_pat_cur_offset(0)
            )

        for (source_pat_size, source_pat_count) in zip(
                var.source_pat_sizes, var.source_pat_counts):
            self.seq.If(source_start)(
                source_pat_count(source_pat_size - 1)
            )

        fsm_id = self.fsm_id_count
        self.fsm_id_count += 1

        prefix = self._prefix(name)

        fsm_name = '_%s_source_pat_fsm_%d' % (prefix, fsm_id)
        var.source_pat_fsm = FSM(self.module, fsm_name,
                                 self.clock, self.reset,
                                 as_module=self.fsm_as_module)

        var.source_pat_fsm.If(source_start).goto_next()

        source_all_offset = self.module.Wire('_%s_source_pat_all_offset' % prefix,
                                             self.addrwidth)
        source_all_offset_val = var.source_offset
        for source_pat_cur_offset in var.source_pat_cur_offsets:
            source_all_offset_val += source_pat_cur_offset
        source_all_offset.assign(source_all_offset_val)

        self.seq.If(var.source_pat_fsm.here)(
            var.source_ram_raddr(source_all_offset),
            var.source_ram_renable(1)
        )

        upcond = None

        for (source_pat_cur_offset, source_pat_size,
             source_pat_stride, source_pat_count) in zip(
                 var.source_pat_cur_offsets, var.source_pat_sizes,
                 var.source_pat_strides, var.source_pat_counts):

            self.seq.If(var.source_pat_fsm.here, upcond)(
                source_pat_cur_offset.add(source_pat_stride),
                source_pat_count.dec()
            )

            reset_cond = source_pat_count == 0
            self.seq.If(var.source_pat_fsm.here, upcond, reset_cond)(
                source_pat_cur_offset(0),
                source_pat_count(source_pat_size - 1)
            )
            upcond = make_condition(upcond, reset_cond)

        fin_cond = upcond

        var.source_pat_fsm.If(fin_cond).goto_next()

        self.seq.If(var.source_pat_fsm.here)(
            var.source_ram_renable(0),
            var.source_idle(1)
        )

        var.source_pat_fsm.goto_init()

    def _make_source_multipattern_vars(self, var, name):
        if var.source_multipat_cur_offsets is not None:
            return

        prefix = self._prefix(name)

        var.source_multipat_num_patterns = self.module.Reg(
            '_source_%s_multipat_num_patterns' % prefix,
            int(math.ceil(math.log(self.max_multipattern_length, 2))), initval=0)
        var.source_multipat_offsets = [
            self.module.Reg('_source_%s_multipat_%d_offset' % (prefix, j),
                            self.addrwidth, initval=0)
            for j in range(self.max_multipattern_length)]
        var.source_multipat_cur_offsets = [
            self.module.Reg('_source_%s_multipat_%d_cur_offset' % (prefix, i),
                            self.addrwidth, initval=0)
            for i in range(self.max_pattern_length)]
        var.source_multipat_sizes = [[self.module.Reg('_source_%s_multipat_%d_size_%d' %
                                                      (prefix, j, i),
                                                      self.addrwidth + 1, initval=0)
                                      for i in range(self.max_pattern_length)]
                                     for j in range(self.max_multipattern_length)]
        var.source_multipat_strides = [[self.module.Reg('_source_%s_multipat_%d_stride_%d' %
                                                        (prefix, j, i),
                                                        self.addrwidth, initval=0)
                                        for i in range(self.max_pattern_length)]
                                       for j in range(self.max_multipattern_length)]
        var.source_multipat_counts = [[self.module.Reg('_source_%s_multipat_%d_count_%d' %
                                                       (prefix, j, i),
                                                       self.addrwidth + 1, initval=0)
                                       for i in range(self.max_pattern_length)]
                                      for j in range(self.max_multipattern_length)]

    def _synthesize_set_source_multipattern(self, var, name):
        if var.source_pat_fsm is not None:
            return

        wdata = var.source_ram_rdata
        wenable = var.source_ram_rvalid
        var.write(wdata, wenable)

        source_start = vtypes.Ands(self.start,
                                   vtypes.And(var.source_mode, mode_multipattern))

        self.seq.If(source_start)(
            var.source_idle(0)
        )

        self.seq.If(source_start)(
            var.source_multipat_num_patterns.dec()
        )

        for source_multipat_cur_offset in var.source_multipat_cur_offsets:
            self.seq.If(source_start)(
                source_multipat_cur_offset(0)
            )

        for (source_multipat_size, source_multipat_count) in zip(
                var.source_multipat_sizes[0], var.source_multipat_counts[0]):
            self.seq.If(source_start)(
                source_multipat_count(source_multipat_size - 1)
            )

        fsm_id = self.fsm_id_count
        self.fsm_id_count += 1

        prefix = self._prefix(name)

        fsm_name = '_%s_source_multipat_fsm_%d' % (prefix, fsm_id)
        var.source_multipat_fsm = FSM(self.module, fsm_name,
                                      self.clock, self.reset,
                                      as_module=self.fsm_as_module)

        var.source_multipat_fsm.If(source_start).goto_next()

        source_all_offset = self.module.Wire('_%s_source_multipat_all_offset' % prefix,
                                             self.addrwidth)
        source_all_offset_val = var.source_multipat_offsets[0]
        for source_multipat_cur_offset in var.source_multipat_cur_offsets:
            source_all_offset_val += source_multipat_cur_offset
        source_all_offset.assign(source_all_offset_val)

        self.seq.If(var.source_multipat_fsm.here)(
            var.source_ram_raddr(source_all_offset),
            var.source_ram_renable(1)
        )

        upcond = None

        for (source_multipat_cur_offset, source_multipat_size,
             source_multipat_stride, source_multipat_count) in zip(
                 var.source_multipat_cur_offsets, var.source_multipat_sizes[0],
                 var.source_multipat_strides[0], var.source_multipat_counts[0]):

            self.seq.If(var.source_multipat_fsm.here, upcond)(
                source_multipat_cur_offset.add(source_multipat_stride),
                source_multipat_count.dec()
            )

            reset_cond = source_multipat_count == 0
            self.seq.If(var.source_multipat_fsm.here, upcond, reset_cond)(
                source_multipat_cur_offset(0),
                source_multipat_count(source_multipat_size - 1)
            )
            upcond = make_condition(upcond, reset_cond)

        fin_cond = upcond

        prev_offset = var.source_multipat_offsets[0]
        for multipat_offset in var.source_multipat_offsets[1:]:
            self.seq.If(fin_cond, var.source_multipat_fsm.here)(
                prev_offset(multipat_offset)
            )
            prev_offset = multipat_offset

        prev_sizes = var.source_multipat_sizes[0]
        for multipat_sizes in var.source_multipat_sizes[1:]:
            for prev_size, size in zip(prev_sizes, multipat_sizes):
                self.seq.If(fin_cond, var.source_multipat_fsm.here)(
                    prev_size(size)
                )
            prev_sizes = multipat_sizes

        prev_strides = var.source_multipat_strides[0]
        for multipat_strides in var.source_multipat_strides[1:]:
            for prev_stride, stride in zip(prev_strides, multipat_strides):
                self.seq.If(fin_cond, var.source_multipat_fsm.here)(
                    prev_stride(stride)
                )
            prev_strides = multipat_strides

        self.seq.If(fin_cond, var.source_multipat_fsm.here)(
            var.source_multipat_num_patterns.dec()
        )

        var.source_multipat_fsm.If(fin_cond,
                                   var.source_multipat_num_patterns == 0).goto_next()

        self.seq.If(var.source_multipat_fsm.here)(
            var.source_ram_renable(0),
            var.source_idle(1)
        )

        var.source_multipat_fsm.goto_init()

    def _setup_sink_ram(self, ram, var, port, set_cond):
        if ram._id() in var.sink_ram_id_map:
            ram_id = var.sink_ram_id_map[ram._id()]
            self.seq.If(set_cond)(
                var.sink_ram_sel(ram_id)
            )
            return

        if ram._id() not in self.ram_id_map:
            ram_id = self.ram_id_count
            self.ram_id_count += 1
            self.ram_id_map[ram._id()] = ram_id
        else:
            ram_id = self.ram_id_map[ram._id()]

        var.sink_ram_id_map[ram._id()] = ram_id

        self.seq.If(set_cond)(
            var.sink_ram_sel(ram_id)
        )

        ram_cond = (var.sink_ram_sel == ram_id)
        wenable = vtypes.Ands(var.sink_ram_wenable, ram_cond)
        ram.write_rtl(var.sink_ram_waddr, var.sink_ram_wdata,
                      port=port, cond=wenable)

    def _synthesize_set_sink(self, var, name):
        if var.sink_fsm is not None:
            return

        sink_start = vtypes.Ands(self.start,
                                 vtypes.And(var.sink_mode, mode_normal))

        fsm_id = self.fsm_id_count
        self.fsm_id_count += 1

        prefix = self._prefix(name)

        fsm_name = '_%s_sink_fsm_%d' % (prefix, fsm_id)
        var.sink_fsm = FSM(self.module, fsm_name, self.clock, self.reset,
                           as_module=self.fsm_as_module)

        self.seq.If(var.sink_fsm.here)(
            var.sink_ram_wenable(0)
        )

        var.sink_fsm.If(sink_start).goto_next()

        self.seq.If(var.sink_fsm.here)(
            var.sink_ram_waddr(var.sink_offset - var.sink_stride),
            var.sink_count(var.sink_size)
        )

        num_wdelay = self._write_delay()
        for _ in range(num_wdelay):
            var.sink_fsm.goto_next()

        if name in self.sink_when_map:
            when = self.sink_when_map[name]
            wcond = when.read()
        else:
            wcond = None

        rdata = var.read()

        self.seq.If(var.sink_fsm.here)(
            var.sink_ram_wenable(0)
        )
        self.seq.If(var.sink_fsm.here, wcond)(
            var.sink_ram_waddr.add(var.sink_stride),
            var.sink_ram_wdata(rdata),
            var.sink_ram_wenable(1),
            var.sink_count.dec()
        )

        var.sink_fsm.If(wcond, var.sink_count == 1).goto_init()

    def _make_sink_pattern_vars(self, var, name):
        if var.sink_pat_cur_offsets is not None:
            return

        prefix = self._prefix(name)

        var.sink_pat_cur_offsets = [self.module.Reg('_sink_%s_pat_cur_offset_%d' % (prefix, i),
                                                    self.addrwidth, initval=0)
                                    for i in range(self.max_pattern_length)]
        var.sink_pat_sizes = [self.module.Reg('_sink_%s_pat_size_%d' % (prefix, i),
                                              self.addrwidth + 1, initval=0)
                              for i in range(self.max_pattern_length)]
        var.sink_pat_strides = [self.module.Reg('_sink_%s_pat_stride_%d' % (prefix, i),
                                                self.addrwidth, initval=0)
                                for i in range(self.max_pattern_length)]
        var.sink_pat_counts = [self.module.Reg('_sink_%s_pat_count_%d' % (prefix, i),
                                               self.addrwidth + 1, initval=0)
                               for i in range(self.max_pattern_length)]

    def _synthesize_set_sink_pattern(self, var, name):
        if var.sink_pat_fsm is not None:
            return

        sink_start = vtypes.Ands(self.start,
                                 vtypes.And(var.sink_mode, mode_pattern))

        fsm_id = self.fsm_id_count
        self.fsm_id_count += 1

        prefix = self._prefix(name)

        fsm_name = '_%s_sink_pat_fsm_%d' % (prefix, fsm_id)
        var.sink_pat_fsm = FSM(self.module, fsm_name,
                               self.clock, self.reset,
                               as_module=self.fsm_as_module)

        self.seq.If(var.sink_pat_fsm.here)(
            var.sink_ram_wenable(0)
        )

        var.sink_pat_fsm.If(sink_start).goto_next()

        for sink_pat_cur_offset in var.sink_pat_cur_offsets:
            self.seq.If(var.sink_pat_fsm.here)(
                sink_pat_cur_offset(0)
            )

        for (sink_pat_size, sink_pat_count) in zip(
                var.sink_pat_sizes, var.sink_pat_counts):
            self.seq.If(var.sink_pat_fsm.here)(
                sink_pat_count(sink_pat_size - 1)
            )

        num_wdelay = self._write_delay()
        for _ in range(num_wdelay):
            var.sink_pat_fsm.goto_next()

        if name in self.sink_when_map:
            when = self.sink_when_map[name]
            wcond = when.read()
        else:
            wcond = None

        sink_all_offset = self.module.Wire('_%s_sink_pat_all_offset' % prefix,
                                           self.addrwidth)
        sink_all_offset_val = var.sink_offset
        for sink_pat_cur_offset in var.sink_pat_cur_offsets:
            sink_all_offset_val += sink_pat_cur_offset
        sink_all_offset.assign(sink_all_offset_val)

        if name in self.sink_when_map:
            when = self.sink_when_map[name]
            wcond = when.read()
        else:
            wcond = None

        rdata = var.read()

        self.seq.If(var.sink_pat_fsm.here)(
            var.sink_ram_wenable(0)
        )
        self.seq.If(var.sink_pat_fsm.here, wcond)(
            var.sink_ram_waddr(sink_all_offset),
            var.sink_ram_wdata(rdata),
            var.sink_ram_wenable(1)
        )

        upcond = None

        for (sink_pat_cur_offset, sink_pat_size,
             sink_pat_stride, sink_pat_count) in zip(
                 var.sink_pat_cur_offsets, var.sink_pat_sizes,
                 var.sink_pat_strides, var.sink_pat_counts):

            self.seq.If(var.sink_pat_fsm.here, upcond)(
                sink_pat_cur_offset.add(sink_pat_stride),
                sink_pat_count.dec()
            )

            reset_cond = sink_pat_count == 0
            self.seq.If(var.sink_pat_fsm.here, upcond, reset_cond)(
                sink_pat_cur_offset(0),
                sink_pat_count(sink_pat_size - 1)
            )
            upcond = make_condition(upcond, reset_cond)

        fin_cond = upcond

        var.sink_pat_fsm.If(fin_cond).goto_init()

    def _make_sink_multipattern_vars(self, var, name):
        if var.sink_multipat_cur_offsets is not None:
            return

        prefix = self._prefix(name)

        var.sink_multipat_num_patterns = self.module.Reg(
            '_sink_%s_multipat_num_patterns' % prefix,
            int(math.ceil(math.log(self.max_multipattern_length, 2))), initval=0)
        var.sink_multipat_offsets = [
            self.module.Reg('_sink_%s_multipat_%d_offset' % (prefix, j),
                            self.addrwidth, initval=0)
            for j in range(self.max_multipattern_length)]
        var.sink_multipat_cur_offsets = [
            self.module.Reg('_sink_%s_multipat_%d_cur_offset' % (prefix, i),
                            self.addrwidth, initval=0)
            for i in range(self.max_pattern_length)]
        var.sink_multipat_sizes = [[self.module.Reg('_sink_%s_multipat_%d_size_%d' %
                                                    (prefix, j, i),
                                                    self.addrwidth + 1, initval=0)
                                    for i in range(self.max_pattern_length)]
                                   for j in range(self.max_multipattern_length)]
        var.sink_multipat_strides = [[self.module.Reg('_sink_%s_multipat_%d_stride_%d' %
                                                      (prefix, j, i),
                                                      self.addrwidth, initval=0)
                                      for i in range(self.max_pattern_length)]
                                     for j in range(self.max_multipattern_length)]
        var.sink_multipat_counts = [[self.module.Reg('_sink_%s_multipat_%d_count_%d' %
                                                     (prefix, j, i),
                                                     self.addrwidth + 1, initval=0)
                                     for i in range(self.max_pattern_length)]
                                    for j in range(self.max_multipattern_length)]

    def _synthesize_set_sink_multipattern(self, var, name):
        if var.sink_multipat_fsm is not None:
            return

        sink_start = vtypes.Ands(self.start,
                                 vtypes.And(var.sink_mode, mode_multipattern))

        fsm_id = self.fsm_id_count
        self.fsm_id_count += 1

        prefix = self._prefix(name)

        fsm_name = '_%s_sink_multipat_fsm_%d' % (prefix, fsm_id)
        var.sink_multipat_fsm = FSM(self.module, fsm_name,
                                    self.clock, self.reset,
                                    as_module=self.fsm_as_module)

        self.seq.If(var.sink_multipat_fsm.here)(
            var.sink_ram_wenable(0)
        )

        self.seq.If(sink_start)(
            var.sink_multipat_num_patterns.dec()
        )

        var.sink_multipat_fsm.If(sink_start).goto_next()

        for sink_multipat_cur_offset in var.sink_multipat_cur_offsets:
            self.seq.If(var.sink_multipat_fsm.here)(
                sink_multipat_cur_offset(0)
            )

        for (sink_multipat_size, sink_multipat_count) in zip(
                var.sink_multipat_sizes[0], var.sink_multipat_counts[0]):
            self.seq.If(sink_start)(
                sink_multipat_count(sink_multipat_size - 1)
            )

        num_wdelay = self._write_delay()
        for _ in range(num_wdelay):
            var.sink_multipat_fsm.goto_next()

        if name in self.sink_when_map:
            when = self.sink_when_map[name]
            wcond = when.read()
        else:
            wcond = None

        sink_all_offset = self.module.Wire('_%s_sink_multipat_all_offset' % prefix,
                                           self.addrwidth)
        sink_all_offset_val = var.sink_multipat_offsets[0]
        for sink_multipat_cur_offset in var.sink_multipat_cur_offsets:
            sink_all_offset_val += sink_multipat_cur_offset
        sink_all_offset.assign(sink_all_offset_val)

        if name in self.sink_when_map:
            when = self.sink_when_map[name]
            wcond = when.read()
        else:
            wcond = None

        rdata = var.read()

        self.seq.If(var.sink_multipat_fsm.here)(
            var.sink_ram_wenable(0)
        )
        self.seq.If(var.sink_multipat_fsm.here, wcond)(
            var.sink_ram_waddr(sink_all_offset),
            var.sink_ram_wdata(rdata),
            var.sink_ram_wenable(1)
        )

        upcond = None

        for (sink_multipat_cur_offset, sink_multipat_size,
             sink_multipat_stride, sink_multipat_count) in zip(
                 var.sink_multipat_cur_offsets, var.sink_multipat_sizes[0],
                 var.sink_multipat_strides[0], var.sink_multipat_counts[0]):

            self.seq.If(var.sink_multipat_fsm.here, upcond)(
                sink_multipat_cur_offset.add(sink_multipat_stride),
                sink_multipat_count.dec()
            )

            reset_cond = sink_multipat_count == 0
            self.seq.If(var.sink_multipat_fsm.here, upcond, reset_cond)(
                sink_multipat_cur_offset(0),
                sink_multipat_count(sink_multipat_size - 1)
            )
            upcond = make_condition(upcond, reset_cond)

        fin_cond = upcond

        prev_offset = var.sink_multipat_offsets[0]
        for multipat_offset in var.sink_multipat_offsets[1:]:
            self.seq.If(fin_cond, var.sink_multipat_fsm.here)(
                prev_offset(multipat_offset)
            )
            prev_offset = multipat_offset

        prev_sizes = var.sink_multipat_sizes[0]
        for multipat_sizes in var.sink_multipat_sizes[1:]:
            for prev_size, size in zip(prev_sizes, multipat_sizes):
                self.seq.If(fin_cond, var.sink_multipat_fsm.here)(
                    prev_size(size)
                )
            prev_sizes = multipat_sizes

        prev_strides = var.sink_multipat_strides[0]
        for multipat_strides in var.sink_multipat_strides[1:]:
            for prev_stride, stride in zip(prev_strides, multipat_strides):
                self.seq.If(fin_cond, var.sink_multipat_fsm.here)(
                    prev_stride(stride)
                )
            prev_strides = multipat_strides

        self.seq.If(fin_cond, var.sink_multipat_fsm.here)(
            var.sink_multipat_num_patterns.dec()
        )

        var.sink_multipat_fsm.If(fin_cond,
                                 var.sink_multipat_num_patterns == 0).goto_init()

    def _set_flag(self, fsm, prefix='_set_flag'):
        flag = self.module.TmpReg(initval=0, prefix=prefix)
        cond = fsm.here

        self.seq(
            flag(0)
        )
        self.seq.If(cond)(
            flag(1)
        )

        return flag

    def _implement_stream(self):
        self.implement()
        self.stream_synthesized = True

    def _write_delay(self):
        depth = self.pipeline_depth()
        return depth + self.ram_delay

    def _to_pattern(self, shape, order):
        pattern = []
        for p in order:
            if not isinstance(p, int):
                raise TypeError(
                    "Values of 'order' must be 'int', not %s" % str(type(p)))
            size = shape[p]
            basevalue = 1 if isinstance(size, int) else vtypes.Int(1)
            stride = functools.reduce(lambda x, y: x * y,
                                      shape[p + 1:], basevalue)
            pattern.append((size, stride))
        return tuple(pattern)

    def _prefix(self, name):
        return '%s_%s' % (self.name, name)

    def _dataname(self, name):
        return '%s_data' % self._prefix(name)

    def _collect_substreams(self):
        ret = []

        for sub in self.substreams:
            ret.extend(sub._collect_substreams())

        return ret

    def __getattr__(self, attr):
        f = BaseStream.__getattr__(self, attr)

        if (callable(f) and
            (f.__name__.startswith('Reduce') or
             f.__name__.startswith('Counter') or
             f.__name__.startswith('Pulse'))):
            if self.reduce_reset is None:
                self.reduce_reset = self.module.Reg(
                    '_'.join(['', self.name, 'reduce_reset']), initval=1)
                self.reduce_reset_var = self.Variable(
                    self.reduce_reset, width=1)

            return functools.partial(f, reset=self.reduce_reset_var)

        return f


class Substream(BaseSubstream):

    def __init__(self, module, clock, reset, substrm, strm=None):
        self.module = module
        self.clock = clock
        self.reset = reset
        self.reset_delay = 0
        BaseSubstream.__init__(self, substrm, strm)

    def to_source(self, name, data):
        source_name = self.substrm._dataname(name)
        cond = self.module.Reg(compiler._tmp_name(self.name('%s_cond' % source_name)),
                               initval=0)
        BaseSubstream.write(self, source_name, data, cond)

    def to_constant(self, name, data):
        constant_name = self.substrm._dataname(name)
        cond = self.module.Reg(compiler._tmp_name(self.name('%s_cond' % constant_name)),
                               initval=0)
        BaseSubstream.write(self, constant_name, data, cond)

    def from_sink(self, name):
        sink_name = self.substrm._dataname(name)
        return BaseSubstream.read(self, sink_name)

    def _collect_substreams(self):
        ret = []
        self.reset_delay = 0
        ret.append(self)
        ret.extend(self.substrm._collect_substreams())
        for s in ret:
            s.reset_delay += 1
        return ret


def add_mux(targ, cond, value):
    prev_assign = targ._get_assign()
    if not prev_assign:
        targ.assign(vtypes.Mux(cond, value, 0))
    else:
        prev_value = prev_assign.statement.right
        prev_assign.overwrite_right(
            vtypes.Mux(cond, value, prev_value))
        targ.module.remove(prev_assign)
        targ.module.append(prev_assign)
