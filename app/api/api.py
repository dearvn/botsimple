import flask
from flask import request, jsonify
from worker.tasks import get_quote_exe

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Flask API</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/quote-get', methods=['GET'])
def api_get_quote():
    ticker = request.args.get('ticker')
    if ticker:
        get_quote_exe.delay(ticker)

    return jsonify([])

app.run()