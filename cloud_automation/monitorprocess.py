from os.path import curdir
import subprocess
import sqlalchemy
import atexit
import time
import logging
from alice_blue import *
import json
import datetime
import os
from pathlib import Path
from threading import Thread
from sqlalchemy import create_engine, pool
import pandas as pd
import util
logging.basicConfig(level=logging.INFO)

bashCommand = "pkill -f hello_busy.py"
SQL_QUERY_TO_VALIDATE="SELECT time(ts) FROM `db-stocks`.AXISBANK order by ts desc limit 1;"

_clUtil = util.clUtil()
base_path = _clUtil.get_project_root()


class clBeginGetData(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.system_cred = _clUtil.loadJson(filename=os.path.join(
            base_path.parent, "credentials", "env_credential.json"))
        self.msql_engine = create_engine("mysql+pymysql://{user}:{pw}@{endpoint}/{db}"
                                         .format(endpoint=self.system_cred["mysql"]["endpoint"],
                                                 user=self.system_cred["mysql"]["username"],
                                                 pw=self.system_cred["mysql"]["password"],
                                                 db=self.system_cred["mysql"]["dbschema"]))
        atexit.register(self.cleanup)

    def cleanup(self):  # Dont leave your footprints dispose whats not needed after job is done
        self.msql_engine.dispose()
        # print("doing cleanup")
        # print("Job execution ended at {0}".format(datetime.datetime.now()))

    def convert_timedelta(self, duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return hours, minutes, seconds
    def kill_process(self):
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def GetRows(self):
        current_time_minutes = datetime.datetime.now().hour * 60 + \
            datetime.datetime.now().minute
        print(current_time_minutes)
        _data = self.msql_engine.execute(SQL_QUERY_TO_VALIDATE)
        # print(_data[0])
        _rm = _data.fetchone()[0]
        sql_hours, sql_minutes, sql_seconds = self.convert_timedelta(_rm)
        sql_current_time_minutes= sql_hours*60+sql_minutes
        print(sql_current_time_minutes)
        if((current_time_minutes-sql_current_time_minutes)>5): #If diff in greater than 5 minutes restart job
            print("Inside if")
            self.kill_process()
        process = subprocess.Popen("/home/awsgui/algodev/ec2-algo-automation/cloud_automation/monitor_job.sh".split(), stdout=subprocess.PIPE)
        output, error = process.communicate()


    


cl = clBeginGetData()
cl.GetRows()
