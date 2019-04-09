from os import listdir
from os.path import isfile, join
import numpy as np

np.set_printoptions(suppress=True)

dataset_path = "./SurveyLogs/" # Keep trailing /
destination_path = "./SFBased/" # Keep trailing /
files = [f for f in listdir(dataset_path) if isfile(join(dataset_path, f))]
numTxPkts = 30.


def splitSpread():
    for fl in files:
        with open(dataset_path+fl, 'r') as log_file:
            logs = log_file.readlines()
            name = logs[1].split(",")[0]
            lat = logs[1].split(",")[1]
            lon = logs[1].split(",")[2][:-1]
            for row in logs[4:]:
                new_row = row[:-1] + "," + name + "," + lat + "," + lon + "\n"
                sf = row.split(",")[2]
                with open(sf+".csv", "a") as f:
                    f.write(new_row)
            
           
def splitGeoCombine():
    for fl in files:
        sfbin = {} 
        #print("\n\n File, " + fl)
        with open(dataset_path+fl, 'r') as log_file:
            logs = log_file.readlines()
            lat = logs[1].split(",")[1]
            lon = logs[1].split(",")[2][:-1]

            for row in logs[4:]:
                row = row.strip("\n").split(",")
                sf = row[2]
                if sf in sfbin.keys() :
                    sfbin[sf] = np.concatenate((sfbin[sf], np.array([[float(row[0]), float(row[1])]])), axis=0)
                else:
                    sfbin[sf] = np.array([[float(row[0]), float(row[1])]])
            for sf in sfbin:
                rowStat = lat + "," + lon + "," + sf + "," + str(np.average(sfbin[sf][:,0])) + "," + str(np.average(sfbin[sf][:,1])) + "," + str(int(100*(numTxPkts-len(sfbin[sf]))/numTxPkts)) + "\n"
                with open(destination_path+sf+".csv", "a") as f:
                    f.write(rowStat)
            notEmptyFLag = 0



def main():
    splitGeoCombine()


if __name__ == "__main__":
    main()
