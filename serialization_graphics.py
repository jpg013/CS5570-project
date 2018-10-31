from graphics import *

def drawSerializationGraph(history=None,relations=[(1,2),(2,3),(3,2)]): #remove default parameters after testing
    
    transactionList = [1,2,3] #for testing
    
    #for transaction in history.transactions:
    #    transactionList.append(transaction.id)

    #==CONSTANTS==
    
    #screen-size
    xMax = 600
    yMax = 600
    
    circleScalingNumber = 20 #randomly chosen scaling number for circle size
    lineScalingNumber = 3 #randomly chosen scaling number for line offset

    #==END CONSTANTS==

    win = GraphWin('test', xMax, yMax)

    #==START SETUP CIRCLES==
    circleSize = (xMax+yMax)/circleScalingNumber #circle size based on screen-size and scaling number

    #center of screen
    centerX = xMax/2
    centerY = yMax/2

    #define left, right, up, and down boundaries for circles
    left = (xMax-centerX)/2
    right = (xMax+centerX)/2
    up = (yMax-centerY)/2
    down = (yMax+centerY)/2

    #define a cirlce at each boundary
    c1Point = Point(left,up)
    c2Point = Point(right,up)
    c3Point = Point(left,down)
    c4Point = Point(right,down)

    #used for drawing lines between circles
    #none is there to start indexing at 1 because of how the serialization graph is generated
    #(uses transaction id and there is never transaction id 0)
    circlePointList = [None,c1Point,c2Point,c3Point,c4Point]

    c1 = Circle(c1Point,circleSize)
    c2 = Circle(c2Point,circleSize)
    c3 = Circle(c3Point,circleSize)
    c4 = Circle(c4Point,circleSize)

    #==END SETUP CIRCLES==


    #==START DRAW LINES==
    baseOffset = circleSize/lineScalingNumber #see if there isn't a better way to do this
    offset = baseOffset
    
    #offset on x or offset on y
    x = False
    y = True
    for i in range(1,5):
        for j in range(1,5):
            
            if i == j:
                continue

            #only draw relations in the graph
            if tuple((i,j)) not in relations:
                continue

            #text for the label for the line
            labelText = str(i) + "-" + str(j)
            
            #not super pretty, but it only wastes a few cycles
            #checks if we want to draw lines up or down
            #(between 1 and 2 and 3 and 4 is horizontal, else, vertical)
            if (i>2 and j>2) or (i<=2 and j<=2):
                x = False
                y = True
            else:
                x = True
                y = False

            #offset for x
            if x:
                if i>j: #change the offset if we're going the OTHER way (instead of from 1 to 2, from 2 to 1)
                    offset = -baseOffset
                else:
                    offset = baseOffset
                    
                #build line
                lineLeftPoint = Point(circlePointList[i].x+offset,circlePointList[i].y)
                lineRightPoint = Point(circlePointList[j].x+offset,circlePointList[j].y)
                newLine = Line(lineLeftPoint,lineRightPoint)
                newLine.draw(win)

                #build label
                labelPoint = (Point((lineLeftPoint.x+lineRightPoint.x)/2,(lineLeftPoint.y+lineRightPoint.y)/2))
                label = Text(labelPoint,labelText)
                label.draw(win)
                
            #offset for y
            if y:
                if i>j: #change the offset if we're going the OTHER way (instead of from 1 to 2, from 2 to 1)
                    offset = -baseOffset
                else:
                    offset = baseOffset
                    
                #build line    
                lineLeftPoint = Point(circlePointList[i].x,circlePointList[i].y+offset)
                lineRightPoint = Point(circlePointList[j].x,circlePointList[j].y+offset)
                newLine = Line(lineLeftPoint,lineRightPoint)            
                newLine.draw(win)

                #build label
                labelPoint = (Point((lineLeftPoint.x+lineRightPoint.x)/2,(lineLeftPoint.y+lineRightPoint.y)/2))
                label = Text(labelPoint,labelText)
                label.draw(win)

    #==END DRAW LINES==

    fill = 'white'

    c1.setFill(fill)
    c2.setFill(fill)
    c3.setFill(fill)
    c4.setFill(fill)

    #draw the circle and the label if it's in the transactionList
    #yeah there's probably a better way to do this but uh, this is linear time too and it's on 4 items
    #we also have no plans to have more than 4 transactions so this is fine for the project
    if 1 in transactionList:
        c1.draw(win)
        Text(c1Point,"T1").draw(win)
    if 2 in transactionList:
        c2.draw(win)
        Text(c2Point,"T2").draw(win)
    if 3 in transactionList:
        c3.draw(win)
        Text(c3Point,"T3").draw(win)
    if 4 in transactionList:
        c4.draw(win)
        Text(c4Point,"T4").draw(win)

    win.getMouse()
    win.close()

drawSerializationGraph() #for testing purposes
