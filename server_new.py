import argparse
import socket
import cv2 as cv
import pickle as pi
import struct as st

def server(host,port):
	Soc_Server = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
	Soc_Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print('HOST IP:',host)

	Add_soc = (host,port)

	Soc_Server.bind(Add_soc)

	Soc_Server.listen()
	print("LISTENING AT:",Add_soc)

	while True:
		soc_client,addr = Soc_Server.accept()
		print('CONNECTED TO:',addr)
		if soc_client:
			Feed = cv.VideoCapture(0)

			while(Feed.isOpened()):
				img,fr = Feed.read()
				fr = cv.resize(fr, None, fx = 0.5, fy = 0.5, interpolation = cv.INTER_AREA)
				a = pi.dumps(fr)
				message = st.pack("Q",len(a))+a
				soc_client.sendall(message)

				cv.imshow('WEBCAM FEED SENDING',fr)
				key = cv.waitKey(1) & 0xFF
				if key ==ord('q'):
					soc_client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' MP-TCP protocol sharing')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=6000,
                        help='TCP port (default 6000)')
    args = parser.parse_args()
    server(args.host, args.p)
