from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect, secure_filename

from web import db
from ..forms import UploadForm
from web.models import UploadInfo, ModelList

### 원본 사진 저장/출력까지 잘 되는 상태



bp = Blueprint('result', __name__, url_prefix='/result')


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

            # TS실행시키는 코드 추가
            # ??????????????????????????????????????



            
            image_path2 = 'inputImage/'+image_name
            image_path2 = str(image_path2)
            return render_template('model_result.html', image_name=image_name, 
                                    image_path=image_path2, model=model)

        return render_template('model.datail', model_id=model_id)





