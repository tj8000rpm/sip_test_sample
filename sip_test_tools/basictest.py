#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pysipp
from capture import *
from trollius.executor import TimeoutError

class BasicTest:
    uas_scean     = None
    uas_ip        = None
    uas_port      = None
    uas_info_file = None

    uac_scean     = None
    uac_ip        = None
    uac_port      = None
    uac_info_file = None
    uac_dest_port = None
    uac_dest_ip   = None

    timeout=30
    capture_interface='lo'

    def __init__(  self,
                   timeout=30,
                   capture_interface='lo',
                   uas_scean=[None]      ,  uac_scean=[None]          ,
                   uas_ip=['127.0.0.1']  ,  uac_ip=['127.0.0.1']      ,
                   uas_port=[5060]       ,  uac_port=[5061]           ,
                   uas_info_file=[None]  ,  uac_info_file=[None]      ,
                                            uac_dest_ip=['127.0.0.1'] ,
                                            uac_dest_port=[5060] 
                ):

        if max(len(uas_scean),len(uas_ip),len(uas_port),len(uas_info_file)) != min(len(uas_scean),len(uas_ip),len(uas_port),len(uas_info_file)):
            raise AttributeError
        if max(
                len(uac_scean),len(uac_ip),len(uac_port),len(uac_info_file)
                ) != min(
                len(uac_scean),len(uac_ip),len(uac_port),len(uac_info_file),len(uac_dest_ip),len(uac_dest_port)
                ):

            raise AttributeError
        self.uas_scean=uas_scean
        self.uas_ip=uas_ip
        self.uas_port=uas_port
        self.uas_info_file=uas_info_file

        self.uac_scean=uac_scean
        self.uac_ip=uac_ip
        self.uac_port=uac_port
        self.uac_info_file=uac_info_file
        self.uac_dest_ip  =uac_dest_ip
        self.uac_dest_port=uac_dest_port

        self.timeout=timeout
        self.capture_interface=capture_interface


    def run_test_case(self):
        test_thread=CaptureThread(self.timeout,self.capture_interface)
        test_thread.start()
        uass=[]
        uacs=[]
        finalizes=[]

        for idx in range(len(self.uas_ip)):
            uas = pysipp.server(
                            srcaddr=(self.uas_ip[idx], self.uas_port[idx]),
                            scen_file=self.uas_scean[idx],
                            info_file=self.uas_info_file[idx]
                        )
            uass.append(uas)
        for idx in range(len(self.uac_ip)):
            uac = pysipp.client( 
                            srcaddr=(self.uac_ip[idx], self.uac_port[idx]),
                            destaddr=(self.uac_dest_ip[idx], self.uac_dest_port[idx]),
                            scen_file=self.uac_scean[idx],
                            info_file=self.uac_info_file[idx]
                        )
            uacs.append(uac)

        for uas in uass:
            fin=uas(block=False) # returns a `pysipp.launch.PopenRunner` instance by default
            finalizes.append(fin)
        for uac in uacs:
            fin=uac(block=False) # run client synchronously
            finalizes.append(fin)

        try:
            for join in finalizes:
                join(timeout=self.timeout)
        except Exception:
            pass

        test_thread.close()

        test_thread.join()

        return test_thread.getResult()

