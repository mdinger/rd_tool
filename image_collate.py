#!/usr/bin/env python2

from __future__ import print_function

import argparse
import os
import sys
import threading
import subprocess
from time import sleep
from datetime import datetime
import multiprocessing
import boto.ec2.autoscale
from pprint import pprint
import json
import awsremote
import scheduler

#our timestamping function, accurate to milliseconds
#(remove [:-3] to display microseconds)
def GetTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

if 'DAALA_ROOT' not in os.environ:
    print(GetTime(),"Please specify the DAALA_ROOT environment variable to use this tool.")
    sys.exit(1)

daala_root = os.environ['DAALA_ROOT']

class Work:
    def __init__(self):
        self.failed = False
    def get_command(self):
        return '/home/ec2-user/daala/tools/ab_meta_compare.sh'
    def job_type(self):
        return 'image_collate'
    def parse(self, stdout, stderr): pass

aws_group_name = 'Daala Test'
total_num_of_jobs = 1
num_instances_to_use = 1

#a logging message just to get the regex progress bar on the AWCY site started...
print(GetTime(),'0 out of',total_num_of_jobs,'finished.')

machines = awsremote.get_machines(num_instances_to_use, aws_group_name)

#set up our instances and their free job slots
for machine in machines:
    machine.setup()

slots = awsremote.get_slots(machines)

if len(slots) < 1:
    print(GetTime(),'All AWS machines are down.')
    sys.exit(1)

work_items = []
work_items.append(Work())

work_done = scheduler.run(work_items, slots)
