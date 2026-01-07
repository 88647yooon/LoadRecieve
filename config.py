
# 1. 네트워크 통신 설정
PORT = 5000             # 서버들이 공통으로 사용할 포트 번호
BUFFER_SIZE = 1024       # 패킷 수신 버퍼 크기 (1KB)
TIMEOUT = 2.0            # 서버 응답 대기 시간 (초) - 이 시간이 지나면 서버 장애로 판단

# 2. 실험 대상 서버(Worker) 리스트
# 각 기기(비보북, 미니 PC 등)의 고정 IP 주소를 여기에 적습니다.
SERVER_LIST = [
    "192.168.0.53",      # 예: 비보북 IP
    "192.168.0.141",      # 예: 미니 PC IP
    # "192.168.0.25",    # 추가 서버가 있다면 주석을 풀고 IP 입력
]

# 3. 로드밸런싱 알고리즘 설정
# 'ROUND_ROBIN', 'LEAST_CONNECTION' 등 실험하고 싶은 알고리즘 이름을 지정 가능
#CURRENT_ALGORITHM = "ROUND_ROBIN"

# 4. 실험 로깅 관련
#LOG_FILE = "experiment_results.csv"  # 결과가 저장될 파일명