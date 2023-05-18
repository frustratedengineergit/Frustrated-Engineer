from django.shortcuts import render, redirect
from django import forms
from .models import ContactData

# Create your views here.
def index(request):
    return render(request,'contact-us.html')

#Form Start Here

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    contact = forms.IntegerField(label='Contact')
    message = forms.CharField(label='Message', widget=forms.Textarea)

def submit(request):
    return render(request, 'index.html')


def my_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            message = form.cleaned_data['message']
            # ... Save Data

            contact_data = ContactData(name=name, email=email,contact=contact, message=message)
            contact_data.save()
            return redirect('submit')
    else:
        form = ContactForm()
    
    return render(request, 'my_template.html', {'form': form})


