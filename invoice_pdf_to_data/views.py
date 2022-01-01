from django.shortcuts import render
# This is for extract the data from the pdf file
from pdf2image import convert_from_path
import easyocr
import numpy as np
import PIL
from PIL import ImageDraw
import spacy
import os
# Create your views here.

reader = easyocr.Reader(['en'])
file_path = os.path.join('static', '6.PDF')
def home(request):
    images = convert_from_path(file_path)
    print(len(images))
    bounds = reader.readtext(np.array(images[0]))
    print(bounds)
    text = ''
    extracted_word_list = list()
    for i in range(len(bounds)):
        extracted_word_list.append(bounds[i][2])
        text += bounds[i][1]+'\n'
    return render(request, 'home.html', {'name': 'Habib', 'age': extracted_word_list})
