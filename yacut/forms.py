from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    URL,
    Optional,
    ValidationError,
)


class URLForm(FlaskForm):
    original_link = URLField(
        "Введите оригинальную ссылку",
        validators=[
            DataRequired(message="Обязательное поле"),
            URL(message="Введите URL"),
        ],
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Length(
                1, 16, message="Указано недопустимое имя для короткой ссылки"
            ),
            Optional(),
        ],
    )
    submit = SubmitField("Добавить")

    def validate_custom_id(self, field):
        if not field.data.isalpha() or not field.data.isascii():
            raise ValidationError(
                "Указано недопустимое имя для короткой ссылки"
            )
