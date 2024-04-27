from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField,IntegerField,TextAreaField,DateTimeField
from wtforms.validators import DataRequired,Email,Length

#신규 물품 작성 폼
class ItemForm(FlaskForm):
    itemname = StringField(
        "물품명",
        validators=[
            DataRequired(message="물품명은 필수입니다."),
        ]
    )
    item_quantity=IntegerField(
        "수량",
        validators=[
            DataRequired(message="수량은 필수입니다."),
        ]
    )
    time=DateTimeField(
        "날짜 시간",
        format="%Y-%m-%d %H:%M",
        validators=[
            DataRequired(message="날짜,시간을 정확히 입력해주세요. 예시)2020-04-07 17:26")
        ]
    )
    item_description=TextAreaField(
        "물품 설명",
        validators=[
            DataRequired(message="설명을 제대로 작성해주세요.")
        ]
    )
    submit = SubmitField("신규 물품 등록")

