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

@login_required
def TeamRosterView(request,id):
    
    if(request.method == 'GET'):
       teamID = get_object_or_404(Team, TeamID=id)
       teamRosters = TeamRoster.objects.filter(Team_id=id).all()
       teamRosterForm = TeamRosterForm()
       return render(request, 'teams/players/TeamRoster.html', {'TeamRoster': teamRosters, 'Team_Roster_Form': teamRosterForm})
    elif (request.method == 'POST'):
          team = get_object_or_404(Team, TeamID=id)
          form = TeamRosterForm(request.POST, files = request.FILES)
          if(form.is_valid()):
             newRoster = form.save(commit=False)
             newRoster.Team = team
             newRoster.save()
             msg = "Player has been added."
             messages.success(request, msg)
             return redirect(to='team-rosters', id=id)
          else:
              teamRosterForm = TeamRosterForm(request.POST, files = request.FILES, instance=teamID)
              return render(request, 'teams/players/TeamRoster.html', {'TeamRoster': teamRosters, 'Team_Roster_Form': form})

@login_required
def EditTeamRosterView(request,id):
    
    if(request.method == 'GET'):
       player = get_object_or_404(TeamRoster, TeamPlayerID=id)
       teamID = player.Team.TeamID
       teamRosterForm = TeamRosterForm(instance=player)
       return render(request, 'teams/players/EditRosterPlayer.html', {'Team_Roster_Form': teamRosterForm, 'TeamID': teamID})
    elif (request.method == 'POST'):
          player = get_object_or_404(TeamRoster, TeamPlayerID=id)
          form = TeamRosterForm(request.POST, files = request.FILES, instance=player)
          if(form.is_valid()):
             newRoster = form.save(commit=True)
             newRoster.Team.TeamID
             msg = "Player has been updated."
             messages.success(request, msg)
             return redirect(to='team-rosters', id=newRoster.Team.TeamID)
          else:
              teamRosterForm = TeamRosterForm(instance=player)
              return render(request, 'teams/players/EditRosterPlayer.html', {'Team_Roster_Form': teamRosterForm})
          
@login_required
def DeleteTeamRosterView(request,id):
    
    if(request.method == 'GET'):
       player = get_object_or_404(TeamRoster, TeamPlayerID=id)
       teamID = player.Team.TeamID 
       teamRosterForm = TeamRosterForm(instance=player)
       return render(request, 'teams/players/DeleteRosterPlayer.html', {'PlayerFullName': player.FullName, "TeamID": teamID})
    elif (request.method == 'POST'):
          player = get_object_or_404(TeamRoster, TeamPlayerID=id)
          TeamRoster.objects.filter(TeamPlayerID=player.TeamPlayerID).delete()
          teamID = player.Team.TeamID
          msg = "Player has been deleted."
          messages.success(request, msg)
          return redirect(to='team-rosters', id=teamID)
