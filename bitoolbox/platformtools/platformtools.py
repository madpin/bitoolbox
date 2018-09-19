# -*- coding: utf-8 -*-
import platform

def get_hostname():
    return platform.node()


def get_current_ip():
    import socket
    return socket.gethostbyname(get_hostname())


def get_os():
    return platform.uname().system


def get_python_version():
    return platform.python_version()


def get_linux_distro():
    return platform.dist()[0]