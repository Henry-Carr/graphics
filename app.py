from flask import Flask, render_template, request
from graphics.perimetre import start_the_programe
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def drawing():

   #feature = [typelist, subtype, offset, length, height1, height2, inward, side, inneroffset, name, leadingto]

   year_built = 2022
   box = [20,20]
   #features = []
   features = [[0, 0, 15, 5, 0, 5, 0, 0, 0, "triangle feature thing1", ""]
              ,[0, 0, 19, 2, 0, 2, 0, 0, 0, "triangle feature thing2", ""]
              ,[0, 0, 16, 2, 2, 0, 0, 0, 0, "triangle feature thing2", ""]]

   """
   features = [[0, 0, 70, 5, 0, 5, 0, 0, 0, "triangle feature thing1", ""]
              ,[0, 0, 50, 5, 0, 5, 0, 0, 0, "triangle feature thing2", ""]
              ,[0, 0, 30, 5, 0, 5, 0, 0, 0, "triangle feature thing3", ""]
              ,[0, 0, 10, 5, 0, 5, 0, 0, 0, "triangle feature thing4", ""]]"""
   js_data = start_the_programe(box,features,year_built)
   print(js_data)
   return render_template('drawing.html', value=js_data)



if __name__ == '__main__':
   app.run()