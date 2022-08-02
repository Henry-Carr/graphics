from flask import Flask, render_template, request
from graphics.perimetre import start_the_programe
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def drawing():
   
   year_built = 2022
   box = [20,20]
   #features = []
   features = [[0, 0, 0, 15, 5, 0, 5, 0, 0, "triangle feature thing1", ""]]
   """features = [[0, 0, 0, 70, 7, 7, 7, 0, 0, "triangle feature thing1", ""]
              ,[0, 0, 0, 50, 5, 5, 5, 0, 0, "triangle feature thing2", ""]
              ,[0, 0, 0, 30, 3, 3, 3, 0, 0, "triangle feature thing3", ""]
              ,[0, 0, 0, 10, 1, 1, 1, 0, 0, "triangle feature thing4", ""]]"""
   js_data = start_the_programe(box,features,year_built)
   print(js_data)
   return render_template('drawing.html', value=js_data)



if __name__ == '__main__':
   app.run()