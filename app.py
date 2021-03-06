import json
from flask import (Flask, render_template, redirect,
                   url_for, request, make_response,
                   flash)
from options import DEFAULTS

app = Flask(__name__)
app.secret_key = '1s2d3vv5g6h67yrwexcvb'

# Return a Python dictionary stored in the requester's (browser) 'Character' cookie.
# If nothing is there send an empty dictionary.
def get_saved_data():
    try:
        data = json.loads(request.cookies.get('character'))
    except TypeError:
        data = {}
    return data

@app.route('/')
def index():
    return render_template('index.html', saves=get_saved_data())

@app.route('/builder')
def builder():
    return render_template(
        'builder.html',
        saves=get_saved_data(),
        options=DEFAULTS
    )

@app.route('/save', methods=['POST'])
def save():
    flash("Alright! That look's nice :)")
    # In our response we will send a redirect to the browser.
    response = make_response(redirect(url_for('builder')))
    data = get_saved_data()
    # Grab the items that was POSTed from the form sent by the browser,
    # and turn them into a dict to update or add into data.
    data.update(dict(request.form.items()))
    # Name the cookie as 'character' and load it with a JSONifed version of data.
    response.set_cookie('character', json.dumps(data))
    return response

app.run(debug=True, host='0.0.0.0', port=8001)