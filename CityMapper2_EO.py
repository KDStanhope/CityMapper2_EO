import os, sys
import xmltodict
import glob

import tkinter as tk
from tkinter import filedialog, messagebox
'''
Makes EO data from the Hexagon 'hexstp' files from the citymapper2
'''


def daily_strip_consolidator():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title='Easy EO', message="Please select the root folder for the \n day which has each of the stip directories in it")
    day_dir = filedialog.askdirectory(title="root folder of day's acquisition")
    hexstp_list = glob.glob(str(day_dir)+"/**/*[0-9].hexstp")
    return hexstp_list
    

def create_csv_from_hexstp(hexstp_file):
    image = 0
    with open(hexstp_file) as hx:
        hx_dict = xmltodict.parse(hx.read())
    
    hex2csv = str(hexstp_file.split('\\')[-3].split('/')[-1])+"_Extracted_EO.csv"

    csv = open(hex2csv,'a')

    for i in hx_dict['Strip']['Take']:
        try:
            csv.write(i['Image']['@name']+', '+
                  i['Image']['AcquisitionTime']['#text']+', '+
                  i['Image']['Start']['Position']['Latitude']['#text']+', '+
                  i['Image']['Start']['Position']['Longitude']['#text']+', '+
                  i['Image']['Start']['Position']['EllipsoidHeight']['#text']+', '+
                  i['Image']['Attitude']['Roll']['#text']+', '+
                  i['Image']['Attitude']['Pitch']['#text']+', '+
                  i['Image']['Attitude']['Heading']['#text']+'\n')
            image += 1
        except:
            pass
    csv.close()
    return image

strips = 0
images = 0
for hexstp in daily_strip_consolidator():
    strips += 1
    image_count = create_csv_from_hexstp(hexstp)
    images += image_count


    
root = tk.Tk()
root.withdraw()
messagebox.showinfo(title='DONE', message=str(strips)+" Strips Processed \n"+str(images)+" Images Total")   
