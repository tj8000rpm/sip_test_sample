#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pysipp
import pyshark
import time
import timeout_decorator
import multiprocessing 
import threading
import unittest
import trollius as asyncio

class Test_Sample(unittest.TestCase):
    #@timeout_decorator.timeout(seconds=3)
    caps = None
    def cap(self,queue,output):
        self.caps = pyshark.LiveCapture(interface='6',bpf_filter='ip and udp')
        #proc.value=caps
        for packet in self.caps.sniff_continuously(packet_count=15):
            ############################################################
            ### SIPメッセージの取り出し
            ############################################################
            msg_fields=packet.layers[-1]._all_fields
            if 'sip.Request-Line' in msg_fields:
                output=output+str(msg_fields['sip.Request-Line'])+'\n'
            else:
                output=output+str(msg_fields['sip.Status-Line'])+'\n'
            output=output+str(msg_fields['sip.msg_hdr']).replace('\\xd\\xa','\r\n')
            
            output=output+'\n'
            msg_fields=None
            ############################################################
            output=output+'------------------------------------\n'

    def test_sample1(self):
        queue=None
        ret=''
        myth=threading.Thread(target=self.cap,args=(queue,ret,))
        myth.start()
        time.sleep(0.2)
        uas = pysipp.server(srcaddr=('192.168.1.9', 5060))
        uac = pysipp.client(destaddr=uas.srcaddr)
        
        # run server async
        uas(block=False) # returns a `pysipp.launch.PopenRunner` instance by default
        uac()            # run client synchronously
        time.sleep(2)
        #myth.terminate()
        #myth.join()
        print self.caps.eventloop
        self.caps.eventloop=None
        print self.caps.eventloop

        #myth.join()
        find=ret.value.find('183 Session Progress')
        self.assertNotEqual(find,-1)

if __name__ == "__main__":
    unittest.main()


