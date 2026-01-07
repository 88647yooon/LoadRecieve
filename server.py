import socket
import time
import psutil  # CPU 상태 확인용
from config import PORT, BUFFER_SIZE

def start_worker():
    # 소켓 설정 (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT)) # 모든 인터페이스에서 접속 허용
    server_socket.listen(5)
    
    print(f"[*] Worker 서버가 {PORT}번 포트에서 대기 중입니다...")

    while True:
        client_socket, addr = server_socket.accept()
        # 1. 데이터 수신
        data = client_socket.recv(BUFFER_SIZE).decode()
        
        if data:
            # 2. 부하 시뮬레이션 (예: 간단한 계산이나 sleep)
            # 실험 신뢰성을 위해 "일하는 시간"을 의도적으로 부여
            start_proc = time.perf_counter()
            time.sleep(0.1) # 0.1초 동안 작업 처리 중임을 가정
            
            # 3. 현재 서버 상태 측정
            cpu_usage = psutil.cpu_percent()
            end_proc = time.perf_counter()
            
            # 4. 응답 전송 (처리 완료 신호 + 현재 상태)
            response = f"SUCCESS|CPU:{cpu_usage}%|TIME:{end_proc-start_proc:.4f}"
            client_socket.send(response.encode())
            
        client_socket.close()

if __name__ == "__main__":
    start_worker()