from celery import Celery
from celery.schedules import crontab
from django.conf import settings

app = Celery("favlinks-celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour="*"),  # Every hour
        validate_urls_and_update_titles.s(),
    )
    sender.add_periodic_task(
        crontab(minute=0, hour="0"),  # Every day
        clean_up_invalid_validurl_instances.s(),
    )


@app.task(bind=True)
def validate_urls_and_update_titles():
    from favourite_manager.models import ValidUrl

    for valid_url_obj in ValidUrl.objects.all():
        valid_url_obj.validate_url_and_get_title()


@app.task(bind=True)
def clean_up_invalid_validurl_instances():
    from favourite_manager.models import ValidUrl

    ValidUrl.objects.filter(is_valid=False).delete()
