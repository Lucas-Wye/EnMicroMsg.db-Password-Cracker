# 1. install openssl dev package:
#    $ sudo apt-get install libssl-dev

# 2. compile password_cracker.c:
#    $ gcc password_cracker.c  -l crypto -o password_cracker.o

# 3. modify following parameters in this file and then run.

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--db', help='the path of EnMicroMsg.db', default='EnMicroMsg.db')
parser.add_argument('--passwd', help='the path of output file `pass.txt`', default='pass.txt')
parser.add_argument('--num_of_process', help='the num of process used', default=4)
parser.add_argument('--pass_start', help='the start of password', default=0x0000000)
parser.add_argument('--pass_end', help='the end of password', default=0xfffffff)
parser.add_argument('--pass_truck_size', help='the truck size of password', default=4000)
parser.add_argument('--bin_path', help='the path of password_cracker.o', default='bin/password_cracker.o')
args = parser.parse_args()

db_file_name = args.db
pass_file_name = args.passwd
process_no = args.num_of_process

pass_start = args.pass_start
pass_end =   args.pass_end
pass_truck_size = args.pass_truck_size

# ====================================


import threading
import time, os
import Queue, subprocess

pass_seg = Queue.Queue()
bin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.bin_path)

class workerThread(threading.Thread):
    def __init__(self, threadID, name, pass_seg_):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pass_seg = pass_seg_

    def run(self):
        print('Thread %d started...' % (self.threadID))
        while not pass_seg.empty():
            sn_start, sn_end = self.pass_seg.get()
            if sn_start is None:
                break
            print(subprocess.check_output([bin_path, db_file_name,
                                           pass_file_name,
                                          hex(sn_start), hex(sn_end)]))


if os.path.exists(pass_file_name):
    print('Pls delete %s and then try again.' % (pass_file_name))
    exit(0)

if not os.path.exists(bin_path):
    print('Code has NOT been complied. Pls complie it first.')
    exit(0)

while pass_start<= pass_end:
    pass_seg.put((pass_start,min(pass_start+pass_truck_size-1, pass_end)))
    pass_start += pass_truck_size

thread_pool =[]
for i in range(process_no):
    thread_pool.append(workerThread(i, 'Worker %d' % i, pass_seg))

[x.start() for x  in thread_pool]

[x.join() for x in thread_pool]

print("Exiting Main Thread")
