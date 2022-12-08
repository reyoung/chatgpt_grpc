FROM python
COPY . /workspace
RUN pip install --no-cache tls_client && pip install --no-cache git+https://github.com/reyoung/chatgpt-python.git
RUN cd /workspace && pip install --no-cache . && cd / && rm -rf /workspace && mkdir /workspace
WORKDIR /workspace
CMD ["chatgpt_grpc"]