from django.utils import timezone

now = timezone.now()


def year(request):
    context = {'year': now}
    return (context)
