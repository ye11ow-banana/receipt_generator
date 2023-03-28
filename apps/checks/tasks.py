from celery import shared_task


@shared_task()
def check_generator(order_id: int, check_type: str) -> None:
    pass
