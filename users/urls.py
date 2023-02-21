from django.urls import path
from .views import home, profile, RegisterView 
from .team_views import CreateTeam, DeleteTeamView,EditTeamView,AllTeamsView
from .teamsite_views import EditDeleteWebsiteDocument, PublicWebsiteView,EditWebsiteDetailsView,EditDeleteWebsiteLink
from .teamcoach_views import TeamCoachView, TeamCoachRemoveView,EditTeamCoachDetailView
from .teamfan_views import TeamFanView,TeamFanRemoveView
from .teamroster_views import TeamRosterView, EditTeamRosterView,DeleteTeamRosterView
from .team_invites import *
from .team_events import *
urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('team/createteam', CreateTeam, name='createteam'),
    path('team/', AllTeamsView, name='teams'),
    path('team/edit/<int:id>/', EditTeamView, name='teamedit'),
    path('team/remove/<int:id>/', DeleteTeamView, name='teamdelete'),
    path('team/sites/public/<int:id>/', PublicWebsiteView, name='publicteamsite'),
    path('team/sites/internal/<int:id>/', RegisterView.as_view(), name='internalteamsite'),
    path('team/sites/<int:id>', EditWebsiteDetailsView, name='website-edit' ),
    path('team/sites/documents/edit/<int:id>', EditDeleteWebsiteDocument, name='website-editdelete-document'),
    path('team/sites/links/edit/<int:id>', EditDeleteWebsiteLink, name='website-editdelete-link'),
    path('team/rosters/<int:id>', TeamRosterView, name='team-rosters'),
    path('team/rosters/edit/<int:id>', EditTeamRosterView, name='team-edit-roster'),
    path('team/rosters/delete/<int:id>', DeleteTeamRosterView, name='team-delete-roster'),
    path('team/fans/<int:id>', TeamFanView, name='team-fans'),
    path('team/fans/remove/<int:id>', TeamFanRemoveView, name='team-fans-remove'),
    path('team/coaches/<int:id>', TeamCoachView, name='team-coaches'),
    path('team/coaches/edit/<int:id>', EditTeamCoachDetailView, name='team-edit-coach'),
    path('team/coaches/remove/<int:id>', TeamCoachRemoveView, name='team-remove-coach'),
    path('team/invites', AllMyTeamInvitesView, name='team-invites'),
    path('team/invites/accept/<int:id>', AcceptInviteView, name='team-accept-invite'),
    path('team/invites/decline/<int:id>', RejectInviteView, name='team-reject-invite'),
    path('team/invites/requestforaccess', RequestForTeamAccessView,name='team-invites-access' ),
    path('team/invites/requestforteamaccess/action/<int:id>', RequestForTeamAccessAction, name='team-request-team-access-action'),
    path('team/invites/requestforfanaccess/<int:id>', RequestForTeamFanAccessView, name='team-request-fan-access'),
    path('team/invites/requestforcoachaccess/<int:id>', RequestForTeamCoachAccessView, name='team-request-coach-access'),
    path('team/approvals/approverequest/<int:id>', ApproveUserTeamAccessAction, name="team-approve-user-request"),
    path('team/events/<int:id>', AllTeamEventsView, name="team-events"),
    path('team/event/practice/create/<int:id>', CreateTeamPracticeViewAction, name="team-practice-create"),
    path('team/event/practice/edit/<int:id>', UpdateTeamPracticeViewAction, name="team-practice"),
    path('team/event/game/home/create/<int:id>', CreateHomeTeamGameViewAction, name="team-home-game-create"),
    path('team/event/game/away/create/<int:id>', CreateAwayTeamGameViewAction, name="team-away-game-create"),
    path('team/event/game/home/edit/<int:id>', UpdateHomeTeamGameViewAction, name="team-home-game-edit"),
    path('team/event/game/away/edit/<int:id>', UpdateAwayTeamGameViewAction, name="team-away-game-edit"),
    path('team/event/game/home/edit/stats/<int:id>', UpdateHomeTeamsGameStatViewAction, name="team-home-game-stats-edit"),
    path('team/event/game/away/edit/stats/<int:id>', UpdateAwayTeamsGameStatViewAction, name="team-away-game-stats-edit"),
]
