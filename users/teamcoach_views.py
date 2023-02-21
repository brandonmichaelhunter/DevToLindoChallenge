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
def TeamCoachView(request, id):
    if(request.method == 'GET'):
       teamID = get_object_or_404(Team, TeamID=id)
       teamCoaches = TeamCoach.objects.filter(Team_id=id).all()
       currentUserID = request.user.id
       ownerUserID = 0
       teamOwner = TeamMember.objects.filter(AssignedTeam_id=teamID, MemberUser_id=currentUserID, TeamOwner=True).first()
       IsTeamOwner = False
       if teamOwner != None:
          IsTeamOwner = True
          ownerUserID = currentUserID
       
       invite_form = TeamFanInviteForm()
       return render(request, 'teams/coaches/TeamCoaches.html', {'TeamCoaches': teamCoaches, 'invite_form':invite_form, 'CurrentUserID': currentUserID, "IsTeamOwner":IsTeamOwner, "OwnerUserID": ownerUserID})
    elif (request.method == 'POST'):
          inviteCode = User.objects.make_random_password(length=10, allowed_chars='123456789')
          currentTeam = get_object_or_404(Team, TeamID=id)
          TeamFanInviteRequest.objects.create(EmailContact=request.POST["EmailContact"], AssignedTeam=currentTeam, DateCreated=datetime.now(), DateApprovedRejected=datetime.now(), RequestStatus='PENDING', InviteCode=inviteCode, MemberType='COACH')
          context ={
            "TeamName":currentTeam.TeamName,
            "InviteCode": inviteCode
          }
          html_content = render_to_string("teams/invites/inviteemail.html", context)
          text_content = strip_tags(html_content)
          msg = MIMEMultipart()
          msg.attach(MIMEText(html_content, "html"))
          msg['Subject'] = "You have been invited to {} team".format(currentTeam.TeamName)
          msg['From']    = "SportsManagerInvites@scm.com"
          msg['To']      = "brandonmichaelhunter@live.com" # change this after testing. request.POST["EmailContact"]
        
          s = smtplib.SMTP('smtp.mailgun.org', 587)

          s.login('postmaster@sandbox1c3e7756461c4d71a242366405c4447d.mailgun.org', '797b720f1d68472f645a1d224fead921-75cd784d-78232018')
          s.sendmail(msg['From'], msg['To'], msg.as_string())
          s.quit()
          msg = "Invite was sent"
          messages.success(request, msg)
          return redirect(to='team-coaches', id=id) 

@login_required
def TeamCoachRemoveView(request, id):
    teamCoach = get_object_or_404(TeamCoach, TeamCoachID=id)
    if(request.method == 'GET'):
        coachName = "{} {}".format(teamCoach.Coach.first_name, teamCoach.Coach.last_name)
        assignedTeamID = teamCoach.Team_id
        return render(request, 'teams/coaches/TeamRemoveCoach.html', {"Name": coachName, "AssignedTeamID": assignedTeamID})
    elif (request.method == 'POST'):
          teamCoachID = teamCoach.TeamCoachID
          teamCoachUserID = teamCoach.Coach_id
          teamID = teamCoach.Team.TeamID
          teamFanName = "{} {}".format(teamCoach.Coach.first_name, teamCoach.Coach.last_name)
          TeamCoach.objects.filter(TeamCoachID=teamCoachID).delete()
          TeamMember.objects.filter(MemberUser_id = teamCoachUserID).delete()
          msg= "{} has been removed from the team".format(teamFanName)
          messages.success(request, msg)
          return redirect(to='team-coaches', id=teamID)

@login_required
def EditTeamCoachDetailView(request, id):
    coach = get_object_or_404(TeamCoach, TeamCoachID = id)
    coachName = "{} {}".format(coach.Coach.first_name, coach.Coach.last_name)
    teamID = coach.Team.TeamID
    if(request.method == 'GET'):
       coachName = "{} {}".format(coach.Coach.first_name, coach.Coach.last_name)
       coachTitle = ""
       if(coach.CoachTitle != ''):
          coachTitle = coach.CoachTitle
        
       form = TeachCoachForm(instance=coach, initial={'CoachName': coachName, 'CoachTitle': coachTitle})
       assignedTeamID = coach.Team.TeamID
       context={'form': form, "TeamID": teamID}
       return render(request,'teams/coaches/EditCoach.html',context)
    elif(request.method== 'POST'):
         coachTitle = request.POST['CoachTitle']
         coach.CoachTitle = request.POST['CoachTitle']
         coach.save()
         msg= "{} record has been updated.".format(coachName)
         messages.success(request, msg)
         return redirect(to='team-coaches', id=teamID)

#TODO - add a TeamCoachView and include invite piece
#TODO - update the TeamCoach model to include job title
#TODO - Add to the team model Season Type (Fall, Winter, Spring or Summer) and Current Year
#TODO - When a new team is created, add the team to a new model that copies the TeamName, City, State, Zip, Season Type
#TODO - Add the ability create a game, set roster (posiiton, batting order) and enter game stats
#TODO - Add the ability to look stats per game for any team the user has access too.
#TODO - Allow MemberTypes of PARENT that is assigned to a team, to request to add their child from the roster.
#TODO - Create an approval queue for parents and coaches request accessing to a team or assigned a child to their contacts
#TODO - Pretty up the site.
#TODO - When creating a new team, allow the user, who is a coach on teams, to copy over the roster and parent contacts to the new team.
#TODO - Create a message module for a team that will allow users to create chat groups, request invite to chat in existing rooms and contriute chat in existing rooms.
#TODO - Deploy to linode.         
             
          