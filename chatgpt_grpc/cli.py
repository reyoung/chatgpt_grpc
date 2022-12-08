from chatgpt_grpc.protocol_pb2_grpc import ChatGPTServiceStub
from chatgpt_grpc.protocol_pb2 import ChatRequest
import grpc
import sys


def stdin_iterator():
    for line in sys.stdin:
        yield ChatRequest(text=line.strip())


def main():
    channel = grpc.insecure_channel(sys.argv[1])
    stub = ChatGPTServiceStub(channel)

    for rsp in stub.Chat(stdin_iterator()):
        if len(rsp.error) != 0:
            print(rsp.error, file=sys.stderr)
        else:
            print(rsp.text, file=sys.stdout)


if __name__ == '__main__':
    main()
