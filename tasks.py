import cv2
from cv2 import dnn_superres
from celery import Celery
import os
import time

print("tasks запущен")

app = Celery(broker="redis://127.0.0.1:6379/0",   # в качестве брокера сообщений.
             backend="redis://127.0.0.1:6379/1",  # в качестве backend.
             broker_connection_retry_on_startup=True)  # перезапуск соединения с брокером.


@app.task()
def upscale(input_path: str, output_path: str, model_path: str = 'EDSR_x2.pb') -> None:

    print("upscale запущен")

    start_time = time.time()  # Засекаем начальное время

    try:
        scaler = dnn_superres.DnnSuperResImpl_create()
        scaler.readModel(model_path)
        scaler.setModel("edsr", 2)

        if not os.path.exists(input_path):
            print(f"Input file {input_path} does not exist.")
            return

        image = cv2.imread(input_path)
        if image is None:
            print(f"Failed to read {input_path}")
            return

        result = scaler.upsample(image)
        cv2.imwrite(output_path, result)
        print(f"Upscaled image saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()  # Засекаем конечное время
    elapsed_time = end_time - start_time  # Вычисляем затраченное время
    print(f"Time taken: {elapsed_time:.2f} seconds")  # Выводим затраченное время


@app.task()
def example():
    print("example tasks запущен")
    upscale('lama_300px.png', 'lama_600px.png')


app.tasks.register(example)
app.tasks.register(upscale)

if __name__ == '__main__':
    example()
