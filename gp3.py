#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#   Iperf3 GUI version
#   Nov 14, 2019 11:18:09 AM
#   Stephen Hsu

import datetime
import logging
import queue
import re
import subprocess as sub
import sys
import threading
from time import sleep

logger = logging.getLogger('')
perfCMD = ""
dict_config = {}
list_perfCMD = []
bool_btnStart = False
daemon = False

try:
    import Tkinter as tk
    from Tkinter import Messagebox
except ImportError:
    import tkinter as tk
    from tkinter import messagebox

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

import gp3_support


def vp_start_gui():
    """Starting point when module is the main routine."""
    global val, w, root
    root = tk.Tk()
    gp3_support.set_Tk_var()
    top = mainlevel(root)
    gp3_support.init(root, top)
    # Add logging to scrolled text function and detect break stephenhsu.20191114_1136
    logging.basicConfig(level=logging.INFO)
    root.protocol("WM_DELETE_WINDOW", disable_event)
    root.iconbitmap("mainIcon.ico")
    root.mainloop()


w = None

def disable_event():
    pass

def closeMain():
    sys.exit()

def create_mainlevel(root, *args, **kwargs):
    """Starting point when module is imported by another program."""
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    gp3_support.set_Tk_var()
    top = mainlevel(w)
    gp3_support.init(w, top, *args, **kwargs)

    return (w, top)


def destroy_mainlevel():
    global w
    w.destroy()
    w = None


