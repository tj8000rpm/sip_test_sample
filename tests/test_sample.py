#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sip_test_tools.basictest import *
from sip_test_tools.analyzing_tools import *
import unittest

class Test_Sample(unittest.TestCase):
    def test_sample1(self):
        uas=[UAServer(ip='127.0.0.1',port=5060,scen_file='/root/scenarios/rcv-default.xml')]
        uac=[UAClient(ip='127.0.0.1',port=5061,dest_ip='127.0.0.1',dest_port=5060,scen_file='/root/scenarios/snd-default.xml',info_file='/root/rcv-info.csv')]
        result=BasicTest( uas_array=uas, uac_array=uac, timeout=20, capture_filter='sip').run_test_case()

        self.assertEqual(AnalyzingTools.getFinalResponse(result),'200')

    def test_sample2(self):
        uas=[]
        uas.append(UAServer(scen_file='/root/scenarios/rcv-default.error.xml',ip='127.0.0.1',port=5060))
        uac=[]
        uac.append(UAClient(scen_file='/root/scenarios/snd-default.xml',ip='127.0.0.1',port=5061,dest_ip='127.0.0.1',dest_port=5060,info_file='/root/rcv-info.csv'))

        result=BasicTest(uas_array=uas, uac_array=uac, timeout=20, capture_filter='sip').run_test_case()

        #for packet in result:
        #    print packet["timestamp"],
        #    print packet["src"],
        #    print packet["dst"],
        #    print packet["first_line"]

        self.assertEqual(AnalyzingTools.getFinalResponse(result),'200')

if __name__ == "__main__":
    unittest.main()

