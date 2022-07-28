from ast import Pass
from flask import Flask, render_template, request
from graphics.perimetre import start_the_programe
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def drawing():
   
   year_built = 2022
   box = [20,20]
   #features = []
   features = [[0, 0, 0, 25, 5, 5, 4, 0, 0, "triangle feature thing1", ""]]
   #features = [[0, 0, 0, 45, 5, 15, 14, 0, 0, "triangle feature thing1", ""]
   #          ,[0, 0, 0, 8, 1, 1, 1, 0, 0, "triangle feature thing2", ""]]
   js_data = start_the_programe(box,features,year_built)
   print(js_data)
   return render_template('drawing.html', value=js_data)



if __name__ == '__main__':
   app.run()