class mainlevel:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""
        self.clock = Clock()
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])


        top.geometry("459x381+321+181")
        top.minsize(116, 1)
        top.maxsize(1028, 750)
        top.resizable(0, 0)
        top.title("IPERF3 UI")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.lframe_Server = tk.LabelFrame(top)
        self.lframe_Server.place(relx=0.211, rely=0.0, relheight=0.197
                                 , relwidth=0.327)
        self.lframe_Server.configure(relief='groove')
        self.lframe_Server.configure(foreground="black")
        self.lframe_Server.configure(text='''Server Mode''')
        self.lframe_Server.configure(background="#d9d9d9")
        self.lframe_Server.configure(highlightbackground="#d9d9d9")
        self.lframe_Server.configure(highlightcolor="black")

        self.entry_srvPort = tk.Entry(self.lframe_Server, state='disabled')
        self.entry_srvPort.place(relx=0.66, rely=0.613, height=17, relwidth=0.293
                                 , bordermode='ignore')
        self.entry_srvPort.configure(background="white")
        self.entry_srvPort.configure(disabledforeground="#a3a3a3")
        self.entry_srvPort.configure(font="TkFixedFont")
        self.entry_srvPort.configure(foreground="#000000")
        self.entry_srvPort.configure(highlightbackground="#d9d9d9")
        self.entry_srvPort.configure(highlightcolor="black")
        self.entry_srvPort.configure(insertbackground="black")
        self.entry_srvPort.configure(selectbackground="#c4c4c4")
        self.entry_srvPort.configure(selectforeground="black")
        tooltip_font = "TkDefaultFont"
        ToolTip(self.entry_srvPort, tooltip_font, '''"Server port number must match with client port"''', delay=0.5)

        self.entry_srvInterval = tk.Entry(self.lframe_Server, state='disabled')
        self.entry_srvInterval.place(relx=0.667, rely=0.307, height=17
                                     , relwidth=0.293, bordermode='ignore')
        self.entry_srvInterval.configure(background="white")
        self.entry_srvInterval.configure(disabledforeground="#a3a3a3")
        self.entry_srvInterval.configure(font="TkFixedFont")
        self.entry_srvInterval.configure(foreground="#000000")
        self.entry_srvInterval.configure(highlightbackground="#d9d9d9")
        self.entry_srvInterval.configure(highlightcolor="black")
        self.entry_srvInterval.configure(insertbackground="black")
        self.entry_srvInterval.configure(selectbackground="#c4c4c4")
        self.entry_srvInterval.configure(selectforeground="black")

        self.chk_srvinterval = tk.Checkbutton(self.lframe_Server, command=self.function_UISwitch)
        self.chk_srvinterval.place(relx=0.067, rely=0.267, relheight=0.347
                                   , relwidth=0.567, bordermode='ignore')
        self.chk_srvinterval.configure(activebackground="#ececec")
        self.chk_srvinterval.configure(activeforeground="#000000")
        self.chk_srvinterval.configure(background="#d9d9d9")
        self.chk_srvinterval.configure(disabledforeground="#a3a3a3")
        self.chk_srvinterval.configure(foreground="#000000")
        self.chk_srvinterval.configure(highlightbackground="#d9d9d9")
        self.chk_srvinterval.configure(highlightcolor="black")
        self.chk_srvinterval.configure(justify='left')
        self.chk_srvinterval.configure(text='''Interval (s)''')
        self.chk_srvinterval.configure(variable=gp3_support.che59)

        self.chk_srvPort = tk.Checkbutton(self.lframe_Server, command=self.function_UISwitch)
        self.chk_srvPort.place(relx=0.04, rely=0.573, relheight=0.347
                               , relwidth=0.413, bordermode='ignore')
        self.chk_srvPort.configure(activebackground="#ececec")
        self.chk_srvPort.configure(activeforeground="#000000")
        self.chk_srvPort.configure(background="#d9d9d9")
        self.chk_srvPort.configure(disabledforeground="#a3a3a3")
        self.chk_srvPort.configure(foreground="#000000")
        self.chk_srvPort.configure(highlightbackground="#d9d9d9")
        self.chk_srvPort.configure(highlightcolor="black")
        self.chk_srvPort.configure(justify='left')
        self.chk_srvPort.configure(text='''Port''')
        self.chk_srvPort.configure(variable=gp3_support.che50)

        self.lframe_ClientMode = tk.LabelFrame(top)
        self.lframe_ClientMode.place(relx=0.013, rely=0.199, relheight=0.669
                                     , relwidth=0.392)
        self.lframe_ClientMode.configure(relief='groove')
        self.lframe_ClientMode.configure(foreground="black")
        self.lframe_ClientMode.configure(text='''Client Mode''')
        self.lframe_ClientMode.configure(background="#d9d9d9")
        self.lframe_ClientMode.configure(highlightbackground="#d9d9d9")
        self.lframe_ClientMode.configure(highlightcolor="black")

        self.label_IP = tk.Label(self.lframe_ClientMode)
        self.label_IP.place(relx=0.017, rely=0.078, height=22, width=67
                            , bordermode='ignore')
        self.label_IP.configure(activebackground="#f9f9f9")
        self.label_IP.configure(activeforeground="black")
        self.label_IP.configure(background="#d9d9d9")
        self.label_IP.configure(disabledforeground="#a3a3a3")
        self.label_IP.configure(foreground="#000000")
        self.label_IP.configure(highlightbackground="#d9d9d9")
        self.label_IP.configure(highlightcolor="black")
        self.label_IP.configure(text='''IP address''')

        self.entry_ipaddr = tk.Entry(self.lframe_ClientMode)
        self.entry_ipaddr.place(relx=0.411, rely=0.082, height=17, relwidth=0.522
                                , bordermode='ignore')
        self.entry_ipaddr.configure(background="white")
        self.entry_ipaddr.configure(disabledforeground="#a3a3a3")
        self.entry_ipaddr.configure(font="-family {細明體} -size 8")
        self.entry_ipaddr.configure(foreground="#000000")
        self.entry_ipaddr.configure(highlightbackground="#d9d9d9")
        self.entry_ipaddr.configure(highlightcolor="black")
        self.entry_ipaddr.configure(insertbackground="black")
        self.entry_ipaddr.configure(selectbackground="#c4c4c4")
        self.entry_ipaddr.configure(selectforeground="black")

        self.chk_clientInterval = tk.Checkbutton(self.lframe_ClientMode, command=self.function_UISwitch)
        self.chk_clientInterval.place(relx=0.017, rely=0.161, relheight=0.102
                                      , relwidth=0.511, bordermode='ignore')
        self.chk_clientInterval.configure(activebackground="#ececec")
        self.chk_clientInterval.configure(activeforeground="#000000")
        self.chk_clientInterval.configure(background="#d9d9d9")
        self.chk_clientInterval.configure(disabledforeground="#a3a3a3")
        self.chk_clientInterval.configure(foreground="#000000")
        self.chk_clientInterval.configure(highlightbackground="#d9d9d9")
        self.chk_clientInterval.configure(highlightcolor="black")
        self.chk_clientInterval.configure(justify='left')
        self.chk_clientInterval.configure(text='''Interval (s)''')
        self.chk_clientInterval.configure(variable=gp3_support.che47)

        self.entry_cInterval = tk.Entry(self.lframe_ClientMode, state='disabled')
        self.entry_cInterval.place(relx=0.578, rely=0.173, height=17
                                   , relwidth=0.356, bordermode='ignore')
        self.entry_cInterval.configure(background="white")
        self.entry_cInterval.configure(disabledforeground="#a3a3a3")
        self.entry_cInterval.configure(font="TkFixedFont")
        self.entry_cInterval.configure(foreground="#000000")
        self.entry_cInterval.configure(highlightbackground="#d9d9d9")
        self.entry_cInterval.configure(highlightcolor="black")
        self.entry_cInterval.configure(insertbackground="black")
        self.entry_cInterval.configure(selectbackground="#c4c4c4")
        self.entry_cInterval.configure(selectforeground="black")

        self.chk_cListenedPort = tk.Checkbutton(self.lframe_ClientMode, command=self.function_UISwitch)
        self.chk_cListenedPort.place(relx=0.028, rely=0.235, relheight=0.102
                                     , relwidth=0.283, bordermode='ignore')
        self.chk_cListenedPort.configure(activebackground="#ececec")
        self.chk_cListenedPort.configure(activeforeground="#000000")
        self.chk_cListenedPort.configure(background="#d9d9d9")
        self.chk_cListenedPort.configure(disabledforeground="#a3a3a3")
        self.chk_cListenedPort.configure(foreground="#000000")
        self.chk_cListenedPort.configure(highlightbackground="#d9d9d9")
        self.chk_cListenedPort.configure(highlightcolor="black")
        self.chk_cListenedPort.configure(justify='left')
        self.chk_cListenedPort.configure(text='''Port''')
        self.chk_cListenedPort.configure(variable=gp3_support.che49)

        self.entry_cListenedPort = tk.Entry(self.lframe_ClientMode, state='disabled')
        self.entry_cListenedPort.place(relx=0.583, rely=0.259, height=17
                                       , relwidth=0.356, bordermode='ignore')
        self.entry_cListenedPort.configure(background="white")
        self.entry_cListenedPort.configure(disabledforeground="#a3a3a3")
        self.entry_cListenedPort.configure(font="TkFixedFont")
        self.entry_cListenedPort.configure(foreground="#000000")
        self.entry_cListenedPort.configure(highlightbackground="#d9d9d9")
        self.entry_cListenedPort.configure(highlightcolor="black")
        self.entry_cListenedPort.configure(insertbackground="black")
        self.entry_cListenedPort.configure(selectbackground="#c4c4c4")
        self.entry_cListenedPort.configure(selectforeground="black")
        tooltip_font = "TkDefaultFont"
        ToolTip(self.entry_cListenedPort, tooltip_font, '''"Client port number must match with server port"''',
                delay=0.5)

        self.chk_testDuration = tk.Checkbutton(self.lframe_ClientMode, command=self.function_UISwitch)
        self.chk_testDuration.place(relx=0.017, rely=0.318, relheight=0.102
                                    , relwidth=0.55, bordermode='ignore')
        self.chk_testDuration.configure(activebackground="#ececec")
        self.chk_testDuration.configure(activeforeground="#000000")
        self.chk_testDuration.configure(background="#d9d9d9")
        self.chk_testDuration.configure(disabledforeground="#a3a3a3")
        self.chk_testDuration.configure(foreground="#000000")
        self.chk_testDuration.configure(highlightbackground="#d9d9d9")
        self.chk_testDuration.configure(highlightcolor="black")
        self.chk_testDuration.configure(justify='left')
        self.chk_testDuration.configure(text='''Test time (s)''')
        self.chk_testDuration.configure(variable=gp3_support.che51)

        self.entry_testTime = tk.Entry(self.lframe_ClientMode, state='disabled')
        self.entry_testTime.place(relx=0.578, rely=0.349, height=17
                                  , relwidth=0.356, bordermode='ignore')
        self.entry_testTime.configure(background="white")
        self.entry_testTime.configure(disabledforeground="#a3a3a3")
        self.entry_testTime.configure(font="TkFixedFont")
        self.entry_testTime.configure(foreground="#000000")
        self.entry_testTime.configure(highlightbackground="#d9d9d9")
        self.entry_testTime.configure(highlightcolor="black")
        self.entry_testTime.configure(insertbackground="black")
        self.entry_testTime.configure(selectbackground="#c4c4c4")
        self.entry_testTime.configure(selectforeground="black")

        self.chk_numOfParallelClient = tk.Checkbutton(self.lframe_ClientMode, command=self.function_UISwitch)
        self.chk_numOfParallelClient.place(relx=0.044, rely=0.416
                                           , relheight=0.102, relwidth=0.9, bordermode='ignore')
        self.chk_numOfParallelClient.configure(activebackground="#ececec")
        self.chk_numOfParallelClient.configure(activeforeground="#000000")
        self.chk_numOfParallelClient.configure(background="#d9d9d9")
        self.chk_numOfParallelClient.configure(disabledforeground="#a3a3a3")
        self.chk_numOfParallelClient.configure(foreground="#000000")
        self.chk_numOfParallelClient.configure(highlightbackground="#d9d9d9")
        self.chk_numOfParallelClient.configure(highlightcolor="black")
        self.chk_numOfParallelClient.configure(justify='left')
        self.chk_numOfParallelClient.configure(text='''Number of  Parallel Client''')
        self.chk_numOfParallelClient.configure(variable=gp3_support.che53)

        self.entry_numOfParallelClient = tk.Entry(self.lframe_ClientMode, state='disabled')
        self.entry_numOfParallelClient.place(relx=0.15, rely=0.502, height=17
                                             , relwidth=0.467, bordermode='ignore')
        self.entry_numOfParallelClient.configure(background="white")
        self.entry_numOfParallelClient.configure(disabledforeground="#a3a3a3")
        self.entry_numOfParallelClient.configure(font="TkFixedFont")
        self.entry_numOfParallelClient.configure(foreground="#000000")
        self.entry_numOfParallelClient.configure(highlightbackground="#d9d9d9")
        self.entry_numOfParallelClient.configure(highlightcolor="black")
        self.entry_numOfParallelClient.configure(insertbackground="black")
        self.entry_numOfParallelClient.configure(selectbackground="#c4c4c4")
        self.entry_numOfParallelClient.configure(selectforeground="black")

        self.chk_enableUDP = tk.Checkbutton(self.lframe_ClientMode)
        self.chk_enableUDP.place(relx=0.028, rely=0.569, relheight=0.102
                                 , relwidth=0.511, bordermode='ignore')
        self.chk_enableUDP.configure(activebackground="#ececec")
        self.chk_enableUDP.configure(activeforeground="#000000")
        self.chk_enableUDP.configure(background="#d9d9d9")
        self.chk_enableUDP.configure(disabledforeground="#a3a3a3")
        self.chk_enableUDP.configure(foreground="#000000")
        self.chk_enableUDP.configure(highlightbackground="#d9d9d9")
        self.chk_enableUDP.configure(highlightcolor="black")
        self.chk_enableUDP.configure(justify='left')
        self.chk_enableUDP.configure(text='''Enable UDP''')
        self.chk_enableUDP.configure(variable=gp3_support.che56)

        self.chk_bandwidth = tk.Checkbutton(self.lframe_ClientMode, command=self.function_UISwitch)
        self.chk_bandwidth.place(relx=0.028, rely=0.651, relheight=0.102
                                 , relwidth=0.511, bordermode='ignore')
        self.chk_bandwidth.configure(activebackground="#ececec")
        self.chk_bandwidth.configure(activeforeground="#000000")
        self.chk_bandwidth.configure(background="#d9d9d9")
        self.chk_bandwidth.configure(disabledforeground="#a3a3a3")
        self.chk_bandwidth.configure(foreground="#000000")
        self.chk_bandwidth.configure(highlightbackground="#d9d9d9")
        self.chk_bandwidth.configure(highlightcolor="black")
        self.chk_bandwidth.configure(justify='left')
        self.chk_bandwidth.configure(text='''BandWidth''')
        self.chk_bandwidth.configure(variable=gp3_support.che63)

        self.entry_bw = tk.Entry(self.lframe_ClientMode, state='disabled')
        self.entry_bw.place(relx=0.156, rely=0.737, height=17, relwidth=0.356
                            , bordermode='ignore')
        self.entry_bw.configure(background="white")
        self.entry_bw.configure(disabledforeground="#a3a3a3")
        self.entry_bw.configure(font="TkFixedFont")
        self.entry_bw.configure(foreground="#000000")
        self.entry_bw.configure(highlightbackground="#d9d9d9")
        self.entry_bw.configure(highlightcolor="black")
        self.entry_bw.configure(insertbackground="black")
        self.entry_bw.configure(selectbackground="#c4c4c4")
        self.entry_bw.configure(selectforeground="black")

        self.cmb_BWrate = ttk.Combobox(self.lframe_ClientMode, state='disabled')
        self.cmb_BWrate.place(relx=0.556, rely=0.718, relheight=0.086
                              , relwidth=0.294, bordermode='ignore')
        self.value_list = ['KB', 'MB']
        self.cmb_BWrate.configure(values=self.value_list)
        self.cmb_BWrate.configure(takefocus="")
        self.cmb_BWrate.set('KB')

        self.chk_windowSize = tk.Checkbutton(self.lframe_ClientMode, command=self.function_UISwitch)
        self.chk_windowSize.place(relx=0.028, rely=0.804, relheight=0.102
                                  , relwidth=0.567, bordermode='ignore')
        self.chk_windowSize.configure(activebackground="#ececec")
        self.chk_windowSize.configure(activeforeground="#000000")
        self.chk_windowSize.configure(background="#d9d9d9")
        self.chk_windowSize.configure(disabledforeground="#a3a3a3")
        self.chk_windowSize.configure(foreground="#000000")
        self.chk_windowSize.configure(highlightbackground="#d9d9d9")
        self.chk_windowSize.configure(highlightcolor="black")
        self.chk_windowSize.configure(justify='left')
        self.chk_windowSize.configure(text='''Window Size''')
        self.chk_windowSize.configure(variable=gp3_support.che68)

        self.entry_windowSize = tk.Entry(self.lframe_ClientMode, state='disabled')
        self.entry_windowSize.place(relx=0.156, rely=0.89, height=17
                                    , relwidth=0.356, bordermode='ignore')
        self.entry_windowSize.configure(background="white")
        self.entry_windowSize.configure(disabledforeground="#a3a3a3")
        self.entry_windowSize.configure(font="TkFixedFont")
        self.entry_windowSize.configure(foreground="#000000")
        self.entry_windowSize.configure(highlightbackground="#d9d9d9")
        self.entry_windowSize.configure(highlightcolor="black")
        self.entry_windowSize.configure(insertbackground="black")
        self.entry_windowSize.configure(selectbackground="#c4c4c4")
        self.entry_windowSize.configure(selectforeground="black")

        self.cmb_WindowSize = ttk.Combobox(self.lframe_ClientMode, state='disabled')
        self.cmb_WindowSize.place(relx=0.556, rely=0.886, relheight=0.086
                                  , relwidth=0.294, bordermode='ignore')
        self.value_list = ['KB', 'MB']
        self.cmb_WindowSize.configure(values=self.value_list)
        self.cmb_WindowSize.configure(takefocus="")
        self.cmb_WindowSize.set('KB')

        # self.btn_Start = tk.Button(top,command=self.runPerf)
        self.btn_Start = tk.Button(top, command=self.go)
        self.btn_Start.place(relx=0.784, rely=0.026, height=66, width=78)
        self.btn_Start.configure(activebackground="#ececec")
        self.btn_Start.configure(activeforeground="#000000")
        self.btn_Start.configure(background="#d9d9d9")
        self.btn_Start.configure(disabledforeground="#a3a3a3")
        self.btn_Start.configure(foreground="#000000")
        self.btn_Start.configure(highlightbackground="#d9d9d9")
        self.btn_Start.configure(highlightcolor="black")
        self.btn_Start.configure(pady="0")
        self.btn_Start.configure(text='''Start''')

        self.btn_Reset = tk.Button(top, command=self.clearState)
        self.btn_Reset.place(relx=0.566, rely=0.026, height=66, width=78)
        self.btn_Reset.configure(activebackground="#ececec")
        self.btn_Reset.configure(activeforeground="#000000")
        self.btn_Reset.configure(background="#d9d9d9")
        self.btn_Reset.configure(disabledforeground="#a3a3a3")
        self.btn_Reset.configure(foreground="#000000")
        self.btn_Reset.configure(highlightbackground="#d9d9d9")
        self.btn_Reset.configure(highlightcolor="black")
        self.btn_Reset.configure(pady="0")
        self.btn_Reset.configure(text='''Reset''')

        self.label_iperfCmd = tk.Label(top)
        self.label_iperfCmd.place(relx=0.002, rely=0.869, height=22, width=107)
        self.label_iperfCmd.configure(activebackground="#f9f9f9")
        self.label_iperfCmd.configure(activeforeground="black")
        self.label_iperfCmd.configure(background="#d9d9d9")
        self.label_iperfCmd.configure(disabledforeground="#a3a3a3")
        self.label_iperfCmd.configure(foreground="#000000")
        self.label_iperfCmd.configure(highlightbackground="#d9d9d9")
        self.label_iperfCmd.configure(highlightcolor="black")
        self.label_iperfCmd.configure(text='''iperf command''')

        self.entry_runCMD = tk.Entry(top)
        self.entry_runCMD.place(relx=0.015, rely=0.919, height=17
                                , relwidth=0.379)
        self.entry_runCMD.configure(background="white")
        self.entry_runCMD.configure(disabledforeground="#a3a3a3")
        self.entry_runCMD.configure(font="TkFixedFont")
        self.entry_runCMD.configure(foreground="#000000")
        self.entry_runCMD.configure(highlightbackground="#d9d9d9")
        self.entry_runCMD.configure(highlightcolor="black")
        self.entry_runCMD.configure(insertbackground="black")
        self.entry_runCMD.configure(selectbackground="#c4c4c4")
        self.entry_runCMD.configure(selectforeground="black")
        self.entry_runCMD.configure(state='readonly')
        tooltip_font = "TkDefaultFont"
        ToolTip(self.entry_runCMD, tooltip_font, '''"Generate the iperf3 command automatically"''', delay=0.5)

        self.label_ver = tk.Label(top)
        self.label_ver.place(relx=0.808, rely=0.924, height=22, width=79)
        self.label_ver.configure(activebackground="#f9f9f9")
        self.label_ver.configure(activeforeground="black")
        self.label_ver.configure(background="#d9d9d9")
        self.label_ver.configure(disabledforeground="#a3a3a3")
        self.label_ver.configure(font="-family {微軟正黑體} -size 8")
        self.label_ver.configure(foreground="#000000")
        self.label_ver.configure(highlightbackground="#d9d9d9")
        self.label_ver.configure(highlightcolor="black")
        self.label_ver.configure(text='''Ver. 1.2.0211''')

        self.lframe_output = tk.LabelFrame(top)
        self.lframe_output.place(relx=0.414, rely=0.197, relheight=0.669
                                 , relwidth=0.566)
        self.lframe_output.configure(relief='flat')
        self.lframe_output.configure(foreground="black")
        self.lframe_output.configure(relief="flat")
        self.lframe_output.configure(text='''Output''')
        self.lframe_output.configure(background="#d9d9d9")
        self.lframe_output.configure(highlightbackground="#d9d9d9")
        self.lframe_output.configure(highlightcolor="black")

        self.scrolledtxt_output = ScrolledText(self.lframe_output, state='normal', height=12)
        self.scrolledtxt_output.place(relx=0.015, rely=0.071, relheight=0.91
                                      , relwidth=0.965, bordermode='ignore')
        self.scrolledtxt_output.configure(background="white")
        self.scrolledtxt_output.configure(font="TkTextFont")
        self.scrolledtxt_output.configure(foreground="black")
        self.scrolledtxt_output.configure(highlightbackground="#d9d9d9")
        self.scrolledtxt_output.configure(highlightcolor="black")
        self.scrolledtxt_output.configure(insertbackground="black")
        self.scrolledtxt_output.configure(insertborderwidth="3")
        self.scrolledtxt_output.configure(selectbackground="#c4c4c4")
        self.scrolledtxt_output.configure(selectforeground="black")
        self.scrolledtxt_output.configure(wrap="none")

        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.lframe_output.after(100, self.poll_log_queue)

        self.combox_modeSwitch = ttk.Combobox(top)
        self.combox_modeSwitch.place(relx=0.024, rely=0.081, relheight=0.058
                                     , relwidth=0.159)
        self.value_list = ['Server', 'Client']
        self.combox_modeSwitch.configure(values=self.value_list)
        self.combox_modeSwitch.configure(takefocus="")
        self.combox_modeSwitch.set('Server')

        self.label_Mode = tk.Label(top)
        self.label_Mode.place(relx=0.022, rely=0.018, height=22, width=37)
        self.label_Mode.configure(activebackground="#f9f9f9")
        self.label_Mode.configure(activeforeground="black")
        self.label_Mode.configure(background="#d9d9d9")
        self.label_Mode.configure(disabledforeground="#a3a3a3")
        self.label_Mode.configure(foreground="#000000")
        self.label_Mode.configure(highlightbackground="#d9d9d9")
        self.label_Mode.configure(highlightcolor="black")
        self.label_Mode.configure(text='''Mode''')

        self.btn_Close = tk.Button(top, command=closeMain)
        self.btn_Close.place(relx=0.44, rely=0.879, height=36, width=78)
        self.btn_Close.configure(activebackground="#ececec")
        self.btn_Close.configure(activeforeground="#000000")
        self.btn_Close.configure(background="#d9d9d9")
        self.btn_Close.configure(disabledforeground="#a3a3a3")
        self.btn_Close.configure(foreground="#000000")
        self.btn_Close.configure(highlightbackground="#d9d9d9")
        self.btn_Close.configure(highlightcolor="black")
        self.btn_Close.configure(pady="0")
        self.btn_Close.configure(text='''Exit''')
    # ======================================================
    # Customized function
    # ======================================================

    def function_UISwitch(self):
        if gp3_support.che59.get() == 1:
            self.entry_srvInterval.configure(state='normal')
        elif gp3_support.che59.get() == 0:
            self.entry_srvInterval.delete(0, 'end')
            self.entry_srvInterval.configure(state='disabled')
        if gp3_support.che50.get() == 1:
            self.entry_srvPort.configure(state='normal')
        elif gp3_support.che50.get() == 0:
            self.entry_srvPort.delete(0, 'end')
            self.entry_srvPort.configure(state='disabled')

        if gp3_support.che47.get() == 1:
            self.entry_cInterval.configure(state='normal')
        elif gp3_support.che47.get() == 0:
            self.entry_cInterval.delete(0, 'end')
            self.entry_cInterval.configure(state='disabled')
        if gp3_support.che49.get() == 1:
            self.entry_cListenedPort.configure(state='normal')
        elif gp3_support.che49.get() == 0:
            self.entry_cListenedPort.delete(0, 'end')
            self.entry_cListenedPort.configure(state='disabled')
        if gp3_support.che51.get() == 1:
            self.entry_testTime.configure(state='normal')
        elif gp3_support.che51.get() == 0:
            self.entry_testTime.delete(0, 'end')
            self.entry_testTime.configure(state='disabled')
        if gp3_support.che53.get() == 1:
            self.entry_numOfParallelClient.configure(state='normal')
        elif gp3_support.che53.get() == 0:
            self.entry_numOfParallelClient.delete(0, 'end')
            self.entry_numOfParallelClient.configure(state='disabled')
        if gp3_support.che63.get() == 1:
            self.entry_bw.configure(state='normal')
            self.cmb_BWrate.configure(state='normal')
        elif gp3_support.che63.get() == 0:
            self.entry_bw.delete(0, 'end')
            self.entry_bw.configure(state='disabled')
            self.cmb_BWrate.configure(state='disabled')
        if gp3_support.che68.get() == 1:
            self.entry_windowSize.configure(state='normal')
            self.cmb_WindowSize.configure(state='normal')
        elif gp3_support.che68.get() == 0:
            self.entry_windowSize.delete(0, 'end')
            self.entry_windowSize.configure(state='disabled')
            self.cmb_WindowSize.configure(state='disabled')

    def go(self):
        global thread_num, bool_btnStart
        dict_config.clear()
        if bool_btnStart == False:
            if daemon:
                self.clock.resume()
            else:
                self.clock.start()
            self.btn_Start.configure(text='''Stop''')
            self.btn_Reset.configure(state="disabled")
            self.delRunCmd()
            self.collectAllofConfig()
            perfOpt = self.genPerfOpt()
            self.fillInPerfcmd("iperf3 {0}".format(perfOpt))
            bool_btnStart = True
            if dict_config['mode'] == "Client":
                self.delRunCmd()
                self.clock.stop()
                self.btn_Reset.configure(state="normal")
                self.btn_Start.configure(text='''Start''')
                bool_btnStart = False
                self.outToLog()
        else:
            self.delRunCmd()
            self.clock.stop()
            self.outToLog()
            self.btn_Reset.configure(state="normal")
            self.btn_Start.configure(text='''Start''')
            bool_btnStart = False

    def outToLog(self):
        content = self.scrolledtxt_output.get('1.0','end')
        with open("iperf3_{0}.log".format(self.clock.getCurrentTime()), "a") as fn:
            fn.writelines(content.strip('\r\n') + '\n')
            fn.flush()

    def delRunCmd(self):
        self.entry_runCMD.delete(0, 'end')
        self.entry_runCMD.configure(state='readonly')

    def isValidiP(self, ip):
        m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
        return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

    def isNum(self, content):
        return str(content).isdigit()

    def collectAllofConfig(self):
        mode = self.combox_modeSwitch.get()  # mode

        if mode == 'Server':
            dict_config['mode'] = mode
            if gp3_support.che59.get() == 1:
                if self.entry_srvInterval.get() is None:
                    messagebox.showerror("Server Interval", "Please fill in the required interval time")
                    return
                elif not self.isNum(self.entry_srvInterval.get()):
                    messagebox.showerror("Server Interval", "A non-numeric value encountered")
                    return
                else:
                    dict_config['srvInterval'] = self.entry_srvInterval.get()

            if gp3_support.che50.get() == 0:
                dict_config['srvPort'] = '5201'
            elif gp3_support.che50.get() == 1:
                if self.entry_srvPort.get() is None:
                    messagebox.showerror("Server Port", "Please fill in the Server Listened port number")
                    return
                elif self.isNum(self.entry_srvPort.get()):
                    dict_config['srvPort'] = self.entry_srvPort.get()
                elif not self.isNum(self.entry_srvPort.get()):
                    messagebox.showerror("Server Listened Port", "A non-numeric value encountered")
                    return

        elif mode == 'Client':
            dict_config['mode'] = mode
            if self.entry_ipaddr.get() is None:
                messagebox.showerror("IP Address", "Please fill in the Server IP address")
                return
            elif not self.isValidiP(self.entry_ipaddr.get()):
                messagebox.showerror("ERROR", "IP address is invalid")
                return
            else:
                dict_config['ipaddr'] = self.entry_ipaddr.get()

            # option
            if gp3_support.che49.get() == 0:
                dict_config['cPort'] = '5201'  # default port: 5201
            elif gp3_support.che49.get() == 1:
                if self.entry_cListenedPort.get() is None:
                    messagebox.showerror("Client Listened Port", "Please fill in the Client Listened port number")
                elif not self.isNum(self.entry_cListenedPort.get()):
                    messagebox.showerror("Client Listened Port", "A non-numeric value encountered")
                    return
                else:
                    dict_config['cPort'] = self.entry_cListenedPort.get()
            if gp3_support.che47.get() == 1:
                if self.entry_cInterval.get() is None:
                    messagebox.showerror("Client Interval", "Please fill in the required interval time")
                elif not self.isNum(self.entry_cInterval.get()):
                    messagebox.showerror("Client Interval", "A non-numeric value encountered")
                    return
                else:
                    dict_config['cInterval'] = self.entry_cInterval.get()
            if gp3_support.che51.get() == 1:
                if self.entry_testTime.get() is None:
                    messagebox.showerror("Test Time", "Please fill in the required Test time")
                    return
                elif not self.isNum(self.entry_testTime.get()):
                    messagebox.showerror("Test Time", "A non-numeric value encountered")
                    return
                else:
                    dict_config['cTestTime'] = self.entry_testTime.get()

            if gp3_support.che53.get() == 1:
                if self.entry_numOfParallelClient.get() is None:
                    messagebox.showerror("Number Of Parallel Client", "Please fill in the Number Of Parallel Client")
                    return
                elif not self.isNum(self.entry_numOfParallelClient.get()):
                    messagebox.showerror("Number Of Parallel Client", "A non-numeric value encountered")
                    return
                else:
                    dict_config['numOfParallelClient'] = self.entry_numOfParallelClient.get()
            if gp3_support.che56.get() == 1:
                dict_config['udp'] = 'True'

            if gp3_support.che63.get() == 1:
                if self.entry_bw.get() is None:
                    messagebox.showerror("Bandwidth", "Please fill in the bandwdith vaule")
                    return
                elif not self.isNum(self.entry_bw.get()):
                    messagebox.showerror("Bandwidth", "A non-numeric value encountered")
                    return
                else:
                    dict_config['cBW'] = self.entry_bw.get() + self.cmb_BWrate.get()[0]

            if gp3_support.che68.get() == 1:
                if self.entry_windowSize.get() is None:
                    messagebox.showerror("WindowSize", "Please fill in the Window Size value")
                    return
                elif not self.isNum(self.entry_windowSize.get()):
                    messagebox.showerror("WindowSize", "A non-numeric value encountered")
                    return
                else:
                    dict_config['cWindowSize'] = self.entry_windowSize.get() + self.cmb_WindowSize.get()[0]
        else:
            messagebox.showerror("Mode Switch", "Please check your Mode configuration")
            return

    def genPerfOpt(self):
        if len(list_perfCMD) > 0:
            list_perfCMD.clear()
        if dict_config.get('mode') == "Server":
            list_perfCMD.append("-s")
            if 'srvInterval' in dict_config:
                list_perfCMD.append("-i {0}".format(dict_config.get('srvInterval')))
            if 'srvPort' in dict_config:
                list_perfCMD.append("-p {0}".format(dict_config.get('srvPort')))
        elif dict_config.get('mode') == "Client":
            if 'ipaddr' in dict_config:
                list_perfCMD.append("-c {0}".format(dict_config.get('ipaddr')))
            if 'udp' in dict_config:
                list_perfCMD.append("-u")
            if 'cBW' in dict_config:
                list_perfCMD.append("-b {0}".format(dict_config.get('cBW')))
            if 'numOfParallelClient' in dict_config:
                list_perfCMD.append("-P{0}".format(dict_config.get('numOfParallelClient')))
            if 'cPort' in dict_config:
                list_perfCMD.append("-p {0}".format(dict_config.get('cPort')))
            if 'cTestTime' in dict_config:
                list_perfCMD.append("-t {0}".format(dict_config.get('cTestTime')))
            if 'cInterval' in dict_config:
                list_perfCMD.append("-i {0}".format(dict_config.get('cInterval')))
            if 'cWindowSize' in dict_config:
                list_perfCMD.append("-w {0}".format(dict_config.get('cWindowSize')))
        return " ".join(list_perfCMD)

    def display(self, record):
        print(record)
        msg = self.queue_handler.format(record)
        self.scrolledtxt_output.insert("end", msg + "\n")

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.lframe_output.after(100, self.poll_log_queue)

    def quit(self, *args):
        try:
            if self.clock.is_alive():
                self.clock.stop()
        except:
            self.clock.stop()

    def clearState(self):
        global list_perfCMD, bool_btnStart
        list_perfCMD.clear()
        # disable all of checked box
        gp3_support.che47.set(0)
        gp3_support.che49.set(0)
        gp3_support.che50.set(0)
        gp3_support.che51.set(0)
        gp3_support.che53.set(0)
        gp3_support.che56.set(0)
        gp3_support.che59.set(0)
        gp3_support.che63.set(0)
        gp3_support.che68.set(0)
        # Clear all of textbox
        self.btn_Start.configure()
        self.entry_srvInterval.delete(0, 'end')
        self.entry_srvPort.delete(0, 'end')
        self.entry_ipaddr.delete(0, 'end')
        self.entry_cInterval.delete(0, 'end')
        self.entry_cListenedPort.delete(0, 'end')
        self.entry_testTime.delete(0, 'end')
        self.entry_numOfParallelClient.delete(0, 'end')
        self.entry_bw.delete(0, 'end')
        self.entry_windowSize.delete(0, 'end')
        self.entry_runCMD.configure(state='normal')
        self.entry_runCMD.delete(0, 'end')
        self.entry_runCMD.configure(state='readonly')
        self.combox_modeSwitch.set('Server')
        self.scrolledtxt_output.delete('1.0', 'end')
        self.cmb_WindowSize.set('KB')
        self.cmb_BWrate.set('KB')
        # disable all of entry textbox
        self.entry_bw.configure(state='disabled')
        self.entry_cInterval.configure(state='disabled')
        self.entry_cListenedPort.configure(state='disabled')
        self.entry_numOfParallelClient.configure(state='disabled')
        self.entry_srvInterval.configure(state='disabled')
        self.entry_srvPort.configure(state='disabled')
        self.entry_testTime.configure(state='disabled')
        self.entry_windowSize.configure(state='disabled')

    def fillInPerfcmd(self, cmd):
        self.entry_runCMD.configure(state='normal')
        self.entry_runCMD.insert(0, cmd)
        self.entry_runCMD.configure(state='readonly')


