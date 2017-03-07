import urllib.request
from itertools import cycle
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def chart(stocks):
    """
    Graph the stocks found in the Pandas Dataframe
    that is passed as a parameter.

    stocks = Pandas Dataframe with each stock that we want to plot.

    """
    fig, ax = plt.subplots()

    axes = [ax]
    for stock in stocks[1:]:
        # Twin the x-axis twice to make independent y-axes.
        axes.append(ax.twinx())

    extra_ys = len(axes[2:])

    # Make some space on the right side for the extra y-axes.
    if extra_ys > 0:
        # Reduce the figure's width as the number of y axes increases.
        width = max(0.9 - 0.05*extra_ys, 0.5)

        # Adjust the spacing on the right of the figure.
        fig.subplots_adjust(right=width)
        right_additive = (0.98 - width) / float(extra_ys)

    # Move the y-axes over to the right by x% of the space on the right side of
    # the figure.
    i = 1.
    for ax in axes[2:]:
        ax.spines['right'].set_position(('axes', 1.+right_additive*i))
        i += 1.

    columns = []
    lines = []
    # Create two cycles: one for the line styles, and another for the colors,
    # which will be used by the different functions.
    line_styles = cycle(['-', '-', '-', '--', '-.', ':', '.',
                         ',', 'o', 'v', '^', '<', '>', '1',
                         '2', '3', '4', 's', 'p', '*', 'h',
                         'H', '+', 'x', 'D', 'd', '|', '_'])
    colors = cycle(matplotlib.rcParams['axes.prop_cycle'].by_key()['color'])

    # Travel through the Matplotlib axes, and the dataframe's columns. Merge all
    # the data, creating one plot for each pair of (axis, column), using the
    # colors and line styles from their respective cycles.
    for ax, stock in zip(axes, stocks.columns):
        ls = next(line_styles)
        col = stock
        columns.append(col)
        color = next(colors)
        lines.append(ax.plot(stocks.index, stocks[col], linestyle=ls,
                             label=col, color=color))
        ax.set_ylabel(col, color=color)
        ax.spines['right'].set_color(color)

    axes[0].set_xlabel('Date')  # Set the x axis label.

    plot_sum = lines[0]  # Create a plot with all the lines.
    for l in lines[1:]:
        plot_sum += l
    axes[0].legend(plot_sum, columns, loc=0)  # The legends of the y axes

    plt.show()


def addStock(stocks, stock_id):
    """
    Downloads the prices of the stock whose id is stock_id
    (from google.com/finance), and then adds the closing prices
    of each day to the stock DataFrame, which stores dates and
    closing prices of every stock we've downloaded.
    """
    # The path of the CSV file, which will have the stock data.
    file_location = './stocks/%s.csv' % stock_id

    # Try to download the stock's data from Google.
    urllib.request.urlretrieve('http://www.google.com/finance/historical?q='
                       '%s&output=csv' % stock_id, file_location)

    # Add the data from the downloaded CSV file to the stocks DataFrame.
    stock_data = pd.DataFrame.from_csv(file_location)
    stocks[stock_id] = stock_data['Close']
