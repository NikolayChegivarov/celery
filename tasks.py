from celery import Celery
import cv2
from cv2 import dnn_superres

app = Celery(broker="redis://127.0.0.1:6379/0",   # в качестве брокера сообщений.
             backend="redis://127.0.0.1:6379/1",  # в качестве backend.
             broker_connection_retry_on_startup=True)  # перезапуск соединения с брокером.


def upscale(input_path: str, output_path: str, model_path: str = 'EDSR_x2.pb') -> None:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """

    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)


@app.task()
def example():
    upscale('lama_300px.png', 'lama_600px.png')