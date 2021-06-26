from flask import Flask
from flask import Flask, render_template, request, json
app = Flask(__name__)
@app.route("/")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


def main():
    #return "Welcome!"
    return render_template('index.html')
if __name__ == "__main__":
    app.run()    

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>Todos los campos están bien !!</span>'})
    else:
        return json.dumps({'html':'<span>Ingrese la información requerida</span>'})


@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']