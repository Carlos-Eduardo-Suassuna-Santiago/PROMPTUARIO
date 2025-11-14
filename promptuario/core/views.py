from django.shortcuts import render

def login(request):
    return render(request, 'core/login.html')

def cadastroPaciente(request):
    return render(request, 'core/cadastroPaciente.html')

