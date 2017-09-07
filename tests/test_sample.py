#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sip_test_tools.basictest import *
from sip_test_tools.analyzing_tools import *
import unittest

class Test_Sample(unittest.TestCase):
    def test_sample1(self):
        result=BasicTest(
                    uas_scean=['/root/scenarios/rcv-default.xml'],
                    uac_info_file=['/root/rcv-info.csv']       ,
                    uac_scean=['/root/scenarios/snd-default.xml'],
                    timeout=15
                ).run_test_case()

        for packet in result:
            print packet["timestamp"],
            print packet["src"],
            print packet["dst"],
            print packet["first_line"]

        self.assertEqual(AnalyzingTools.getFinalResponse(result),'200')
        print '--------------------'

    def test_sample2(self):

        result=BasicTest(
                    uas_scean=['/root/scenarios/rcv-default.error.xml'],
                    uas_ip=['127.0.0.1'],
                    uas_port=[5060],
                    uas_info_file=[None]             ,
                    uac_info_file=['/root/rcv-info.csv']             ,
                    uac_scean=['/root/scenarios/snd-default.xml']      ,
                    timeout=5
                ).run_test_case()

        for packet in result:
            print packet["timestamp"],
            print packet["src"],
            print packet["dst"],
            print packet["first_line"]

        self.assertEqual(AnalyzingTools.getFinalResponse(result),'200')
        print '--------------------'

if __name__ == "__main__":
    unittest.main()

