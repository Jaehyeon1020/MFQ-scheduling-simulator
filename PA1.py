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
        self.__pid = int(pid)
        self.__arrival_time = int(arrival_time)
        self.__init_queue = int(init_queue)
        self.__cycles = int(cycles)
        self.sequence = sequence
        self.current_queue = int(init_queue)
        self.turnaround_time = 0  # completion time - arrival time
        self.waiting_time = 0  # queue에 있는 총 시간
        self.starting_time = 0  # cpu 처음 할당 받을 때 시간
        self.completion_time = 0  # 모든 burst 마친 뒤 시간
        self.remaining_cpu_burst = 0
        self.remaining_io_burst = 0
        self.timeslice = 0
        self.process_status = 0  # process 생성 안됐으면 0, ready queue에 있으면 1, cpu-burst중이면 2, io-burst 중이면 3, 종료했으면 -1
        self.current_cycle = 1  # 현재 몇 번째 cycle을 진행중인지 기록 -> 새로운 cpu burst 시작할때마다 +1
        self.is_been_cpu = False  # cpu에 올라간 적이 있으면 True, 없으면 False

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
        print("Process PID: %d" % self.__pid)
        print("Arrival Time: %d" % self.__arrival_time)
        print("Init Queue: %d" % self.__init_queue)
        print("Current Queue: %d" % self.current_queue)
        print("# of Cycles: %d" % self.__cycles)
        print("Sequences: ", end='')
        print(self.sequence)

    def print_process_tt_wt(self):
        print("- Process %d" % self.pid)
        print("  PID: %d" % self.pid)
        print("  Turnaround Time: %d" % self.turnaround_time)
        print("  Wating Time: %d" % self.waiting_time)
        print("--------------------")  # - 20개


def split_process_info(process_info_line):
    process_info_line = process_info_line.split(maxsplit=4)
    return process_info_line


