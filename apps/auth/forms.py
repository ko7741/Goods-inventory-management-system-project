from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired,Email,Length

class SignUpForm(FlaskForm):
    username = StringField(
        "사용자명",
        validators=[
            DataRequired(message="사용자명은 필수입니다."),
        ]
    )
    useremail=StringField(
        "메일 주소",
        validators=[
            DataRequired(message="메일 주소는 필수입니다."),
            Email("메일 주소의 형식으로 입력해 주세요."),
        ]
    )
    password=PasswordField(
        "비밀번호",
        validators=[
            DataRequired(message="비밀번호는 필수입니다.")
        ]
    )

    submit = SubmitField("신규 관리자 등록")

class LoginForm(FlaskForm):
    useremail = StringField(
        "메일 주소",
        validators=[
            DataRequired("이메일 주소는 필수입니다. "),
            Email("이메일 주소의 형식으로 입력하세요. "),
        ],
    )
    password = PasswordField("비밀번호", validators=[DataRequired("비밀번호는 필수입니다. ")])
    submit = SubmitField("로그인")