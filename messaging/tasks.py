import json
from datetime import *

from django.core.mail import send_mail

from config import settings
from config.celery import app
from messaging.models import Mailing, Log


@app.task(bind=True)
def mailing_task(self, **kwargs):
    print('---------- working task start ---------------')

    # Получает объект (c info) планировщика, который запускает task
    periodic_task_info = self.request.properties

    # Получает объект рассылки, которая создала планировщика
    id = int(periodic_task_info['periodic_task_name'])
    object_mailing = Mailing.objects.get(id=id)

    # Список возврата ответов от send_mail
    mail_report: dict = {}

    # Если статус "создано" или задача зависла обозначив статус "запущено" запускается проверка временного диапазона
    if object_mailing.status == 'created' or object_mailing.status == 'launched':
        object_mailing.status = 'launched'
        object_mailing.save()

        # Получает время начало и конец рассылки, время сейчас (в секундах)
        time_begin = object_mailing.dtime_begin
        time_begin = time_begin.timestamp()
        time_end = object_mailing.dtime_end
        time_end = time_end.timestamp()
        time_now = datetime.now()
        time_now = time_now.timestamp()

        # Если время сейчас попадает в интервал времени рассылки запускает рассылку
        if time_begin <= time_now <= time_end:
            # Получает клиентов
            clients = object_mailing.clients.all()

            #Отправка сообщений клиентам
            for client in clients:
                mail_report[client.email] = send_mail(
                    subject=object_mailing.message.topic,
                    message=object_mailing.message.text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email]
                )


            object_mailing.status = 'completed'
            object_mailing.save()

    mail_report = json.dumps(mail_report)
    Log.objects.create(
        dtime_mailing=datetime.now(),
        status_mailing='completed',
        name=object_mailing.name,
        server_response=mail_report
    )
