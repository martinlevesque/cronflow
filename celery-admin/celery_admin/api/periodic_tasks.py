
import logging
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django_celery_beat.models import PeriodicTask, PeriodicTasks, CrontabSchedule


# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(['GET'])
def latest(request):
    p = PeriodicTask.objects.latest('id')
    return Response(model_to_dict(p))


@api_view(['POST'])
def create(request):
    body = request.data

    crontab, _ = CrontabSchedule.objects.get_or_create(
        minute='35',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*'
    )

    p_task = PeriodicTask.objects.create(
        crontab=crontab,                  # we created this above.
        name=body.get('name'),          # simply describes this periodic task.
        task=body.get('task'),
        kwargs=json.dumps(body.get('kwargs'))
    )

    return Response(model_to_dict(p_task))