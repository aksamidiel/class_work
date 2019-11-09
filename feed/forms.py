from django import forms  # помогает делать джанго формы


class SendEmailForm(forms.Form):   # форма отправки письма
    my_email = forms.CharField(max_length=100)
    address = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
