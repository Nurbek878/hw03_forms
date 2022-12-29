import datetime

time_now = datetime.date.today()


def year(request):
    context = {'year': time_now.year, }
    return (context)
