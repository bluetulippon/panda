#!/usr/bin/env python3
import os
import time
import threading
from typing import Any, List

from panda import Panda

JUNGLE = "JUNGLE" in os.environ
if JUNGLE:
  from panda_jungle import PandaJungle

# The TX buffers on pandas is 0x100 in length.
NUM_MESSAGES_PER_BUS = 10000

def flood_tx(panda):
  print('Sending!')
  msg = b"\xaa" * 4
  packet = [[0xaa, None, msg, 0], [0xaa, None, msg, 1], [0xaa, None, msg, 2]] * NUM_MESSAGES_PER_BUS
  panda.can_send_many(packet)
  print(f"Done sending {3*NUM_MESSAGES_PER_BUS} messages!")

if __name__ == "__main__":
  serials = Panda.list()
  if JUNGLE:
    sender = Panda()
    receiver = PandaJungle()
  else:
    if len(serials) != 2:
      raise Exception("Connect two pandas to perform this test!")
    sender = Panda(serials[0])
    receiver = Panda(serials[1])
    receiver.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  sender.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
  sender.set_heartbeat_disabled()

  # Start transmisson
  threading.Thread(target=flood_tx, args=(sender,)).start()

  # Receive as much as we can in a few second time period
  rx: List[Any] = []
  old_len = 0
  start_time = time.time()
  while time.time() - start_time < 3 or len(rx) > old_len:
    old_len = len(rx)
    rx.extend(receiver.can_recv())
  print(f"Received {len(rx)} messages")
