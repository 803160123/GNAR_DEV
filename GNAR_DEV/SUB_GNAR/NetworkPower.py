######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240308
# Purpose: Network Power Check Class
# Functions: GNAR Network Power
# Update: v1
# NEED TO ADD ALL EXCEPTION HANDLING
######################################################################################


# import os
import sys
import datetime
import pandas as pd
# import numpy as np
# import tabulate
import SUB_GNAR.DBConnection as DB

TODAY = datetime.datetime.now()
TIMESTAMP = TODAY.strftime('%Y%m%d')
# TIMESTAMP = TODAY.strftime('%Y%m%d-%H%M%S')

powerCheckSql = """WITH SECTF AS( --B
					SELECT 
					-- USID,
					ENODEB, -- NEED TO FIX THIS
					SECTORFUNCTIONREF,
					(CASE WHEN COUNT(EUTRANCELLFDD) = 2 AND MAX(PRODUCTNAME) IN ('RRUS 11 B12','RRUS11') THEN SUM(DLCHANNELBANDWIDTH/2) ELSE SUM(DLCHANNELBANDWIDTH)END) AS TOTAL_DLBW, 
					-- SUM(DLCHANNELBANDWIDTH)/5 AS TEST,
					-- (CASE WHEN ENODEB IN ('UNL02036','UNL04501') THEN ROUND(MIN(ENM_MAXTXPWR)/(MIN(DLCHANNELBANDWIDTH)/5),1) ELSE 
					ROUND(SUM(ENM_MAXTXPWR)/(SUM(DLCHANNELBANDWIDTH)/5),1) AS PWRPER5MHZ,
					(CASE WHEN (COUNT(EUTRANCELLFDD) = 2 AND MAX(PRODUCTNAME) IN ('RRUS 11 B12','RRUS11')) OR (ENODEB = 'UNL04501') THEN SUM(ENM_MAXTXPWR/2) ELSE SUM(ENM_MAXTXPWR) END) AS TOTAL_TXPWR, --TEST W/ 850 SHARED
					(CASE WHEN COUNT(EUTRANCELLFDD) = 2 AND MAX(PRODUCTNAME) IN ('RRUS 11 B12','RRUS11') THEN SUM(ENM_NOOFTX/2) ELSE SUM(ENM_NOOFTX) END) AS TOTAL_NOOFTX,
					(CASE WHEN COUNT(EUTRANCELLFDD) = 2 AND MAX(PRODUCTNAME) IN ('RRUS 11 B12','RRUS11') THEN (COUNT(EUTRANCELLFDD)/2) ELSE COUNT(EUTRANCELLFDD) END) AS FDD_CNT,
					(SUM(ENM_NOOFTX)/COUNT(EUTRANCELLFDD)) AS RRU_PORT_COUNT,
					(CASE WHEN COUNT(EUTRANCELLFDD) = 2 AND MAX(PRODUCTNAME) IN ('RRUS 11 B12','RRUS11') THEN SUM(ENM_MAXTXPWR/2)/(SUM(ENM_NOOFTX)/COUNT(EUTRANCELLFDD)) 
						ELSE SUM(ENM_MAXTXPWR)/(SUM(ENM_NOOFTX)/COUNT(EUTRANCELLFDD)) END) AS PWR_PER_PORT,
					(CASE WHEN COUNT(EUTRANCELLFDD) = 2 AND MAX(PRODUCTNAME) IN ('RRUS 11 B12','RRUS11') THEN 1 ELSE 0 END) AS CSRF
					--
				FROM [GNAR_DEV].[dbo].[NETWORK_STATUS_20240226]
				WHERE 1=1
				AND EUTRANCELLFDD NOT LIKE '%_DB'
				-- AND USID = '301886'
				-- AND USID = 1179
				AND FREQBAND IN (2,4,5,17,29,66)
				AND PRODUCTNAME NOT IN ('RRUS A2 B25','RRUS A2 B4')
				GROUP BY
				-- USID,
				ENODEB,
				SECTORFUNCTIONREF
				-- RRU_ID
				),
				FDD AS ( -- A
					SELECT
					PULLDATE,
					USID,
					ENODEB,	
					EUTRANCELLFDD,
					STATUS,
					FREQBAND,
					DLCHANNELBANDWIDTH,
					ULCHANNELBANDWIDTH,
					SECTORCARRIERREF,
					SECTORFUNCTIONREF,
					ENM_NOOFTX,	
					ENM_NOOFRX,	
					ENM_MAXTXPWR,
					RRU_ID,	
					RRU_SPLIT,
					PRODUCTNAME,
					PRODUCTNUMBER
				--
				FROM [GNAR_DEV].[dbo].[NETWORK_STATUS_20240226]
				WHERE 1=1
				AND EUTRANCELLFDD NOT LIKE '%_DB'
				-- AND USID = 301886
				-- AND USID = 2693
				AND FREQBAND IN (2,4,5,17,29,66)
				),
				PWR AS (
				SELECT
					A.PULLDATE,
					A.USID,
					A.ENODEB,	
					A.EUTRANCELLFDD,
					A.STATUS,
					A.FREQBAND,
					A.DLCHANNELBANDWIDTH,
					A.ULCHANNELBANDWIDTH,
					A.SECTORCARRIERREF,
					A.SECTORFUNCTIONREF,
					B.SECTORFUNCTIONREF AS SECTFUNCREF, -- FOR TESTING
					A.ENM_NOOFTX,	
					A.ENM_NOOFRX,	
					A.ENM_MAXTXPWR,
					B.FDD_CNT,
					-- (CASE WHEN CSRF = 1 THEN (B.TOTAL_DLBW/2) ELSE B.TOTAL_DLBW END) 
					B.TOTAL_DLBW,
					-- B.TEST,
					ROUND(((A.DLCHANNELBANDWIDTH/5) * PWRPER5MHZ),0) AS CALC_ENM_PWR,
					B.PWRPER5MHZ,
					B.TOTAL_TXPWR,
					B.TOTAL_NOOFTX,
					B.RRU_PORT_COUNT,
					B.PWR_PER_PORT,
					A.RRU_ID,	
					A.RRU_SPLIT,
					A.PRODUCTNAME,
					(CASE WHEN A.PRODUCTNAME = 'Radio 8843 B2 B66A' and A.FREQBAND = 2 AND B.RRU_PORT_COUNT = 2 THEN 60000 -- SHOULD I JUST CHANGE THESE TO 40
					WHEN A.PRODUCTNAME = 'Radio 8843 B2 B66A' and A.FREQBAND IN (4,66) AND B.RRU_PORT_COUNT = 2 THEN 80000 -- SHOULD I JUST CHANGE THESE TO 40
					WHEN A.PRODUCTNAME = 'Radio 8843 B2 B66A' and B.RRU_PORT_COUNT = 4 THEN 40000
					WHEN A.ENODEB = 'UNL04522' AND A.PRODUCTNAME = 'Radio 4449 B5 B12A' and B.RRU_PORT_COUNT = 2 THEN 60000
					WHEN A.PRODUCTNAME = 'Radio 4449 B5 B12A' THEN 40000
					WHEN A.PRODUCTNAME = 'Radio 2260 22B2/B25 22B66 C' THEN B.PWR_PER_PORT
					WHEN A.PRODUCTNAME = 'RRUS 32 B2' THEN 40000
					WHEN A.PRODUCTNAME ='RRUS 32 B30' THEN 25000
					WHEN A.PRODUCTNAME ='RRUS 32 B66A' THEN 40000
					WHEN A.PRODUCTNAME = 'Radio 4478 B12A' THEN 40000
					-- WHEN A.PRODUCTNAME = 'Radio 4478 B14' THEN 40000
					WHEN A.PRODUCTNAME = 'Radio 4478 B5' THEN 40000
					WHEN A.PRODUCTNAME = 'Radio 4426 B66' THEN 60000
					WHEN A.PRODUCTNAME = 'Radio 4402 B2/B25' THEN 5000
					WHEN A.PRODUCTNAME = 'Radio 4402 B66A' THEN 5000
					WHEN A.PRODUCTNAME = 'Radio 4415 B2 B25' THEN 40000
					-- WHEN A.PRODUCTNAME = 'Radio 4415 B30' THEN 25000
					WHEN A.PRODUCTNAME ='RRUS 11 B12' AND PRODUCTNUMBER = 'KRC 161 241/2' THEN 40000
					WHEN A.PRODUCTNAME ='RRUS 11 B12' THEN 30000
					WHEN A.PRODUCTNAME ='RRUS11' THEN 30000
					WHEN A.PRODUCTNAME ='RRUS 11 B2' THEN 40000
					WHEN A.PRODUCTNAME ='RRUS 11 B4' THEN 40000
					WHEN A.PRODUCTNAME ='RRUS 11 B5' THEN 40000
					WHEN A.PRODUCTNAME ='RRUS 12 B2' THEN 60000
					WHEN A.PRODUCTNAME ='RRUS 12 B4' THEN 60000
					WHEN A.PRODUCTNAME ='RRUS 12 B5' THEN 60000
					WHEN A.PRODUCTNAME ='RRUS 0Z B4' THEN 60000
					WHEN A.PRODUCTNAME ='RRUS E2 B29' THEN 40000
					WHEN A.PRODUCTNAME ='Radio 2012 B29' THEN 40000
					ELSE NULL END) AS RRU_PORT_SPEC,
					--
					B.CSRF,
					A.PRODUCTNUMBER
				FROM FDD A
				JOIN SECTF B ON A.ENODEB = B.ENODEB AND A.SECTORFUNCTIONREF = B.SECTORFUNCTIONREF
				WHERE 1=1
				)
				-----------------------------------------------------------------------------------
				SELECT
					P.PULLDATE,
					P.USID,
					P.ENODEB,	
					P.EUTRANCELLFDD,
					P.STATUS,
					P.FREQBAND,
					P.DLCHANNELBANDWIDTH,
					P.ULCHANNELBANDWIDTH,
					P.SECTORCARRIERREF,
					P.SECTORFUNCTIONREF,
					-- P.SECTFUNCREF, -- FOR TESTING
					P.ENM_NOOFTX,	
					-- P.ENM_NOOFRX,	
					P.ENM_MAXTXPWR,
					P.FDD_CNT,
					P.TOTAL_DLBW,
					-- B.TEST,
					P.CALC_ENM_PWR,
					P.PWRPER5MHZ,
					P.TOTAL_TXPWR,
					P.TOTAL_NOOFTX,
					P.RRU_PORT_COUNT,
					P.PWR_PER_PORT,
					P.RRU_ID,	
					P.RRU_SPLIT,
					P.PRODUCTNAME,
					P.RRU_PORT_SPEC,
					--
					P.PRODUCTNUMBER,
					P.CSRF,
					(CASE WHEN P.RRU_PORT_SPEC <> P.PWR_PER_PORT AND P.ENM_MAXTXPWR <> P.CALC_ENM_PWR THEN 'RRU_PORT_PWR + ENM_MAXPWR'
					WHEN P.RRU_PORT_SPEC <> P.PWR_PER_PORT THEN 'RRU_PORT_PWR'
					WHEN P.ENM_MAXTXPWR <> P.CALC_ENM_PWR THEN 'ENM_MAXPWR'
					ELSE '' END) AS FLAG
				FROM PWR P
				WHERE 1=1
				AND P.USID = 95345
                -- AND P.USID IN (95345,95314)
				-- AND P.RRU_PORT_SPEC IS NULL
				AND P.PRODUCTNAME NOT IN ('RRUS A2 B4','RRUS A2 B25')
				AND P.EUTRANCELLFDD NOT LIKE 'UNL14025_8%'
				ORDER BY 
				P.USID,
				P.ENODEB,	
				P.EUTRANCELLFDD
				;
				"""


