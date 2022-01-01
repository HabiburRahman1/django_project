import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
import pandas as pd
import re
import requests
import json

file = '/home/habib/Downloads/django_project/static/AMERICAN.pdf'
images = convert_from_path(file)
# table_header_first_coordinates = [150,825,1400,80]
col1_x = 150
vertical_y = 825
vertical_height = 825

for k, img in enumerate(images):

    print(type(img))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    
    # cv2.imwrite(
    #     '/home/habib/Downloads/django_project/static/image'+str(k)+'.jpg', img)
    # img = cv2.imread(
    #     '/home/habib/Downloads/django_project/static/image'+str(k)+'.jpg')


    # img = img[vertical_y:vertical_y+825, col1_x:col1_x+1400]
    # img = img[75:70+800, 0:0+1400]

    print("Before API call")

    data = requests.post('http://api.ocr.space/parse/image',files={'ssss.jpg':cv2.imencode('.jpg', img)[1].tobytes()},data={'apikey':'75e8fb2fdd88957'})
    api_result = data.content.decode()
    print(api_result)
    api_result = json.loads(api_result)
    api_string = api_result['ParsedResults'][0]['ParsedText'].strip()

    api_list = api_string.split('\r\n')
    print(api_list)
    print(len(api_list)/8)
    row_counter = 0
    data_list = list()
    data_dict = dict()
    col = 1
    exceptional_data = list()
    store = -1
    lenght_of_api_list = int(len(api_list)/8)
    for i in api_list:

        print(len(api_list))
        if lenght_of_api_list == row_counter:
            data_dict['col'+str(col)] = data_list
            data_list = list()
            print(i)
            row_counter = 0
            col += 1
            
        
        if col == 1:
            if i.startswith('0') and i.isdigit():
                print(i)
                i = 'FD'+i[1:]
                data_list.append(i)
                row_counter += 1
            elif i.startswith('+') and i[1:].isdigit():
                i= 'HP'+i[1:]
                data_list.append(i)
                row_counter += 1

            else:
                try:
                    i = float(i)
                    exceptional_data.append(i)
                except Exception as e:
                    data_list.append(i)
                    row_counter += 1
        
        elif col == 2:
            try :
                i = float(i)
                exceptional_data.append(i)
            except Exception as e:
                data_list.append(i)
                row_counter += 1
        elif col == 3:
            print(col)
            print(len(i))
            print(i)
            if len(i) == 8:
                data_list.append(i)
                row_counter += 1
        
        elif col == 4:
            if i.isdigit():
                data_list.append(i)
                row_counter += 1
        
        elif col == 5:
            try:
                i = float(i)
                data_list.append(i)
                row_counter += 1
            except Exception as e:
                pass
        elif col == 6:
            if '%' in i:
                data_list.append(i)
                row_counter += 1
        elif col == 7:
            if not i.isdigit():
                try:
                    i = float(i)
                    data_list.append(i)
                    row_counter += 1
                except Exception as e:
                    pass
            else:
                store = i
                data_list.extend(exceptional_data)
                row_counter = int(len(api_list)/8)
        
        elif col == 8:
            if store != -1:
                data_list.append(store)
                store = -1
            if i.isdigit():
                data_list.append(i)
                row_counter += 1
    
    if not 'col8' in data_dict.keys():
        data_dict['col'+str(8)] = data_list

    print(data_dict)

    pd.DataFrame.from_dict(data_dict).to_csv('/home/habib/Downloads/django_project/static/'+ str(k) +'data.csv')