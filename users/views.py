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


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        inviteCode = ""
        if('invitecode' in request.POST):
           # check if the user provided an invite code
           
           inviteCode = request.POST["invitecode"]
           if(inviteCode != ''):
              validRequest = TeamFanInviteRequest.objects.filter(InviteCode=inviteCode)
              if(validRequest.exists()==False):
                 messages.error(request, f'You have enter an invalid invite code {inviteCode}')
                 return render(request, self.template_name, {'form': form})
              elif validRequest.first().RequestStatus == 'APPROVED' or validRequest.first().RequestStatus == 'REJECTED':
                   messages.error(request, 'This invite code had already be used.')
                   return render(request, self.template_name, {'form': form})
                         
        if form.is_valid():
            form.save()
            # Look up the invite code and update the TeamFanInviteRequest table. Assign the user to the team.
            #if('invitecode' in request.POST):
            if(inviteCode != ''):
               inviteRequest =TeamFanInviteRequest.objects.filter(InviteCode=inviteCode).first()
               inviteRequest.RequestStatus = "APPROVED"
               inviteRequest.DateApprovedRejected = datetime.now()
               inviteRequest.save()
               # Add the user to the team parents list.
               newUser = User.objects.filter(username=request.POST['username']).first()
               TeamMember.objects.create(MemberUser=newUser, MemberType=inviteRequest.MemberType, AssignedTeam = inviteRequest.AssignedTeam)
               if(inviteRequest.MemberType == 'COACH'):
                  TeamCoach.objects.create(Coach=newUser, Team=inviteRequest.AssignedTeam,IsHeadCoach=False,CoachTitle="")
               elif (inviteRequest.MemberType == 'PARENT'):
                     TeamFan.objects.create(FanUser=newUser, AssignedTeam = inviteRequest.AssignedTeam)
               
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})





#TODO - Add the ability create a game, set roster (posiiton, batting order) and enter game stats
#TODO - Add the ability to look stats per game for any team the user has access too.
#TODO - Pretty up the site.
#TODO - When creating a new team, allow the user, who is a coach on teams, to copy over the roster and parent contacts to the new team.
#TODO - Create a message module for a team that will allow users to create chat groups, request invite to chat in existing rooms and contriute chat in existing rooms.
#TODO - Deploy to linode.         
             
          