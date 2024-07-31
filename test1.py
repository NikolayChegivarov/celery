from celery import Celery


app = Celery(broker="redis://127.0.0.1:6379/0",   # в качестве брокера сообщений.
             backend="redis://127.0.0.1:6379/1",  # в качестве backend.
             broker_connection_retry_on_startup=True)  # перезапуск соединения с брокером.


@app.task()
def test_1(number, number_2):  # значение функции можно прописать по умолчанию.
    print('test1')
    result = number * number_2
    return print(result)


if __name__ == "__main__":
    test_1(3, 3)
