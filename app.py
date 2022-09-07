from flask import Flask, render_template, request
from graphics.perimetre import start_the_programe
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def drawing():
   js_data = start_the_programe()
   print(js_data)
   return render_template('drawing.html', value=js_data)



if __name__ == '__main__':
   app.run()