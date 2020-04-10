from flask import request, render_template, make_response
from flask import current_app as app


@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome you to Page!!'
