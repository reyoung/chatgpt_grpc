#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="chatgpt-grpc",
    version="0.0.1",
    description="",
    packages=['chatgpt_grpc'],
    install_requires=[
        "revChatGPT",
        "grpcio-tools"
    ],
    entry_points={
        'console_scripts': [
            'chatgpt_grpc = chatgpt_grpc.main:main',
            'chatgpt_grpc_cli = chatgpt_grpc.cli:main',
        ],
    },
)