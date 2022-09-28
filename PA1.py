"""
# 2019314891 김재현 PA1
# MFQ scheduling simulation

# 구현
Ready Queue : Q0, Q1, Q2
Q0 : Time quantum 2, RR scheduling
Q1 : Time quantum 4, RR scheduling
Q2 : SRTN scheduling

input.txt에서 1 line 단위로 입력, 공백 기준으로 구분
1st line: number of Processes
other line: <PID, ArrivalTime, InitQueue, #Cycles, Sequence of burst cycles(CPU burst, IO burst)>
"""

from collections import deque


class Process:
    def __init__(self, pid, arrival_time, init_queue, cycles, sequence):
        self.__pid = pid
        self.__arrival_time = arrival_time
        self.__init_queue = init_queue
        self.__cycles = cycles
        self.sequence = sequence
        self.current_queue = init_queue
        self.turnaround_time = 0
        self.waiting_time = 0
        self.starting_time = 0  # cpu 처음 할당 받을 때 시간
        self.completion_time = 0  # 모든 cpu burst 마친 뒤 시간 (completion_time - arrival time = Turnarround Time)
        self.cpu_burst = True  # cpu burst 시간 내에 있으면 True, IO burst 시간 내에 있으면 False
        self.in_cpu = False
        self.remaining_cpu_burst = 0
        self.remaining_io_burst = 0
        self.timeslice = 0

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, pid):
        if pid < 0:
            raise ValueError("Invalid value")
        self.__pid = pid

    @property
    def arrival_time(self):
        return self.__arrival_time

    @arrival_time.setter
    def arrival_time(self, arrival_time):
        if arrival_time < 0:
            raise ValueError("Invalid value")
        self.__arrival_time = arrival_time

    @property
    def init_queue(self):
        return self.__init_queue

    @init_queue.setter
    def init_queue(self, init_queue):
        if init_queue < 0:
            raise ValueError("Invalid value")
        self.__init_queue = init_queue

    @property
    def cycles(self):
        return self.__cycles

    @cycles.setter
    def cycles(self, cycles):
        if cycles < 0:
            raise ValueError("Invalid value")
        self.__cycles = cycles

    def print_process(self):
        print("Process PID: " + self.__pid)
        print("Arrival Time: " + self.__arrival_time)
        print("Init Queue: " + self.__init_queue)
        print("Current Queue: " + self.current_queue)
        print("# of Cycles: " + self.__cycles)
        print("Sequences: ", end='')
        print(self.sequence)
        print("")


def split_process_info(process_info_line):
    process_info_line = process_info_line.split(maxsplit=4)
    return process_info_line


def mfq(process_list):
    """
    MFQ scheduling function
    time 값이 1 증가할 때 : RQ에 진입할(다시 진입 포함) Process 확인, 현재 Process 나가야 되는지 확인, 끝나면 completion time 기록

    :param process_list: input.txt로부터 추출한 전체 Process 인스턴스 리스트
    :return: None
    """
    q0 = deque([])  # ready queue 0
    q1 = deque([])  # ready queue 1
    q2 = deque([])  # ready queue 2

    # process의 init_queue값에 맞게 ready queue에 삽입
    def insert_rq(process):
        if process.init_queue == 0:
            process.timeslice = 2
            q0.appendleft(process)
        elif process.init_queue == 1:
            process.timeslice = 4
            q1.appendleft(process)
        else:
            q2.appendleft(process)


    time = 0  # 반복문 돌며 1씩 증가: cpu 시간을 표현
    current_process = None  # 현재 cpu를 할당받고 있는 Process
    current_queue = 0  # 현재 몇번째 ready queue에서 Process를 실행하는지

    while True:
        for process in process_list:  # ready queue에 대한 처리 : queue 최초 진입, preemption, wakeup
            if process.arrival_time == time:  # 최초 ready queue 진입 Process
                insert_rq(process)
            if current_process.timeslice = 0: # 이 이후 preemption 구현




try:
    input_file = open("./input.txt", "rt")
    file_text = input_file.readlines()
except FileNotFoundError:
    print("There is no input.txt")
finally:
    input_file.close()

number_of_processes = int(file_text[0][0])  # txt 파일의 첫번째 줄(프로세스의 개수) 저장
process_info = []  # Process 객체에 저장하기 전 txt 파일의 프로세스 정보 구분해 저장
process_list = []  # Process 객체들 저장

# process_info에 프로세스의 수 만큼 프로세스 정보 저장
for i in range(1, number_of_processes + 1):
    process_info.append(split_process_info(file_text[i]))

# process_list에 프로세스 객체 저장
for i in range(0, number_of_processes):
    process_list.append(Process(process_info[i][0], process_info[i][1],
                                process_info[i][2], process_info[i][3],
                                process_info[i][4]))

# Process 객체의 sequence 뭉쳐 있는 문자열 숫자 단위로 쪼개기
for i in range(0, len(process_list)):
    process_list[i].sequence = process_list[i].sequence.split()

mfq(process_list)