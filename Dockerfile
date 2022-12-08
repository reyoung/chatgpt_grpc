FROM python
COPY . /workspace
RUN cd /workspace && pip install --no-cache . && cd / && rm -rf /workspace
CMD ["chatgpt_grpc"]