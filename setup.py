#!/usr/bin/env python

from setuptools import setup

setup(
    name="Pump_gui",
    description="Simple qt gui for demo connecxion to opcua",
    author="Jérémie Probst",
    author_email="jprobst@operametrix.fr",
    url="https://github.com/jerempr/Pump_gui.git",
    entry_points={
        "console_scripts": [
            "Pump_app=control.main:__main__",
        ]
    },
    install_requires=["asyncqt","asyncua","PySide2","seeed_python_reterminal"],
)
