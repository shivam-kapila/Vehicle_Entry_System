import requests
import json 
from flask import Flask, escape, request,  render_template

app = Flask(__name__,)


@app.route('/')
def home():
    return render_template("home.html", name = "Shivam")

@app.route('/register')
def register():
    dict = {'phy':50,'che':60,'maths':70}
    return render_template("register.html")

@app.route('/entry')
def entry():
    dict = {'phy':50,'che':60,'maths':70}
    return render_template("entry.html", result = dict)
@app.route('/registrations')
def registrations():
    dict = {'phy':50,'che':60,'maths':70}
    return render_template("registrations.html", result = dict)
@app.route('/entries')
def entries():
    dict = {'phy':50,'che':60,'maths':70}
    return render_template("entries.html", result = dict)
        
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug='True', port=3000)
