from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(TeamType)
admin.site.register(Sport)
# admin.site.register(UserType)
admin.site.register(Team)
admin.site.register(TeamRoster)
admin.site.register(TeamCoach)
admin.site.register(UserRelationship)
admin.site.register(TeamWebsite)
admin.site.register(TeamDocument)
admin.site.register(TeamWebsiteExternalLink)