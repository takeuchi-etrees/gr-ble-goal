"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time


class RangeDetector(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, range=0.1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.range = range
        self.cur_val = 0.0
        self.in_range = False
        self.count = 0
        self.time = 0
        self.seq = 0

    def work(self, input_items, output_items):
        for i in range(len(input_items[0])):
            if input_items[0][i] < self.cur_val - self.range:
                self.cur_val = input_items[0][i]
                self.count = 0
                self.time = int(time.time()*1000)
            elif input_items[0][i] > self.cur_val + self.range:
                self.cur_val = input_items[0][i]
                self.count = 0
                self.time = int(time.time()*1000)
            else:
                self.cur_val = input_items[0][i]
                self.count += 1
            
            if self.count > 320:
                output_items[0][i] = 1.0
            else:
                output_items[0][i] = 0.0
                
            if self.count == 320:
                tag_key = pmt.intern("in_range")
                tag_value = pmt.intern("{0}@{1}@{2}".format(self.cur_val, self.time, self.seq))
                tag_offset = i
                self.add_item_tag(0, self.nitems_written(0) + tag_offset, tag_key, tag_value)
                self.seq += 1
                           
        return len(output_items[0])
