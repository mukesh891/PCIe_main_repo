import sys, os, time, traceback, warnings, weakref, collections, re, yaml, random
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/rc_src")
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/ep_src")
sys.path.append("/home/mukesh/PCIe/PCIe_repo/src/")
import logging
# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level to INFO
logger.setLevel(logging.INFO)

# Create a custom formatter that includes line numbers
formatter = logging.Formatter('%(levelname)s:[%(filename)s:%(lineno)d] %(message)s ')

# Create a console handler and set the formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

from pprint import pprint
import argparse
logger.info("ROOT COMPLEX : Compiling pcie_lib.py file")
