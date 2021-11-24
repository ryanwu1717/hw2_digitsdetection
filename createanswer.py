'''TO create the json file'''
import json
from PIL import Image
import os 



with open("result.json","r",encoding="utf-8") as f:
    data = json.load(f)

final = []
data_listdir = os.listdir("data/IOC/test")
data_listdir.sort(key = lambda x: int(x[:-4]))
i=0
for file in data_listdir: 
    if file.endswith(".png"):
     
        FILE_PATH ='data/IOC/test/{}'.format(file)
        image_id =  int(file[:-4])
        img = Image.open(FILE_PATH)
        imgSize = img.size
        w = img.width
        h = img.height
        for pred in data[i]['objects']:
            pos = []
            x_center = pred['relative_coordinates']['center_x']
            y_center = pred['relative_coordinates']['center_y']
            pr_w = pred['relative_coordinates']['width']
            pr_h = pred['relative_coordinates']['height']
            x1 = w * x_center - (w * pr_w) / 2
            x2 = w * x_center + (w * pr_w) / 2
            y1 = h * y_center - (h * pr_h) / 2
            y2 = h * y_center + (h * pr_h) / 2
            tmpwid = w *pr_w
            tmphei = h *pr_h
            pos.append((x1))
            pos.append((y1))
            pos.append((tmpwid))
            pos.append((tmphei))
            
            tmpName = pred['name']
            if pred['name'] == 10:
                tmpName = 0
            tmmpvalue = {"image_id":image_id,"bbox":pos,"score":pred['confidence'],"category_id":int(tmpName)}
            final.append(tmmpvalue)
        # final.append(value)
        i+=1
with open('answer.json', 'w', encoding='utf-8') as f:
    json.dump(final, f)
    