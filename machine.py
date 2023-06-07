import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def analyze_stock_data(file_name, target_column):
    # Загрузка данных из CSV файла в DataFrame
    data = pd.read_csv(file_name)

    # Преобразование столбца с датами из строкового формата в объекты даты/времени
    data['date'] = pd.to_datetime(data['1. open'])

    # Получение числового представления даты
    data['date_numeric'] = (data['1. open'] - data['1. open'].min()).at.days

    # Извлечение характеристики в качестве целевой переменной
    target = data[target_column]

    # Извлечение других характеристик в качестве признаков
    features = data.drop(['1. open', target_column], axis=1)

    # Создание и обучение модели линейной регрессии
    model = LinearRegression()
    model.fit(features, target)

    # Прогнозирование значений на основе признаков
    predictions = model.predict(features)

    # Визуализация исторических значений и прогнозов
    plt.plot(data['1. open'], target, label='Actual')
    plt.plot(data['1. open'], predictions, label='Predicted')
    plt.xlabel('Time')
    plt.ylabel(target_column)
    plt.legend()
    plt.show()

    # Возвращаем результаты анализа
    return data, target, predictions

# Пример использования функции
file_name = 'AAPL.csv'
target_column = '4. close'
data, target, predictions = analyze_stock_data(file_name, target_column)
