FROM python as builder
COPY . /workspace
RUN cd /workspace && python setup.py bdist_wheel

FROM python
