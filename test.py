
from graphics import *
from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import generate_transactions
from main import checks
from serialization_graphics import drawSerializationGraph
from math import floor


def undrawGraphics(graphics):
    if graphics == None:
        return
    for circle in graphics[0]:
        circle.undraw()
    for line in graphics[1]:
        line.undraw()
    for label in graphics[2]:
        label.undraw()

def transformText(text):
    ret = ""
    i = 0
    for char in text:
        ret += char
        if char == '\n':
            i = 0
        if i == 100:
            ret += '\n'
            i = 0
        i += 1
    
    return ret
        
        


wind = GraphWin("concurency control manager",1100,900)

inp = Entry(Point(650,600),40)
inp.draw(wind)
repText = Text(Point(650,300),"")
repText.draw(wind)

graphics = None

while True:
    if wind.checkKey() == "Return":
        undrawGraphics(graphics)
        inpText = inp.getText()
        inp.setText("")
        repText.setText("")
        try:
            hist = HistoryQueryBuilder(inpText).process()
            ret = checks(hist)
            rep = ret[0]
            serOrNot = ret[1][0]
            conflicts = ret[1][1]
            graphics = drawSerializationGraph(wind,hist,conflicts)
            repString = rep.give_report()
            if(serOrNot):
                repString += "The history is serializable"
            else:
                repString += "The history is not serializable"
            formatRepString = transformText(repString)
            print(formatRepString)
            repText.setText(formatRepString)
            
        except Exception as e:
            print(e)
            repText.setText(e)




    
