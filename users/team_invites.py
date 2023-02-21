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
def AllMyTeamInvitesView(request):
    if(request.method == 'GET'):
       # Show all active invites assigned to a person email address.
       currentUser = User.objects.filter(id=request.user.id).first()
       currentUserPrimaryEmail = currentUser.email
       teamOwnerMembers = TeamMember.objects.filter(TeamOwner=True).all()
       # My Approval Requests
       myApprovalRequests = AccessRequestQueue.objects.filter(Approver_id = currentUser.id).all()
       myApprovalRequestsCount = myApprovalRequests.count()
       # My Request For Approvals
       myRequestApprovals = AccessRequestQueue.objects.filter(Requestor_id = currentUser.id).all()
       myRequestApprovalsCount = myRequestApprovals.count()
       # Look up invites
       query = "select team.TeamID, team.TeamName, member.MemberType, invites.RequestStatus. invites.DateTimeCreated from users_team team inner join users_teammember member on member.AssignedTeam_id = team.TeamID inner join users_teamfaninviterequest invites on invites.AssignedTeam_id = team.TeamID where member.TeamOwner = 1;"
       invitesSentFromMeList = TeamFanInviteRequest.objects.filter(AssignedTeam_id=Subquery(TeamMember.objects.filter(MemberUser_id = request.user.id).values('AssignedTeam_id'))).all()
       teamsUserOwns = TeamMember.objects.filter(MemberUser_id = request.user.id).all()
       invitesSentFromMeListCount = invitesSentFromMeList.count()
       
       # Invites sent to me.
       invitesSentToMeList = TeamFanInviteRequest.objects.filter(EmailContact=currentUserPrimaryEmail).all()
       invitesSentToMeListCount = invitesSentToMeList.count()
       
       context = {"InviteList": invitesSentFromMeList, "InviteListCount": invitesSentFromMeListCount,  
                  "TeamOwners": teamOwnerMembers, "ApprovalRequests": myApprovalRequests, 
                  "ApprovalRequestsCount": myApprovalRequestsCount, "RequestForApprovals": myRequestApprovals,
                  "RequestForApprovalsCount": myRequestApprovalsCount, "MyTeamOwnership": teamsUserOwns,
                  'InvitesSentToMeList': invitesSentToMeList, "InvitesSentToMeListCount": invitesSentToMeListCount}
       return render(request, 'teams/invites/invites.html',context)

@login_required
def AcceptInviteView(request, id):
    if(request.method == 'GET'):
       inviteRequest = TeamFanInviteRequest.objects.filter(TeamFanInviteRequest=id).first()
       inviteRequest.RequestStatus='APPROVED'
       inviteRequest.DateApprovedRejected = datetime.now()
       inviteRequest.save()    
       inviteUserID = request.user.id
       inviteUser = User.objects.filter(id = inviteUserID).first()
       # Add the user to the team parents list.
       newUser = User.objects.filter(id = inviteUserID).first()
       if(TeamMember.objects.filter(MemberUser=inviteUser, AssignedTeam = inviteRequest.AssignedTeam).exists() == False):
          TeamMember.objects.create(MemberUser=inviteUser, MemberType=inviteRequest.MemberType, AssignedTeam = inviteRequest.AssignedTeam)
       
       if(inviteRequest.MemberType == 'COACH'):
          if(TeamCoach.objects.filter(Coach=inviteUser, Team=inviteRequest.AssignedTeam).exists() == False):
             TeamCoach.objects.create(Coach=inviteUser, Team=inviteRequest.AssignedTeam,IsHeadCoach=False,CoachTitle="")
       elif (inviteRequest.MemberType == 'PARENT'):
             if(TeamFan.objects.filter(FanUser=inviteUser, AssignedTeam = inviteRequest.AssignedTeam).exists() == False):
                TeamFan.objects.create(FanUser=inviteUser, AssignedTeam = inviteRequest.AssignedTeam)
                     
       return redirect(to='team-invites')
   
@login_required
def RejectInviteView(request, id):
    if(request.method == 'GET'):
       inviteRequest = TeamFanInviteRequest.objects.filter(TeamFanID=id).first()
       inviteRequest.Request='REJECTED'
       inviteRequest.DateApprovedRejected = datetime.now()
       inviteRequest.save()    
       return redirect(to='team-invites')
   
