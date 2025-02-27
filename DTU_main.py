import serial
import time
import threading

class DTUCommunicator:
    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # 等待串口初始化
        self.running = True  # Flag to control the threads

    def read_serial(self):
        while self.running:
            if self.ser.in_waiting > 0:
                received = self.ser.readline().decode('utf-8').strip()
                if received:
                    print(f"[来自DTU] {received}")
            time.sleep(0.1)

    def write_serial(self):
        while self.running:
            user_input = input("输入要发送的消息（或按回车跳过）: ")
            if user_input:
                self.ser.write(f"{user_input}\n".encode('utf-8'))  # 添加换行符
                print(f"已发送: {user_input}")
            time.sleep(0.1)

    def close(self):
        self.running = False
        self.ser.close()

if __name__ == "__main__":
    dtu = DTUCommunicator(port='/dev/ttyUSB0')  # 修改为实际端口
    try:
        # Create threads for reading and writing
        read_thread = threading.Thread(target=dtu.read_serial)
        write_thread = threading.Thread(target=dtu.write_serial)

        # Start the threads
        read_thread.start()
        write_thread.start()

        # Wait for threads to complete
        read_thread.join()
        write_thread.join()
    except KeyboardInterrupt:
        dtu.close()
        print("串口已关闭")