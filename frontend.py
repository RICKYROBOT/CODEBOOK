"""
Program that uses sqlLite to store code snippets from a user.
UI design by QT designer
@author aspect
"""

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import SQL
import sys
import syntax_pars



class Ui_MainWindow(object):
    CurrentCat = ""
    CurrentSnip = ""

    resized = QtCore.pyqtSignal()

    #Setup Basic Layout and create the Widgets.
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(1300, 700)




        width = 1280
        height = 800
        # setting  the fixed size of window
        MainWindow.setFixedSize(width, height)

        #change Window icon.
        MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))




        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")




        # add CSS 2 LOGO / TITLE


        logoCSS = """
        /* Main LineEdit Setting */
        QLabel{
            
            color: #FFFFFF;
            font-size:46px;
            font-weight: bold;
            background-color: #333333;
            #background-image: url("header.png");
            background-repeat: no-repeat;
            background-position: center;

        }
        """        


        # creating a label widget
        # by default label will display at top left corner
        #self.label = QtWidgets.QLabel(self.centralwidget)


       
        #self.label.setText("RIRO'S\nCODE BOOK")
        #self.label.setText('<font color="#FFFFFF">RICKYROBOTS</font><br><font color="#6863ff" background-color="#000000" >CODE </font><font color="#dddddd">BOOK</font>')

        #self.label.setGeometry(QtCore.QRect(20, 10, 450, 70))
       # self.label.setBaseSize(QtCore.QSize(0, 0))

       # self.label.setStyleSheet(logoCSS)


        self.CategoriesBox = QtWidgets.QGroupBox(self.centralwidget)
        self.CategoriesBox.setGeometry(QtCore.QRect(10, 10, 150, 650))
        self.CategoriesBox.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        
        font.setBold(False)        
        font.setPointSize(8)
        
        self.CategoriesBox.setFont(font)
        self.CategoriesBox.setObjectName("CategoriesBox")



        #CategoryListBox
        self.CatListBox = QtWidgets.QListWidget(self.CategoriesBox)
        self.CatListBox.setGeometry(QtCore.QRect(10, 150, 150, 580))
        self.CatListBox.setObjectName("CatListBox")


        qrc1 = """
        /* Main LineEdit Setting */
        QListWidget{
            
            color: #FFF;
            font-size:18px;
               
        }

        /* when in hover */
        QListWidget:hover{
            
        }

        /* when has focus */
        QListWidget:focus{
            color: #fff; 
            background-color: #111;
        }
        """
        self.CatListBox.setStyleSheet(qrc1)





        # Populate the Categories (tables) List
        #Bind function that gets rows from categories table when changed.
        self.CatListBox.itemClicked.connect(self.UpdateSnipets)
        self.CatListBox.doubleClicked.connect(self.RenameCategory)

        #Catagory Edit (add) Box
        self.CatAddEdit = QtWidgets.QLineEdit(self.CategoriesBox)
        self.CatAddEdit.setGeometry(QtCore.QRect(10, 100, 141, 20))
        self.CatAddEdit.setObjectName("CatAddEdit")

        #Create the Add category Button, and bind AddCategory to it.
        self.CatAddBtn = QtWidgets.QPushButton(self.CategoriesBox)
        self.CatAddBtn.setGeometry(QtCore.QRect(10, 120, 141, 23))
        self.CatAddBtn.setObjectName("CatAddBtn")
        self.CatAddBtn.clicked.connect(self.AddCategory)

        #Remove a Category
        self.CatRemoveBtn = QtWidgets.QPushButton(self.CategoriesBox)
        self.CatRemoveBtn.setGeometry(QtCore.QRect(10, 740, 140, 23))
        self.CatRemoveBtn.setObjectName("CatRemoveBtn")
        self.CatRemoveBtn.clicked.connect(self.RemoveCategory)

       #removed
        #When user types in filter, we filter the ctegory list.
        self.CatFilterEdit = QtWidgets.QLineEdit(self.CategoriesBox)
        self.CatFilterEdit.setGeometry(QtCore.QRect(-10, -30, 141, 20))
        self.CatFilterEdit.setObjectName("CatFilterEdit")
        self.CatFilterEdit.textChanged.connect(self.UpdateCatList)


        self.label = QtWidgets.QLabel(self.CategoriesBox)
        self.label.setGeometry(QtCore.QRect(-110, 30, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        
        self.label.setFont(font)
        self.label.setObjectName("label")




        self.SnipetsBox = QtWidgets.QGroupBox(self.centralwidget)
        self.SnipetsBox.setGeometry(QtCore.QRect(180, 80, 220, 670))
        font = QtGui.QFont()
        font.setBold(False)
        
        self.SnipetsBox.setFont(font)
        self.SnipetsBox.setObjectName("SnipetsBox")

        qrc2 = """
        /* Main LineEdit Setting */
        QListWidget{
            
            color: #FFF;
            font-size:18px;
               
        }

        /* when in hover */
        QListWidget:hover{
            
        }

        /* when has focus */
        QListWidget:focus{
            color: #fff; 
            background-color: #111;
        }
        """
        self.SnipetsBox.setStyleSheet(qrc2)




        #Our Snipet List. When user clicks, we update the code window.
        self.SnipListBox = QtWidgets.QListWidget(self.SnipetsBox)
        self.SnipListBox.setGeometry(QtCore.QRect(10, 150, 220, 580))
        self.SnipListBox.setObjectName("SnipListBox")
        self.SnipListBox.itemClicked.connect(self.SetCode)
        self.SnipListBox.doubleClicked.connect(self.RenameSnip)


        self.SnipAddEdit = QtWidgets.QLineEdit(self.SnipetsBox)
        self.SnipAddEdit.setGeometry(QtCore.QRect(10, 100, 200, 20))
        self.SnipAddEdit.setObjectName("SnipAddEdit")

        #Button for Adding Codes to the currently selected Category(Table)
        self.SnipAddBtn = QtWidgets.QPushButton(self.SnipetsBox)
        self.SnipAddBtn.setGeometry(QtCore.QRect(10, 120, 200, 23))
        self.SnipAddBtn.setObjectName("SnipAddBtn")
        self.SnipAddBtn.clicked.connect(self.AddSnipet)

        #Button for removing Snipets
        self.SnipRemoveBtn = QtWidgets.QPushButton(self.SnipetsBox)
        self.SnipRemoveBtn.setGeometry(QtCore.QRect(10, 740, 200, 23))
        self.SnipRemoveBtn.setObjectName("SnipRemoveBtn")
        self.SnipRemoveBtn.clicked.connect(self.RemoveSnip)

       #removed
        #When user types in filter, we filter the snip list.
        self.SnipFilterEdit = QtWidgets.QLineEdit(self.SnipetsBox)
        self.SnipFilterEdit.setGeometry(QtCore.QRect(-10, -30, 220, 20))
        self.SnipFilterEdit.setObjectName("SnipFilterEdit")
        self.SnipFilterEdit.textChanged.connect(self.UpdateSnipets)


        self.label_2 = QtWidgets.QLabel(self.SnipetsBox)
        self.label_2.setGeometry(QtCore.QRect(-110, 30, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.label.setFont(font)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.CodeBox = QtWidgets.QGroupBox(self.centralwidget)
        self.CodeBox.setGeometry(QtCore.QRect(470, 50, 825, 661))
      

        font = QtGui.QFont()
        font.setBold(False)
       
        self.CodeBox.setFont(font)
        self.CodeBox.setObjectName("CodeBox")





        #Code for our Code Window


        self.CodeWindow = QtWidgets.QPlainTextEdit(self.CodeBox)
        self.CodeWindow.setStyleSheet("""QPlainTextEdit{
            font-family:'Consolas'; 
            color: #FFF; 
            font-size:14px;
            padding-left:15px;            
            background-color: #0f0f0f;}""")
    
       
        
        self.CodeWindow.setGeometry(QtCore.QRect(10, 30, 850, 700))
        # setting the minimum size
          



        

        font = QtGui.QFont()
        font.setBold(False)
        
        self.CodeWindow.setFont(font)
        self.CodeWindow.setObjectName("CodeWindow")
        self.CodeWindow.setEnabled(False)


        self.highlight = syntax_pars.PythonHighlighter(self.CodeWindow.document())
       


        #Code to Save Code Changes to The Currently selected Code
        self.CodeUpdateSaveBtn = QtWidgets.QPushButton(self.CodeBox)
        self.CodeUpdateSaveBtn.setGeometry(QtCore.QRect(10, 740,  840, 23))
        self.CodeUpdateSaveBtn.setObjectName("CodeUpdateSaveBtn")
        self.CodeUpdateSaveBtn.clicked.connect(self.UpdateCode)

        #update our Category List When Program finishes loading widgets,
        self.UpdateCatList()

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        # adding table_widget to central widget
        self.layout = QGridLayout()


        # place in LAYOUT


        self.CategoriesBox.setMinimumWidth(160)
        self.SnipetsBox.setMinimumWidth(220)

     
        self.CategoriesBox.setMaximumWidth(160)
        self.SnipetsBox.setMaximumWidth(220)

        self.CodeWindow.setMinimumWidth(400)
        #self.CodeBox.setMaximumWidth(self.CodeBox.sizeHint());      

        self.layout.addWidget(self.CategoriesBox, 0, 0)
        self.layout.addWidget(self.SnipetsBox, 0, 1)
        self.layout.addWidget(self.CodeBox, 0, 2)  
       
        self.centralwidget.setLayout(self.layout)
        # end

     



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RIRO'S CODE BOOK"))
        self.CategoriesBox.setTitle(_translate("MainWindow", "Categories"))
        self.CatAddBtn.setText(_translate("MainWindow", "Add"))
        self.CatRemoveBtn.setText(_translate("MainWindow", "Remove"))
        self.label.setText(_translate("MainWindow", "Filter"))
        self.SnipetsBox.setTitle(_translate("MainWindow", "Snippets"))
        self.SnipAddBtn.setText(_translate("MainWindow", "Add"))
        self.SnipRemoveBtn.setText(_translate("MainWindow", "Remove"))
        self.label_2.setText(_translate("MainWindow", "Filter"))
        self.CodeBox.setTitle(_translate("MainWindow", "Code"))
        self.CodeUpdateSaveBtn.setText(_translate("MainWindow", "Save"))


    # Button Event Handling
    def AddCategory(self):
        catExists = False
        catValid = True
        catList = [self.CatListBox.item(i).text() for i in range(self.CatListBox.count())]
        if(self.CatAddEdit.text()):
            for chars in self.CatAddEdit.text():
                if not chars.isalpha():
                    catValid = False
            if (catValid):
                for items in catList:
                    if(items == self.CatAddEdit.text()):
                        MessageBox("Error", "Category already exists.")
                        catExists = True
                if not (catExists):
                    SQL.addCategory(str(self.CatAddEdit.text()))
                    self.UpdateCatList()
            else:
                MessageBox("Error", "Category can only contain letters")
        else:
            MessageBox("Error", "No Category Entered")

    #Update CategoryList When we Start the program or add/remove Categories or change the filter
    def UpdateCatList(self):
        self.CatListBox.clear()
        for items in SQL.getCategories():
            if(self.CatFilterEdit.text()):
                if (self.CatFilterEdit.text().lower() in items[0].lower()):
                    self.CatListBox.addItem(items[0])
            else:
                self.CatListBox.addItem(items[0])

    #Update Code Snipets List when new Categories are selected
    def UpdateSnipets(self):
        self.CurrentCat = [item.text() for item in self.CatListBox.selectedItems()][0]
        self.SnipListBox.clear()
        self.CodeWindow.clear()
        self.CodeWindow.setEnabled(False)
        for items in SQL.getSnipets(self.CurrentCat):
            if(self.SnipFilterEdit.text()):
                if (self.SnipFilterEdit.text().lower() in items[0].lower()):
                    self.SnipListBox.addItem(items[0])
            else:
                self.SnipListBox.addItem(items[0])

    #Add Code Sniplet to current selected Category Table.
    def AddSnipet(self):
        snipExists = False
        snipList = [self.SnipListBox.item(i).text() for i in range(self.SnipListBox.count())]
        if(self.SnipAddEdit.text()):
            for items in snipList:
                if(items == self.SnipAddEdit.text()):
                    MessageBox("Error", "Snippet already exists.")
                    snipExists = True
            if(self.CurrentCat):
                if not (snipExists):
                    SQL.addSnipet(self.CurrentCat, str(self.SnipAddEdit.text()))
                    self.UpdateSnipets()
            else:
                MessageBox("Error", "No Category Selected.")
        else:
            MessageBox("Error", "No Snippet Name Entered.")

    def UpdateCode(self):
        if(self.CodeWindow.toPlainText()):
                if(self.CurrentSnip):
                    SQL.updateCode(self.CurrentCat, self.CurrentSnip, str(self.CodeWindow.toPlainText()))
                    MessageBox("Saved", "Code was saved successfully")
                else:
                    MessageBox("Error", "No Code Snippet Selected")
        else:
            MessageBox("Error", "No Snippet Name Entered.")

    def SetCode(self):
        self.CurrentSnip = [item.text() for item in self.SnipListBox.selectedItems()][0]
        self.CodeWindow.clear()
        self.CodeWindow.appendPlainText(SQL.getCode(self.CurrentCat, self.CurrentSnip))
        self.CodeWindow.verticalScrollBar().setValue(0)
        self.CodeWindow.setEnabled(True)

    def RemoveCategory(self):
        if ([item.text() for item in self.CatListBox.selectedItems()]):
            self.CatListBox.clear()
            self.SnipListBox.clear()
            SQL.removeCat(self.CurrentCat)
            self.CurrentCat = ""
            self.UpdateCatList()
        else:
            MessageBox("Error", "No Category Selected.")

    def RemoveSnip(self):
        if ([item.text() for item in self.SnipListBox.selectedItems()]):
            self.SnipListBox.clear()
            self.CodeWindow.clear()
            SQL.removeSnip(self.CurrentCat, self.CurrentSnip)
            self.CurrentSnip = ""
            self.UpdateSnipets()
            self.CodeWindow.setEnabled(False)
        else:
            MessageBox("Error", "No Snippets Selected.")

    def RenameCategory(self):
        catList = [self.CatListBox.item(i).text() for i in range(self.CatListBox.count())]
        catExists= False
        self.CurrentCat = [item.text() for item in self.CatListBox.selectedItems()][0]
        if (self.CurrentCat):
            newName = self.getText("Rename:", "New Category Name:")
            if (newName):
                if(newName.isalpha()):
                    for items in catList:
                        if(items == newName):
                            MessageBox("Error", "Category already exists.")
                            catExists = True
                    if not (catExists):
                        SQL.renamecategory(self.CurrentCat, newName)
                        self.UpdateCatList()
                else:
                    MessageBox("Error", "Category can only contain letters")
            else:
                if(newName != False):
                    MessageBox("Error", "You must enter a name")

    def RenameSnip(self):
        snipList = [self.SnipListBox.item(i).text() for i in range(self.SnipListBox.count())]
        snipExists= False
        self.CurrentSnip = [item.text() for item in self.SnipListBox.selectedItems()][0]
        if (self.CurrentSnip):
            newName = self.getText("Rename", "New Snippet Name:")
            if (newName):
                for items in snipList:
                    if(items == newName):
                        MessageBox("Error", "Snippet already exists.")
                        snipExists = True
                if not (snipExists):
                    SQL.renamesnip(self.CurrentCat, self.CurrentSnip, newName)
                    self.UpdateSnipets()
            else:
                if (newName != False):
                    MessageBox("Error", "You must enter a name")



    def getText(self, title, message):
        text, okPressed = QInputDialog.getText(self.centralwidget, title, message, QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
        if not okPressed:
            return False




def MessageBox(Title, Message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(Message)
    msg.setWindowTitle(Title)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


if __name__ == "__main__":
    #Setup the QT window and handle themes.
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    app.setStyle('Fusion')

    #Set Dark Theme Look/Feel
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(50, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.white)
    app.setPalette(palette)




    #Create the database if one doesn't exist.
    SQL.connect()

    #Show the window
    MainWindow.show()
    sys.exit(app.exec_())



