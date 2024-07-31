from celery import Celery
from test1 import test_1

app = Celery(broker="redis://127.0.0.1:6379/0",
             backend="redis://127.0.0.1:6379/1",
             broker_connection_retry_on_startup=True)


@app.task
def test_callback(result):
    print(f"Result of test_1: {result}")


def test_2():
    print('test2')
    async_result = test_1.apply_async(args=(1, 2), link=test_callback.s())

    # Если вы все еще хотите получить результат напрямую, используйте get()
    # Но помните о риске блокировки выполнения программы из-за таймаута
    result = async_result.get()  # timeout=70


if __name__ == "__main__":
    test_2()


