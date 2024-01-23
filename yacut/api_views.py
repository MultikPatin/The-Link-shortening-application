from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short_id, is_link


@app.route("/api/id/", methods=["POST"])
def add_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")

    original = data.get("url")
    if not original or original == "":
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not is_link(original):
        raise InvalidAPIUsage("Введите URL")

    short: str = data.get("custom_id")
    if short:
        if len(short) > 16 or not short.isalpha() or not short.isascii():
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки"
            )
        if URLMap.query.filter_by(short=short).first():
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует."
            )
    else:
        short = get_unique_short_id()

    url_map = URLMap(original=original, short=short)
    db.session.add(url_map)
    db.session.commit()
    context = dict(
        url=url_map.original,
        short_link=url_for("index_view", _external=True) + short,
    )
    return jsonify(context), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_long_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.to_dict()["url"]}), HTTPStatus.OK
