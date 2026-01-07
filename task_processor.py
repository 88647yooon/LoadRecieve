import socket
import time
# psutil 설치 필요: pip install psutil
import psutil 

PORT = 5000
BUFFER_SIZE = 10240  # 10KB 패킷을 한 번에 받기 위해 설정

def start_overloaded_worker():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(100) # 대기 큐 크기
    
    print(f"[*] 서버 시작 (10KB 패킷 수신 대기 중...)")
    
    count = 0
    start_test_time = time.time()

    while True:
        try:
            client_socket, addr = server_socket.accept()
            # 1. 데이터 수신 (10KB)
            data = client_socket.recv(BUFFER_SIZE)
            
            # 2. 아주 기본적인 처리 (문자열 변환)만 수행
            _ = data.decode('utf-8', errors='ignore')
            
            count += 1
            
            # 1000개 단위로 현재 상태 출력
            if count % 1000 == 0:
                elapsed = time.time() - start_test_time
                cpu = psutil.cpu_percent()
                print(f"[!] {count}개 처리 중... 소요시간: {elapsed:.2f}s | CPU: {cpu}%")
                # 여기서 소요시간이 1초를 훌쩍 넘긴다면 이미 '지연'이 발생하고 있는 것임

            # 3. 짧은 응답 전송 후 즉시 닫기
            client_socket.send(b"ACK")
            client_socket.close()

        except Exception as e:
            print(f"에러 발생: {e}")
            break

if __name__ == "__main__":
    start_overloaded_worker()