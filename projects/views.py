from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth .decorators import login_required
from django.contrib import messages
from users.views import profiles
from .models import Project, Review, Tag
from .form import ProjectForm, ReviewForm
from .utils import searchProjects, paginationProjects

def projects(request):   
    projects, search_query = searchProjects(request)
    custom_range, projects = paginationProjects(request, projects, 6)
    
    context = {'projects': projects,
               'search_query': search_query,
               'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectobj = Project.objects.get(id = pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectobj
        review.owner = request.user.profiles
        review.save()

        projectobj.getVoteCount

        #Update 
        messages.success(request, 'successfully posted')
        return redirect('project', pk=projectobj.id)
        

    return render(request, 'projects/single-project.html', {'project': projectobj, 'form': form })

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profiles

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
           project = form.save(commit=False)
           project.owner = profile
           project.save()
           return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES , instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profiles
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)