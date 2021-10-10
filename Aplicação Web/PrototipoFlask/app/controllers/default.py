from flask import render_template

from app import app


#Decorator / pagina principal
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


#Redirecionamento pagina estados.html
@app.route("/estados")
def estados():
    return render_template('estados.html')


#Redirecionamento pagina 'municipios.html
@app.route("/municipios")
def municipios():
    return render_template('municipios.html')


if __name__ =="__main__":
    app.run(debug=True)