from django.shortcuts import render
from fifa_draft.forms import GroupForm

def home(request):
    return render(request, 'home.html')

def create_group(request):
    form = GroupForm()
    # if request.method == "POST":
    #     form = GroupForm(request.POST)
    context = {'form': form}
    return render(request, 'group-form.html', context)
