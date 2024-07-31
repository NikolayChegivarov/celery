from tasks import example
from tasks import upscale
from celery.result import AsyncResult


def main():
    print("def main запущен")

    async_result = upscale.delay('lama_300px.png', 'lama_600px.png')
    result = AsyncResult(async_result.id)
    print(result.status)
    print(async_result)

    try:
        result = async_result.get(timeout=70)  # Установка тайм-аута в секундах
        print(result)
    except Exception as e:
        print(f"Ошибка при получении результата: {e}")


if __name__ == "__main__":
    main()

