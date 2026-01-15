import socket
import time
import sys
from monitor import monitor
from config import PORT as DEFAULT_PORT # 기본 포트

def start_worker(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR는 소켓 종료 후 포트가 'Wait' 상태일 때 즉시 재사용하게 해줍니다.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(100)
        print(f" [논리 노드 가동] 포트: {port}에서 패킷 대기 중...")
    except Exception as e:
        print(f" 포트 {port} 바인딩 실패: {e}")
        return

    count = 0
    start_test_time = None # 첫 패킷 수신 시점을 기준으로 측정하기 위해 None 설정

    try:
        while True:
            client_socket, addr = server_socket.accept()
            # 첫 연결 시 타이머 시작
            if start_test_time is None:
                start_test_time = time.time()
                
            print(f" Sender 접속됨: {addr} (Node Port: {port})")
            
            try:
                # 데이터 수신 효율을 위해 makefile 사용
                f = client_socket.makefile('r', encoding='utf-8')
                
                while True:
                    line = f.readline()
                    if not line:
                        break
                    
                    count += 1
                    
                    # 100개 단위로 실시간 상태 출력
                    if count % 100 == 0:
                        status = monitor.get_status_string()
                        elapsed = time.time() - start_test_time
                        print(f"[Port {port}] {count}개 처리 중... 소요시간: {elapsed:.2f}s | {status}")

            except Exception as e:
                print(f"전송 오류 발생 (Port {port}): {e}")
            finally:
                client_socket.close()
                print(f"{port}번 노드 연결 종료. 다음 패킷 대기...")

    except KeyboardInterrupt:
        # 실험 종료 시 논문에 넣을 최종 결과 출력
        end_time = time.time()
        elapsed = end_time - start_test_time if start_test_time else 0
        print("\n" + "="*50)
        print(f"[실험 종료 리포트 - Port {port}]")
        print(f"- 최종 수신 패킷: {count} 개")
        print(f"- 총 소요 시간: {elapsed:.2f} 초")
        if elapsed > 0:
            print(f"- 평균 처리 속도: {count/elapsed:.2f} TPS")
        print("="*50)
    finally:
        server_socket.close()

if __name__ == "__main__":
    # 터미널 인자가 있으면 해당 포트 사용, 없으면 config의 기본 포트 사용
    # 실행 예: python task_processor.py 6000
    target_port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    start_worker(target_port)