class NetworkPower():
    """NETWORK POWER CHECK AUDIT OBJECT THAT TAKES IN A QUERY THAT CONVERTS AND CLEANS DATA AND CREATES A DF TO CHECK POWER PARMS ARE SET CORRECT"""
    def __init__(self):
       print("Network Power Audit Constructor")

    def BuildNetPowerDF(self):
        """ THIS METHOD IS RESPONSIBLE FOR QUERYING THE NETWORK MSSQL DB AND RETURNING ALL APPLICABLE PARMS (RAW DATAFRAME)"""   
        curs = DB.mssqlConnection()
        curs.execute(powerCheckSql)
        tempDf = curs.fetchall()
        pwrDf = pd.DataFrame.from_records(tempDf, columns=[x[0] for x in curs.description])
		# cursor.commit()  #commits to the table
        DB.closeCursor(curs)
        # print(pwrDf.to_markdown(tablefmt="grid"))  
        return pwrDf


    def PwrSummary(self):
        splitDf = self.BuildNetPowerDF()
        splitDf["STATUS"] = (splitDf["enm_maxtxpwr"] == splitDf["calc_enm_pwr"]) & (splitDf["rru_port_spec"] == splitDf["pwr_per_port"])
        # splitDf["STATUS"] = splitDf.apply(lambda row: row["calc_enm_pwr"] + splitDf["enm_maxtxpwr"], axis =1)
        print(splitDf.to_markdown(tablefmt="grid")) 
        return splitDf
    
    def CreateDaily(self):
        pass
        """ THIS IS A METHOD THAT WILL CREATE A DAILY TABLE FOR CHANGES """
        # NEED TO ADD ERROR HANDLING 
        # EXAMPLE NEED A CURSOR AND OPEN CONNECTION
        # cursor.execute("use GNAR_DEV; drop table if exists testtable")
		# cursor.execute("use GNAR_DEV; create table testtable (column1 varchar, column2 varchar, column3 float, column4 int)")
		# cursor.commit()  #commits to the table


        # SVAE TO DF --> csv WHY ?? BECAUSE OF THE DF DTYPES
        # df.to_csv('testfile.csv', header=df.columns, index=False, encoding='utf-8') 
		# my_file = open('testfile.csv')
		# print("FILE OPENED")
		# SQL_STATEMENT = 

		
		# cursor.commit()  #commits to the table
        """ conn = mysql.connector.connect(user='root', password='somepassword', host='localhost', port='3306', database='db')
		cursor = conn.cursor()

		for i,row in df.iterrows():
			sql = "INSERT INTO table_name (title, summary, url) VALUES (%s,%s,%s)"
			cursor.execute(sql, tuple(row))

		conn.commit()
		conn.close() """


    def updateNetworkPwr(self):
        """ THIS METHOD IS RESPONSIBLE FOR TAKING THE FAILING DATAFRAM VALUES AND UPDATING THE CORRECT TABLE TO REMEDIATE THE POWER IN THE SQL DB """
        tdf =  self.PwrSummary()
        # print(tdf["STATUS"].dtype())
        target_value = True
        """ NEED TO BUILD THE QUERY TO EXECUTE
        # NEED TO CHECK IF THIS FUNCTION NEEDS TO RUN AT ALL
        if (tdf["STATUS"] == target_value).any().any():
            print("THe VALUE EXISTS")
            THIS WILL BE FOR THE SQL CODE STATEMENT LOOP
            return True
        else:
            print("THE VALUE DOES NOT EXIST")
            return False
        """    
        """
		for column in tdf.columns:
            if (tdf["STATUS"] == target_value).any():
                print(f"VALUE {target_value} EXISTS IN COLUMN '{column}'")
                return True
    
        print(f"VALUE {target_value} DOES NOT EXIST IN THE DataFrame")
        return False
		"""
        for index, row in tdf.iterrows():
        # Construct the SQL UPDATE statement
            
            for column, value in row.items():
                # if (tdf["STATUS"].bool() == False): 
                if tdf["flag"].notnull().any():
                    # update_query += f"ENM_MAXTXPWR = "+tdf["calc_enm_pwr"]+" WHERE EUTRANCELLFDD = "+tdf["eutrancellfdd"]+", "
                    update_query += f'THIS IS A TEST {tdf["calc_enm_pwr"].astype(str)}, '
            update_query = update_query[:-2]  # Remove the trailing comma and space
            # update_query += f" WHERE EUTRANCELLFDD = '{row[key_column]}'"
        print(update_query)
						
        # curs = DB.mssqlConnection()
        # curs.execute(powerCheckSql)
		# DB.closeCursor(curs)

    def TempNetworkPwr(self):
        """ THIS IS A TEST VERSION METHOD FOR MY SQL CODE GENERATION """
        tdf =  self.PwrSummary()
        table_name = "[dbo].[NETWORK_STATUS_20240226]"
        update_query = f"UPDATE {table_name} SET "
        key_column = tdf["freqband"]
		
        for index, row in tdf.iterrows():
            if row["STATUS"] == False: 
                update_query += f"ENM_MAXTXPWR = {row['calc_enm_pwr']} WHERE EUTRANCELLFDD = {row['eutrancellfdd']}, "
				# print(f"THIS IS A TEST F-STRING {row['eutrancellfdd']} AND MORE {row['STATUS']}")
        
        update_query = update_query[:-2]  # Remove the trailing comma and space
        print(update_query)
                
			
        """
		# Iterate over rows in the DataFrame
        for index, row in tdf.iterrows():
        # Construct the SQL UPDATE statement
            update_query = f"UPDATE {table_name} SET "
            for column, value in row.items():
                if column != key_column:
                    update_query += f"{column} = '{value}', "
        update_query = update_query[:-2]  # Remove the trailing comma and space
        # update_query += f" WHERE {key_column} = '{row[key_column]}'"
        
        print(update_query)
        """
        
    # END OF CLASS


# END OF NetworkPower PY SCRIPT






