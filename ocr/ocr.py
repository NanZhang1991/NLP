import os
import paddle
from pathlib import Path
import cv2
from paddleocr import PaddleOCR, draw_ocr,PPStructure, draw_structure_result, save_structure_res
from PIL import Image
import pandas as pd
import numpy as np
import json

# import paddle
# paddle.fluid.install_check.run_check()

def text_ocr(img_path, save_folder='./data/output'):
    ocr = PaddleOCR(use_angle_cls=False, lang='ch', use_gpu=False)
    result = ocr.ocr(img_path, cls=True)
    out_txt = os.path.join(save_folder, os.path.basename(img_path).rsplit('.',1)[0] + '.txt')
    out_txt = Path(out_txt).as_posix()
    with open(out_txt, 'w', encoding='utf-8') as f:
        for line in result:
            # print(line[1])
            f.write(line[1][0]+'\n')
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
    im_show = Image.fromarray(im_show)
    res_im_path = os.path.join(save_folder, os.path.basename(img_path).rsplit('.',1)[0] + '_result.jpg') 
    res_im_path= Path(res_im_path).as_posix()
    im_show.save(res_im_path, dpi=(300.0,300.0))

def table_ocr(img_path, save_folder='./data/output'):
    img_name = os.path.basename(img_path).split('.')[0]
    total={}
    table_engine = PPStructure(show_log=True)
    img = cv2.imread(img_path)
    res = table_engine(img)
    save_structure_res(res, save_folder, img_name)
    for region in res:
        region.pop('img')
        # print(f'---------\n{region}')
        dic = table3_to_dic(save_folder, img_name, region)
        total.update(dic)
    res_json = json.dumps(total ,ensure_ascii=False)
    print("-"*20,'\n',res_json)
    json_fp = os.path.join(save_folder, img_name, 'res.json')
    with open(json_fp, 'w') as f:
        json.dump(total, f, ensure_ascii=False)
    return res_json
    # image = Image.open(img_path).convert('RGB')
    # im_show = draw_structure_result(image, result, font_path='simfang.ttf')
    # im_show = Image.fromarray(im_show)
    # res_im_path = os.path.join(save_folder, os.path.basename(img_path).rsplit('.',1)[0], 'result.jpg') 
    # res_im_path = Path(res_im_path).as_posix()
    # im_show.save(res_im_path, dpi=(300.0,300.0))

def table3_to_dic(save_folder, img_name, region):
    excel_save_folder = os.path.join(save_folder, img_name)
    excel_path = os.path.join(excel_save_folder,
                                '{}.xlsx'.format(region['bbox']))
    df = pd.read_excel(excel_path,header=None)
    # print(df.shape,'\n', df)
    df.replace(np.nan, None, inplace=True)
    key = pd.Series()
    value =  pd.Series()
    for row in df.iterrows():
        if row[0] % 2 ==0:
            key = key.append(row[1])
        else:
            value = value.append(row[1])
    dic = dict(zip(key, value))
    return dic

def get_img_path(dir_path):
    img_l = []
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            if name.endswith('.png'):
                fn = os.path.join(root,name)
                img_l.append(fn)
    return img_l
   

# if __name__=="__mian__":
#     dir_path = 'data/input/'
#     img_l = get_img_path(dir_path)

    # img_path = './data/input/text0.jpg'
    # text_ocr(img_path)

    # img_path = './data/input/table3.jpg'
    # table_ocr(img_path)
    # print('Complete')

img_path = './data/input/table3.jpg'
table_ocr(img_path)
print('Complete')