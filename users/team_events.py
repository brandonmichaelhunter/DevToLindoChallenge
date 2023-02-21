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
from django.http import JsonResponse
from collections import namedtuple
def home(request):
    return render(request, 'users/home.html')
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

@login_required
def AllTeamEventsView(request, id):
    team = get_object_or_404(Team, TeamID=id)
    teamID = team.TeamID
    currentUser = User.objects.filter(id = request.user.id).first()
    currentUserID = request.user.id
    userTeamMembershipType = TeamMember.objects.filter(AssignedTeam_id = teamID, MemberUser_id = currentUserID).first().MemberType
    # Retrieve All Team Practices
    teamPractices = TeamPractice.objects.filter(AssignedTeam_id = teamID).all()
    teamPracticesCount = teamPractices.count()
    # Retrieve All Team Games
    teamHomeGames = TeamGame.objects.filter(HomeTeam_id = teamID).all()
    teamHomeGamesCount = teamHomeGames.count()
    teamAwayGames = TeamGame.objects.filter(AwayTeam_id = teamID).all()
    teamAwayGamesCount = teamAwayGames.count()
    context = {"TeamPractices": teamPractices, "TeamPracticesCount": teamPracticesCount, 
               "TeamHomeGames": teamHomeGames, "TeamHomeGamesCount": teamHomeGamesCount,
               "TeamAwayGames": teamAwayGames, "TeamAwayGamesCount": teamAwayGamesCount,
               "MembershipType": userTeamMembershipType, "TeamName": team.TeamName,"TeamID": teamID}
    return render(request, "teams/events/AllTeamEvents.html", context)

@login_required
def CreateTeamPracticeViewAction(request,id):
    team = get_object_or_404(Team, TeamID=id)
    teamID = team.TeamID
    currentUser = User.objects.filter(id = request.user.id).first()
    currentUserID = request.user.id
    pageTitle = "Create {} Practice Event".format(team.TeamName)
    if(request.method == 'GET'):
       form = TeamPracticeForm()
       form.fields['AssignedTeam'].initial = teamID
       #form.AssignedTeam = 
       
       return render(request, 'teams/events/CreateTeamPractice.html', {'form': form, "PageTitle": pageTitle, "TeamID": teamID})
    elif(request.method == 'POST'):
         form = TeamPracticeForm(request.POST)
         form.fields['AssignedTeam'].initial = teamID
         if(form.is_valid()):
            form.save()
            messages.success(request,"A practice event has been created.")
            return redirect(to='team-events',id=teamID)
         else:
             return render(request, 'teams/events/CreateTeamPractice.html', {'form': form, "PageTitle": pageTitle, "TeamID": teamID})
@login_required
def UpdateTeamPracticeViewAction(request,id):
    teamPractice = get_object_or_404(TeamPractice, TeamPracticeID = id)
    teamID = teamPractice.AssignedTeam_id
    teamName = teamPractice.AssignedTeam.TeamName
    pageTitle = "Edit {} Practice Event".format(teamName)
    if(request.method == 'GET'):
       form = TeamPracticeForm(instance=teamPractice)
       return render(request, 'teams/events/EditTeamPractice.html', {'form': form, "PageTitle": pageTitle, "TeamID": teamID})
    elif(request.method == 'POST'):
         form=TeamPracticeForm(request.POST, instance=teamPractice)
         form.fields['AssignedTeam'].initial = teamID
         if('update' in request.POST):
            if(form.is_valid()):
               form.save()
               messages.success(request,"You practice event has been updated.")
               return redirect(to='team-events',id=teamID)
            else:
                return render(request, 'teams/events/CreateTeamPractice.html', {'form': form, "PageTitle": pageTitle, "TeamID": teamID})
         elif('remove' in request.POST):
              deletePractice = TeamPractice.objects.filter(TeamPracticeID = teamPractice.TeamPracticeID).delete();
              messages.success(request,"You practice event has been deleted.")
              return redirect(to='team-events',id=teamID)
  
@login_required
def CreateHomeTeamGameViewAction(request,id):
    homeTeam = get_object_or_404(Team, TeamID=id)
    homeTeamID = homeTeam.TeamID
    pageTitle= "Create New Home Game For {}".format(homeTeam.TeamName)
    if(request.method == 'GET'):
        form = TeamGameForm()
        form.fields['HomeTeam'].initial = homeTeamID
        
        #form.fields['HomeTeam'].widget.attrs['readonly'] = True
        return render(request, 'teams/events/CreateTeamGame.html', {'form': form, "PageTitle": pageTitle, "TeamID": homeTeamID})
    elif(request.method == 'POST'):
         form=TeamGameForm(request.POST)
         form.fields["HomeTeam"].initial = homeTeam
         if(form.is_valid()):
            awayTeam = Team.objects.filter(TeamID=request.POST["AwayTeam"]).first()
            rec = TeamGame.objects.create(HomeTeam=homeTeam, 
                                          AwayTeam=awayTeam, 
                                          Start_Game_DateTime=request.POST["StartGameDateTime"],
                                          End_Game_DateTime=request.POST["EndGameDateTime"],
                                          Location = request.POST["Location"])
            rec.save()
            messages.success(request, "You home game has been created.")
            return redirect(to='team-events',id=homeTeamID)
         else:
             form.fields["HomeTeam"].initial = homeTeamID
             return render(request, 'teams/events/CreateTeamGame.html', {'form': form, "PageTitle": pageTitle, "TeamID": homeTeamID})
            
