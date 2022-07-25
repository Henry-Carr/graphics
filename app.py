from ast import Pass
from flask import Flask, render_template, request
from graphics.perimetre import start_the_programe
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def drawing():
   
   box = [20,20]
   #features = [[0, 0, 0, 7, 3, 0, 4, 0, 0, "triangle feature thing1", ""]
   #          ,[0, 0, 0, 8, 1, 1, 1, 0, 0, "triangle feature thing2", ""]]
   features = []
   js_data = start_the_programe(box,features)
   print(js_data)
   return render_template('drawing.html', value=js_data)



if __name__ == '__main__':
   app.run()