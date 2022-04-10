from quickstart.models import Advice


def my_scheduled_job():
    a = Advice.objects.first()
    a.text += 'привет '
    a.save()
