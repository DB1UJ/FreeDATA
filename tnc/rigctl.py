#!/usr/bin/env python3
# Intially created by Franco Spinelli, IW2DHW, 01/2022
# Updated by DJ2LS
#
#
# versione mia di rig.py per gestire Ft897D tramite rigctl e senza
# fare alcun riferimento alla configurazione
#
# e' una pezza clamorosa ma serve per poter provare on-air il modem
#
import subprocess
import structlog
import time
import sys
import os
# for rig_model -> rig_number only

# set global hamlib version
hamlib_version = 0
               
class radio:
    """ """
    def __init__(self):
    
        self.devicename = ''
        self.devicenumber = ''
        self.deviceport = ''
        self.serialspeed = ''
        self.hamlib_ptt_type = ''
        self.my_rig = ''
        self.pttport = ''
        self.data_bits = ''
        self.stop_bits = ''
        self.handshake = ''
 
    def open_rig(self, devicename, deviceport, hamlib_ptt_type, serialspeed, pttport, data_bits, stop_bits, handshake, rigctld_ip, rigctld_port):    
        """

        Args:
          devicename: 
          deviceport: 
          hamlib_ptt_type: 
          serialspeed: 
          pttport: 
          data_bits: 
          stop_bits: 
          handshake: 
          rigctld_ip: 
          rigctld_port: 

        Returns:

        """
        
        self.devicename = devicename
        self.deviceport = deviceport
        self.serialspeed = str(serialspeed) # we need to ensure this is a str, otherwise set_conf functions are crashing
        self.hamlib_ptt_type = hamlib_ptt_type
        self.pttport = pttport
        self.data_bits = data_bits
        self.stop_bits = stop_bits
        self.handshake = handshake
 
 
         # check if we are running in a pyinstaller environment
        try:
            app_path = sys._MEIPASS
        except:
            app_path = os.path.abspath(".")
        sys.path.append(app_path)            
        
        # get devicenumber by looking for deviceobject in Hamlib module
        try:
            import Hamlib
            self.devicenumber = int(getattr(Hamlib, self.devicename))
        except:
            if int(self.devicename):
                self.devicenumber = int(self.devicename)
            else:
                self.devicenumber = 6 #dummy
                structlog.get_logger("structlog").warning("[RIGCTL] RADIO NOT FOUND USING DUMMY!", error=e)   
        
        # set deviceport to dummy port, if we selected dummy model
        if self.devicenumber == 1 or self.devicenumber == 6:
            self.deviceport = '/dev/ttyUSB0'
            
        print(self.devicenumber, self.deviceport, self.serialspeed)




        # select precompiled executable for win32/win64 rigctl
        # this is really a hack...somewhen we need a native hamlib integration for windows
        if sys.platform == 'win32' or sys.platform == 'win64':
            self.cmd = app_path + 'lib\\hamlib\\'+sys.platform+'\\rigctl -m %d -r %s -s %d ' % (int(self.devicenumber), self.deviceport, int(self.serialspeed))
 
        else:
            self.cmd = 'rigctl -m %d -r %s -s %d ' % (int(self.devicenumber), self.deviceport, int(self.serialspeed))

        # eseguo semplicemente rigctl con il solo comando T 1 o T 0 per
        # il set e t per il get        

        # set ptt to false if ptt is stuck for some reason
        self.set_ptt(False)
        return True
            
    def get_frequency(self):
        """ """
        cmd = self.cmd + ' f'
        sw_proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        time.sleep(0.5)
        freq = sw_proc.communicate()[0]
        #print('get_frequency', freq, sw_proc.communicate())
        try:
            return int(freq)
        except:
            return False

        
    def get_mode(self):
        """ """
        #(hamlib_mode, bandwith) = self.my_rig.get_mode()
        #return Hamlib.rig_strrmode(hamlib_mode)
        try:
            return 'PKTUSB'
        except:
            return False

    
    def get_bandwith(self):
        """ """
        #(hamlib_mode, bandwith) = self.my_rig.get_mode()
        bandwith = 2700

        try:
            return bandwith
        except:
            return False

    def set_mode(self, mode):
        """

        Args:
          mode: 

        Returns:

        """
        # non usata
        return 0
      
    def get_ptt(self):
        """ """
        cmd = self.cmd + ' t'
        sw_proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)  
        time.sleep(0.5)
        status = sw_proc.communicate()[0]

        try:
            return status
        except:
            return False
                  
    def set_ptt(self, state):
        """

        Args:
          state: 

        Returns:

        """
        cmd = self.cmd + ' T '
        print('set_ptt', state)
        if state:
            cmd = cmd + '1'
        else:
            cmd = cmd + '0'
        print('set_ptt', cmd)

        sw_proc = subprocess.Popen(cmd, shell=True, text=True)  
        try:
            return state
        except:
            return False
        
    def close_rig(self):
        """ """
        #self.my_rig.close()
        return
