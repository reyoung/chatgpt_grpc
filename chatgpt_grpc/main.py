import logging
import os
import time
from concurrent import futures
import grpc

from chatgpt_grpc.protocol_pb2_grpc import ChatGPTServiceServicer, add_ChatGPTServiceServicer_to_server
from chatgpt_grpc.protocol_pb2 import ChatResponse
from chatgpt.chatgpt import Conversation

logging.basicConfig(
    filename="./log.out",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Servicer(ChatGPTServiceServicer):
    def Chat(self, request_iterator, context):
        conversation = Conversation(email=os.getenv("OPENAI_EMAIL", None), password=os.getenv("OPENAI_PASSWORD", None),
                                    access_token=os.getenv("OPENAI_TOKEN", None))
        c_id = f"{id(conversation)}_{time.time()}"
        logger.info(f"create conversion, id=({c_id})")
        for req in request_iterator:
            logger.info(f'send text, text="{req.text}", c_id="{c_id}"')
            try:
                result = conversation.chat(req.text)
            except:
                import traceback as tb
                logger.error(f'error, {tb.format_exc()}, c_id="{c_id}')
                yield ChatResponse(error=tb.format_exc())
            else:
                logger.info(f'recv text, text={result}')
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
