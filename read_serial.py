import serial
import sys
import time

try:
    # Open serial port
    ser = serial.Serial('COM4', 115200, timeout=0.1)
    print("Listening on COM4 for 20 seconds...")
    
    start_time = time.time()
    while time.time() - start_time < 20:
        if ser.in_waiting:
            try:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                if line:
                    print(line)
            except Exception as e:
                print(f"Read error: {e}")
        time.sleep(0.01)
        
    ser.close()
    print("Finished listening.")
    
except Exception as e:
    print(f"Error opening serial port: {e}")
