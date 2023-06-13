from flask import Flask, redirect, url_for, render_template, request, session
from Code.channel_stats import channel_url, fun_calls
import random
import string


app = Flask(__name__)
app.secret_key = ''.join(random.choice((string.ascii_letters + string.digits)) for _ in range(15))


@app.route('/')
def welcome_page():
    return render_template('index.html')


@app.route('/output')
def output():
    # result={}
    channel_id = session.get('channel_id')
    no_ofvideos = int(str(session.get('videos_count')).replace(",", ""))
    print(no_ofvideos, type(no_ofvideos))
    stats = fun_calls(channel_id, no_ofvideos)
    return render_template('output.html', di=stats)


@app.route('/submit', methods=['POST'])
def app_fetch():
    if request.method == 'POST':
        if "search" in request.form:
            url_fetch = request.form['search']
            session['channel_id'] = channel_url(url_fetch)
        else:
            return "no channel id" + str(request.form)
        session['videos_count'] = request.form['videos_count']
        print(session)
    return redirect(url_for('output'))


if __name__ == '__main__ ':
    app.run(debug=True)
