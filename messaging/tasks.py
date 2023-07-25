from celery import shared_task

@shared_task
def mailing_check(mailing_pk):
    print(f'rabotaet selery {mailing_pk}')
