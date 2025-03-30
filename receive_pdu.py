import zmq
import pmt

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:3333")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    msg = socket.recv()
    pdu = pmt.deserialize_str(msg)
    metadata = pmt.car(pdu)
    data = pmt.cdr(pdu)
    
    if pmt.is_dict(metadata):
        print("Metadata:", pmt.to_python(metadata))
