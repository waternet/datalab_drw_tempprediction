import sys
import datetime
import glob
import pandas as pd
import matplotlib.pyplot as plt

#importing the pims module requires adding the following module to the python path
sys.path.append("/home/waternet/programmeren/python/datalab/datalab_drw_pims")

import wnpims

TAGS = [
    "1N305KM01TIT001",
    "1N625SW03TT001",
    "1N625SW02TT001",
    "1N315KM01TIT001",
    "1N315KM02TIT003",
    "1Q325TB03TT151",
    "1D325TA01TT001",
    "T-WRK-Schiphol_STUW12",
    "1L635KM05TT002",
    "1L635KM05TT001",
    "1L315KM01TT001",
    "3H325WT01TT001",
    "3A415DR01_Temp1",
    "3A415DR01_Temp2",
    "3A415DR01_Temp3",
    "3A415DR01_Temp4",
    "3A415DR01_Temp5",
    "3A415DR01_Temp6"
]

TAGS_NIEUWEGEIN = TAGS[0:5]
TAGS_LEIDUIN = TAGS[8:11]

def get_data():
    """Haal de data op uit de PIMS database en sla het op in individuele
    csv bestanden met naam <TAG>-<YYYYMMDD>-<YYYYMMDD>"""
    api = wnpims.API()

    for tag in TAGS:
        print "[INFO] reading data for tag:", tag
        start = datetime.datetime(2015,1,1)
        end = datetime.datetime.now()
        sstart = start.strftime("%Y%m%d")
        send = end.strftime("%Y%m%d")
        df = api.get_trend_pivot(tag, "", start, end, calc='avg')
        filename = "data/%s-%s-%s.csv" % (tag, sstart, send)
        df.to_csv(filename)

def combine_data():
    """Combineer de csv bestanden tot 1 gecombineerd bestand."""
    try:
        import os
        os.remove("data/combined_data.csv")
    except:
        pass

    csvfiles = glob.glob("data/*.csv")

    result = pd.DataFrame()
    for i in range(0, len(csvfiles)):
        columnname = csvfiles[i].split('/')[1][:-22] #22 is the amount of space used by the dates
        df = pd.read_csv(csvfiles[i])
        result[columnname] = df.ix[:,-1:]

    result.to_csv('data/combined_data.csv')

def plot_them_all():
    data = pd.read_csv('data/combined_data.csv')
    data.reset_index().plot(x='index', y=TAGS[:])
    plt.show()

if __name__=="__main__":
    get = raw_input("Data ophalen? (j/n): ")
    if get == 'J':
        get_data()
    combine_data()
    plot_them_all()
