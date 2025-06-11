import sys
import time
import zmq
import pmt

def main(args):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    for i in range(1, len(args)):
        socket.connect("tcp://127.0.0.1:"+str(args[i]))
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    start_localtime = int(time.mktime(time.localtime()))
    prev_time = 0.0
    count = 0
    time_pool = []

    while True:
        msg = socket.recv()
        pdu = pmt.deserialize_str(msg)
        pdu_metadata = pmt.car(pdu)
        pdu_data = pmt.cdr(pdu)
    
        if pmt.is_dict(pdu_metadata):
            metadata = pmt.to_python(pdu_metadata)
            if metadata == None:
                continue
            if "MAC" in metadata:
                v = metadata["MAC"].split("@")

                if v[0] != 'C8:9D:1B:27:58:7E':
                    pass
                else:
                    mac_address = v[0]
                    cur_time = int(v[1]) / 1000.0

                    if cur_time in time_pool:
                        pass
                    else:
                        if cur_time in time_pool:
                            pass
                        elif cur_time - 0.001 in time_pool:
                            pass
                        elif cur_time + 0.001 in time_pool:
                            pass
                        else:
                            result = []
                            result.append(f'{cur_time:.3f}')
                            result.append("MAC")
                            result.append(mac_address)

                            count += 1

                            print(result, end='')
                            print(' ', end='')
                            cur_localtime = int(time.mktime(time.localtime()))
                            if cur_localtime - start_localtime != 0:
                                print(int(count / (cur_localtime - start_localtime) * 100.0))

                                time_pool.append(cur_time)

                        prev_time = cur_time

if __name__ =='__main__':
    main(sys.argv)
