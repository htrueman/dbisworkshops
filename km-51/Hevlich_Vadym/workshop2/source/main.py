from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello from Flask<h1>'


repo_dictionary = {
    "user": "test_user",
    "deep_link": "https://github.com/igortereshchenko/dbisworkshops",
    "relative_dir": "some/path/",
}

user_dictionary = {
    "username": "test_users",
    "password": "password"
}

available_dictionary = dict.fromkeys(['repo_dictionary', 'user_dictionary'], "dict_name")


@app.route('/api/<action>', methods=['GET'])
def apiGet(action):
    if action == "repo":
        return render_template("repo.html", repo=repo_dictionary)
    elif action == "user":
        return render_template("user.html", user=user_dictionary)
    elif action == "all":
        return render_template("all.html", repo=repo_dictionary, user=user_dictionary)
    else:
        return render_template("404.html", action_value=action, available=available_dictionary)


@app.route('/api', methods=['POST'])
def apiPost():
    if request.form["action"] == "repo_update":
        repo_dictionary["user"] = request.form["user"]
        repo_dictionary["deep_link"] = request.form["deep_link"]
        repo_dictionary["relative_dir"] = request.form["relative_dir"]

        return redirect(url_for('apiGet', action="all"))

    elif request.form["action"] == "user_update":
        user_dictionary["username"] = request.form["username"]
        user_dictionary["password"] = request.form["password"]

        return redirect(url_for('apiGet', action="all"))


if __name__ == '__main__':
    app.run(debug=True)
