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


class Process:
    def __init__(self, pid, arrival_time, init_queue, cycles, sequence):
        self.__pid = pid
        self.__arrival_time = arrival_time
        self.__init_queue = init_queue
        self.__cycles = cycles
        self.sequence = sequence

    @property
    def pid(self):
        return self.pid

    @pid.setter
    def pid(self, pid):
        if pid < 0:
            raise ValueError("Invalid value")
        self.pid = pid

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


def split_process_info(process_info_line):
    process_info_line = process_info_line.split(maxsplit=4)
    return process_info_line


try:
    input_file = open("./input.txt", "rt")
    file_text = input_file.readlines()
except FileNotFoundError:
    print("There is no input.txt !")
finally:
    input_file.close()

number_of_processes = int(file_text[0][0])  # txt 파일의 첫번째 줄(프로세스의 개수) 저장
process_info = []  # Process 객체에 저장하기 전 txt 파일의 프로세스 정보 구분해 저장
process_list = []  # Process 객체들 저장

# process_info에 프로세스의 수 만큼 프로세스 정보 저장
for i in range(1, number_of_processes + 1):
    process_info.append(split_process_info(file_text[i]))
print(process_info)

# process_list에 프로세스 객체 저장
for i in range(0, number_of_processes):
    process_list.append(Process(process_info[i][0], process_info[i][1],
                                process_info[i][2], process_info[i][3],
                                process_info[i][4]))