@login_required
def CreateAwayTeamGameViewAction(request,id):
    awayTeam = get_object_or_404(Team, TeamID=id)
    awayTeamID = awayTeam.TeamID
    pageTitle= "Create New Away Game For {}".format(awayTeam.TeamName)
    if(request.method == 'GET'):
        form = TeamGameForm()
        form.fields['AwayTeam'].initial = awayTeamID
        
        #form.fields['HomeTeam'].widget.attrs['readonly'] = True
        return render(request, 'teams/events/CreateAwayTeamGame.html', {'form': form, "PageTitle": pageTitle, "TeamID": awayTeamID})
    elif(request.method == 'POST'):
         form=TeamGameForm(request.POST)
         form.fields["AwayTeam"].initial = awayTeam
         if(form.is_valid()):
            homeTeam = Team.objects.filter(TeamID=request.POST["HomeTeam"]).first()
            rec = TeamGame.objects.create(HomeTeam=homeTeam, 
                                          AwayTeam=awayTeam, 
                                          Start_Game_DateTime=request.POST["StartGameDateTime"],
                                          End_Game_DateTime=request.POST["EndGameDateTime"],
                                          Location = request.POST["Location"])
            rec.save()
            messages.success(request, "You away game has been created.")
            return redirect(to='team-events',id=awayTeamID)
         else:
             form.fields["AwayTeam"].initial = awayTeamID
             return render(request, 'teams/events/CreateAwayTeamGame.html', {'form': form, "PageTitle": pageTitle, "TeamID": awayTeamID})

@login_required
def UpdateHomeTeamGameViewAction(request,id):
    teamGame = get_object_or_404(TeamGame, TeamGameID = id)
    gameID = id
    teamSide='Home'
    teamID = 0
    teamName = ""
    if teamSide == 'Home':
       teamID = teamGame.HomeTeam_id
       teamHame = teamGame.HomeTeam.TeamName
    elif teamSide == 'Away':   
         teamID = teamGame.AwayTeam_id
         teamHame = teamGame.AwayTeam.TeamName
    
    
    pageTitle = "Edit {} {} Game".format(teamSide, teamName)
    if(request.method == 'GET'):
       form = TeamGameForm(instance=teamGame)
       form.fields['StartGameDateTime'].initial = teamGame.Start_Game_DateTime
       form.fields['EndGameDateTime'].initial = teamGame.End_Game_DateTime
       return render(request, 'teams/events/Edit{}TeamGame.html'.format(teamSide), {'form': form, "PageTitle": pageTitle, "TeamID": teamID, "TeamSide": teamSide, "TeamGameID": gameID})
    elif(request.method == 'POST'):
         form=TeamGameForm(request.POST, instance=teamGame)
         form.fields['{}Team'.format(teamSide)].initial = teamID
         if('update' in request.POST):
            if(form.is_valid()):
               rec = TeamGame.objects.filter(TeamGameID=id).first()
               rec.HomeTeam = Team.objects.filter(TeamID = teamID).first()
               rec.AwayTeam = Team.objects.filter(TeamID=request.POST["AwayTeam"]).first()
               rec.Start_Game_DateTime=request.POST["StartGameDateTime"]
               rec.End_Game_DateTime=request.POST["EndGameDateTime"]
               rec.Location = request.POST["Location"]
               rec.save()
               messages.success(request,"You {} game has been updated.".format(teamSide))
               return redirect(to='team-{}-game-edit'.format(teamSide.lower()),id=gameID)
            else:
                return render(request, 'teams/events/Edit{}TeamGame.html'.format(teamSide), {'form': form, "PageTitle": pageTitle, "TeamID": teamID, "TeamSide": teamSide, "TeamGameID": gameID})
         elif('remove' in request.POST):
              TeamGame.objects.filter(TeamGameID = teamGame.TeamGameID).delete();
              messages.success(request,"You {} game has been deleted.".format(teamSide))
              return redirect(to='team-events',id=teamID)
            
