# Rafael Abreu Fonseca - RA 21700439
from flask import Flask, render_template, request, session, redirect, url_for, escape
from db import DB

# Flask Object
app = Flask(__name__)
db = DB()


# Route to /
@app.route('/')
def home():
    return render_template('index.html')


# Route to /register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db.insert_url(db.connect(), request.form.get('old_url'))
        return render_template('confirme.html', url=db.find_last_url(db.get_cursor()))

    return render_template('index.html', erro='METHOD ERRADO!!!')


# Route to /redirecionador
@app.route('/redirecionador/<url>')
def redirecionador(url):
    new_url = db.change_url_by_old_url(db.get_cursor(), url)
    db.update_acessos(db.connect(), url)
    return redirect(new_url)


# Route to /relatorio
@app.route('/relatorio')
def relatorio():
    data = db.get_all(db.get_cursor())
    data.sort(key=lambda acessos: acessos[2], reverse=True)

    return render_template('relatorio.html', db=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/405')
def page_really_not_found():
    return render_template('405.html')

#  start app
if __name__ == '__main__':
    app.run(debug=True)
