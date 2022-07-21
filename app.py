from ast import Pass
from flask import Flask, render_template, request
from graphics.perimetre import initial_perim, perimeter_length

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def drawing():
   roomlength = 9
   roomwidth = 8
   list = []
   list[0]=initial_perim(roomlength,roomwidth)
   perimeter_length(list[0],0)
   return render_template('drawing.html', value=list)



if __name__ == '__main__':
   app.run()