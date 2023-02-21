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
def EditWebsiteDetailsView(request, id):
    
    if request.method == 'GET':
       websiteContent = get_object_or_404(TeamWebsite, TeamWebsiteID=id)
       website_form = TeamSiteForm(instance=websiteContent)
       website_document_form = TeamSiteDocumentsForm()
       website_documents_list = TeamDocument.objects.filter(SiteID_id=id).all()
       website_links_list = TeamWebsiteExternalLink.objects.filter(SiteID_id=id).all()
       website_link_form = TeamSiteLinksForm()
       context = {'website_form': website_form, 
                  'website_document_form': website_document_form, 
                  'website_link_form': website_link_form,
                  'website_documents_list': website_documents_list, 
                  'website_links_list': website_links_list}
       return render(request, 'teams/site/EditWebsite.html', context)
    elif request.method == 'POST':
         websiteContent = get_object_or_404(TeamWebsite, TeamWebsiteID=id)
         if 'websitecontent' in request.POST:
             form = TeamSiteForm(request.POST, files = request.FILES, instance=websiteContent)
             if form.is_valid():
                form.save()
                TeamWebsite.objects.filter(TeamWebsiteID = id).update(SiteStyleOption = request.POST["SiteStyleOption"])
                messages.success(request, 'Website content changes has been saved.')
                return redirect(to='website-edit', id=id)
         elif 'websitedocuments' in request.POST:
               form = TeamSiteDocumentsForm(request.POST, files = request.FILES, instance=websiteContent)
               if form.is_valid():
                  _showOnPublicWebsite = False
                  if request.POST.get("ShowOnPublicWebsite") != None and request.POST['ShowOnPublicWebsite'] == 'on':
                     _showOnPublicWebsite = True
                  _showOnInternalWebsite = False
                  if request.POST.get("ShowOnInternalWebsite") != None and request.POST['ShowOnInternalWebsite'] == 'on':
                     _showOnInternalWebsite = True
                  newDocument = TeamDocument(Document=request.FILES['Document'], SiteID_id=id, 
                                             ShowOnPublicWebsite=_showOnPublicWebsite, ShowOnInternalWebsite=_showOnInternalWebsite, FileName=request.POST["FileName"])
                  newDocument.save()
                  messages.success(request, '{} document has been saved.'.format(request.POST["FileName"]))
                  return redirect(to='website-edit', id=id)
              
         elif 'websitelinks' in request.POST:
               form = TeamSiteLinksForm(request.POST, files = request.FILES, instance=websiteContent)
               if form.is_valid():
                  _showOnPublicWebsite = False
                  if request.POST.get("ShowOnPublicWebsite") != None and request.POST['ShowOnPublicWebsite'] == 'on':
                     _showOnPublicWebsite = True
                  _showOnInternalWebsite = False
                  if request.POST.get("ShowOnInternalWebsite") != None and request.POST['ShowOnInternalWebsite'] == 'on':
                     _showOnInternalWebsite = True
                     
                  newLink = TeamWebsiteExternalLink(LinkName=request.POST['LinkName'], SiteID_id=id, Url=request.POST['Url'],
                                                    ShowOnPublicWebsite=_showOnPublicWebsite, ShowOnInternalWebsite=_showOnInternalWebsite) 
                  newLink.save()
                  messages.success(request, '{} link has been created.'.format(request.POST['LinkName']))
                  return redirect(to='website-edit', id=id)
   
def PublicWebsiteView(request, id):
    publicWebsite = get_object_or_404(TeamWebsite, TeamWebsiteID=id)
    site_documents = TeamDocument.objects.filter(SiteID_id=id, ShowOnPublicWebsite=True).all()
    site_links = TeamWebsiteExternalLink.objects.filter(SiteID_id=id, ShowOnPublicWebsite=True).all()
    return render(request, 'teams/site/public/teamsite.html', {'website': publicWebsite, "documents": site_documents, 'links': site_links})
    
@login_required
def EditDeleteWebsiteDocument(request, id):
    document = get_object_or_404(TeamDocument, TeamDocumentID=id)
    documentFileName = document.FileName
    websiteID = document.SiteID_id
    if request.method == 'GET':
        context = {'team_document_form': TeamSiteDocumentsForm(instance=document), 'id': id, 'FileName': document.FileName, 'TeamWebSiteID': websiteID}
        return render(request,'teams/site/EditDeleteDocument.html',context)
    elif request.method == 'POST':
         if 'updatedocument' in request.POST:
             form = TeamSiteDocumentsForm(request.POST, files = request.FILES, instance=document)
             if form.is_valid():
                form.save()
                msg = "{} document properties has been updated.".format(documentFileName)
         elif 'deletedocument' in request.POST:
               TeamDocument.objects.filter(TeamDocumentID=id).delete()
               msg = "{} link has been deleted.".format(documentFileName)
         
         messages.success(request, msg)
         return redirect(to='website-edit', id=websiteID)
     
@login_required
def EditDeleteWebsiteLink(request, id):
    link = get_object_or_404(TeamWebsiteExternalLink, LinkID=id)
    linkName = link.LinkName
    websiteID = link.SiteID_id
    if request.method == 'GET':
        context = {'team_link_form': TeamSiteLinksForm(instance=link), 'id': id, 'LinkName': link.LinkName, 'TeamWebSiteID': websiteID}
        return render(request,'teams/site/EditDeleteExternalLink.html',context)
    elif request.method == 'POST':
         if 'updatelink' in request.POST:
             form = TeamSiteLinksForm(request.POST, instance=link)
             if form.is_valid():
                form.save()
                msg = "{} link has been updated.".format(linkName)
         elif 'deletelink' in request.POST:
               TeamWebsiteExternalLink.objects.filter(LinkID=id).delete()
               msg = "{} link has been deleted.".format(linkName)
         
         messages.success(request, msg)
         return redirect(to='website-edit', id=websiteID)
