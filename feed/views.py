from django.shortcuts import render
from feed.models import Record
# Create your views here.
# экшен

def all_records(request):
    records = Record.objects.all()                   # загрузка всего из базы
    return render(request, 'list.html', {'records': records})  # возрат в ответе