class Clock(threading.Thread):
    """Class to display the time every seconds

    Every 5 seconds, the time is displayed using the logging.ERROR level
    to show that different colors are associated to the log levels
    """

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self._can_run = threading.Event()
        self._stop_event.set()
        self._can_run.set()
        self.daemon = False

    def pause(self):
        self._can_run.clear()
        self._stop_event.wait()

    def resume(self):
        self._can_run.set()

    def getCurrentTime(self):
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f')

    def run(self):
        global daemon, fn
        daemon = True
        while True:
            self._can_run.wait()
            try:
                self._stop_event.clear()
                # do the thing
                logger.debug('[Debug] Thread clock started.')
                previous = -1
                second_resp = b''
                p = sub.Popen("dir /b", stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
                # p = sub.Popen("iperf3 {0}".format(" ".join(list_perfCMD)), stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
                # while not self._stop_event.is_set():
                fn_file = self.getCurrentTime()
                now = datetime.datetime.now()
                if previous != now.second:
                    previous = now.second
                    if dict_config['mode'] == "Server":
                        while True:
                            outResp = p.stdout.readline()
                            if bool_btnStart != False:
                                if now.second % 1 == 0:
                                    level = logging.ERROR
                                else:
                                    level = logging.INFO
                                if outResp == b"":
                                    sleep(0.5)
                                else:
                                    logger.log(level, outResp.decode('utf-8').strip('\r\n'))
                            else:
                                break
                    else:
                        for resp in p.stdout:
                            second_resp = resp
                            if now.second % 1 == 0:
                                level = logging.ERROR
                            else:
                                level = logging.INFO
                            logger.log(level, resp.decode('utf-8').strip('\r\n'))
                            #self.outToLog(second_resp, fn_file, True)
                    logger.log(level, "=========================")
                    # mode detect
                    # if mode = server, keep monitor the port
                    self.pause()
                    self.stop()
                    #self.outToLog(second_resp, fn_file, False)
                sleep(0.2)
            finally:
                self._stop_event.set()

    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


# ======================================================
# End of customized function
# ======================================================

from time import time


class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """

    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=1, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initialise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                   font=tooltip_font,
                   aspect=1000).grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in miliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root + 20, event.y_root - 10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()


# ===========================================================
#                   End of Class ToolTip
# ===========================================================

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                      | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                      + tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


class ScrolledText(AutoScroll, tk.Text):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


import platform


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    vp_start_gui()
