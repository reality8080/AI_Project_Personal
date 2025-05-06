import pygame

def createBtn():
    btnLabels=[
        "BFS",
        "DFS",
        "UCS",
        "ID",
        "Greedy",
        "AStar",
        "IDAStar",
        "SimpleHillClimbing",
        "SHillClimbing",
        "RHillClimbing",
        "SimulatedAnne",
        "Beam Search",
        "Genetic Algorithm",
        "AND_OR",
        "NoOb",
        "SeePartOfMatrix",
        "CSPBacktracking",
        "QLearning",
        "QUIT"
    ]
    btns=[]
    cols=3
    colWidth=190
    startX=125
    startY=100

    for i, label in enumerate(btnLabels):
        col=i%cols
        row=i//cols
        
        x=startX+col*colWidth
        y=startY+row*60
        
        btns.append((label,pygame.Rect(x,y,180,40)))
    return btns