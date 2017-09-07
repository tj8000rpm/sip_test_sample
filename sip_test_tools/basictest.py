#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pysipp
from capture import *
from trollius.executor import TimeoutError

# abstract
class SIPAgent(object):
    scen_file  = None
    ip         = None
    port       = None
    info_file  = None

    def __init__(self,ip='127.0.0.1',port=5060,scen_file=None,info_file=None):
        self.ip = ip
        self.port = port
        self.scen_file = scen_file
        self.info_file = info_file

    def __str__(self):
        msg=''
        msg+='src='+self.ip+':'+str(self.port)+', '
        if self.scen_file :
            msg+='scen_file='+self.scen_file+', '
        if self.info_file:
            msg+='info_file='+self.info_file+', '
        return msg

# UAS用設定クラス
class UAServer(SIPAgent):
    pass

# UAC用設定クラス
class UAClient(SIPAgent):
    dest_ip    = None
    dest_port  = None

    def __init__(self,ip='127.0.0.1',port=5061,dest_ip='127.0.0.1',dest_port=5060,scen_file=None,info_file=None):
        self.dest_ip   = dest_ip
        self.dest_port = dest_port
        super(UAClient,self).__init__(ip,port,scen_file,info_file)

    def __str__(self):
        msg=super(UAClient,self).__str__()
        if self.dest_ip:
            msg+='dst='+self.dest_ip+':'+str(self.dest_port)+', '
        return msg



class BasicTest(object):

    uas_array=[]
    uac_array=[]

    timeout=30
    capture_interface='lo'
    capture_filter=None

    def __init__(  self,
                   timeout=30,
                   capture_interface='lo',
                   capture_filter='ip and udp',
                   uas_array=[]          ,
                   uac_array=[]
                ):

        self.timeout=timeout
        self.capture_interface=capture_interface
        self.capture_filter=capture_filter

        self.uas_array=uas_array
        self.uac_array=uac_array


    def run_test_case(self):
        uass=[]
        uacs=[]
        finalizes=[]

        # tharkのパケットキャプチャを設定
        capture=CaptureThread(timeout=self.timeout,capture_interface=self.capture_interface,capture_filter=self.capture_filter)
        # キャプチャ開始
        capture.start()
        
        #設定されたuasを1台ずつ設定し、uassリストに追加
        for agent in self.uas_array:
            uas = pysipp.server(
                            srcaddr=(agent.ip, agent.port ),
                            scen_file=agent.scen_file,
                            info_file=agent.info_file
                        )
            uass.append(uas)
        #設定されたuacを1台ずつ設定し、uacsリストに追加
        for agent in self.uac_array:
            uac = pysipp.client( 
                            srcaddr=(agent.ip, agent.port),
                            destaddr=(agent.dest_ip, agent.dest_port),
                            scen_file=agent.scen_file,
                            info_file=agent.info_file
                        )
            uacs.append(uac)

        # sippを非同期で起動
        # リストから1ユニットずつ起動する
        for uas in uass:
            fin=uas(block=False) # returns a `pysipp.launch.PopenRunner` instance by default
            finalizes.append(fin)
        for uac in uacs:
            fin=uac(block=False) # run client synchronously
            finalizes.append(fin)

        # 非同期で起動したsippがすべて終わるのを待つ
        # timeoutで満了した場合も含めて処理
        try:
            for join in finalizes:
                join(timeout=self.timeout)
        except Exception:
            pass

        # sippが終了したらキャプチャ停止
        capture.close()
        capture.join()

        # キャプチャ結果を出力して終了
        return capture.getResult()

