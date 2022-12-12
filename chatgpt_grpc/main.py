import logging
import os
import time
from concurrent import futures
import grpc

from chatgpt_grpc.protocol_pb2_grpc import ChatGPTServiceServicer, add_ChatGPTServiceServicer_to_server
from chatgpt_grpc.protocol_pb2 import ChatResponse,ChatStreamResponse
from revChatGPT.revChatGPT import Chatbot

logging.basicConfig(
    filename="./log.out",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

email = os.getenv("OPENAI_EMAIL", None)
password = os.getenv("OPENAI_PASSWORD", None)
access_token = os.getenv("OPENAI_TOKEN", None)
timeout = int(os.getenv("OPENAI_TIMEOUT", "120"))
cf_clearance = os.getenv('OPENAI_CF_CLEARANCE', None)
user_agent = os.getenv('OPENAI_USER_AGENT', None)


def create_chatbot() -> Chatbot:
    config = dict()
    if email is not None:
        raise RuntimeError("email currently is not support")
    if access_token is not None:
        config["session_token"] = access_token

    if cf_clearance is not None:
        config['cf_clearance'] = cf_clearance
        config['user_agent'] = user_agent
    else:
        raise RuntimeError("cf_clearance/user_agent must set")


    return Chatbot(config)


class Servicer(ChatGPTServiceServicer):
    def Chat(self, request_iterator, context):
        chatbot = create_chatbot()
        c_id = f"{id(chatbot)}_{time.time()}"
        logger.info(f"create conversion, id=({c_id})")
        for req in request_iterator:
            logger.info(f'send text, text="{req.text}", c_id="{c_id}"')
            try:
                result = chatbot.get_chat_response(req.text)["message"]
            except:
                import traceback as tb
                logger.error(f'error, {tb.format_exc()}, c_id="{c_id}')
                yield ChatResponse(error=tb.format_exc())
            else:
                logger.info(f'recv text, text={result}')
                yield ChatResponse(text=result)

    def StreamChat(self, request_iterator, context):
        chatbot = create_chatbot()
        c_id = f"{id(chatbot)}_{time.time()}"
        logger.info(f"create convsersion, id=({c_id})")
        for req in request_iterator:
            logger.info(f'send text, text="{req.text}", c_id="{c_id}"')
            try:
                for msg in chatbot.get_chat_response(req.text, output="stream"):
                    yield ChatStreamResponse(text=msg["message"])

                logger.info(f'get msg, msg={msg["message"]}, parent id="{chatbot.parent_id}", c_id="{c_id}"')
                yield ChatStreamResponse(end_of_stream=True)
            except:
                import traceback as tb
                logger.error(f'error, {tb.format_exc()}, c_id="{c_id}')
                yield ChatStreamResponse(error=tb.format_exc())


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ChatGPTServiceServicer_to_server(
        Servicer(), server)
    server.add_insecure_port(f'[::]:{os.getenv("PORT", 9000)}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
