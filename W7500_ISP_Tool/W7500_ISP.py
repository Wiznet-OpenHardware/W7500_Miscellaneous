# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import serial.tools.list_ports
import w7500_isp_cmd
import binascii
import filecmp
import time
import os
import subprocess

SW_VERSION = '1.0.0.1'

def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))

def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))

###########################################################################
## Class W7500_ISP
###########################################################################


class W7500_ISP ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"W7500 ISP Tool", pos=wx.DefaultPosition,
                          size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(-1, -1), wx.DefaultSize)
        self.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Verdana"))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer_Step1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Step 1 - Serial Option"), wx.VERTICAL)

        fgSizer4 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        self.m_staticText_serial_port = wx.StaticText(sbSizer_Step1.GetStaticBox(), wx.ID_ANY, u"Serial Port",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_serial_port.Wrap(-1)

        fgSizer4.Add(self.m_staticText_serial_port, 1,
                     wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        m_comboBox_serial_portChoices = []
        self.m_comboBox_serial_port = wx.ComboBox(sbSizer_Step1.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                  wx.DefaultPosition, wx.DefaultSize, m_comboBox_serial_portChoices, 0)
        fgSizer4.Add(self.m_comboBox_serial_port, 1,
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_button_serial_refresh = wx.Button(sbSizer_Step1.GetStaticBox(), wx.ID_ANY, u"Refresh",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer4.Add(self.m_button_serial_refresh, 0, wx.ALL, 5)

        self.m_staticText_baud_rate = wx.StaticText(sbSizer_Step1.GetStaticBox(), wx.ID_ANY, u"Baud Rate",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_baud_rate.Wrap(-1)

        fgSizer4.Add(self.m_staticText_baud_rate, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        m_comboBox_baud_rateChoices = [u"2400", u"9600", u"14400", u"19200", u"38400", u"57600", u"76800", u"115200",
                                       u"230400", u"460800"]
        self.m_comboBox_baud_rate = wx.ComboBox(sbSizer_Step1.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.DefaultSize, m_comboBox_baud_rateChoices, 0)
        self.m_comboBox_baud_rate.SetSelection(7)
        fgSizer4.Add(self.m_comboBox_baud_rate, 1,
                     wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_button_serial_open = wx.Button(sbSizer_Step1.GetStaticBox(), wx.ID_ANY, u"Open", wx.DefaultPosition,
                                              wx.DefaultSize, 0)

        self.m_button_serial_open.SetDefault()
        fgSizer4.Add(self.m_button_serial_open, 1,
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_button_serial_close = wx.Button(sbSizer_Step1.GetStaticBox(), wx.ID_ANY, u"Close", wx.DefaultPosition,
                                               wx.DefaultSize, 0)

        self.m_button_serial_close.SetDefault()
        self.m_button_serial_close.Enable(False)

        fgSizer4.Add(self.m_button_serial_close, 1,
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        fgSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        sbSizer_Step1.Add(fgSizer4, 1, wx.EXPAND, 5)

        bSizer13.Add(sbSizer_Step1, 1, wx.EXPAND, 5)

        sbSizer_Step2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Step 2 - Erase"), wx.VERTICAL)

        bSizer_Step2_Child = wx.BoxSizer(wx.VERTICAL)

        self.m_checkBox_erase_mass = wx.CheckBox(sbSizer_Step2.GetStaticBox(), wx.ID_ANY, u"Erase All Data/Code Memory",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_checkBox_erase_mass.SetValue(True)
        bSizer_Step2_Child.Add(self.m_checkBox_erase_mass, 0, wx.ALL | wx.EXPAND, 5)

        self.m_checkBox_erase_chip = wx.CheckBox(sbSizer_Step2.GetStaticBox(), wx.ID_ANY, u"Erase All Code Memory",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Step2_Child.Add(self.m_checkBox_erase_chip, 0, wx.ALL | wx.EXPAND, 5)

        self.m_checkBox_erase_data0 = wx.CheckBox(sbSizer_Step2.GetStaticBox(), wx.ID_ANY, u"Erase Data0(0x0003FE00)",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Step2_Child.Add(self.m_checkBox_erase_data0, 0, wx.ALL, 5)

        self.m_checkBox_erase_data1 = wx.CheckBox(sbSizer_Step2.GetStaticBox(), wx.ID_ANY, u"Erase Data1(0x0003FF00)",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Step2_Child.Add(self.m_checkBox_erase_data1, 0, wx.ALL, 5)

        sbSizer_Step2.Add(bSizer_Step2_Child, 0, wx.EXPAND, 5)

        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_start_step2 = wx.Button(sbSizer_Step2.GetStaticBox(), wx.ID_ANY, u"Start Step2",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button_start_step2.SetFont(
            wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Verdana"))

        bSizer18.Add(self.m_button_start_step2, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer_Step2.Add(bSizer18, 1, wx.ALL | wx.EXPAND, 5)

        bSizer13.Add(sbSizer_Step2, 1, wx.EXPAND, 5)

        sbSizer_Step3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Step 3 - Code Read Lock or Data R/W Lock"),
                                          wx.VERTICAL)

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_checkBox_all_code_read_lock = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY,
                                                         u"All Code Read Lock/Data Read Write Lock", wx.DefaultPosition,
                                                         wx.DefaultSize, 0)
        bSizer9.Add(self.m_checkBox_all_code_read_lock, 0, wx.ALL, 5)

        self.m_checkBox_all_code_read_unlock = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY,
                                                           u"All Code Read Unlock/Data Read Write Unlock",
                                                           wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer9.Add(self.m_checkBox_all_code_read_unlock, 0, wx.ALL, 5)

        sbSizer_Step3.Add(bSizer9, 0, wx.ALL, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_crl = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY, u"Code Read Lock",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.m_checkBox_crl, 0, wx.ALL, 5)

        self.m_checkBox_cabwl = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY, u"All Code Write Lock",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_checkBox_cabwl.Enable(False)

        bSizer10.Add(self.m_checkBox_cabwl, 0, wx.ALL, 5)

        sbSizer_Step3.Add(bSizer10, 0, wx.ALL, 5)

        bSizer101 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_drl1 = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY, u"Data1 Read Lock",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer101.Add(self.m_checkBox_drl1, 0, wx.ALL, 5)

        self.m_checkBox_drl0 = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY, u"Data0 Read Lock",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer101.Add(self.m_checkBox_drl0, 0, wx.ALL, 5)

        sbSizer_Step3.Add(bSizer101, 0, wx.EXPAND, 5)

        bSizer111 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_dwl1 = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY, u"Data1 Write Lock",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer111.Add(self.m_checkBox_dwl1, 0, wx.ALL, 5)

        self.m_checkBox_dwl0 = wx.CheckBox(sbSizer_Step3.GetStaticBox(), wx.ID_ANY, u"Data0 Write Lock",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer111.Add(self.m_checkBox_dwl0, 0, wx.ALL, 5)

        sbSizer_Step3.Add(bSizer111, 0, wx.EXPAND, 5)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_start_step3 = wx.Button(sbSizer_Step3.GetStaticBox(), wx.ID_ANY, u"Start Step3",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer19.Add(self.m_button_start_step3, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer_Step3.Add(bSizer19, 1, wx.EXPAND, 5)

        bSizer13.Add(sbSizer_Step3, 1, wx.EXPAND, 5)

        bSizer5.Add(bSizer13, 1, wx.EXPAND, 5)

        bSizer151 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer_Step4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Step 4 - Code Write Lock"), wx.VERTICAL)

        bSizer11 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_all_code_write_lock = wx.CheckBox(sbSizer_Step4.GetStaticBox(), wx.ID_ANY,
                                                          u"All Code Write Lock", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer11.Add(self.m_checkBox_all_code_write_lock, 0, wx.ALL, 5)

        self.m_checkBox_all_code_write_unlock = wx.CheckBox(sbSizer_Step4.GetStaticBox(), wx.ID_ANY,
                                                            u"All Code Write Unlock", wx.DefaultPosition,
                                                            wx.DefaultSize, 0)
        bSizer11.Add(self.m_checkBox_all_code_write_unlock, 0, wx.ALL, 5)

        sbSizer_Step4.Add(bSizer11, 0, wx.EXPAND | wx.ALL, 5)

        sbSizer_code_write_block = wx.StaticBoxSizer(wx.StaticBox(sbSizer_Step4.GetStaticBox(), wx.ID_ANY, u"Block"),
                                                     wx.VERTICAL)

        gSizer8 = wx.GridSizer(0, 16, 0, 0)

        self.m_staticText_cwl31 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"31",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl31.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl31, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.m_staticText_cwl30 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"30",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl30.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl30, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText_cwl29 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"29",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl29.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl29, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl28 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"28",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl28.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl28, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl27 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"27",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl27.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl27, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl26 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"26",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl26.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl26, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl25 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"25",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl25.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl25, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl24 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"24",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl24.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl24, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl23 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"23",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl23.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl23, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl22 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"22",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl22.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl22, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl21 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"21",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl21.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl21, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl20 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"20",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl20.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl20, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl19 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"19",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl19.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl19, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl18 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"18",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl18.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl18, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl17 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"17",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl17.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl17, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl16 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"16",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl16.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl16, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl31 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl31, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl30 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl30, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl29 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl29, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl28 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl28, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl27 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl27, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl26 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl26, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl25 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl25, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl24 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl24, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl23 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl23, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl22 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl22, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl21 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl21, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl20 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl20, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl19 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl19, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl18 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl18, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl17 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl17, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl16 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl16, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl15 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"15",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl15.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl15, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl14 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"14",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl14.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl14, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl13 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"13",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl13.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl13, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl12 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"12",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl12.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl12, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl11 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"11",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl11.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl11, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl10 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"10",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl10.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl10, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl9 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"9",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl9.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl8 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"8",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl8.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl7 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"7",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl7.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl6 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"6",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl6.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl5 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"5",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl5.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl4 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"4",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl4.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl3 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"3",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl3.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl2 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"2",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl2.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl1 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"1",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl1.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_cwl0 = wx.StaticText(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, u"0",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_cwl0.Wrap(-1)

        gSizer8.Add(self.m_staticText_cwl0, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl15 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl15, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl14 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl14, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl13 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl13, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl12 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl12, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl11 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl11, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl10 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl10, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl9 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl8 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl7 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl6 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl5 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl4 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl3 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl2 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl1 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_cwl0 = wx.CheckBox(sbSizer_code_write_block.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_checkBox_cwl0, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        sbSizer_code_write_block.Add(gSizer8, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        sbSizer_Step4.Add(sbSizer_code_write_block, 0, wx.EXPAND | wx.ALL, 5)

        bSizer23 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_start_step4 = wx.Button(sbSizer_Step4.GetStaticBox(), wx.ID_ANY, u"Start Step4",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer23.Add(self.m_button_start_step4, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer_Step4.Add(bSizer23, 1, wx.EXPAND, 5)

        sbSizer_Step4.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer151.Add(sbSizer_Step4, 1, wx.EXPAND, 5)

        sbSizer_Step5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Step 5 - Select the binary file"),
                                          wx.VERTICAL)

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        fgSizer5 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText_Binary_File = wx.StaticText(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Binary File :",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_Binary_File.Wrap(-1)

        fgSizer5.Add(self.m_staticText_Binary_File, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_File_Path = wx.TextCtrl(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.Size(200, -1), 0)
        fgSizer5.Add(self.m_textCtrl_File_Path, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button_browse = wx.Button(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Browse", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        fgSizer5.Add(self.m_button_browse, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer14.Add(fgSizer5, 1, wx.EXPAND, 5)

        sbSizer_Step5.Add(bSizer14, 0, wx.EXPAND | wx.ALL, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_verify = wx.CheckBox(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Verify after programming",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.m_checkBox_verify, 0, wx.ALL, 5)

        self.m_checkBox_WriteMainFlash = wx.CheckBox(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Write MainFlash",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_checkBox_WriteMainFlash.SetValue(True)
        bSizer15.Add(self.m_checkBox_WriteMainFlash, 0, wx.ALL, 5)

        self.m_checkBox_WriteDataFlash = wx.CheckBox(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Write DataFlash",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.m_checkBox_WriteDataFlash, 0, wx.ALL, 5)

        self.m_checkBox_Reset = wx.CheckBox(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Reset", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_checkBox_Reset.SetValue(True)
        bSizer15.Add(self.m_checkBox_Reset, 0, wx.ALL, 5)

        sbSizer_Step5.Add(bSizer15, 0, wx.EXPAND | wx.ALL, 5)

        bSizer24 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_start_step5 = wx.Button(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Start Step5",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer24.Add(self.m_button_start_step5, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer_Step5.Add(bSizer24, 1, wx.EXPAND, 5)

        bSizer91 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_Isp_start = wx.Button(sbSizer_Step5.GetStaticBox(), wx.ID_ANY, u"Start All Steps",
                                            wx.DefaultPosition, wx.Size(300, 30), 0)
        self.m_button_Isp_start.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Verdana"))

        bSizer91.Add(self.m_button_Isp_start, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer_Step5.Add(bSizer91, 1, wx.EXPAND, 5)

        sbSizer_Step5.Add((0, 0), 1, wx.EXPAND, 5)

        sbSizer_Step5.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer151.Add(sbSizer_Step5, 1, wx.EXPAND, 5)

        bSizer5.Add(bSizer151, 1, wx.EXPAND, 5)

        bSizer92 = wx.BoxSizer(wx.VERTICAL)

        bSizer92.SetMinSize(wx.Size(850, 20))

        bSizer5.Add(bSizer92, 0, 0, 5)

        self.SetSizer(bSizer5)
        self.Layout()
        bSizer5.Fit(self)
        self.m_statusBar_W7500_Status = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu_file = wx.Menu()
        self.m_menu_file.AppendSeparator()

        self.m_menu2 = wx.Menu()
        self.m_menu_file.AppendSubMenu(self.m_menu2, u"&Quit\tCtrl+Q")

        self.m_menubar1.Append(self.m_menu_file, u"&File")

        self.m_menu_ISP = wx.Menu()
        self.m_menu_Dump = wx.Menu()
        self.m_menuItem_MainFlashDump = wx.MenuItem(self.m_menu_Dump, wx.ID_ANY, u"&Main Flash Dump", wx.EmptyString,
                                                    wx.ITEM_NORMAL)
        self.m_menu_Dump.Append(self.m_menuItem_MainFlashDump)

        self.m_menuItem_Data_Dump = wx.MenuItem(self.m_menu_Dump, wx.ID_ANY, u"&Data Dump ", wx.EmptyString,
                                                wx.ITEM_NORMAL)
        self.m_menu_Dump.Append(self.m_menuItem_Data_Dump)

        self.m_menu_ISP.AppendSubMenu(self.m_menu_Dump, u"&Dump")

        self.m_menubar1.Append(self.m_menu_ISP, u"&ISP")

        self.m_menu_help = wx.Menu()
        self.m_menuItem_version = wx.MenuItem(self.m_menu_help, wx.ID_ANY, u"Version", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_help.Append(self.m_menuItem_version)

        self.m_menubar1.Append(self.m_menu_help, u"Help")

        self.SetMenuBar(self.m_menubar1)

        self.Centre(wx.VERTICAL)

        # Connect Events
        self.m_button_serial_refresh.Bind(wx.EVT_BUTTON, self.onRefresh)
        self.m_button_serial_open.Bind(wx.EVT_BUTTON, self.onSerialOpen)
        self.m_button_serial_close.Bind(wx.EVT_BUTTON, self.onSerialClose)
        self.m_checkBox_erase_mass.Bind(wx.EVT_CHECKBOX, self.onCheckEraseMass)
        self.m_checkBox_erase_chip.Bind(wx.EVT_CHECKBOX, self.onCheckEraseChip)
        self.m_checkBox_erase_data0.Bind(wx.EVT_CHECKBOX, self.onCheckEraseData0)
        self.m_checkBox_erase_data1.Bind(wx.EVT_CHECKBOX, self.onCheckEraseData1)
        self.m_button_start_step2.Bind(wx.EVT_BUTTON, self.onStartStep2)
        self.m_checkBox_all_code_read_lock.Bind(wx.EVT_CHECKBOX, self.onAllCodeReadLock)
        self.m_checkBox_all_code_read_unlock.Bind(wx.EVT_CHECKBOX, self.onAllCodeReadUnlock)
        self.m_checkBox_crl.Bind(wx.EVT_CHECKBOX, self.onCodeReadLock)
        self.m_checkBox_drl1.Bind(wx.EVT_CHECKBOX, self.onData1ReadLock)
        self.m_checkBox_drl0.Bind(wx.EVT_CHECKBOX, self.onData0ReadLock)
        self.m_checkBox_dwl1.Bind(wx.EVT_CHECKBOX, self.onData1WriteLock)
        self.m_checkBox_dwl0.Bind(wx.EVT_CHECKBOX, self.onData0WriteLock)
        self.m_button_start_step3.Bind(wx.EVT_BUTTON, self.onStartStep3)
        self.m_checkBox_all_code_write_lock.Bind(wx.EVT_CHECKBOX, self.onAllCodeWriteLock)
        self.m_checkBox_all_code_write_unlock.Bind(wx.EVT_CHECKBOX, self.onAllCodeWriteUnlock)
        self.m_button_start_step4.Bind(wx.EVT_BUTTON, self.onStartStep4)
        self.m_button_browse.Bind(wx.EVT_BUTTON, self.onBrowse)
        self.m_checkBox_WriteMainFlash.Bind(wx.EVT_CHECKBOX, self.onWriteMainFlash)
        self.m_checkBox_WriteDataFlash.Bind(wx.EVT_CHECKBOX, self.onWriteDataFlash)
        self.m_button_start_step5.Bind(wx.EVT_BUTTON, self.onStartStep5)
        self.m_button_Isp_start.Bind(wx.EVT_BUTTON, self.onStartAllSteps)
        self.Bind(wx.EVT_MENU, self.onFlashDump, id=self.m_menuItem_MainFlashDump.GetId())
        self.Bind(wx.EVT_MENU, self.onDataDump, id=self.m_menuItem_Data_Dump.GetId())
        self.Bind(wx.EVT_MENU, self.onVersion, id=self.m_menuItem_version.GetId())

        # Kaizen User Code
        self.GetComPortList()

    def __del__( self ):
        if self.isopen == 1:
            self.isp.__del__()
    
    # Virtual event handlers, overide them in your derived class
    def onRefresh( self, event ):
        self.GetComPortList()
         
    def onSerialOpen( self, event ):
        self.m_statusBar_W7500_Status.SetStatusText("W7500 ISP is Auto Negotiating....(Please Wait 30s)")
        
        com = self.m_comboBox_serial_port.GetValue()
        baud = int(self.m_comboBox_baud_rate.GetValue())
        if com =='':
            wx.MessageBox("Please Select Serial Port", 'Warning',wx.OK | wx.ICON_ERROR)
            return
        
        self.isp = w7500_isp_cmd.W7500_ISP_CMD(com,baud,self,0.5)
        if( self.isp.negoComP() == -1 ):
            self.isp.__del__()
            wx.MessageBox("Serial Open Error.\r\nPlease check BOOT pin and retry after reset the W7500 board", 'Warning',wx.OK | wx.ICON_ERROR)
            return
        
        #Check Lock Info
        self.checkbox_flockr0_list = [self.m_checkBox_crl,self.m_checkBox_cabwl,self.m_checkBox_drl1,self.m_checkBox_drl0,self.m_checkBox_dwl1,self.m_checkBox_dwl0]

        self.checkbox_flockr1_list  = [self.m_checkBox_cwl31,self.m_checkBox_cwl30,self.m_checkBox_cwl29,self.m_checkBox_cwl28,self.m_checkBox_cwl27,self.m_checkBox_cwl26,self.m_checkBox_cwl25,self.m_checkBox_cwl24]
        self.checkbox_flockr1_list += [self.m_checkBox_cwl23,self.m_checkBox_cwl22,self.m_checkBox_cwl21,self.m_checkBox_cwl20,self.m_checkBox_cwl19,self.m_checkBox_cwl18,self.m_checkBox_cwl17,self.m_checkBox_cwl16]
        self.checkbox_flockr1_list += [self.m_checkBox_cwl15,self.m_checkBox_cwl14,self.m_checkBox_cwl13,self.m_checkBox_cwl12,self.m_checkBox_cwl11,self.m_checkBox_cwl10,self.m_checkBox_cwl9,self.m_checkBox_cwl8]
        self.checkbox_flockr1_list += [self.m_checkBox_cwl7,self.m_checkBox_cwl6,self.m_checkBox_cwl5,self.m_checkBox_cwl4,self.m_checkBox_cwl3,self.m_checkBox_cwl2,self.m_checkBox_cwl1,self.m_checkBox_cwl0]

        self.isp.writeCmd("","3")
        result = self.isp.writeCmd("LOCK READ").split()

        str_flockr1 = result.pop()
        str_flockr0 = result.pop()

        self.bin_flockr1 = hex_to_binary(str_flockr1)
        self.bin_flockr0 = hex_to_binary(str_flockr0)

        for idx in range(len(self.checkbox_flockr1_list)):
            if( (self.bin_flockr1[idx]) == '1') :
                self.checkbox_flockr1_list[idx].SetValue(True)
            else:
                self.checkbox_flockr1_list[idx].SetValue(False)

        for idx in range(len(self.checkbox_flockr0_list)):
            if(idx < 2):
                if( self.bin_flockr0[idx] == '1'):
                    self.checkbox_flockr0_list[idx].SetValue(True)
                else:
                    self.checkbox_flockr0_list[idx].SetValue(False)
            else:
                if( self.bin_flockr0[idx+26] == '1' ):
                    self.checkbox_flockr0_list[idx].SetValue(True)
                else:
                    self.checkbox_flockr0_list[idx].SetValue(False)

        self.m_button_serial_open.Disable()
        self.m_button_serial_close.Enable()
        self.isopen = True
        self.m_statusBar_W7500_Status.SetStatusText("Serial Open Complete")

    
    def onSerialClose( self, event ):
        try:
            self.isp.writeCmd("REST",'8')

            self.isp.__del__()
            self.m_button_serial_open.Enable()
            self.m_button_serial_close.Disable()
            self.isopen = False
        except:
            self.isp.__del__()
            self.m_button_serial_open.Enable()
            self.m_button_serial_close.Disable()
            self.isopen = False

    def onCheckEraseMass( self, event ):
        self.m_checkBox_erase_chip.SetValue(False)
        self.m_checkBox_erase_data0.SetValue(False)
        self.m_checkBox_erase_data1.SetValue(False)

    def onCheckEraseChip( self, event ):
        self.m_checkBox_erase_mass.SetValue(False)

    def onCheckEraseData0(self, event):
        self.m_checkBox_erase_mass.SetValue(False)

    def onCheckEraseData1(self, event):
        self.m_checkBox_erase_mass.SetValue(False)

    def onAllCodeReadLock( self, event ):
        self.m_checkBox_all_code_read_unlock.SetValue(False)
        for idx in range(len(self.checkbox_flockr0_list)):
            self.checkbox_flockr0_list[idx].SetValue(True)
            
    def onAllCodeReadUnlock( self, event ):
        self.m_checkBox_all_code_read_lock.SetValue(False)
        for idx in range(len(self.checkbox_flockr0_list)):
            self.checkbox_flockr0_list[idx].SetValue(False)

    def onCodeReadLock(self, event):
        self.m_checkBox_all_code_read_unlock.SetValue(False)

    def onData1ReadLock(self, event):
        self.m_checkBox_all_code_read_unlock.SetValue(False)

    def onData0ReadLock(self, event):
        self.m_checkBox_all_code_read_unlock.SetValue(False)

    def onData1WriteLock(self, event):
        self.m_checkBox_all_code_read_unlock.SetValue(False)

    def onData0WriteLock(self, event):
        self.m_checkBox_all_code_read_unlock.SetValue(False)

    def onAllCodeWriteLock( self, event ):
        self.m_checkBox_all_code_write_unlock.SetValue(False)
        for idx in range(len(self.checkbox_flockr1_list)):
            self.checkbox_flockr1_list[idx].SetValue(True)
        
    def onAllCodeWriteUnlock( self, event ):
        self.m_checkBox_all_code_write_lock.SetValue(False)
        for idx in range(len(self.checkbox_flockr1_list)):
            self.checkbox_flockr1_list[idx].SetValue(False)
        
    def onBrowse( self, event ):
        filename = ''
        dlg = wx.FileDialog(self, message='Choose a file')
        
        if dlg.ShowModal() == wx.ID_OK:
            #get the new filename from the dialog
            filename = dlg.GetPath()
        dlg.Destroy() #
        
        if filename:
            self.m_textCtrl_File_Path.SetValue(filename)

    def onWriteMainFlash( self, event ):
        self.m_checkBox_WriteDataFlash.SetValue(False)
        self.m_checkBox_WriteMainFlash.SetValue(True)
    
    def onWriteDataFlash( self, event ):
        self.m_checkBox_WriteMainFlash.SetValue(False)
        self.m_checkBox_WriteDataFlash.SetValue(True)

    def doStep2(self):
        if self.isopen != True:
            wx.MessageBox("Serial is not opened", 'Warning',wx.OK | wx.ICON_ERROR)
            return False

        # Step 2
        if self.m_checkBox_erase_mass.IsChecked():
            ret = self.isp.writeCmd("ERAS MASS")
            if ret[0] != '0':
                msg_error = 'ERROR MASS ERASE '
                msg_error += ret
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

        if self.m_checkBox_erase_chip.IsChecked():
            ret = self.isp.writeCmd("ERAS CHIP")
            if ret[0] != '0':
                msg_error = 'ERROR CHIP ERASE '
                msg_error += ret
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

        if self.m_checkBox_erase_data0.IsChecked():
            ret = self.isp.writeCmd("ERAS DAT0")
            if ret[0] != '0':
                msg_error = 'ERROR Data0 ERASE '
                msg_error += ret
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

        if self.m_checkBox_erase_data1.IsChecked():
            ret = self.isp.writeCmd("ERAS DAT1")
            if ret[0] != '0':
                msg_error = 'ERROR Data1 ERASE '
                msg_error += ret
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

        return True

    def doStep3(self):
        bin_flockr0 = list('00000000000000000000000000000000')
        hex_flockr1 = ''
        hex_flockr0 = ''

        if self.isopen != True:
            wx.MessageBox("Serial is not opened", 'Warning', wx.OK | wx.ICON_ERROR)
            return False

        for idx in range(len(self.checkbox_flockr0_list)):
            if(idx < 2):
                if( self.checkbox_flockr0_list[idx].IsChecked() ):
                    bin_flockr0[idx] = '1'
                else:
                    bin_flockr0[idx] = '0'
            else:
                if( self.checkbox_flockr0_list[idx].IsChecked() ):
                    bin_flockr0[idx+26] = '1'
                else:
                    bin_flockr0[idx+26] = '0'

        hex_flockr0 = hex(int("".join(bin_flockr0),2))[2:10]
        hex_flockr1 = hex(int("".join(self.bin_flockr1),2))[2:10]
        cmd = "LOCK PROG" + " " + hex_flockr0.zfill(8) + " " + hex_flockr1.zfill(8)
        resp = self.isp.writeCmd(cmd)
        if( resp[0] != '0'):
            msg_error = "ERROR LOCK PROG : " + resp
            wx.MessageBox(msg_error, 'Warning',wx.OK | wx.ICON_ERROR)
            return False

        self.bin_flockr0 = bin_flockr0
        return True

    def doStep4(self):
        str = ''
        bin_flockr1 = list('00000000000000000000000000000000')
        hex_flockr1 = ''
        hex_flockr0 = ''

        if self.isopen != True:
            wx.MessageBox("Serial is not opened", 'Warning', wx.OK | wx.ICON_ERROR)
            return False

        for idx in range(len(self.checkbox_flockr1_list)):
            if(self.checkbox_flockr1_list[idx].IsChecked()):
                bin_flockr1[idx] = '1'
            else:
                bin_flockr1[idx] = '0'

        hex_flockr0 = hex(int("".join(self.bin_flockr0),2))[2:10]
        hex_flockr1 = hex(int("".join(bin_flockr1),2))[2:10]

        cmd = "LOCK PROG" + " " + hex_flockr0.zfill(8) + " " + hex_flockr1.zfill(8)
        resp = self.isp.writeCmd(cmd)
        if( resp[0] != '0'):
            msg_error = "ERROR LOCK PROG : " + resp
            wx.MessageBox(msg_error, 'Warning',wx.OK | wx.ICON_ERROR)
            return False

        self.bin_flockr1 = bin_flockr1
        return True

    def doStep5(self):
        filename = self.m_textCtrl_File_Path.GetValue()
        if filename == '':
            return False

        if filename.find('.bin') == -1:
            msg_error = "It can use only binary format file.\r\nPlease check your binary file."
            wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
            return False

        self.isp.Xmodem_init()
        if self.m_checkBox_WriteMainFlash.IsChecked():
            if os.stat(filename).st_size > (128 * 1024):
                msg_error = "File size is over."
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

            self.xmodemDialog = wx.ProgressDialog('W7500 Firmware Writing', 'Loading Memory', 1024,
                                                  style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
            self.isp.Xmodem_Send("00000000", "00020000", filename, self.xmodem_callback)
            self.xmodemDialog.Destroy()

            # Verify
            if self.m_checkBox_verify.IsChecked():
                self.FlashDump(os.stat(filename).st_size, 2048)  # FileName will be main_flash.bin
                if self.compareFile(filename, 'main_flash.bin') is False:
                    wx.MessageBox("Fail to verify", 'Warning', wx.OK | wx.ICON_ERROR)
                    return False

            wx.MessageBox("Download Complete(Code Memory)", 'W7500ISP', wx.OK | wx.ICON_INFORMATION)

        elif self.m_checkBox_WriteDataFlash.IsChecked():
            f = open(filename, "rb")
            file_size = os.stat(filename).st_size
            file_size_str = '{:08x}'.format(file_size)

            if file_size > 512:
                f.close()
                msg_error = "File size is over. It can use only 512byte file."
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

            # Write data to SRAM
            command = "DOWN 20000000 " + file_size_str
            self.isp.writeCmd(command, "0", 1, 0)
            for i in range(file_size):
                self.isp.ser.write(f.read())

            resp = self.isp.ser.readline()
            if resp[0] != '0':
                f.close()
                wx.MessageBox("[ERROR] Write to SRAM", 'Warning', wx.OK | wx.ICON_ERROR)
                return False

            # Write to DAT0
            resp = self.isp.writeCmd("PROG DAT0 20000000")
            if resp[0] != '0':
                f.close()
                msg_error = "[ERROR] Write DAT0"
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

            # Write to DAT1
            resp = self.isp.writeCmd("PROG DAT1 20000100")
            if resp[0] != '0':
                f.close()
                msg_error = "[ERROR] Write DAT1"
                wx.MessageBox(msg_error, 'Warning', wx.OK | wx.ICON_ERROR)
                return False

            if self.m_checkBox_verify.IsChecked():
                self.DataDump()
                if self.compareFile(filename, 'data_flash.bin') is False:
                    wx.MessageBox("Fail to verify", 'Warning', wx.OK | wx.ICON_ERROR)
                    return False

            wx.MessageBox("Download complete(DAT0 & DAT1)", 'W7500ISP', wx.OK | wx.ICON_INFORMATION)

        return True

    def onStartStep2(self, event):
        if self.doStep2()== True:
            wx.MessageBox("Step2 is done", 'W7500ISP', wx.OK | wx.ICON_INFORMATION)

    def onStartStep3(self, event):
        if self.doStep3() == True:
            wx.MessageBox("Step3 is done", 'W7500ISP', wx.OK | wx.ICON_INFORMATION)

    def onStartStep4(self, event):
        if self.doStep4() == True:
            wx.MessageBox("Step4 is done", 'W7500ISP', wx.OK | wx.ICON_INFORMATION)

    def onStartStep5(self, event):
        if self.doStep5() == True:
            if self.m_checkBox_Reset.IsChecked():
                self.isp.writeCmd("REMP FLSH")
                self.isp.writeCmd("REST")

                self.isp.__del__()
                self.m_button_serial_open.Enable()
                self.m_button_serial_close.Disable()
                self.isopen = False

    def onStartAllSteps( self, event ):
        if self.doStep2() == False:
            wx.MessageBox("Fail to execute Step2", 'Warning', wx.OK | wx.ICON_ERROR)
            return
        if self.doStep3() == False:
            wx.MessageBox("Fail to execute Step3", 'Warning', wx.OK | wx.ICON_ERROR)
            return
        if self.doStep4() == False:
            wx.MessageBox("Fail to execute Step4", 'Warning', wx.OK | wx.ICON_ERROR)
            return
        if self.doStep5() == False:
            wx.MessageBox("Fail to execute Step5", 'Warning', wx.OK | wx.ICON_ERROR)
            return

        if self.m_checkBox_Reset.IsChecked():
            self.isp.writeCmd("REMP FLSH")
            self.isp.writeCmd("REST")

            self.isp.__del__()
            self.m_button_serial_open.Enable()
            self.m_button_serial_close.Disable()
            self.isopen = False

    def FlashDump(self,total_size, offset_size):
        progressMax = total_size/4 + 1  # (128K / 4) + 1
        filename = 'main_flash.bin'

        command_cnt = total_size / offset_size
        remain_data_size = total_size % offset_size

        address = 0
        offset_hex_str = '{:08x}'.format(offset_size)
        remain_data_size_str = '{:08x}'.format(remain_data_size)

        loopcnt = 0

        progressDialog = wx.ProgressDialog('W7500 Flash Dump', 'Loading Memory', progressMax, style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME| wx.PD_AUTO_HIDE)

        f = open(filename, "wb")
        try:
            for i in range(command_cnt):
                cmd = "DUMP" + " " + '{:08X}'.format(address) + " " + offset_hex_str + "\r"
                #print (cmd)
                self.isp.ser.write(cmd)
                binary = []

                for j in range(offset_size/4):        # Offset_Size / 4byte
                    loopcnt = loopcnt + 1
                    respData = self.isp.ser.readline()
                    #print (respData)

                    if len(respData) != 19:
                        f.close()
                        progressDialog.Destroy()
                        wx.MessageBox("[ERROR:200] Flash Dump ", 'Warning', wx.OK | wx.ICON_ERROR)
                        return
                    else:
                        little_enddian = ""
                        little_enddian = respData[15:17] + respData[13:15] + respData[11:13] + respData[9:11]
                        binary.append(binascii.a2b_hex(little_enddian))

                progressDialog.Update(loopcnt)
                for cnt in range(len(binary)):
                    f.write(binary[cnt])

                respData = self.isp.ser.readline()
                #print(respData)
                if respData[:2] != '0\r':
                    f.close()
                    wx.MessageBox("[ERROR:201] Flash Dump Command Error ", 'Warning', wx.OK | wx.ICON_ERROR)
                    return

                address = address + offset_size

            if remain_data_size is not 0:
                cmd = "DUMP" + " " + '{:08X}'.format(address) + " " + remain_data_size_str + "\r"
                #print (cmd)
                self.isp.ser.write(cmd)
                binary = []

                if ((remain_data_size % 4) == 0):
                    count = (remain_data_size/4)
                else:
                    count = (remain_data_size/4) + 1

                for j in range(count):
                    loopcnt = loopcnt + 1
                    respData = self.isp.ser.readline()
                    #print(respData)

                    if len(respData) != 19:
                        f.close()
                        progressDialog.Destroy()
                        wx.MessageBox("[ERROR:202] Flash Dump ", 'Warning', wx.OK | wx.ICON_ERROR)
                        return
                    else:
                        little_enddian = ""
                        little_enddian = respData[15:17] + respData[13:15] + respData[11:13] + respData[9:11]
                        binary.append(binascii.a2b_hex(little_enddian))

                progressDialog.Update(loopcnt)
                for cnt in range(len(binary)):
                    f.write(binary[cnt])

                respData = self.isp.ser.readline()
                #print (respData)

                if respData[:2] != '0\r':
                    f.close()
                    wx.MessageBox("[ERROR:203] Flash Dump Command Error ", 'Warning', wx.OK | wx.ICON_ERROR)
                    return

            f.close()
            progressDialog.Destroy()

        except ValueError:
            f.close()
            wx.MessageBox("[ERROR:202] Data Flash Dump Error ", 'Warning', wx.OK | wx.ICON_ERROR)
            return

    def DataDump(self):
        progressMax = 128 + 1  # (512B / 4) + 1
        filename = 'data_flash.bin'

        progressDialog = wx.ProgressDialog('W7500 Flash Dump', 'Loading Memory', progressMax,
                                           style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

        cmd = "DUMP 0003FE00 00000200" + "\r"
        # print "Send Command : %s" % cmd
        self.isp.ser.write(cmd)
        f = open(filename, "wb")

        time.sleep(1)
        for i in range(progressMax):
            respData = self.isp.ser.readline()

            little_enddian = ""
            little_enddian = respData[15:17] + respData[13:15] + respData[11:13] + respData[9:11]
            binary = binascii.a2b_hex(little_enddian)

            # binary = binascii.a2b_hex(respData[9:17])
            f.write(binary)
            progressDialog.Update(i)

        f.close()
        progressDialog.Destroy()

    def onFlashDump( self, event ):
        if self.isopen != 1:
            wx.MessageBox("Serial is not open.", 'Warning',wx.OK | wx.ICON_ERROR)
            return

        self.FlashDump(128*1024,2048)

        subprocess.Popen(["tool\wxHexEditor\wxHexEditor-32Bit.exe","main_flash.bin"])

    def onDataDump( self, event ):
        if self.isopen != 1:
            wx.MessageBox("Serial is not open.", 'Warning',wx.OK | wx.ICON_ERROR)
            return

        self.DataDump()
        subprocess.Popen(["tool\wxHexEditor\wxHexEditor-32Bit.exe", "data_flash.bin"])

    def xmodem_callback(self,total_packets, success_count, error_count):
        self.xmodemDialog.Update(success_count)
        
    def GetComPortList(self):
        comboBox_serial_portChoices = []
        self.ports_available = list(serial.tools.list_ports.comports())
        for self.port in self.ports_available:
            if(self.port[2] != 'n/a'):
                comboBox_serial_portChoices.append(self.port[0])
 
        self.m_comboBox_serial_port.SetItems(comboBox_serial_portChoices)


    def compareFile(self,src_file,dst_file):
        with open(src_file) as f1:
            with open(dst_file) as f2:
                if f1.read(1) != f2.read(1):    #1byte
                   return False

        return True

    def onVersion(self, event):
        msg = 'Software Version is ' + SW_VERSION
        wx.MessageBox(msg, 'W7500ISP', wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App(0)
    w7500_isp = W7500_ISP(None)
    app.SetTopWindow(w7500_isp)
    w7500_isp.Show()
    app.MainLoop()
    