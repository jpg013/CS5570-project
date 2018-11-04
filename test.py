from graphics import *
from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import generate_transactions

win = GraphWin("concurency control manager",400,400)

inp = Entry(Point(200,200),40)
inp.draw(win)
txt = Text(Point(200,100),"")
txt.draw(win)


while True:
    
    if win.getKey() == "Return":
        inpText = inp.getText()
        inp.setText("")
        try:
            hist = HistoryQueryBuilder(inpText).process()
            t = hist.pretty_print()
            txt.setText(t)
        except Exception as e:
            print(e)
            txt.setText(e)
