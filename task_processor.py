import socket
import time
import json
from monitor import monitor  #
from config import PORT      #

def start_worker():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(100)
    
    print(f"reciever 통합 서버 대기 중 - 포트: {PORT}")

    count = 0
    start_test_time = time.time()

    while True:
        # [중요] accept는 바깥 루프에서 한 번만!
        client_socket, addr = server_socket.accept()
        print(f"sender 접속됨: {addr}")
        
        try:
            # 맥북이 보낸 패킷 끝의 '\n'을 인식하기 위해 makefile 사용
            f = client_socket.makefile('r', encoding='utf-8')
            
            while True:
                line = f.readline()
                if not line: # 맥북이 연결을 끊으면 안쪽 루프 탈출
                    break
                
                count += 1
                
                # 100개 단위로 상태 출력
                if count % 100 == 0:
                    status = monitor.get_status_string() #
                    elapsed = time.time() - start_test_time
                    print(f"{count}개 처리 중... 소요시간: {elapsed:.2f}s | {status}")

        except Exception as e:
            print(f"전송 오류 발생: {e}")
        finally:
            # 맥북이 통신을 완전히 끝냈을 때만 소켓을 닫음
            client_socket.close()
            print(f"sender 연결 종료. 다음 연결 대기...")

if __name__ == "__main__":
    start_worker()