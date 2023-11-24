from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.views.generic import CreateView

from account.forms import CustomUserCreationForm

# create a new user
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('/')
    template_name = 'signin.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): # check if the form is valid
            user = form.save(commit=True)
            user.save()
            return HttpResponseRedirect("/login")

        else: # otherwise, show the form again
            print(form.errors)
            return render(request, self.template_name, {'form':form})
