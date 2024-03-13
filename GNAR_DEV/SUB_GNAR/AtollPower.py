######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240312
# Purpose: Network ATOLLPower Check Class
# Functions: GNAR ATOLL Power
# Update: v1
# NEED TO ADD ALL EXCEPTION HANDLING
######################################################################################


# import os
# import sys
import datetime
import pandas as pd
# import numpy as np
# import tabulate
import SUB_GNAR.DBConnection as DB

TODAY = datetime.datetime.now()
TIMESTAMP = TODAY.strftime('%Y%m%d')
# TIMESTAMP = TODAY.strftime('%Y%m%d-%H%M%S')

atollSql = """




           """
           
class AtollPower():
    """ATOLL SIMULATION POWER CHECK AUDIT OBJECT THAT TAKES IN A QUERY THAT CONVERTS AND CLEANS DATA AND CREATES A DF TO CHECK POWER PARMS ARE CORRECT"""
    """ CHANGE THIS TO PASS IN THE SQL AS A PARAMETER """
    def __init__(self):
       print("Atoll Power Audit Constructor")

    def BuildAtollPowerDF(self):
        """ THSIS DF WILL BE USED FOR MULTIPLE SIMULATION TESTS AND REMEDIATION """
        pass
