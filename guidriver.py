import io
import csv
import folium
from pathlib import Path
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
import pathfinding as search
import graphdriver as g
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QWidget):
    bus_stop = []
    lrt = []
    hdb = []
    types = []
    type = None;
    loaded = False
    lat = 0
    lon = 0
    loadedfilename = ""

    #######################################################################
    # Setup UI widgets
    def setupUi(self, MainWindow):

        font = QtGui.QFont()  # init font obj
        font.setFamily("Verdana")  # set font style
        font.setPixelSize(7)  # set pixel size
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 450)
        MainWindow.setFixedSize(850, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(113, 370, 83, 34))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radio_fastest = QtWidgets.QRadioButton(self.widget)
        self.radio_fastest.setObjectName("radio_fastest")
        self.radio_fastest.setFont(font)
        self.verticalLayout.addWidget(self.radio_fastest)
        self.radio_shortest = QtWidgets.QRadioButton(self.widget)
        self.radio_shortest.setObjectName("radio_shortest")
        self.radio_shortest.setFont(font)
        self.verticalLayout.addWidget(self.radio_shortest)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(220, 370, 150, 62))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radio_dijkstra = QtWidgets.QRadioButton(self.widget1)
        self.radio_dijkstra.setObjectName("radio_dijkstra")
        self.radio_dijkstra.setFont(font)
        self.verticalLayout_2.addWidget(self.radio_dijkstra)
        self.radio_astar = QtWidgets.QRadioButton(self.widget1)
        self.radio_astar.setFont(font)
        self.radio_astar.setObjectName("radio_astar")
        self.verticalLayout_2.addWidget(self.radio_astar)
        self.radio_breathfirst = QtWidgets.QRadioButton(self.widget1)
        self.radio_breathfirst.setFont(font)
        self.radio_breathfirst.setObjectName("radio_breathfirst")
        self.verticalLayout_2.addWidget(self.radio_breathfirst)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(200, 370, 20, 62))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.combo_end_pt = QtWidgets.QComboBox(self.centralwidget)
        self.combo_end_pt.setGeometry(QtCore.QRect(140, 343, 421, 20))
        self.combo_end_pt.setFont(font)
        self.combo_end_pt.setObjectName("combo_end_pt")
        self.help_button = QtWidgets.QPushButton(self.centralwidget)
        self.help_button.setGeometry(QtCore.QRect(5, 370, 91, 61))
        self.help_button.setFont(font)
        self.help_button.clicked.connect(self.help)
        self.help_button.setObjectName("help_button")
        self.combo_end_type = QtWidgets.QComboBox(self.centralwidget)
        self.combo_end_type.setGeometry(QtCore.QRect(65, 343, 71, 19))
        self.combo_end_type.currentIndexChanged[str].connect(self.load_combo_end_pt)
        self.combo_end_type.setObjectName("combo_end_type")
        self.combo_end_type.setFont(font)
        self.combo_start_type = QtWidgets.QComboBox(self.centralwidget)
        self.combo_start_type.setGeometry(QtCore.QRect(65, 320, 71, 19))
        self.combo_start_type.setFont(font)
        self.combo_start_type.currentIndexChanged[str].connect(self.load_combo_start_pt)
        self.combo_start_type.setObjectName("combo_start_type")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(5, 343, 43, 16))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.combo_start_pt = QtWidgets.QComboBox(self.centralwidget)
        self.combo_start_pt.setGeometry(QtCore.QRect(140, 320, 421, 20))
        self.combo_start_pt.setFont(font)
        self.combo_start_pt.setObjectName("combo_start_pt")
        self.button_calculate = QtWidgets.QPushButton(self.centralwidget)
        self.button_calculate.setGeometry(QtCore.QRect(360, 370, 98, 61))
        self.button_calculate.clicked.connect(self.calculate)
        self.button_calculate.setFont(font)
        self.button_calculate.setObjectName("button_calculate")
        self.button_load = QtWidgets.QPushButton(self.centralwidget)
        self.button_load.setGeometry(QtCore.QRect(462, 370, 98, 61))
        self.button_load.setFont(font)
        self.button_load.clicked.connect(self.getFile)
        self.button_load.setObjectName("button_load")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFont(font)
        self.label.setGeometry(QtCore.QRect(5, 320, 51, 16))
        self.label.setObjectName("label")
        ###################################################################################################################
        m = folium.Map(location=[1.357779, 103.825951],
                       zoom_start=11)  # loads folium map with singapore as starting position
        data = io.BytesIO()
        m.save(data, close_file=False)  # saves folium map
        self.map = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.map.setZoomFactor(0.6)
        self.map.setHtml(data.getvalue().decode())  # loads folium html map into webkit engine
        self.map.setObjectName("map")
        self.map.setGeometry(QtCore.QRect(5, 2, 553, 311))
        ####################################################################################################################
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(565, 2, 281, 431))
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 854, 18))
        self.menubar.setObjectName("menubar")
        self.menubar.setFont(font)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionTeam_Information = QtWidgets.QAction(MainWindow)
        self.actionTeam_Information.setObjectName("actionTeam_Information")
        self.actionTeam_Information.setFont(font)
        self.actionTeam_Information.triggered.connect(self.teaminfo)
        self.menuFile.addAction(self.actionTeam_Information)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    ##############################################################################################
    # sets widget text
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Punggol Router", "Punggol Router"))
        self.radio_fastest.setText(_translate("Punggol Router", "Time (Minutes)"))
        self.radio_shortest.setText(_translate("Punggol Router", "Distance (Meters)"))
        self.radio_dijkstra.setText(_translate("Punggol Router", "Dijkstra\'s (Shortest Route)"))
        self.radio_astar.setText(_translate("Punggol Router", "A* Search (Shortest Route)"))
        self.radio_breathfirst.setText(_translate("Punggol Router", "Breath First (Least Transfers)"))
        self.help_button.setText(_translate("Punggol Router", "Help"))
        self.label_2.setText(_translate("Punggol Router", "Destination:"))
        self.button_calculate.setText(_translate("Punggol Router", "Calculate"))
        self.button_load.setText(_translate("Punggol Router", "Load Map"))
        self.label.setText(_translate("Punggol Router", "Starting point:"))
        self.menuFile.setTitle(_translate("Punggol Router", "About"))
        self.actionTeam_Information.setText(_translate("Punggol Router", "Team Information"))

    #############################################################################################

    #############################################################################################
    def readFile(self, file):  # reads data from csv dataset and loads into graph and vertex object
        self.bus_stop.append("")
        self.lrt.append("")
        self.hdb.append("")

        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_cnt = 0
            size = 0
            self.lat = 0
            self.lon = 0
            for row in csv_reader:  # loop to add sum node lon lat in dataset, also adds respective nodes to their respective arrays types e.g.(bus stops/lrt/hdb)
                if line_cnt == 0: # skips first row
                    line_cnt += 1
                else:
                    size += 1
                    self.lat += float(row[2])
                    self.lon += float(row[3])
                    if row[1] == 'Bus Stop':
                        self.bus_stop.append(row[0])
                    elif row[1] == 'LRT':
                        self.lrt.append(row[0])
                    elif row[1] == 'HDB':
                        self.hdb.append(row[0])

            self.lat = self.lat / size  # gets avg lat to set folium map to the avg location of all nodes in the file
            self.lon = self.lon / size  # gets avg lon to set folium map to the avg location of all nodes in the file

            self.types = list(dict.fromkeys(self.types))  # 'removes' duplicate types only leaving unique ones

        self.loadFile()#call loadfile funtion


    ###################################################################################################################
    def initGraph(self, type): #function to init and load graph 'datastructure'
        graph = g.Graph()
        with open(self.loadedfilename, 'r') as csv_file: #open csv file
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_cnt = 0
            for row in csv_reader:  # loop to add all nodes with their lon and lat
                if line_cnt == 0:
                    line_cnt += 1
                else:
                    graph.add_vertex(row[0], float(row[3]), float(row[2]), row[1])

        with open(self.loadedfilename, 'r') as csv_file: #open csv file
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_cnt = 0
            for row in csv_reader: # loop to thru rows
                if line_cnt == 0:
                    line_cnt += 1
                else:
                    if type == 'fastest': #if type is fastest, we need to init weight to be travel time
                        for i in range(4, len(row), 4): #for loop to add edges of each node
                            if (row[i] or row[i + 1]) != "":
                                if row[i + 3] == 'Bus':
                                    graph.add_edge(row[i + 2], row[i + 3], row[0], row[i + 1], float(row[i]) / 329)
                                    #adds edge and converts edge weight originally based on travel distance into
                                     #travel time by dividing est travelspeed with the weight
                                elif row[i + 3] == 'LRT':
                                    graph.add_edge(row[i + 2], row[i + 3], row[0], row[i + 1], float(row[i]) / 400)
                                    #adds edge and converts edge weight originally based on travel distance into
                                     #travel time by dividing est travelspeed with the weight
                                elif row[i + 3] == 'walk':
                                    graph.add_edge(row[i + 2], row[i + 3], row[0], row[i + 1], float(row[i]) / 80)
                                    #adds edge and converts edge weight originally based on travel distance into
                                     #travel time by dividing est travelspeed with the weight
                            else:
                                break
                    elif type == 'shortest': # if type is shortest we just need to to init weight without doing anything, as original dataset already uses distance as weight
                        for i in range(4, len(row), 4): #for loop to add edges of each node
                            if (row[i] or row[i + 1]) != "":
                                graph.add_edge(row[i + 2], row[i + 3], row[0], row[i + 1], float(row[i])) #adds edge
                            else:
                                break
        return graph # returns graph object






    def calculate(self): # calculates route
        if self.loaded: #checks if there is a file loaded
            if self.radio_fastest.isChecked(): #inits type variable based on radiobutton checked
                self.type = 'fastest'
            else: #inits type variable based on radiobutton checked
                self.type = 'shortest'
            if(self.combo_start_pt.currentText()==""):
                QMessageBox.warning(self, "Error", "Please select start point!", QtWidgets.QMessageBox.Ok)
            elif(self.combo_end_pt.currentText()==""):
                QMessageBox.warning(self, "Error", "Please select end point!", QtWidgets.QMessageBox.Ok)
            elif(self.combo_end_pt.currentText()==self.combo_start_pt.currentText()):
                QMessageBox.warning(self, "Error", "Starting point and destination cannot be the same!", QtWidgets.QMessageBox.Ok)
            else:
                graph = self.initGraph(self.type)  #calls init graph function
                start_node = graph.get_vertex(self.combo_start_pt.currentText())  #gets start node based on combobox value
                end_node = graph.get_vertex(self.combo_end_pt.currentText())    #gets dest node based on combobox value
                if self.radio_dijkstra.isChecked(): #runs dijkstra pathfinding if dijkstra radiobutton is check
                    output = search.dijkstra(graph, start_node, end_node, self.type)
                elif self.radio_astar.isChecked(): #runs A* searh pathfinding if A* search radiobutton is check
                    output = search.astar(graph, start_node, end_node, self.type)
                else: #run breathfirst search to find least transfers
                    output = search.breathFirst(graph, start_node, end_node, self.type)

                self.print_directions(output) #calls print direction function
        else:
            QMessageBox.warning(self, "Error", "Please load a dataset!", QtWidgets.QMessageBox.Ok)





    def print_directions(self, output):  # prints directions, total travel time/distance and number of edges checked
        self.textEdit.clear() #clears current text off the text 'display'
        self.textEdit.append('Travel Directions') #write text


        if output: #prints directions
            for directions in output[0][0]:
                self.textEdit.append('===============================================')
                self.textEdit.append(directions)
            data = io.BytesIO()
            output[0][1].save(data, close_file=False)
            self.map.setHtml(data.getvalue().decode())
            self.textEdit.append('\n+++++++++++++++++++++++++++++++++++++++++++++++')
            if self.type == 'fastest': #prints travel time if type selected is fastest
                self.textEdit.append('Total Travel Time = ' + "{0:.2f} Mins".format(output[1]))

            elif self.type == 'shortest': #prints travel dist if type selected is shortest
                self.textEdit.append('Total Distance Travelled: ' + "{0:.2f} Meters".format(output[1]))
            self.textEdit.append('Number of Transfers: ' + str(output[0][2]))
            self.textEdit.append('\n+++++++++++++++++++++++++++++++++++++++++++++++')
            self.textEdit.append('Number of edges checked: ' + str(output[2]))

        else:
            self.textEdit.append('No Route Found Sorry')

    def loadFile(self):  # loads file data to gui, sets combobox values, and reset map locations, sets default radiobutton options
        self.loaded = True
        self.textEdit.clear()
        self.textEdit.append('Data Loaded!!!!!!!')
        self.textEdit.append('===============================================')
        self.textEdit.append('Dataset Contains:')
        self.textEdit.append(str(len(self.lrt)) + ' Lrt Stations')
        self.textEdit.append(str(len(self.bus_stop)) + ' Bus stops')
        self.textEdit.append(str(len(self.hdb)) + ' HDB Flats')
        self.radio_fastest.setChecked(True)
        self.radio_astar.setChecked(True)
        self.combo_start_type.addItems(['LRT', 'Bus Stop', 'HDB'])
        self.combo_end_type.addItems(['LRT', 'Bus Stop', 'HDB'])
        self.combo_end_type.setCurrentIndex(2)
        m = folium.Map(location=[self.lat, self.lon], zoom_start=15)
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map.setHtml(data.getvalue().decode())

    def getFile(self): #opens qfiledialog for user to select a dataset
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = None
        fileName = QFileDialog.getOpenFileNames(None, 'Select Dataset', "./Datasets", None, None, options=options)
        if fileName[1]!='':
            fileName = Path(fileName[0][0]).name
            self.loadedfilename = 'Datasets\\' + fileName
            self.readFile(self.loadedfilename)

    def load_combo_start_pt(self, type): #loads combo_start_pt with nodes based on current values of combo_start_type value
        if type == 'Bus Stop':
            self.combo_start_pt.clear()
            self.combo_start_pt.addItems(self.bus_stop)
        elif type == 'LRT':
            self.combo_start_pt.clear()
            self.combo_start_pt.addItems(self.lrt)
        elif type == 'HDB':
            self.combo_start_pt.clear()
            self.combo_start_pt.addItems(self.hdb)

    def load_combo_end_pt(self, type):#loads combo_end_pt with nodes based on current values of combo_end_type_value
        if type == 'Bus Stop':
            self.combo_end_pt.clear()
            self.combo_end_pt.addItems(self.bus_stop)
        elif type == 'LRT':
            self.combo_end_pt.clear()
            self.combo_end_pt.addItems(self.lrt)
        elif type == 'HDB':
            self.combo_end_pt.clear()
            self.combo_end_pt.addItems(self.hdb)

    def help(self):
        QMessageBox.information(self, 'Help', '1. Click Load button to load in dataset\n2. Select starting point and ' #display message box with user isntructions
                                              'destination\n3. Click Calculate button\n4. Follow instructions to '
                                              'reach destination!')

    def teaminfo(self):
        QMessageBox.information(self, 'Team Information', 'Lab P2 Group 4\n======================\nNicholas Poon Keet ' #display message box with team information
                                                          'Hoe: 1902131\nJeremy Chua Lee Xiang: 1902633\nElango '
                                                          'Sangavi: 1902682\nLee Yan Xun: 1902610\nToh Zhi Hong: '
                                                          '1902700\nChan Shi En: 1902643\n======================',
                                QtWidgets.QMessageBox.Ok)
