# -*- coding: utf-8 -*-
__author__ = 'radek hofman'
"""
this programm runs all FLEXPART runs from our run tree using a given number of cores
usage: 2_run_tree.py <#cores_to_be_used>
"""


import multiprocessing
import sys
import rad_config as rcf
import os
from datetime import datetime as dt
import logging
today = dt.now().strftime("%Y-%m-%d")
logging.basicConfig(filename='2_log_%s.txt' % today, filemode='w', level=logging.DEBUG)


cwd = os.getcwd()

def func(task):
    """
    executes command
    stdout of Flexpart logged into log.txt
    """
    id0 = task[0]
    command = task[1]
    logging.info("Starting job %d" % id0)
    os.chdir(cwd)
    os.chdir("/".join(command.split("/")[:-1]))
    os.system("./"+rcf.FLEXPART_NAME+" > log.txt")
    logging.info("Job %d done" % id0)


def main(cpu_count):
    """
    main... you know, we should have one...
    """

    #firstly, let's acquire a list of runs to run..., ho ho ho
    #it should be in Run_blabla/
    with open(rcf.TREE_PATH+os.sep+rcf.RUN+os.sep+"run_list.txt", "r") as f:
        s = f.readlines()
        #strip new line characters
        tasks = [(id0, line.strip()) for id0, line in enumerate(s)]
        logging.info(tasks)
        #creates a pool for tasks limited to cpu_count processes at once
        pool = multiprocessing.Pool(processes=cpu_count)
        #run all tasks in our pool...
        pool.map(func, tasks)
        logging.info("All FLEXPART runs done, ho ho ho")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cpu_count = int(sys.argv[1])
        max_cpu = multiprocessing.cpu_count()
        if cpu_count > max_cpu:
            logging.info("cores number to large, setting to %d" % max_cpu)
            cpu_count = max_cpu
    else:
        cpu_count = multiprocessing.cpu_count()

    logging.info("Using %d cores" % cpu_count)
    main(cpu_count)
