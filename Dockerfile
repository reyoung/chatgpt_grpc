FROM python
COPY . /workspace
RUN cd /workspace && pip install --no-cache . && cd / && rm -rf /workspace && mkdir /workspace
WORKDIR /workspace
CMD ["chatgpt_grpc"]