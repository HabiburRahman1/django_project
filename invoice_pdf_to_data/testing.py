import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
import pandas as pd
import re
from datascroller import scroll
import requests
import json


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


# file = '/home/habib/Downloads/django_project/static/AMERICAN.pdf'
# b_files = open(file, 'wb')
# # This is the api part of code 
# data = requests.post('http://api.ocr.space/parse/image',files={'ssss.pdf':b_files},data={'apikey':'58e1390a7b88957'})
# api_result = data.content.decode()
# api_result = json.loads(api_result)
# print(api_result['ParsedResults'][0]['ParsedText'])



images = convert_from_path(file)
# table_header_first_coordinates = [150,825,1400,80]
col1_x = 150
vertical_y = 825
vertical_height = 825
for k, img in enumerate(images):
    table_header_first_coordinates_horizontal = [150, 825, 1400, 75]
    table_header_first_coordinates_vertical = [[col1_x, vertical_y, 140, vertical_height], [col1_x, vertical_y, 676-150, vertical_height],
                                               [col1_x, vertical_y, 853-150, vertical_height], [col1_x, vertical_y, 1020-150, vertical_height], [
                                                   col1_x, vertical_y, 1150-150, vertical_height], [col1_x, vertical_y, 1275-150, vertical_height],
                                               [col1_x, vertical_y, 1465-150, vertical_height], [col1_x, vertical_y, 1550-150, vertical_height]]

    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # print(type(img))
    additional = 25
    for j in range(17):
        # d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        # n_boxes = len(d['level'])
        # print(type(table_header_first_coordinates_horizontal))
        (x, y, w, h) = tuple(table_header_first_coordinates_horizontal)
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)

        if j < len(table_header_first_coordinates_vertical):
            (x, y, w, h) = tuple(table_header_first_coordinates_vertical[j])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)

        table_header_first_coordinates_horizontal[1] = table_header_first_coordinates_horizontal[1] + 50+additional
        table_header_first_coordinates_horizontal[3] = 50
        additional = 0

    # img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # print(type(img))
    # print(img.shape)
    # thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
    # img_bin = 255-img_bin
    # plt.imshow(img_bin)
    
    cv2.imwrite(
        '/home/habib/Downloads/django_project/static/image'+str(k)+'.jpg', img)
    img = cv2.imread(
        '/home/habib/Downloads/django_project/static/image'+str(k)+'.jpg', 0)
    # print(img.shape)





    # This is the api part of code 
    data = requests.post('http://api.ocr.space/parse/image',files={'ssss.jpg':cv2.imencode('.jpg', img)[1].tobytes()},data={'apikey':'58e1390a7b88957'})
    api_result = data.content.decode()
    api_result = json.loads(api_result)
    print(api_result['ParsedResults'][0]['ParsedText'])







    img = img[vertical_y:vertical_y+825, col1_x:col1_x+1400]
    thresh, img_bin = cv2.threshold(
        img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = 255-img_bin
    plotting = plt.imshow(img_bin, cmap='gray')
    plt.show()
    kernel_len = np.array(img).shape[1]//100
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
    plotting = plt.imshow(image_1, cmap='gray')
    plt.show()

    image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
    plotting = plt.imshow(image_2, cmap='gray')
    plt.show()

    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(
        img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imwrite("/Users/YOURPATH/img_vh.jpg", img_vh)
    bitxor = cv2.bitwise_xor(img, img_vh)
    bitnot = cv2.bitwise_not(bitxor)
    plotting = plt.imshow(bitnot, cmap='gray')
    plt.show()
    contours, hierarchy = cv2.findContours(
        img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")
    heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
    mean = np.mean(heights)
    box = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (w < 1000 and h < 500):
            image = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            box.append([x, y, w, h])
    plotting = plt.imshow(image, cmap='gray')
    plt.show()

    row = []
    column = []
    j = 0
    for i in range(len(box)):
        if(i == 0):
            column.append(box[i])
            previous = box[i]
        else:
            if(box[i][1] <= previous[1]+mean/2):
                column.append(box[i])
                previous = box[i]
                if(i == len(box)-1):
                    row.append(column)
            else:
                row.append(column)
                column = []
                previous = box[i]
                column.append(box[i])

    countcol = 0
    for i in range(len(row)):
        countcol = len(row[i])
        if countcol > countcol:
            countcol = countcol
    center = [int(row[i][j][0]+row[i][j][2]/2)
              for j in range(len(row[i])) if row[0]]
    center = np.array(center)
    center.sort()

    finalboxes = []
    for i in range(len(row)):
        lis = []
        for k in range(countcol):
            lis.append([])
        for j in range(len(row[i])):
            diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])
        finalboxes.append(lis)

    outer = []
    for i in range(len(finalboxes)):
        for j in range(len(finalboxes[i])):
            inner = ''
            if(len(finalboxes[i][j]) == 0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], finalboxes[i][j][k][3]
                    finalimg = bitnot[x:x+h, y:y+w]
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                    border = cv2.copyMakeBorder(
                        finalimg, 2, 2, 2, 2,   cv2.BORDER_CONSTANT, value=[255, 255])
                    resizing = cv2.resize(
                        border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    dilation = cv2.dilate(resizing, kernel, iterations=1)
                    erosion = cv2.erode(dilation, kernel, iterations=1)

                    out = pytesseract.image_to_string(erosion)
                    # print(out)
                    # t = re.sub(r'[\x0b\x0c\x0e]', '', out)
                    # t = re.sub(r'[^\x00-\x7f]', '', t)
                    # out = t.strip()
                    if(len(out) == 0):
                        out = pytesseract.image_to_string(
                            erosion, config='--psm 3')
                    inner = inner + " " + out
                outer.append(inner)

    # print(outer)
    invoice_address= outer[0]
    deliver_to = outer[1]

    arr = np.array(outer)
    dataframe = pd.DataFrame(arr.reshape(len(row), countcol))
    # ILLEGAL_CHARACTERS_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]')
    # dataframe = dataframe.applymap(lambda x: ILLEGAL_CHARACTERS_RE.sub(r'', x) if isinstance(x, str) else x)
    scroll(dataframe)
    # data = dataframe.style.set_properties(align="left")
    print(dataframe)
    dataframe.to_excel('/home/habib/Downloads/django_project/static/xlsxqqq'+str(k)+'.xlsx', engine='xlsxwriter')

    # plotting = plt.imshow(img)


