from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect, secure_filename

from web import db
from ..forms import UploadForm
from web.models import UploadInfo, ModelList

bp = Blueprint('result2', __name__, url_prefix='/result2')


### projects 코드 불러온 상태 



import json
import numpy as np
import requests
import cv2

def draw_bounding_boxes(image, result):

    height, width, _ = image.shape
    image_ = image.copy()

    # Confidence 값이 0.5 보다 큰 경우를 추려냄    
    detected_object = list(filter( lambda x: x > 0.5, result[0]["detection_scores"] ))

    if len(detected_object) > 0:
        
        boxes = np.array( result[0]["detection_boxes"][0:len(detected_object)] )

        # Classname
        classes_ = list( map( int, result[0]["detection_classes"][0:len(detected_object)] ) )

        classname = ['person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light','fire hydrant',
                    'street sign','stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant',
                    'bear','zebra','giraffe','hat','backpack','umbrella','shoe','eye glasses', 'handbag','tie','suitcase','frisbee',
                    'skis','snowboard','sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                    'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
                    'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window',
                    'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock',
                    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']

        classes = list()

        for class_ in classes_:
            classes.append(classname[ class_-1 ])

        for score, box, cls_ in zip(detected_object, boxes, classes):
            image_ = cv2.rectangle(image_,
                                (int(box[1] * width), int(box[0] * height)),
                                (int(box[3] * width), int(box[2] * height)), 255, 2)
            object_info = str(cls_) + ': ' + str(round(score * 100, 2)) + '%'
            text_size, _ = cv2.getTextSize(text = object_info,
                                        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                                        fontScale = 0.5, thickness = 2)
            image_ = cv2.rectangle(image_,
                                (int(box[1] * width), int(box[0] * height) + 20),
                                (int(box[1] * width) + text_size[0], int(box[0] * height)),
                                255, -1)
            image_ = cv2.putText(image_,
                            object_info,
                            (int(box[1] * width), int(box[0] * height) + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    else:

        object_info = "Failed to detect"
        text_size, _ = cv2.getTextSize(text = object_info,
                                    fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                                    fontScale = 0.5, thickness = 2)
        image_ = cv2.rectangle(image_,
                            (0, 30),
                            (text_size[0]+15, 0),
                            255, -1)
        image_ = cv2.putText(image_,
                        object_info,
                        (5, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    return image_




import json
import numpy as np
import requests
import cv2
import PIL.Image
import base64
import io

def predict(image):
    OBJECT_DETECT_URL = "http://localhost:8080/v1/models/default:predict"
    try:
        image = PIL.Image.open(image)
        original_image = np.array(image)
        if original_image.shape[0] < original_image.shape[1]:
            image_np = cv2.resize(original_image, ( 480, int(480*original_image.shape[0]/original_image.shape[1]) ) )    
        else:
            image_np = cv2.resize(original_image, ( int(320*original_image.shape[1]/original_image.shape[0]), 320 ) )

        payload = {"instances": [image_np.tolist()]}
        response = requests.post(OBJECT_DETECT_URL, json=payload)

        #### 위까지 완료해보기 
        result = response.json()["predictions"]
        image_ = draw_bounding_boxes(image_np, result)
        
        im = PIL.Image.fromarray(image_)
        rawBytes = io.BytesIO()
        im.save(rawBytes, "PNG")
        rawBytes.seek(0)
        
        img_base64 = base64.b64encode(rawBytes.read()).decode()

        message = "Success"

    except:

        img_base64 = str()

        message = "Fail"

    return img_base64, message



# 파일 업로드
import os
import glob
@bp.route('/fileUpload/<int:model_id>', methods=['GET','POST'])
def upload_file(model_id):
    if request.method == 'POST':
        f = request.files['file']
        
        image_name1 = f.filename
        image_path = './web/static/' + f.filename
        
        f.save(image_path)
        
        form = UploadForm()
        if request.method == "POST":
            print(image_name1)

            
            info = UploadInfo(image_name=image_name1, image_path=image_path)
            db.session.add(info)
            u = UploadInfo.query.filter(UploadInfo.image_name==image_name1)
            model = ModelList.query.get_or_404(model_id)
            # model.upload_set.append(u)
            db.session.commit()            



            ### 모델 실행
            from flask_restplus import reqparse
            from werkzeug.datastructures import FileStorage

            parser = reqparse.RequestParser()
            parser.add_argument('file', type=FileStorage, location='files')
            image = parser.parse_args()['file']

            if image.filename.split('.')[-1] in ['jpg', 'jpeg', 'png']:
                image_, message = predict(image)
            else:
                return {"status":"false", "result": { "classes": "", "imageshape": str(), "message": "Your file is not allowed!!" }}
            return {"status":"true", "result": { "classes": "", "message": message ,"imageshape": image_} }

            # print(image_path,'2332333333333333333333')

            # return render_template('model_result.html', image_name=image_name1, 
            #                         image_path=image_path, model=model)

        return render_template('model.datail', model_id=model_id)






