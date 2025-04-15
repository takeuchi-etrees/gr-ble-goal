import zmq
import pmt

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:3333")
socket.connect("tcp://127.0.0.1:3334")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

prev_time = 0
prev_mac_seq = 0
prev_in_range_seq = 0

while True:
    msg = socket.recv()
    pdu = pmt.deserialize_str(msg)
    pdu_metadata = pmt.car(pdu)
    pdu_data = pmt.cdr(pdu)
    
    if pmt.is_dict(pdu_metadata):
        metadata = pmt.to_python(pdu_metadata)
        if len(metadata) != 1:
            del metadata["packet_len"]

#            print(metadata)

            if "MAC" in metadata:
                v = metadata["MAC"]
                v = v.split("@")
                cur_mac_seq = int(v[2])
                if cur_mac_seq > prev_mac_seq:
                    prev_mac_seq = cur_mac_seq

                    cur_time = int(v[1])
                    print("MAC", v)
                    print(cur_time - prev_time)
#                    print((cur_time - prev_time) % 1000)
                    prev_time = cur_time

            if "in_range" in metadata:
                v = metadata["in_range"]
                v = v.split("@")
                cur_in_range_seq = int(v[2])
                if cur_in_range_seq > prev_in_range_seq:
                    prev_in_range_seq = cur_in_range_seq

                    cur_time = int(v[1])
                    print("in_range", v)
#                    print(cur_time - prev_time)
                    prev_time = cur_time
