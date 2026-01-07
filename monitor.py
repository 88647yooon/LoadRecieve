import psutil

class monitor:
    def ger_system_status():
        cpu_usage = psutil.cpu_percent(interval = 0.1)
        memory = psutil.virtual_memory()
        memory_usage = memory.percent

        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv

        return {
            "cpu": cpu_usage,
            "memory": memory_usage,
            "net_sent": bytes_sent,
            "net_recv": bytes_recv
        }
    
    def get_status_string():
        status = monitor.get_system_status()

        return f"CPU:{status['cpu']}%|MEM:{status['memory']}%"
    
   
    if __name__ == "__main__":
    # 단독 실행 시 현재 상태를 출력 (테스트용)
     print("현재 서버 상태 모니터링:")
     print(monitor.get_status_string())