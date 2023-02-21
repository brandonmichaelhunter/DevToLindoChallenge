from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from .models import *
from .forms import * #RegisterForm, LoginForm,TeamSiteForm, UpdateUserForm, UpdateProfileForm, CreateTeamForm,EditTeamForm, DeleteTeamForm
# from django import template
# register = template.Library()
import smtplib
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
def home(request):
    return render(request, 'users/home.html')


@login_required 
def CreateTeam(request):
    if request.method == 'POST':
       team_form = CreateTeamForm(request.POST, files=request.FILES)
       if(team_form.is_valid()):
          newTeam = team_form.save()
          newTeamID = newTeam.TeamID
          teamObject = Team.objects.filter(TeamID = newTeamID)
          
          TeamWebsite.objects.create(SiteTitle="{} {}".format(newTeam.TeamName, newTeam.SportType), TeamName = newTeam, IsPublicSite=True)
         
          newUser = User.objects.filter(id=request.user.id).first()
          TeamMember.objects.create(MemberUser=newUser, MemberType='COACH', AssignedTeam = teamObject.first(), TeamOwner=True)
          TeamCoach.objects.create(Coach=newUser, Team=teamObject.first(),IsHeadCoach=False,CoachTitle="")
          #TeamWebsite.objects.create(SiteTitle="{} {} Internal".format(newTeam.TeamName, newTeam.SportType), TeamName = newTeam, IsPublicSite=False)
          messages.success(request, 'Your New Team Has Been Added.')
          return redirect(to='teams')
    else:
        team_form = CreateTeamForm()
    
    return render(request, 'teams/CreateTeam.html', {'team_form': team_form})

@login_required
def DeleteTeamView(request, id):
    post = get_object_or_404(Team, TeamID=id)
    teamName = post.TeamName

    if request.method == 'GET':
        context = {'team_form': DeleteTeamForm(instance=post), 'id': id, 'TeamName': post.TeamName}
        return render(request,'teams/DeleteTeam.html',context)
    elif request.method == 'POST':
         TeamWebsite.objects.filter(TeamName = post).delete()
         Team.objects.filter(TeamID=id).delete()
         
         msg = "{} has been deleted.".format(teamName)
         messages.success(request, msg)
         return redirect('teams')
        
@login_required
def EditTeamView(request, id):
    post = get_object_or_404(Team, TeamID=id)
    

    if request.method == 'GET':
        publicTeamSite = TeamWebsite.objects.filter(TeamName_id = id, IsPublicSite=True).first()
        internalTeamSite = TeamWebsite.objects.filter(TeamName_id = id, IsPublicSite=False).first()
        public_site_form = TeamSiteForm(instance=publicTeamSite)
        internal_site_form = TeamSiteForm(instance=internalTeamSite)
        context = {'team_form': EditTeamForm(instance=post), 'id': id,
                   'public_site_form': public_site_form, 
                   'internal_site_form': internal_site_form}
        return render(request,'teams/EditTeam.html',context)
    elif request.method == 'POST':
         form = EditTeamForm(request.POST, files=request.FILES, instance=post)
        #TODO - save public and internal website changes.
         if form.is_valid():
            form.save()
            messages.success(request, 'You changes has been updated successfully.')
            return redirect('teams')
         else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'teams/EditTeam.html',{'team_form':form})
 
@login_required
def AllTeamsView(request):
    fanTeams = TeamMember.objects.filter(MemberUser_id = request.user.id).all()
    teamsList = Team.objects.all() #Team.objects.filter(TeamID=Subquery(fanTeams.values('AssignedTeam_id'))).all() #
    teamWebsites = TeamWebsite.objects.all()
    return render(request,'teams/Teams.html', {'FanTeams':fanTeams, 'teams': teamsList, 'sites': teamWebsites})


