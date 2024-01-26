from django.shortcuts import render
from .models import Chat, Group

# Create your views here.
def index(request, group_name):
    group = Group.objects.get_or_create(name=group_name)
    group = Group.objects.get(name=group_name)
    chats = []
    chats = Chat.objects.filter(group=group)
    return render(request, 'app/index.html', {'group_name':group_name, 'chats':chats})