@login_required
def UpdateAwayTeamGameViewAction(request,id):
    teamGame = get_object_or_404(TeamGame, TeamGameID = id)
    gameID = id
    teamSide='Away'
    teamID = 0
    teamName = ""
    if teamSide == 'Home':
       teamID = teamGame.HomeTeam_id
       teamHame = teamGame.HomeTeam.TeamName
    elif teamSide == 'Away':   
         teamID = teamGame.AwayTeam_id
         teamHame = teamGame.AwayTeam.TeamName
    
    
    pageTitle = "Edit {} {} Game".format(teamSide, teamName)
    if(request.method == 'GET'):
       form = TeamGameForm(instance=teamGame)
       form.fields['StartGameDateTime'].initial = teamGame.Start_Game_DateTime
       form.fields['EndGameDateTime'].initial = teamGame.End_Game_DateTime
       return render(request, 'teams/events/Edit{}TeamGame.html'.format(teamSide), {'form': form, "PageTitle": pageTitle, "TeamID": teamID, "TeamSide": teamSide, "TeamGameID": gameID})
    elif(request.method == 'POST'):
         form=TeamGameForm(request.POST, instance=teamGame)
         form.fields['{}Team'.format(teamSide)].initial = teamID
         if('update' in request.POST):
            if(form.is_valid()):
               rec = TeamGame.objects.filter(TeamGameID=id).first()
               rec.AwayTeam = Team.objects.filter(TeamID = teamID).first()
               rec.HomeTeam = Team.objects.filter(TeamID=request.POST["HomeTeam"]).first()
               rec.Start_Game_DateTime=request.POST["StartGameDateTime"]
               rec.End_Game_DateTime=request.POST["EndGameDateTime"]
               rec.Location = request.POST["Location"]
               rec.save()
               messages.success(request,"You {} game has been updated.".format(teamSide))
               return redirect(to='team-{}-game-edit'.format(teamSide.lower()),id=gameID)
            else:
                return render(request, 'teams/events/Edit{}TeamGame.html'.format(teamSide), {'form': form, "PageTitle": pageTitle, "TeamID": teamID, "TeamSide": teamSide, "TeamGameID": gameID})
         elif('remove' in request.POST):
              TeamGame.objects.filter(TeamGameID = teamGame.TeamGameID).delete();
              messages.success(request,"You {} game has been deleted.".format(teamSide))
              return redirect(to='team-events',id=teamID)
       
@login_required
def UpdateHomeTeamsGameStatViewAction(request,id):
    teamGame = get_object_or_404(TeamGame, TeamGameID = id)
    #teamGame = TeamGame.objects.filter(TeamGameID=gameID).first()
    homeTeam = teamGame.HomeTeam #Team.objects.filter(TeamID = teamGame["HomeTeam_id"]).first()
    teamRosters = TeamRoster.objects.filter(Team_id = homeTeam.TeamID).all()
    playerForm = GamePlayerForm()
    
    batterStatsForm = BatterGameStatForm()
    pitcherStatsForm = PitcherGameStatForm()
    pageTitle = ""
    if(request.method == 'GET'):
       form = GamePlayerForm()
       return render(request, 'teams/events/UpdateHomeTeamGameStats.html', 
                     {'PlayerForm': playerForm, "PageTitle": pageTitle, "TeamGameID": id,
                      "BatterStatsForm": batterStatsForm,"PticherForm": pitcherStatsForm,
                      "TeamRoster":teamRosters, "TeamID": homeTeam.TeamID})

@login_required
def UpdateAwayTeamsGameStatViewAction(request,id):
    gameID = get_object_or_404(TeamGame, TeamGameID = id)
    teamGame = TeamGame.objects.filter(TeamGameID=gameID).first()
    awayTeam = Team.objects.filter(TeamID = teamGame["AwayTeam_id"]).first()
    teamRosters = TeamRoster.objects.filter(Team_id = awayTeam.TeamID).all()
    playerForm = GamePlayerForm()
    batterStatsForm = BatterGameStatForm()
    pitcherStatsForm = PitcherGameStatForm()
    pageTitle = ""
    if(request.method == 'GET'):
       form = GamePlayerForm()
       return render(request, 'teams/events/UpdateAwayTeamGameStats.html', 
                     {'PlayerForm': playerForm, "PageTitle": pageTitle, "TeamGameID": id,
                      "BatterStatsForm": batterStatsForm,"PticherForm": pitcherStatsForm,
                      "TeamRoster":teamRosters})
    
#TODO: Cascading drop down on state and city select controls on the RequestForTeamAccess.html page.
#TODO: Allow to conduct a search
#TODO: Allow users to request for access to team.
#TODO: Let the approver know they have requests to approve, maybe show a number next to the Invite header menu. 
#TODO: Create a new section on teh invites.html, load the data.