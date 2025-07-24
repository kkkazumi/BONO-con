import socket
from abc import ABCMeta, abstractmethod
import datetime
from logging import getLogger

from config import *
ROBOT_PC_IP = 'xxx.xxx.xxx.xxx' #get_ip()
# ロガーの作成
bono_logger = getLogger('main').getChild('bono')

import asyncio

from bleak import BleakScanner

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == "BONO06_NEW":
            #bono_logger.info("Bono address: {} {} {}".fomrat(d.address,d.name,d.rssi))
            return d.address
    bono_logger.error("Failed to find BONO06_NEW. Please check robot power is on")

def connection():
    try:
        bono_s=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

        loop = asyncio.get_event_loop()
        bono_add=loop.run_until_complete(run())

        bono_s.connect((bono_add,4))
        bono_s.send(bytes([244, 226, 166, 0, 0, 255]))
    except Exception as e:
        bono_logger.error('Failed to connect Bono. Due to some Bluetooth error {}'.format(e))
    else:
        bono_logger.info('Success to connect with Bono')
        return bono_s

class RobotOperation(metaclass=ABCMeta):
    @abstractmethod
    def send(self, msg):
        pass
    @abstractmethod
    def close(self):
        pass
class DummyBono(RobotOperation):
  def __init__(self):
    pass
  def send(self,msg):
    #print(msg)
    if(msg == "on"):
        bono_logger.info('Send on msg to Bono')
    elif(msg == "off"):
        bono_logger.info('Send off msg to Bono')
    else:
        bono_logger.warning('Unexpected msg has received {}'.format(msg))
  def close(self):
      bono_logger.info('Send close msg to Bono')


class bono(RobotOperation):
  def __init__(self):
    connection()
  def send(self,msg):
    print(msg)
    if(msg == "on"):
      self.s.send(b'on')
      bono_logger.info('Send on msg to Bono')
    elif(msg == "off"):
      self.s.send(b'off')
      bono_logger.info('Send off to Bono')
  def close(self):
    """
    ソケット通信に直接書き込むよりもセーフティに処理するため
    メソッドの処理として隠ぺい
    """
    self.s.close() 

class bono_new(RobotOperation):
    def __init__(self):
        self.s=connection()
        self.t_before=datetime.datetime.now()
        #self.last_msg_sent_at = self.t_before
    def send(self,msg):
        #print(msg)
        bono_logger.info('Send msg {} to Bono'.format(msg))
        if(msg == "on"):
            self.s.send(bytes([244,226,166,0,0,255]))
        elif(msg == "off"):
            #bono_logger.info('Send msg {} to Bono'.format(msg))
            dt=datetime.datetime.now()-self.t_before
            if(dt.total_seconds()>1.5):
                self.s.send(bytes([244,227,179,0,0,0]))
                bono_logger.info('Send msg {} to Bono'.format(msg))
                self.t_before=datetime.datetime.now()
        else:
            bono_logger.warning('Unexpected msg received'.format(msg))
    def close(self):
        pass

if __name__ == "__main__":
  #start()
  b = bono()
  while(True):
    print("input msg")
    msg=input()
    b.send(msg)
