import os
import re
from flask import Flask, render_template, url_for, redirect, request
from exam import search


app = Flask(__name__)


@app.route("/")
def search_page():
    if request.args:
        results = get_results(request.args)
        return render_template('search_page.html', results=results, query=request.args['query'])
    return render_template('search_page.html')


def get_results(args):
    return search(args['query'], args['method'], top=int(args['top']))


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000)))
