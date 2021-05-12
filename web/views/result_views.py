from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect, secure_filename

from web import db
from ..forms import UploadForm
from web.models import UploadInfo, ModelList


bp = Blueprint('result', __name__, url_prefix='/result')



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
        print(response)


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
        
        image_name = f.filename
        image_path = './web/static/' + f.filename
        
        f.save(image_path)

        form = UploadForm()
        if request.method == "POST":

            info = UploadInfo(image_name=image_name, image_path=image_path)
            db.session.add(info)
            u = UploadInfo.query.filter(UploadInfo.image_name==image_name)
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
                print({"status":"false", "result": { "classes": "", "imageshape": str(), "message": "Your file is not allowed!!" }})
            print({"status":"true", "result": { "classes": "", "message": message ,"imageshape": image_} })

            image_path2 = 'inputImage/'+image_name
            image_path2 = str(image_path2)
            return render_template('model_result.html', image_name=image_name, 
                                    image_path=image_path2, model=model)

        return render_template('model.datail', model_id=model_id)