@login_required
def RequestForTeamAccessView(request):
      if (request.method == 'GET'):
        # Retrieve the list of sites the current user already has access to.
        #table1.objects.extra(where=["table1.id NOT IN (SELECT table2.key_to_table1 FROM table2 WHERE table2.id = some_parm)"])
        #teams=Team.objects.extra(where=["users_Team.TeamID NOT IN (SELECT users_TeamMember.AssignedTeam_id from users_TeamMember where users_TeamMember.MemberUser_id = {})".format(request.user.id)]).order_by('TeamName').all()
        #userAssignedTeams = TeamMember.objects.filter(MemberUser_id = request.user.id).all()
        #teams = Team.objects.order_by('TeamName').all()
        #teamsUserAssignedTo = TeamMember.objects.filter(MemberUser_id = request.user.id).all()
        #teamOwners = TeamMember.objects.all()
        #siteUsers = User.objects.all()
        #if('SearchTeam' in request.GET):
        #   searchTeam = request.GET['SearchTeam']
        #   teams = Team.objects.filter(TeamName__contains='{}'.format(searchTeam)).order_by('TeamName').all()
        #else:
        #    teams = Team.objects.order_by('TeamName').all()
        
        
        context = {}
        return render(request, 'teams/invites/RequestForTeamAccess.html',context)
      elif (request.method == 'POST'):
          teams = Team.objects.order_by('TeamName').all()
          teamsUserAssignedTo = TeamMember.objects.filter(MemberUser_id = request.user.id).all()
          teamOwners = TeamMember.objects.all()
          siteUsers = User.objects.all()
          if('SearchTeam' in request.POST):
             searchTeam = request.POST['SearchTeam']
             teams = Team.objects.filter(TeamName__contains='{}'.format(searchTeam)).order_by('TeamName').all()
              
        
          context = {'Teams': teams, 'UserTeams': teamsUserAssignedTo, 'TeamOwners': teamOwners, 'SiteUsers': siteUsers}
          return render(request, 'teams/invites/RequestForTeamAccess.html',context)
@login_required
def RequestForTeamAccessAction(request,id):
    teamID = id
    team = Team.objects.filter(TeamID = id).first()
    teamName = Team.objects.filter(TeamID = teamID).values('TeamName').first()
    requestAccessType = 'FAN'
    context={'TeamID': teamID, 'TeamName': teamName['TeamName'], 'RequestAccessType': requestAccessType} 
    
    if(request.method == 'GET'):
       teamID = id
       teamName = Team.objects.filter(TeamID = teamID).values('TeamName').first()
       requestAccessType = 'FAN'
       context={'TeamID': teamID, 'TeamName': teamName['TeamName'], 'RequestAccessType': requestAccessType} 
       
    elif(request.method == 'POST'):
         if 'fanaccess' in request.POST:
             requestUser = User.objects.filter(id = request.user.id).first()
             approverUserID = TeamMember.objects.filter(AssignedTeam_id = teamID).values('MemberUser_id').first()['MemberUser_id']
             approverUser = User.objects.filter(id = approverUserID).first()
             memberType='PARENT'
             requestCreated = datetime.now()
             requestModified = datetime.now()
             requestStatus = 'PENDING'
             AccessRequestQueue.objects.create(Requestor=requestUser, Approver=approverUser, TeamRequested=team,  MemberType=memberType,DateTimeCreated=requestCreated,DateTimeModified=requestModified, RequestStatus=requestStatus)
             messages.success(request, 'Your FAN request access has been submitted.')
             return redirect(to='team-invites-access')
         elif 'coachaccess' in request.POST:
              requestUser = User.objects.filter(id = request.user.id).first()
              approverUserID = TeamMember.objects.filter(AssignedTeam_id = teamID).values('MemberUser_id').first()['MemberUser_id']
              approverUser = User.objects.filter(id = approverUserID).first()
              memberType='COACH'
              requestCreated = datetime.now()
              requestModified = datetime.now()
              requestStatus = 'PENDING'
              AccessRequestQueue.objects.create(Requestor=requestUser, Approver=approverUser, TeamRequested=team,  MemberType=memberType, DateTimeCreated=requestCreated,DateTimeModified=requestModified, RequestStatus=requestStatus)
              messages.success(request, 'Your COACH request access has been submitted.')
              return redirect(to='team-invites-access')
    return render(request, 'teams/invites/RequestForTeamAccessView.html', context)
      
