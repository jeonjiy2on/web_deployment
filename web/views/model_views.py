
from datetime import datetime
from flask import Blueprint, render_template, url_for, request, send_file
from werkzeug.utils import redirect, secure_filename
from .. import db
from web.models import ModelList, UploadInfo
from ..forms import ModelForm, UploadForm
from flask_wtf.file import FileField


bp = Blueprint('model', __name__, url_prefix='/model')

# 모델 목록
@bp.route('/list/')
def _list():
    # get방식으로 요청한 url에서 page값 5를 가져올때 사용
    page = request.args.get('page', type=int, default=1)
    model_list = ModelList.query.order_by(ModelList.id) 
    # 조회한 데이터 model_list에 페이징 적용
    model_list = model_list.paginate(page, per_page=5)
    return render_template('model_list.html', model_list=model_list)
    
# 모델 상세 조회
@bp.route('/detail/<int:model_id>/')
def detail(model_id):
    model = ModelList.query.get_or_404(model_id)
    return render_template('model_detail.html', model=model)

# 모델 등록
@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = ModelForm()
    if request.method == "POST" and form.validate_on_submit():
        model = ModelList(model_name=form.model_name.data, 
                          model_detail=form.model_detail.data,
                          create_date=datetime.now())
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('model._list'))
    return render_template('model_form.html', form=form)
