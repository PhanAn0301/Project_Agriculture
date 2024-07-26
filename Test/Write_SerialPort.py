import serial
import json
from datetime import datetime

# Mở cổng serial
ser = serial.Serial('COM6', 9600)

# Mở file CSV để ghi dữ liệu
with open('output.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Ghi tiêu đề nếu file còn trống
    csvfile.seek(0)
    if csvfile.read(1) == '':
        csvwriter.writerow(['Timestamp', 'Data'])
    
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            
            # Parse JSON data
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                continue  # Skip invalid JSON data

            # Thêm thời gian vào JSON data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            json_data['time'] = timestamp

            # Chuyển đổi JSON data thành chuỗi và ghi vào file CSV
            data_with_time = json.dumps(json_data)
            csvwriter.writerow([timestamp, data_with_time])
            csvfile.flush()  
            print(f"{timestamp} - {data_with_time}")
