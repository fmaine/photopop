__author__ = "Francois Maine"
__copyright__ = "Copyright 2020, freedom Partners"
__email__ = "fm@freedom-partners.com"

import os
import markupsafe
import flask
import json

import photopop.portfolio

app = flask.Flask('__name__',
            static_url_path='',
            static_folder='static',
            template_folder='photopop/templates')

_portfolio = photopop.portfolio.Portfolio()

@app.route("/")
def index():
    return flask.render_template('carousel.html')

@app.route("/Galerie/<name>")
def galerie(name):
    pf = _portfolio.get_collections()
    label = _portfolio.get_label(name)
    series = []
    for s in pf:
        if s['collection'] == name:
            series.append(s)
    return flask.render_template('album-list.html', series=series, label=label)

@app.route("/Album/<name>")
def album(name):
    print("Album : "+name)
    pf = _portfolio.get_collections()
    serie = None
    for s in pf:
        print(s['id'])
        if s['id'] == name:
            serie = s
    return flask.render_template('album.html', serie=serie)

@app.route("/Page/<name>")
def page(name):
    if name in ['tarifs','apropos','bio']:
        return flask.render_template(name+'.html')
    else:
        return flask.redirect('/',302)



# /images
# Workaround for gunicorn standalons
# Should be served directly in production by nginx
def images(path):
    return flask.send_file('/images/'+path)

# API Photos
@app.route("/photos/<name>", methods=['get'])
def photos(name):
    return json.dumps(_portfolio.get_photos(name))

# API series
@app.route("/series/", methods=['get'])
def series():
    return json.dumps(_portfolio.get_collections())


@app.route("/admin")
def admin():
    return "This is a test"

@app.route("/test")
def test():
    images = _portfolio.get_photos('Scandale')
    return flask.render_template('test.html',images=images)
