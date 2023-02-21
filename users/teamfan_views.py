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
def TeamFanView(request, id):
    currentTeam = get_object_or_404(Team, TeamID=id)
    if(request.method == 'GET'):
       team_fans_list = TeamFan.objects.filter(AssignedTeam_id =id).all()
       invite_form = TeamFanInviteForm()
       return render(request, 'teams/parents/TeamFans.html', {'invite_form': invite_form, 'teamfans': team_fans_list})
    elif(request.method =='POST'):
         inviteCode = User.objects.make_random_password(length=10, allowed_chars='123456789')
         currentTeam = get_object_or_404(Team, TeamID=id)
         TeamFanInviteRequest.objects.create(EmailContact=request.POST["EmailContact"], AssignedTeam=currentTeam, DateCreated=datetime.now(), DateApprovedRejected=datetime.now(), RequestStatus='PENDING', InviteCode=inviteCode, MemberType='PARENT')
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
         return redirect(to='team-fans', id=id)     

@login_required
def TeamFanRemoveView(request, id):
    teamFan = get_object_or_404(TeamFan, TeamFanID=id)
    if(request.method == 'GET'):
        teamFanName = "{} {}".format(teamFan.FanUser.first_name, teamFan.FanUser.last_name)
        fanAssignedTeamID = teamFan.AssignedTeam_id
        return render(request, 'teams/parents/TeamFanRemove.html', {"Name": teamFanName, "FanAssignedTeamID": fanAssignedTeamID})
    elif (request.method == 'POST'):
          teamFanID = teamFan.TeamFanID
          teamID = teamFan.AssignedTeam.TeamID
          teamFanUserID = teamFan.FanUser_id
          teamFanName = "{} {}".format(teamFan.FanUser.first_name, teamFan.FanUser.last_name)
          TeamFan.objects.filter(TeamFanID = teamFanID).delete()
          TeamMember.objects.filter(MemberUser_id = teamFanUserID).delete()
          msg= "{} has been removed from the team".format(teamFanName)
          messages.success(request, msg)
          return redirect(to='team-fans', id=teamID)    
