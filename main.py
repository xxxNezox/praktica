import requests
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd

symbols = ['AAPL', 'GOOG', 'AMZN', 'TSLA']
url_template = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}&outputsize=full'
api_key = 'EJZLFWYWDYSNARXL'


def get_data(symbol):
    print(f'getting {symbol}')
    url = url_template.format(symbol, api_key)
    response = requests.get(url)
    data = response.json()['Time Series (Daily)']
    df = pd.DataFrame.from_dict(data, orient='index')
    filename = f'{symbol}.csv'
    with open(filename, 'w') as f:
        df.to_csv(f)


def plot_stock_data(symbols):
    fig, axs = plt.subplots(len(symbols))

    for i, symbol in enumerate(symbols):
        filename = f'{symbol}.csv'
        df = pd.read_csv(filename, index_col=0, parse_dates=True)
        df = df.iloc[::-1]  # Reverse the DataFrame for proper chronological order

        # Extract relevant columns for plotting
        date = df.index
        close = df['4. close']
        volume = df['6. volume']

        # Plot the closing price on the corresponding axis
        ax = axs[i]
        ax.plot(date, close, color='blue')
        ax.set_xlabel('Date')
        ax.set_ylabel('Closing Price', color='blue')
        ax.tick_params('y', colors='blue')

        # Create a secondary y-axis for volume
        ax2 = ax.twinx()
        ax2.fill_between(date, volume, color='gray', alpha=0.3)
        ax2.set_ylabel('Volume', color='gray')
        ax2.tick_params('y', colors='gray')

        # Set title for the current subplot
        ax.set_title(f'Stock Data for {symbol}')

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()


def generate_statistics_report(input_file, output_file):
    data = pd.read_csv(input_file)
    statistics = data.describe()
    statistics.to_csv(output_file)


def visualize_statistics_report(input_file):
    # Загрузка данных из CSV файла в DataFrame
    data = pd.read_csv(input_file, index_col=0)

    # Удаление столбца "count", так как он не представляет интерес для визуализации
    data = data.drop("count")

    # Создание сетки графиков
    fig, axes = plt.subplots(nrows=len(data.columns), figsize=(10, 6 * len(data.columns)))

    # Построение графиков для каждой характеристики
    for i, column in enumerate(data.columns):
        axes[i].bar(data.index, data[column])
        axes[i].set_title(f"Статистическая характеристика: {column}")
        axes[i].set_xlabel('Характеристика')
        axes[i].set_ylabel('Значение')

    # Размещение графиков в сетке
    plt.tight_layout()

    # Отображение окна с графиками
    plt.show()


visualize_statistics_report('{}_data_report.csv'.format(symbols[0]))

for symbol in symbols:
    generate_statistics_report(symbol+'.csv', '{}_data_report.csv'.format(symbol))
    t = Thread(target=get_data(symbol))
    t.start()

plot_stock_data(symbols)
