import argparse
import socket
import cv2 as comp_vision
import struct as st
import pickle as pi


def client(host,port):
	soc_client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
	soc_client.connect((host,port))
	info_byte = b""
	capacity = struct.calcsize("Q")
	while True:
		while len(info_byte) < capacity:
			packet = soc_client.recv(4*1024)
			if not packet: break
			info_byte+=packet
		size_packet = info_byte[:capacity]
		info_byte = info_byte[capacity:]
		msg_size = struct.unpack("Q",size_packet)[0]

		while len(info_byte) < msg_size:
			info_byte += soc_client.recv(4*1024)
		info_frame = info_byte[:msg_size]
		info_byte  = info_byte[msg_size:]
		frame = pi.loads(info_frame)
		comp_vision.imshow("RECEIVING VIDEO",frame)
		key = comp_vision.waitKey(1) & 0xFF
		if key  == ord('q'):
			break
	soc_client.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MPTCP protocol transfer')
    parser.add_argument('host', help='interface the server listens at;'' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=6000,help='TCP port (default 6000)')
    args = parser.parse_args()
    client(args.host, args.p)
