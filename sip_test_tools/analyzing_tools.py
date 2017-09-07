#!/usr/bin/env python
# -*- coding:utf-8 -*-

class AnalyzingTools:
    # パケットの配列、Dictを引数
    @staticmethod
    def getFinalResponse(packets):
        finalResponse=None
        for packet in packets:
            if 'status-code' in packet and 'cseq_method' in packet:
                statuscode=packet["status-code"]
                cseqmethod=packet["cseq_method"]
                if cseqmethod == 'INVITE':
                    finalResponse=statuscode
        return finalResponse


