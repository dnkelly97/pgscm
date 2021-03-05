from django.shortcuts import render
from student.forms import CreateForm

# Create your views here.
def createPage(response):
    if response.method == 'POST':
        form = CreateForm(response.POST)

        if form.is_valid():

            # Create the user
            student = form.save()

            response = redirect('create')
            return response
        context = {'form': form}
        return render(response, 'create_student.html', context)

    form = CreateForm
    context = {'form': form}
    return render(response, 'create_student.html', context)

def homePage(response):
    return render(response, 'home.html')