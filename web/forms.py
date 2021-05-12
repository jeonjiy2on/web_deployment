
from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired

class ModelForm(FlaskForm):
    model_name = StringField('모델명', validators=[DataRequired('모델명은 필수 입력 항목입니다.')])
    model_detail = TextAreaField('모델 설명', validators=[DataRequired('모델 설명은 필수 입력 항목입니다.')])

class UploadForm(FlaskForm):
    image_name = StringField('이미지명', validators=[DataRequired()])
    image_path = StringField('이미지 경로', validators=[DataRequired()])
