import os
from concurrent import futures
import grpc

from chatgpt_grpc.protocol_pb2_grpc import ChatGPTServiceServicer, add_ChatGPTServiceServicer_to_server
from chatgpt_grpc.protocol_pb2 import ChatResponse
from chatgpt.chatgpt import Conversation


class Servicer(ChatGPTServiceServicer):
    def Chat(self, request_iterator, context):
        conversation = Conversation(email=os.getenv("OPENAI_EMAIL"), password=os.getenv("OPENAI_PASSWORD"))
        for req in request_iterator:
            try:
                result = conversation.chat(req.text)
            except Exception as e:
                yield ChatResponse(error=str(e))
            else:
                yield ChatResponse(text=result)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ChatGPTServiceServicer_to_server(
        Servicer(), server)
    server.add_insecure_port(f'[::]:{os.getenv("PORT", 9000)}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