@login_required
def RequestForTeamFanAccessView(request, id):
    teamID = id
    teamName = Team.objects.filter(TeamID = teamID).values('TeamName').first()
    requestAccessType = 'FAN'
    context={'TeamID': teamID, 'TeamName': teamName['TeamName'], 'RequestAccessType': requestAccessType} 
    
    #TODO - figure out to send this object over to the next page.
    return render(request, 'teams/invites/RequestForTeamAccessView.html', context)

@login_required
def RequestForTeamCoachAccessView(request, id):
    teamID = id
    teamName = Team.objects.filter(TeamID = teamID).values('TeamName').first()
    requestAccessType = 'COACH'
    context={'TeamID': teamID, 'TeamName': teamName, 'RequestAccessType': requestAccessType} 
    return render(request, 'teams/invites/RequestForTeamAccessView.html', context)   
       
@login_required
def RequestForTeamFanAccessAction(request, id):
    teamID = id
    team = Team.objects.filter(TeamID = id).first()
    requestUser = User.objects.filter(id = request.user.id).first()
    approverUserID = TeamMember.objects.filter(AssignedTeam_id = teamID).values('MemberUser_id').first()['MemberUser_id']
    approverUser = User.objects.filter(id = approverUserID).first()
    memberType='PARENT'
    requestCreated = datetime.now()
    requestModified = datetime.now()
    requestStatus = 'PENDING'
    AccessRequestQueue.objects.create(Requestor=requestUser, Approver=approverUser, TeamRequested=team,  MemberType=memberType, 
                                      DateTimeCreated=requestCreated,DateTimeModified=requestModified, RequestStatus=requestStatus)
    context={}
    return render(request, 'teams/invites/RequestForTeamAccess.html',context)
 
@login_required
def RequestForTeamCoachAccessAction(request, id):
    teamID = id
    team = Team.objects.filter(TeamID = id).first()
    requestUser = User.objects.filter(id = request.user.id).first()
    approverUserID = TeamMember.objects.filter(AssignedTeam_id = teamID).values('MemberUser_id').first()['MemberUser_id']
    approverUser = User.objects.filter(id = approverUserID).first()
    memberType='COACH'
    requestCreated = datetime.now
    requestModified = datetime.now
    requestStatus = 'PENDING'
    AccessRequestQueue.objects.create(RequestorUser=requestUser, ApproverUser=approverUser, 
                                     RequestedTeam=team, MemberType=memberType, RequestCreated=requestCreated,
                                     RequestModifed=requestModified, RequestStatus=requestStatus)
    context={}
    return render(request, 'teams/invites/RequestForTeamAccess.html',context)


@login_required
def ApproveUserTeamAccessAction(request, id):
    if request.method == 'GET':
       accessRequest = AccessRequestQueue.objects.filter(AccessRequestQueueID=id).first()
       requestUserID = accessRequest.Requestor_id
       requestor = User.objects.filter(id = requestUserID).first()
       requestorName = "{} {}".format(requestor.first_name, requestor.last_name)
       team = Team.objects.filter(TeamID =accessRequest.TeamRequested_id).first()
       teamName = team.TeamName
       requestID = id
       accessType = accessRequest.MemberType
       context = {"Requester": requestorName, 'TeamName': teamName, "RequestID": requestID, "AccessRequest": accessType }
       return render(request, "teams/invites/ApproveRejectUserRequestView.html", context)
    elif request.method == 'POST':
         if 'ApproveAction' in request.POST:
             requestStatus = "APPROVED"
             accessRequest = AccessRequestQueue.objects.filter(AccessRequestQueueID=id).first()
             accessRequest.RequestStatus = requestStatus
             accessRequest.DateTimeModified = datetime.now()
             accessRequest.save()
             messages.success(request, 'You assigned request has been updated.')
             return redirect(to='team-invites')
         elif 'RejectAction' in request.POST:
               requestStatus = "REJECTED"
               accessRequest = AccessRequestQueue.objects.filter(AccessRequestQueueID=id).first()
               accessRequest.RequestStatus = requestStatus
               accessRequest.DateTimeModified = datetime.now()
               accessRequest.save()
               messages.success(request, 'You assigned request has been updated.')
               return redirect(to='team-invites')
            
       

#TODO: Cascading drop down on state and city select controls on the RequestForTeamAccess.html page.
#TODO: Allow to conduct a search
#TODO: Allow users to request for access to team.
#TODO: Let the approver know they have requests to approve, maybe show a number next to the Invite header menu. 
#TODO: Create a new section on teh invites.html, load the data.