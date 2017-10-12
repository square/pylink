import pylink
import sys
import thread
import time


def read_rtt(jlink):
  try:
    while jlink.connected():
      terminal_bytes = jlink.rtt_read(0, 1024)
      if terminal_bytes:
        sys.stdout.write("".join(map(chr, terminal_bytes)))
        sys.stdout.flush()
      time.sleep(0.1)
  except:
    print("IO read thread exception, exiting...")
    thread.interrupt_main()
    raise


def write_rtt(jlink):
  try:
    while jlink.connected():
      bytes = list(bytearray(raw_input()) + b"\x0A" + b"\x00")
      bytes_written = jlink.rtt_write(0, bytes)
  except:
    print("IO write thread exception, exiting...")
    thread.interrupt_main()
    raise


def main(target_device):
  jlink = pylink.JLink()
  print("connecting to JLink...")
  jlink.open()
  print("connecting to %s..." % target_device)
  jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
  jlink.connect(target_device)
  print("connected, starting RTT...")
  jlink.rtt_start()

  while True:
    try:
      num_up = jlink.rtt_get_num_up_buffers()
      num_down = jlink.rtt_get_num_down_buffers()
      print("RTT started, %d up bufs, %d down bufs." % (num_up, num_down))
      break
    except pylink.errors.JLinkRTTException:
      time.sleep(0.1)
      pass

  try:
    thread.start_new_thread(read_rtt, (jlink,))
    thread.start_new_thread(write_rtt, (jlink,))
    while jlink.connected():
      time.sleep(1)
    print("JLink disconnected, exiting...")
  except KeyboardInterrupt:
    print("ctrl-c detected, exiting...")
    pass

  del jlink


if __name__ == "__main__":
  sys.exit(main(sys.argv[1]))
