from web import db

# class Image_(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     input_img = db.Column(db.String(100), default='default.png', nullable=False)
#     result_img = db.Column(db.String(100), default='default.png')
#     create_date = db.Column(db.DateTime(), nullable=False)

# def __repr__(self):
#     return f"<User('{self.id}')>"

class ModelList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    model_detail = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

class UploadInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modellist_id = db.Column(db.Integer, db.ForeignKey('model_list.id', ondelete='CASCADE'))
    model = db.relationship('ModelList', backref=db.backref('upload_set', ))
    image_name = db.Column(db.String(1000), nullable=False)
    image_path = db.Column(db.String(1000), nullable=False)