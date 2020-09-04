import sys
sys.path.insert(0, "C:/Users/41774/Desktop/game folder/util")


from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
import sudoku_crapper as crapper

import suduko_ui
from random import seed
from random import randint
from datetime import datetime

seed(datetime.now())

class Main(QMainWindow):
    
    
    
    def __init__(self):
        super(Main, self).__init__()
        self.ui = suduko_ui.Ui_MainWindow()
        self.ui.setupUi()
        self.ui.show()

        self.diff = "3"
        self.difficulty_list = ["Easy", "Medium", "Hard"]
        self.ID = 0
        self.set_grid()
        self.ui.pushButton_15.clicked.connect(self.difficulty_change)
        self.ui.pushButton_14.clicked.connect(self.next)
        self.ui.pushButton_11.clicked.connect(self.give_hint)
        self.ui.pushButton_3.clicked.connect(self.check_finish)


    def set_grid(self):
        grid, self.ID = crapper.sudoku_crapper("http://www.menneske.no/sudoku/eng/random.html?diff=" + self.diff)
        self.solved_grid,_ = crapper.sudoku_crapper("http://www.menneske.no/sudoku/eng/solution.html?number=" + str(self.ID)) 




        for i in range(9):
            for j in range(9):
                 
                
                
                string = "Button" + str(i) + str(j)
                tmp = self.ui.findChild(QPushButton, string)
                tmp.setEnabled(True)
                if grid[i][j] == "-1":
                    
                    tmp.setText(" ")
                else:    
                    tmp.setText(grid[i][j])
    
    def difficulty_change(self):
        string = self.ui.pushButton_15.text()
        index = self.difficulty_list.index(string)
        index += 1
        self.diff = str(int(self.diff) + 1)
        if index == 3:
            index = 0
            self.diff = "3" 
        
        self.ui.pushButton_15.setText(self.difficulty_list[index])
        self.set_grid()

    def next(self):
        self.set_grid()


    
    




    

    def give_hint(self):
        list = []
        for i in range(9):
            for j in range(9):
                
                string = "Button" + str(i) + str(j)
                tmp = self.ui.findChild(QPushButton, string)
                if tmp.text() == " ":
                    list.append(tmp)

        if len(list) != 0:
            ind = randint(0, len(list) - 1)
            string = list[ind].objectName()
            i = int(string[-2])
            j = int(string[-1])
            list[ind].setText(str(self.solved_grid[i][j]))
            list[ind].setEnabled(False)

    def fake(self):
        pass

    def check_finish(self):
        num = 0
        for i in range(9):
            for j in range(9):
                string = "Button" + str(i) + str(j)
                tmp = self.ui.findChild(QPushButton, string)
                if tmp.text() != str(self.solved_grid[i][j]):
                    num += 1
        if num == 0:
            print("you have finished the suduko! click next for more game")
        else:
            print("you have " + str(num) + " unfinished/inccorect numbers! keep working!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    

    sys.exit(app.exec_())