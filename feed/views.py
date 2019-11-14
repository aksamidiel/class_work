from django.shortcuts import render, get_object_or_404
from feed.models import Record
from django.views.generic import ListView
from feed.forms import forms, SendEmailForm, RecordForm
from django.core.mail import send_mail

from django.contrib.auth.models import User


# Create your views here.
# экшен

def all_records(request):
    records = Record.objects.all()  # загрузка всего из базы
    return render(request, 'list.html', {'records': records})  # возрат в ответе


class RecordListView(ListView):  # получение всех записей
    queryset = Record.objects.all()
    context_object_name = 'records'
    template_name = 'list.html'  # шаблон базовый


def detailed_view(request, yy, mm, dd, slug):
    record = get_object_or_404(Record,
                               slug=slug,
                               pub__year=yy,
                               pub__month=mm,
                               pub__day=dd)
    return render(request,
                  'detailed.html',
                  {"record": record})


# обработчик формы для отправки письма

def send_email(request, record_id):
    obj = get_object_or_404(Record, id=record_id)
    sent = False
    if request.method == "POST":
        form = SendEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj_url = request.build_absolute_uri(obj.get_absolute_url())
            subject = "Owner {} recommends you reading {}".format(cd['my_email'], obj.title)
            message = "Read {} at {} \n\nAdded comment: {}".format(obj.title,
                                                                   obj_url,
                                                                   cd['comment'])
            send_mail(subject, message, 'admin@myblog.com', [cd['address']])
            sent = True
    else:
        form = SendEmailForm()
    return render(request, 'send.html', {'record': obj,
                                         'form': form,
                                         'sent': sent})


def create_form(request):  # создание формы запроса
    if request.method == "POST":
        record_form = RecordForm(data=request.POST)
        if record_form.is_valid():
            new_record = record_form.save(commit=False)
            new_record.author = User.objects.first()   #получение любой первой записи из реляционной БД
            new_record.slug = new_record.title.replace(' ', '')  #избаввление слага от пробелов
            new_record.save()
            return render(request, 'detailed.html',
                          {'record': new_record})
        else:

            record_form = RecordForm()
            return render(request, 'createForm', {"form": record_form})

    record_form = RecordForm()
    return render(request, 'createForm.html', {'form': record_form})
