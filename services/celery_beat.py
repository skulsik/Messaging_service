from django_celery_beat.models import PeriodicTask, IntervalSchedule


class AddTask:
    """ Добавление задачи в БД """
    def __init__(self, every='day', period='day', name='no_name'):
        """
        :param every: принимает текст, переводит в количество int
        :param period: еденица измерения every (
            дни, секунды - для тестов, имеются другие значения:милисикунды, минуты, часы
        )
        :param name: Имя новой задачи и id рассылки
        """
        every_dict: dict = {
            'day': 1,
            'week': 7,
            'month': 30
        }

        period_dict: dict = {
            'day': IntervalSchedule.DAYS,
            'second': IntervalSchedule.SECONDS
        }

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=every_dict[every],
            period=period_dict[period],
        )

        # Если запись существует, обновляет ее, иначе создает
        if PeriodicTask.objects.filter(name=name):
            obj_task = PeriodicTask.objects.get(name=name)
            obj_task.interval = schedule
            obj_task.save()
        else:
            PeriodicTask.objects.create(
                interval=schedule,
                name=name,
                task='messaging.tasks.mailing_task'
            )
