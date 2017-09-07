#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pyshark
import threading

class CaptureThread(threading.Thread):
    output=None
    timeout=30
    capture_interface='lo'
    caps=None
    def __init__(self,timeout=30,capture_interface='lo'):
        threading.Thread.__init__(self)
        self.timeout=timeout
        self.capture_interface=capture_interface

    def run(self):
        self.caps=None
        output=None
        try:
            self.caps = pyshark.LiveCapture(interface=self.capture_interface,bpf_filter='ip and udp')
            self.caps.sniff(timeout=self.timeout)
            output=[]
            for packet in self.caps._packets:
                ############################################################
                ### パケット受信時刻の取得
                ############################################################
                msg_fields=packet.layers[0]._all_fields
                timestamp=packet.sniff_time
                msg_fields=None
                ############################################################
                ############################################################
                ### IPヘッダの取り出し
                ############################################################
                msg_fields=packet.layers[-3]._all_fields
                ip_dst=msg_fields["ip.dst"]
                ip_src=msg_fields["ip.src"]
                msg_fields=None
                ############################################################
                ############################################################
                ### UDPヘッダの取り出し
                ############################################################
                msg_fields=packet.layers[-2]._all_fields
                udp_dst=msg_fields["udp.dstport"]
                udp_src=msg_fields["udp.srcport"]
                msg_fields=None
                ############################################################
                ############################################################
                ### SIPメッセージの取り出し
                ############################################################
                sip_first_line=""
                udp_body_str=""
                statuscode=None
                method=None
                cseqMethod=None
                msg_fields=packet.layers[-1]._all_fields
                if 'sip.Request-Line' in msg_fields:
                    udp_body_str=udp_body_str+str(msg_fields['sip.Request-Line'])+'\n'
                    method=msg_fields["sip.Method"]
                else:
                    udp_body_str=udp_body_str+str(msg_fields['sip.Status-Line'])+'\n'
                    statuscode=msg_fields["sip.Status-Code"]
                if 'sip.CSeq.method' in msg_fields:
                    cseqMethod=msg_fields["sip.CSeq.method"]

                sip_first_line=udp_body_str.strip()
                udp_body_str=udp_body_str+str(msg_fields['sip.msg_hdr']).replace('\\xd\\xa','\r\n')

                udp_body_str=udp_body_str
                msg_fields=None
                ############################################################

                message={}
                message["timestamp"]=timestamp
                message["src"]=ip_src+":"+udp_src
                message["dst"]=ip_dst+":"+udp_dst
                message["first_line"]=sip_first_line
                message["raw_text"]=udp_body_str
                if method != None:
                    message["method"]=method
                else:
                    message["status-code"]=statuscode
                if cseqMethod != None:
                    message["cseq_method"]=cseqMethod
                output.append(message)
        finally:
            self.output=output
            if self.caps != None:
                self.caps.close()
    def close(self):
        pass
        if self.caps != None:
            self.caps.close()

    def getResult(self):
        return self.output

