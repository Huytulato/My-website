from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Họ và tên')
    email = forms.EmailField(label='Email')
    subject = forms.CharField(max_length=200, label='Tiêu đề')
    message = forms.CharField(widget=forms.Textarea, label='Nội dung')