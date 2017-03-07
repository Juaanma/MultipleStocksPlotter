import os
import pandas as pd
import sys
import plotter
from PyQt4 import QtGui, QtCore

# The main window inherits from QWidget (an empty window).


class MainLayout(QtGui.QWidget):

    def __init__(self):
        # Initialize the object as a QWidget
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Multiple Stocks Plotter")
        self.setMinimumWidth(400)

        # Create the vertical box that lays out the whole form
        self.layout = QtGui.QVBoxLayout()

        # A label of instructions.
        self.label = QtGui.QLabel(self)
        self.label.setText("Enter the names of the stocks that"
                           " you'd like to plot, separated by commas.")
        self.layout.addWidget(self.label)

        self.stocks_input = QtGui.QLineEdit(self)  # Create the input box.
        self.stocks_input.setPlaceholderText("For example: 'AAPL, GOOGL, AMZN'.")
        self.stocks_input.returnPressed.connect(self.parse_and_plot)

        # Add it to the vertical layout.
        self.layout.addWidget(self.stocks_input)
        # Add stretch to separate the input control from the button box.
        self.layout.addStretch(1)

        # Create a horizontal layout to hold the button, which allows us to push
        # it to the right, by adding stretch.
        self.button_box = QtGui.QHBoxLayout()
        self.button_box.addStretch(1)

        # Create the plot button with its caption.
        self.plot_button = QtGui.QPushButton('Plot', self)
        # Connect the function with the button's click event.
        self.plot_button.clicked.connect(self.parse_and_plot)

        # Add it to the horizontal layout.
        self.button_box.addWidget(self.plot_button)

        # Add the button box to the main vertical layout.
        self.layout.addLayout(self.button_box)

        # Set the vertical layout as the window's main layout.
        self.setLayout(self.layout)

    @QtCore.pyqtSlot()
    def parse_and_plot(self):
        # Parse the text in the input box and call the plotter function. Show a
        # message box with errors if anything is wrong.

        # Get the text from the input field, and create the dataframe.
        stock_ids = self.stocks_input.text()
        stocks = pd.DataFrame()

        # If there's no text in the box, we shouldn't do anything.
        if not stock_ids:
            return

        QtGui.QMessageBox.information(self, "Loading",
                                            "The stocks are downloading, "
                                            "please wait.")

        # Split the text typed by the user, which will contain the stock names.
        # Then download these stocks, and add them to the DataFrame that will be
        # plotted.
        # Catch any exceptions raised, and show error messages accordingly.
        try:
            for id in stock_ids.split(', '):
                try:
                    plotter.addStock(stocks, id)
                except pd.parser.CParserError:
                    # If the stock's id is invalid, a webpage will be
                    # downloaded (the one that is shown in case of a 404
                    # error), instead of the file we're trying to
                    # download. If this happens, we'll show a message to the user.
                    QtGui.QMessageBox.critical(self, "Error",
                                                     "The stock or index %s doesn't exist, make sure "
                                                     "you've correctly written its name." % id)
        except IOError:  # The user is not connected to the Internet.
            QtGui.QMessageBox.critical(self, "Error",
                                       "The stocks couldn't be downloaded, make sure "
                                       "you have an Internet connection.")

        # If we succeeded in downloading at least one stock, we'll make a chart.
        if not stocks.empty:
            plotter.chart(stocks)

    def run(self):
        # Focus the window component, so that the QLineEdit doesn't
        # grab the focus initially, and therefore the placeholder
        # text can be shown. Otherwise, this text would be hidden
        # because of the cursor.
        self.setFocus()
        self.show()  # Show the layout.


def main():
    # Create the Qt Application
    qt_app = QtGui.QApplication(sys.argv)
    # Create the layout and show it.
    app = MainLayout()
    app.run()
    qt_app.exec_()

    # Create the folder where the stock data (CSV files) will be downloaded.
    if not os.path.exists('./stocks'):
        os.makedirs('./stocks')

if __name__ == '__main__':
    main()
