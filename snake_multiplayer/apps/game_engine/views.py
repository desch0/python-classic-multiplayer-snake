from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from .gameconfig import field_width, field_height


class MainView(View):

	def get(self, request):
		return render(request, 'welcome.html', {'form' : NameForm()})

	def post(self, request):

		form = NameForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			args = {'player_name': name, 'field_width': field_width, 'field_height': field_height}
			return render(request, 'field.html', args)

		return redirect('/')