def mfq(process_list):
    # print("mfq(): function start")
    scheduling_result = []  # 스케줄링 순서 저장
    ready_queue_0 = deque([])  # ready queue 0
    ready_queue_1 = deque([])  # ready queue 1
    ready_queue_2 = deque([])  # ready queue 2

    time: int = 0  # 반복문 돌며 1씩 증가: cpu 시간을 표현
    current_process: Process = None  # 현재 cpu를 할당받고 있는 Process
    current_queue: int = 0  # 현재 몇번째 ready queue에서 Process를 실행하는지, fetch 하며 업데이트

    def first_insert_rq(process: Process):
        # process의 init_queue값에 맞게 ready queue에 삽입, in-queue status로 전환
        # 처음 들어올때 cycle 1의 cpu burst, IO burst 값 부여 해야함
        # print("called first_insert_rq")  # test

        if process.init_queue == 0:
            process.timeslice = 2  # timeslice 부여
            process.process_status = 1  # 프로세스 상태 in-queue로 전환
            process.remaining_cpu_burst = int(process.sequence[0])  # first cpu burst set
            process.remaining_io_burst = int(process.sequence[1])  # first io burst set
            ready_queue_0.appendleft(process)  # 큐 진입
        elif process.init_queue == 1:
            process.timeslice = 4
            process.process_status = 1
            process.remaining_cpu_burst = int(process.sequence[0])
            process.remaining_io_burst = int(process.sequence[1])
            ready_queue_1.appendleft(process)
        else:
            process.process_status = 1
            process.remaining_cpu_burst = int(process.sequence[0])
            process.remaining_io_burst = int(process.sequence[1])
            ready_queue_2.appendleft(process)

    def wakeup(process: Process):
        # process가 원래 있었던 큐로 돌려보내줌, timeslice 새로 세팅, in-queue status로 전환
        # I\O가 끝났다는 것은 1 cycle이 끝났다는 뜻 -> cycle 증가
        # wakeup 할때마다 cycle이 끝나므로 새로운 cycle의 cpu burst, IO burst값 부여해야함
        # print("called wakeup")  # test

        if process.current_queue == 0:
            process.timeslice = 2  # timeslice set
            process.process_status = 1  # process status set
            process.current_cycle += 1  # current cycle ++
            # print("wakeup : current cycle ++") # test
            # print("current cycle : %d" % process.current_cycle)  # test
            process.remaining_cpu_burst = int(process.sequence[(process.current_cycle-1)*2])  # new cpu burst time set
            if process.current_cycle != process.cycles:  # 마지막 사이클인경우는 io burst는 설정 안함
                process.remaining_io_burst = int(process.sequence[(process.current_cycle-1)*2 + 1])  # new io burst time set
            ready_queue_0.appendleft(process)  # insert process to queue

        elif process.current_queue == 1:
            process.timeslice = 4
            process.process_status = 1
            process.current_cycle += 1
            # print("wakeup : current cycle ++")  # test
            process.remaining_cpu_burst = int(process.sequence[(process.current_cycle - 1) * 2])  # new cpu burst time set
            if process.current_cycle != process.cycles:  # 마지막 사이클인경우는 io burst는 설정 안함
                process.remaining_io_burst = int(
                    process.sequence[(process.current_cycle - 1) * 2 + 1])  # io burst time set
            ready_queue_1.appendleft(process)

        else:
            process.process_status = 1
            process.current_cycle += 1
            # print("wakeup : current cycle ++")  # test
            process.remaining_cpu_burst = int(process.sequence[(process.current_cycle - 1) * 2])  # new cpu burst time set
            if process.current_cycle != process.cycles:  # 마지막 사이클인경우는 io burst는 설정 안함
                process.remaining_io_burst = int(
                    process.sequence[(process.current_cycle - 1) * 2 + 1])  # io burst time set
            ready_queue_2.appendleft(process)

    def shortest_remaining():
        # Q2의 SRNT 스케줄링을 위한 함수
        # Q2에서 가장 남은 cpu burst time이 짧은 프로세스를 반환
        # print("called shortest_remaining")  # test

        shortest = ready_queue_2[0]
        for i in range(1, len(ready_queue_2)):
            if ready_queue_2[i].remaining_cpu_burst < shortest.remaining_cpu_burst:
                shortest = ready_queue_2[i]
        return shortest

    def fetch():
        # process fetch, in-cpu status로 전환
        # print("called fetch")  # test

        nonlocal current_queue
        nonlocal current_process

        if len(ready_queue_0) > 0:
            # print("fetch() : if len(ready_queue_0) > 0")  # test
            if current_queue == 2 and current_process is not None:  # q2 process가 돌고있는 경우
                preemption(current_process)  # q2 프로세스 내보냄

            current_queue = 0  # 현재 큐를 q0로
            current_process = ready_queue_0.pop()  # q0의 프로세스를 cpu에 올림
            current_process.process_status = 2  # 올려진 프로세스의 status : in-cpu
            scheduling_result.append(current_process)

            if current_process.is_been_cpu is False:  # cpu에 한번도 올라간 적이 없으면
                current_process.starting_time = time  # starting time 기록
                current_process.is_been_cpu = True

        elif len(ready_queue_1) > 0:
            # print("fetch() : elif len(ready_queue_1) > 0")  # test
            if current_queue == 2 and current_process is not None: # q2 process가 돌고있는 경우
                preemption(current_process)  # q2 프로세스 내보냄

            current_queue = 1
            current_process = ready_queue_1.pop()
            current_process.process_status = 2
            scheduling_result.append(current_process)

            if current_process.is_been_cpu is False:  # cpu에 한번도 올라간 적이 없으면
                current_process.starting_time = time  # starting time 기록
                current_process.is_been_cpu = True

        elif len(ready_queue_2) > 0:  # SRTN 스케줄링 처리와 이미 current process = None이 된 경우 구분해서 구현
            # print("fetch() : elif len(ready_queue_2) > 0")  # test
            current_queue = 2
            shortest = shortest_remaining()  # 남은 cpu burst time 가장 적은 process 계산

            if current_process is None:  # 이미 current process = None이 된 경우(이미 preemption or sleep된 경우)
                current_process = shortest
                current_process.process_status = 2
                scheduling_result.append(current_process)
                ready_queue_2.remove(shortest)

                if current_process.is_been_cpu is False:  # cpu에 한번도 올라간 적이 없으면
                    current_process.starting_time = time  # starting time 기록
                    current_process.is_been_cpu = True

            elif current_process.remaining_cpu_burst > shortest.remaining_cpu_burst:
                # 현재 cpu에 올라가있는 프로세스가 더 cpu 시간 많이남았으면 교체(SRTN)
                preemption(current_process)
                current_process = shortest
                current_process.process_status = 2
                scheduling_result.append(current_process)
                ready_queue_2.remove(shortest)

                if current_process.is_been_cpu is False:  # cpu에 한번도 올라간 적이 없으면
                    current_process.starting_time = time  # starting time 기록
                    current_process.is_been_cpu = True

    def insert_queue(pc: Process):
        # 인자로 받은 pc를 큐에 저장, in-queue status로 전환, timeslice 새로 부여
        # print("called insert_queue")  # test

        if pc.current_queue == 0:
            pc.process_status = 1
            pc.timeslice = 2
            ready_queue_0.appendleft(pc)
        elif pc.current_queue == 1:
            pc.process_status = 1
            pc.timeslice = 4
            ready_queue_1.appendleft(pc)
        else:
            pc.process_status = 1
            ready_queue_2.appendleft(pc)

    def preemption(pc: Process):
        # process 상태를 in-queue로 바꾸고 한단계 낮은 큐로 진입시킴
        # print("called preemption")  # test
        # print("preempted :", end='')  # test
        # print(pc)  # test

        pc.process_status = 1
        if pc.current_queue != 2:
            pc.current_queue += 1
        insert_queue(pc)

    def check_all_over():
        # print("called check_all_over")  # test
        all_over = True

        for pc in process_list:
            if pc.process_status != -1:  # 끝나지 않은 프로세스가 있다면 all_over->False로
                all_over = False

        if all_over is True:
            # print("check_all_over(): all processes over")  # test
            return True
        else:
            return False

    def print_result():
        for i in range(0, len(scheduling_result)):
            scheduling_result[i] = scheduling_result[i].pid

        print("<Scheduling Result>\n: The following list shows the order of CPU allocation of processes")
        print(scheduling_result)
        print("")
        print("<Turnaround Time & Waiting Time for each processes>")
        for pc in process_list:
            pc.print_process_tt_wt()

        avg_turnaround_time: float = 0.0
        avg_waiting_time: float = 0.0

        for pc in process_list:
            avg_turnaround_time += pc.turnaround_time
            avg_waiting_time += pc.waiting_time

        avg_turnaround_time = avg_turnaround_time / len(process_list)
        avg_waiting_time = avg_waiting_time / len(process_list)

        print("")
        print("<Average Turnaround Time & Average Waiting Time for whole processes>")
        print("- Average Turnaround Time: %f" % avg_turnaround_time)
        print("- Average Waiting Time: %f" % avg_waiting_time)

    if time == 0:  # while loop 들어가기 전에 time=0에 도착하는 첫 번째 process cpu에 올려줌
        for pc in process_list:
            if pc.arrival_time == 0:  # arrival time이 0인 process를
                current_process = pc  # cpu에 바로 올림
                current_queue = current_process.init_queue  # 현재 실행중 큐를 이 프로세스의 시작 큐로
                current_process.starting_time = 0  # 최초로 cpu에 올라간 시간 time=0
                current_process.process_status = 2
                current_process.remaining_cpu_burst = int(current_process.sequence[0])  # first cpu burst set
                current_process.remaining_io_burst = int(current_process.sequence[1])  # first io burst set
                current_process.is_been_cpu = True
                scheduling_result.append(current_process)  # 스케줄링 결과에 기록

                if current_queue == 0:
                    current_process.timeslice = 2
                elif current_queue == 1:
                    current_process.timeslice = 4
                break

    while True:
        """
        while loop 1회 돌 때 일어나야 하는 일:
        ** 맨 처음 프로세스 일단 넣어줘야됨
        ** 시작할 때 모든 프로세스 종료되었는지 확인
            <timer 증감 처리>
            - 현재 IO burst 중인 process들의 remaining IO burst time -- (0보다 클 때)
            - 현재 cpu burst 중인 process들의 remaining cpu burst time -- (0보다 클 때)
            - 현재 cpu에 올려져있는 process가 q0/q1에서 왔다면 timeslice -- (0보다 클 때)
            - 현재 queue 내부에 존재하는 process들의 wating time ++
              ** ready queue 들어올때 sequence에서 cpu, io burst time 세팅 하고 들어올 것
            <preemption & fetch>
            - arrival time 된 process의 rq 진입, IO burst time 0 된 process의 rq 진입(wakeup)
            - 현재 cpu 점유중인 process가 나와야 하는지 확인
              -- cpu burst time 확인해서 0이면 -> 현재 cycle이 마지막 cycle이면 끝, 마지막 아니면 IO burst 상태로 전환
              -- q0,q1에서 스케줄링 중이면 -> time slice == 0인지 확인
                --- 0이면 preemption
              -- q2에서 스케줄링 중이면 -> srtn 적용(fetch 함수에서 접근)
            - 위의 결과로 cpu가 비었다면 새로 fetch
            - time ++
        """
        # print("----------enter while------------")  # test
        # print("time : %d" % time)  # test
        # print(current_process)  # test

        if check_all_over():  # 모든 프로세스가 종료되었다면 mfq 함수 종료(return 1)
            break

        if current_process is not None:  # 현재 프로세스가 있을 때만 실행
            if current_process.current_queue == 0 or current_process.current_queue == 1:  # 현재 cpu 점유 프로세스가 q0/q1에서 왔다면
                # print("timeslice check")  # test
                if current_process.timeslice > 0:  # timeslice 1 이상 남았는지 확인해서
                    # print("timeslice --")  # test
                    current_process.timeslice -= 1  # 남았으면 -1

        # 모든 프로세스에 대해 각 time마다 확인
        for process in process_list:
            # print("for process in process_list 진입")  # test
            # 현재 IO burst 중인 프로세스의 IO burst time --(0보다 클 때)
            if process.process_status == 3 and process.remaining_io_burst > 0:
                # print("io burst --")  # test
                process.remaining_io_burst -= 1
            # 현재 cpu burst 중인 프로세스의 cpu burst time --(0보다 클 때)
            if process.process_status == 2 and process.remaining_cpu_burst > 0:
                # print("cpu burst --")  # test
                process.remaining_cpu_burst -= 1

            # arrival time 된 프로세스 rq 진입
            if process.arrival_time == time and time > 0:
                first_insert_rq(process)
            # IO burst 끝난 프로세스 rq 진입
            if process.process_status == 3 and process.remaining_io_burst == 0:
                wakeup(process)
            # 이 프로세스가 현재 cpu 점유중이라면
            if process is current_process:
                # print("this process is current_process")  # test
                if process.remaining_cpu_burst == 0:  # cpu burst time = 0이면
                    # print("and remaining cpu burst == 0")  # test
                    if process.current_cycle == process.cycles:  # 현재 마지막 cycle이었다면 종료상태로 전환
                        # print("and at last cycle")  # test
                        # print("Process completed")  # test
                        process.process_status = -1
                        process.completion_time = time  # 종료상태 전환 후 completion time 기록
                        current_process = None  # 현재 프로세스 지우기
                        # print("current process setted None")  # test
                    else:  # 마지막 cycle 아니었다면 IO burst 상태로 전환
                        # print("and not at last cycle")  # test
                        # print("converted to IO burst status")  # test
                        process.process_status = 3
                        current_process = None  # 현재 프로세스 지우기
                        # print("current process setted None")  # test
                else:  # cpu burst time 0 아니면
                    # print("and remaining cpu burst != 0")  # test
                    if process.current_queue == 0 or process.current_queue == 1:  # 이 process가 q0 또는 q1에서 왔는지 확인
                        # print("and this process is from q0 or q1")  # test
                        if process.timeslice == 0:  # q0/q1에서 왔으면 timeslice가 0이 됐는지 확인
                            # print("and remaining timeslice 0")  # test
                            preemption(process)  # timeslice 0이라면 preemption
                            current_process = None  # 현재 프로세스 지우기
                            # print("current process setted None")  # test
            # print("for process in process_list 끝")  # test

        if (current_process is None) or (current_process.current_queue == 2):
            # 위 for 문의 결과로 cpu에서 preemption 또는 sleep으로 전환되어 cpu가 비었을 때 또는 q2에서 온 프로세스가 돌고있을 때
            # print("if current process is None or current process.current queue == 2")  # test
            fetch()  # 새로운 프로세스 cpu에 올림(q2의 경우 상위 큐에 프로세스가 들어왔거나 같은 큐에 더 시간 짧은 프로세스가 있을 때 바뀜)

        # 현재 ready queue 내에 존재하는 프로세스의 wating time ++
        for in_rq_process in ready_queue_0:
            in_rq_process.waiting_time += 1
        for in_rq_process in ready_queue_1:
            in_rq_process.waiting_time += 1
        for in_rq_process in ready_queue_2:
            in_rq_process.waiting_time += 1

        time += 1  # time 1 증가, while loop 끝
        # print("----------while END------------")  # test

    for pc in process_list:
        pc.turnaround_time = pc.completion_time - pc.arrival_time
        # print("turnaround time: %d" % pc.turnaround_time)  # test
    print_result()
    # print("mfq(): function over")  # test
    return 1


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

for pc in process_list:
    for i in range(0, len(pc.sequence)):
        pc.sequence[i] = int(pc.sequence[i])

"""for pc in process_list:
    pc.print_process()  # test
    print("")"""

# print("----------------main-----------------\n")  # test
mfq(process_list)
