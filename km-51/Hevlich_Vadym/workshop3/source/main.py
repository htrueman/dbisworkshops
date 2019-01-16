from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = 'secret123'


@app.route('/api/<action>', methods=['GET'])
def apiGet(action):
    if action == "number":
        if 'number' not in session.keys():
            number = ''
        else:
            number = session['number']
        if not number:
            number = request.cookies.get('number') if request.cookies.get('number') else ''
        return render_template("number.html", number=number)
    else:
        return render_template("404.html")


@app.route('/api', methods=['POST'])
def apiPost():
    red = redirect(url_for('apiGet', action="number"))
    response = make_response(red)

    if request.form["action"] == "number_update":
        if 'number' not in session.keys():
            session['number'] = int(request.form["number"])
        else:
            session['number'] = max(int(request.form["number"]), session['number'])
        response.set_cookie('number', str(session['number']))
    elif request.form["action"] == "clear_session":
        session.clear()
    elif request.form["action"] == "clear_cookie":
        response.set_cookie('number', '', expires=0)
    return red
