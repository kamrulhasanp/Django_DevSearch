from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q 
from .models import Profiles, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginationProfiles
# Create your views here.


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username dose not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request,'username or password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User are logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    context ={'page':page, 'form':form}

    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was successfully created!' )

            login(request, user)
            return redirect('edit-account')
        else:
            messages.success(request, 'An error has occurred during registration' )


    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginationProfiles(request, profiles, 3)
    
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'users/profile.html', context)

def userProfile(request, pk):
    profile = Profiles.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile':profile, 'topskills':topSkills, 'otherskills':otherSkills}
    return render(request, 'users/user_profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profiles

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profiles
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profiles
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = { 'form': form }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profiles
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            #skill = form.save(commit=False)
            #skill.owner = profile
            form.save()
            messages.success(request, 'Skill was updated successfully!' )
            return redirect('account')

    context = { 'form': form }
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profiles
    skill= profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!' )
        return redirect('account')

    context ={'object': skill}
    return render(request, 'delete_template.html', context)

@login_required
def inbox(request):
    profile = request.user.profiles
    messagesRequests = profile.messages.all()
    unreadCount = messagesRequests.filter(is_read=False).count()

    context = { 'messagesRequests':messagesRequests, 
                'unreadCount':unreadCount

    }
    return render(request, 'users/inbox.html', context)

@login_required
def viewMessage(request, pk):
    profile = request.user.profiles
    # where are from the 'messages' #
    message = profile.messages.get(id=pk) 
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message':message}
    return render(request, 'users/message.html', context)

@login_required
def createMessage(request,pk):
    recipient = Profiles.objects.get(id=pk)
    form = MessageForm() 
    try:
        sender = request.user.profiles
    except:
            sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient


            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'your message successfully send')
            return redirect('user_profiles', pk=recipient.id)

        

    context = {'recipient':recipient, 'form':form }
    return render(request, 'users/message_form.html', context)