import os
import pandas as pd

readPath = 'tables'
writePath = 'JSON'

files = []
fileBasenames = []

for file_path in os.listdir(readPath):
    if os.path.isfile(os.path.join(readPath, file_path)) and (os.path.splitext(file_path)[1]) == '.csv':    #only convert CSV files
        files.append(os.path.join(readPath, file_path))                                                     #add CSV files to a list
        fileBasenames.append(os.path.splitext(file_path)[0])                                                 #get the file name without the extension to write

for index, convertCSV in enumerate(files):                                                                  #write JSON files for all the found CSV
    df = pd.read_csv(convertCSV)
    df.to_json ((os.path.join(writePath,fileBasenames[index]))+'.json', orient='index')                      



