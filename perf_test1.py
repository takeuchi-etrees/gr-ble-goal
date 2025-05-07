#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Bluetooth LE Receiver
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import etreesModule
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import iio
from gnuradio import zeromq
import sip



class perf_test1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Bluetooth LE Receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Bluetooth LE Receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "perf_test1")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.ble_channel_spacing = ble_channel_spacing = 2e6
        self.ble_channel = ble_channel = 12
        self.ble_base_freq = ble_base_freq = 2402e6
        self.samp_rate = samp_rate = 2e6
        self.freq = freq = ble_base_freq+(ble_channel_spacing * ble_channel)

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink('tcp://127.0.0.1:3334', 100, True)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.float_t, "packet_len")
        self.low_pass_filter_0_0_0 = filter.fir_filter_ccf(
            2,
            firdes.low_pass(
                1,
                samp_rate,
                1e6,
                5e4,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            2,
            firdes.low_pass(
                1,
                samp_rate,
                1e6,
                5e4,
                window.WIN_HAMMING,
                6.76))
        self.iio_fmcomms2_source_0 = iio.fmcomms2_source_fc32('ip:192.168.3.10', [True, True, True, True], 4095)
        self.iio_fmcomms2_source_0.set_len_tag_key('packet_len')
        self.iio_fmcomms2_source_0.set_frequency(int(freq))
        self.iio_fmcomms2_source_0.set_samplerate(int(samp_rate))
        if True:
            self.iio_fmcomms2_source_0.set_gain_mode(0, 'fast_attack')
            self.iio_fmcomms2_source_0.set_gain(0, 64)
        if True:
            self.iio_fmcomms2_source_0.set_gain_mode(1, 'fast_attack')
            self.iio_fmcomms2_source_0.set_gain(1, 64)
        self.iio_fmcomms2_source_0.set_quadrature(True)
        self.iio_fmcomms2_source_0.set_rfdc(True)
        self.iio_fmcomms2_source_0.set_bbdc(True)
        self.iio_fmcomms2_source_0.set_filter_params('Auto', '', 0, 0)
        self.etreesModule_rangeDetector_0 = etreesModule.rangeDetector(0.1)
        self.etreesModule_calcPhaseDiff_0 = etreesModule.calcPhaseDiff()
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_float, 1, 4095, "packet_len")
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(20, 0.05, 4000, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.etreesModule_rangeDetector_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.etreesModule_calcPhaseDiff_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.etreesModule_rangeDetector_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.etreesModule_rangeDetector_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 1), (self.low_pass_filter_0_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.etreesModule_calcPhaseDiff_0, 1))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.etreesModule_calcPhaseDiff_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "perf_test1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_ble_channel_spacing(self):
        return self.ble_channel_spacing

    def set_ble_channel_spacing(self, ble_channel_spacing):
        self.ble_channel_spacing = ble_channel_spacing
        self.set_freq(self.ble_base_freq+(self.ble_channel_spacing * self.ble_channel))

    def get_ble_channel(self):
        return self.ble_channel

    def set_ble_channel(self, ble_channel):
        self.ble_channel = ble_channel
        self.set_freq(self.ble_base_freq+(self.ble_channel_spacing * self.ble_channel))

    def get_ble_base_freq(self):
        return self.ble_base_freq

    def set_ble_base_freq(self, ble_base_freq):
        self.ble_base_freq = ble_base_freq
        self.set_freq(self.ble_base_freq+(self.ble_channel_spacing * self.ble_channel))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_fmcomms2_source_0.set_samplerate(int(self.samp_rate))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 1e6, 5e4, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 1e6, 5e4, window.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.iio_fmcomms2_source_0.set_frequency(int(self.freq))




def main(top_block_cls=perf_test1, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
