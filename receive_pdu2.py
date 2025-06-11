import zmq
import pmt
import curses
import sys
import datetime
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:3333")
socket.connect("tcp://127.0.0.1:3334")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

def main(stdscr):
    delta = datetime.timedelta(hours=9)
    jst = datetime.timezone(delta, 'JST')
    now = datetime.datetime.now(jst)
    data_name = now.strftime('%Y_%m%d_%H%M%S')
    
    prev_time = 0
    prev_mac_seq = 0
    prev_in_range_seq = 0
    data = []

    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(14, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    stdscr.clear()
    stdscr.nodelay(True)
    
    while True:
        c = stdscr.getch()
        if c == ord('w'):
            with open(data_name + '.json', 'w') as file:
                json.dump(data, file, indent=2)
        elif c == ord('q'):
            sys.exit()
        
        msg = socket.recv()
        pdu = pmt.deserialize_str(msg)
        pdu_metadata = pmt.car(pdu)
        pdu_data = pmt.cdr(pdu)
        
        if pmt.is_dict(pdu_metadata):
            metadata = pmt.to_python(pdu_metadata)
            if metadata == None:
                continue
            if len(metadata) != 1:
                del metadata["packet_len"]

                if "MAC" in metadata:
                    result = []
                    
                    v = metadata["MAC"]
                    v = v.split("@")
                    cur_mac_seq = int(v[2])
                    v[2] = cur_mac_seq
                    
                    if cur_mac_seq > prev_mac_seq:
                        prev_mac_seq = cur_mac_seq

                        cur_time = int(v[1]) / 1000.0
                        v[1] = cur_time
                        
                        result.append(v[1])
                        result.append("MAC")
                        result.append(v[0])
                        data.append(result)

                        data = sorted(data, key=lambda x: (x[0], -ord(x[1][0])))

                        print_data(stdscr, data)
                        
                        prev_time = cur_time

                if "in_range" in metadata:
                    result = []
    
                    v = metadata["in_range"]
                    v = v.split("@")
                    cur_in_range_seq = int(v[2])
                    v[2] = cur_in_range_seq
                    if cur_in_range_seq > prev_in_range_seq:
                        prev_in_range_seq = cur_in_range_seq

                        cur_time = int(v[1]) / 1000.0
                        v[1] = cur_time
                                
                        result.append(v[1])
                        result.append("in_range")
                        result.append(v[0])
                        data.append(result)
                        data = sorted(data, key=lambda x: (x[0], -ord(x[1][0])))

                        print_data(stdscr, data)

                        prev_time = cur_time



def print_data(stdscr, data):
    height, width = stdscr.getmaxyx()
    stdscr.clear()
    for y in range(0, height):
        i = len(data) - height + y
        if i >= 0:
            if data[i][1] == 'MAC' and len(data[i]) == 3:
                if data[i - 1][1] == 'MAC':
                    data[i].append('None')
                else:
                    if (data[i - 1][1] == 'in_range') and (data[i][0] - data[i - 1][0] <= 0.002):
                        data[i].append(data[i - 1][2])
                    else:
                        data[i].append('None')
            elif data[i][1] == 'MAC':
                if data[i - 1][1] == 'MAC':
                    data[i][3] = 'None'
                else:
                    if (data[i - 1][1] == 'in_range') and (data[i][0] - data[i - 1][0] <= 0.002):
                        data[i][3] = data[i - 1][2]
                

            if (data[i][1] == 'MAC') and (len(data[i][2]) == 17):
                if data[i][2] == 'E2:FE:71:37:E2:EE':
                    stdscr.addstr(y, 0, str(data[i]), curses.color_pair(9))
                elif data[i][2] == 'C8:9D:1B:27:58:7E':
                    stdscr.addstr(y, 0, str(data[i]), curses.color_pair(13))
                elif data[i][2] == 'CD:C5:0E:2E:C9:58':
                    stdscr.addstr(y, 0, str(data[i]), curses.color_pair(12))
                else:
                    stdscr.addstr(y, 0, str(data[i]), curses.color_pair(7))
            else:
                stdscr.addstr(y, 0, str(data[i]), curses.color_pair(7))
    stdscr.refresh()
        
            
curses.wrapper(main)
