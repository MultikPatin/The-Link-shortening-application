from flask import flash, render_template, url_for, redirect

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short:
            if URLMap.query.filter_by(short=short).first():
                flash("Предложенный вариант короткой ссылки уже существует.")
                return render_template("index.html", form=form)
        else:
            short = get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        short_link = url_for("index_view", _external=True) + url_map.short
        return render_template("index.html", form=form, short=short_link)
    return render_template("index.html", form=form)


@app.route("/<string:short_id>", methods=["GET"])
def redirect_long_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
