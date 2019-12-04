from virtual_serial import UART
from interface import BLE_interface
from bluepy.btle import BTLEDisconnectError
import logging, sys

logging.basicConfig(
    format='%(asctime)s.%(msecs)d | %(levelname)s | %(filename)s: %(message)s', 
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

addr_str = '20:91:48:4c:4c:54'
write_uid = '1000ffe1-0000-1000-8000-00805f9b34fb'

if __name__ == '__main__':
    try:
        uart = UART()
        bt = BLE_interface(addr_str, write_uid)
        bt.set_receiver(uart.write_sync)
        uart.set_receiver(bt.send)
        # bt.printDevInfo()
        logging.info('Running main loop!')
        uart.start()
        while True:
            bt.receive_loop()
    except (BTLEDisconnectError, KeyboardInterrupt):
        logging.warning('Shutdown initiated')
        uart.stop()
        bt.shutdown()
        logging.info('Shutdown complete.')
        exit(0)
    except:
        logging.error(f'Unexpected error: {sys.exc_info()}')