#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pysipp
import pyshark
import time
import timeout_decorator
import multiprocessing 
import unittest

class Test_Sample(unittest.TestCase):
    def cap(self,queue,output):
        caps = pyshark.LiveCapture(interface='6',bpf_filter='ip and udp')
        queue.put(caps) 
        #proc.value=caps
        for packet in caps.sniff_continuously(packet_count=15):
            ############################################################
            ### SIPメッセージの取り出し
            ############################################################
            msg_fields=packet.layers[-1]._all_fields
            if 'sip.Request-Line' in msg_fields:
                output.value=output.value+msg_fields['sip.Request-Line']+'\n'
            else:
                output.value=output.value+msg_fields['sip.Status-Line']+'\n'
            output.value=output.value+msg_fields['sip.msg_hdr'].replace('\\xd\\xa','\r\n')
            
            output.value=output.value+'\n'
            msg_fields=None
            ############################################################
            output.value=output.value+'------------------------------------\n'

    def test_sample1(self):
        manager=multiprocessing.Manager()
        queue=multiprocessing.Queue()
        ret=manager.Value('s','')
        #proc=manager.Value('s',None)
        myth=multiprocessing.Process(target=self.cap,args=(queue,ret,))
        myth.start()
        time.sleep(0.2)
        uas = pysipp.server(srcaddr=('192.168.1.9', 5060))
        uac = pysipp.client(destaddr=uas.srcaddr)
        
        # run server async
        uas(block=False) # returns a `pysipp.launch.PopenRunner` instance by default
        uac()            # run client synchronously
        time.sleep(2)
        #myth.terminate()
        myth.join()
        find=ret.value.find('183 Session Progress')
        print queue.get()
        self.assertNotEqual(find,-1)

if __name__ == "__main__":
    unittest.main()


