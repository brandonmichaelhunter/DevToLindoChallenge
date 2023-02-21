from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    invitecode = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'InviteCode',
                                                             'class': 'form-control',
                                                             }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2','invitecode']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

SEASON_LIST = [('','-----'),('FALL','FALL'),('SPRING','SPRING'),('SUMMER','SUMMER'),('SPRING','SPRING')]        
YEAR_IN_SCHOOL_LIST = [('','-----'),('FR','FRESHMAN'),('SO','SOPHOMORE'),('JR','JUNIOR'),('SR','SENIOR'),('GR','GRADUATE')]
THROWING_BATTING_HAND_LIST = [('', '-----'), ('R','Right'), ('L', 'Left'), ('B', 'Both')]
USER_TYPE_LIST =[('','-----'), ('P', 'Parent'), ('C', 'Coach'), ('PL', 'Player'), ('PC', 'Parent\Coach')]
COLORS_LIST = [('','-----'),]
SITE_STYLE_OPTIONS_LIST = [('','-----'),('default','Default'),('cerulean','Cerulean'),('cosmo','Cosmo'),('cyborg','Cyborg'),('flatly','Flatly'),('journal','Journal'),('litera','Litera'),('lumen','Lumen'),('lux','Lux'),('materia','Materia'),('minty','Minty'),('morph','Morph'),('pulse','Pulse'),('quartz','Quartz'),('sandstone','Sandstone'),('simplex','Simplex'),('sketchy','Sketchy'),('slate','Slate'),('solar','Solar'),('spacelab','Spacelab'),('superhero','Superhero'),('united','United'),('vapor','Vapor'),('yeti','Yeti'),('zephyr','Zephyr')]
FIELD_POSITION_LIST = [('','-----'), ('1B','FIRSTBASE'),('2B','SECONDBASE'),('SS','SHORTSTOP'),('3B','THIRDBASE' ),('LF','LEFTFIELD' ),('CF','CENTERFIELD'),('RG','RIGHTFIELD'),('DH','DESIGNATEDHITTER'),('P','PITCHER'),('C','CATCHER')]

class UpdateProfileForm(forms.ModelForm):
    
    avatar = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    BirthDate = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    PrimaryEmail = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    SecondaryEmail = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    PrimaryPhone = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    SecondPhone = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    City = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    State = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    Zip = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ThrowingHand = forms.ChoiceField(required=False,choices=THROWING_BATTING_HAND_LIST, widget=forms.Select(attrs={'class':'form-control'}))
    BattingHand = forms.ChoiceField(required=False,choices=THROWING_BATTING_HAND_LIST, widget=forms.Select(attrs={'class':'form-control'}))
    ShootingHand = forms.ChoiceField(required=False,choices=THROWING_BATTING_HAND_LIST, widget=forms.Select(attrs={'class':'form-control'}))
    UserType = forms.ChoiceField(required=False,choices=USER_TYPE_LIST, widget=forms.Select(attrs={'class':'form-control'}))
    YearInSchool = forms.ChoiceField(required=False,choices=YEAR_IN_SCHOOL_LIST, widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'BirthDate', 'PrimaryEmail','SecondaryEmail', 'PrimaryPhone','SecondPhone', 
                  'City', 'State', 'Zip', 'ThrowingHand', 'BattingHand',
                  'ShootingHand', 'UserType', 'YearInSchool']

class CreateTeamForm(forms.ModelForm):
      TeamName = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      PrimaryEmail = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SecondaryEmail = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      PrimaryPhone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SecondaryPhone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      City = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      State = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      Zip = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SportType = forms.ModelChoiceField(required=False, queryset=TeamType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'})) 
      TeamLogo = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control-file'}))
      Season = forms.ChoiceField(required=False,choices=SEASON_LIST, widget=forms.Select(attrs={'class':'form-control'}))
      class Meta:
        model = Team
        fields = ['TeamName', 'PrimaryEmail', 'SecondaryEmail', 'PrimaryPhone','SecondaryPhone', 'City','State', 
                  'Zip', 'State', 'Zip', 'SportType', 'TeamLogo', 'Season']
        
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['SportType'].queryset = TeamType.objects.all()
           
class EditTeamForm(forms.ModelForm):
      TeamName = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      PrimaryEmail = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SecondaryEmail = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      PrimaryPhone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SecondaryPhone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      City = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      State = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      Zip = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SportType = forms.ModelChoiceField(required=False, queryset=TeamType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'})) 
      TeamLogo = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control-file'}))
      Season = forms.ChoiceField(required=False,choices=SEASON_LIST, widget=forms.Select(attrs={'class':'form-control'}))
      class Meta:
        model = Team
        fields = ['TeamName', 'PrimaryEmail', 'SecondaryEmail', 'PrimaryPhone','SecondaryPhone', 'City','State', 
                  'Zip', 'State', 'Zip', 'SportType', 'TeamLogo', 'Season']
        
    #   def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     #self.fields['SportType'].queryset = TeamType.objects.all()
        
      def clean(self):
        # Check that email is not duplicate
        teamName = self.cleaned_data["TeamName"]
        email = self.cleaned_data["PrimaryEmail"]
        email = Team.objects.filter(PrimaryEmail=email).exclude(TeamName=teamName)
        if email:
            raise forms.ValidationError('A team with that email already exists.')
        
class DeleteTeamForm(forms.ModelForm):
      TeamName = forms.CharField(required=True,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      PrimaryEmail = forms.EmailField(required=False,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SecondaryEmail = forms.CharField(required=False,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      PrimaryPhone = forms.CharField(required=False,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SecondaryPhone = forms.CharField(required=False,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      City = forms.CharField(required=False,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      State = forms.CharField(required=False,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      Zip = forms.CharField(required=False,  disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      SportType = forms.ModelChoiceField(required=False,  disabled=True, queryset=TeamType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'})) 
      TeamLogo = forms.ImageField(required=False,  disabled=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
      Season = forms.ChoiceField(required=False,choices=SEASON_LIST, widget=forms.Select(attrs={'class':'form-control'}))

      class Meta:
        model = Team
        fields = ['TeamName', 'PrimaryEmail', 'SecondaryEmail', 'PrimaryPhone','SecondaryPhone', 'City','State', 
                  'Zip', 'State', 'Zip', 'SportType', 'TeamLogo', 'Season']
        
    #   def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     #self.fields['SportType'].queryset = TeamType.objects.all()
        
      def clean(self):
        # Check that email is not duplicate
        teamName = self.cleaned_data["TeamName"]
        email = self.cleaned_data["PrimaryEmail"]
        email = Team.objects.filter(PrimaryEmail=email).exclude(TeamName=teamName)
        if email:
            raise forms.ValidationError('A team with that email already exists.')
          
class TeamSiteForm(forms.ModelForm):
      SiteTitle = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
      HeaderImage = forms.ImageField(required=False,   widget=forms.FileInput(attrs={'class': 'form-control-file'}))
      MissionStatement = forms.CharField(required=False, 
                                         widget=forms.TextInput(attrs={'class': 'form-control'}))
      ShowRoster = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
      ShowCoaches = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
      ShowPlayerMedia = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
      ShowGamesAndStats = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
      SiteStyleOption = forms.ChoiceField(required=False,choices=SITE_STYLE_OPTIONS_LIST, widget=forms.Select(attrs={'class':'form-control'}))
    
      class Meta:
        model = TeamWebsite
        fields = ['SiteTitle', 'HeaderImage',  'MissionStatement', 'ShowRoster','ShowCoaches', 
                  'ShowPlayerMedia', 'ShowGamesAndStats','SiteStyleOption']
        
    #   def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     #self.fields['SportType'].queryset = TeamType.objects.all()
        
      # def clean(self):
      #   # Check that email is not duplicate
      #   teamName = self.cleaned_data["TeamName"]
      #   email = self.cleaned_data["PrimaryEmail"]
      #   email = Team.objects.filter(PrimaryEmail=email).exclude(TeamName=teamName)
      #   if email:
      #       raise forms.ValidationError('A team with that email already exists.')
      
class TeamSiteLinksForm(forms.ModelForm):
      LinkName = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      Url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
      ShowOnPublicWebsite = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
      ShowOnInternalWebsite = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    
      class Meta:
        model = TeamDocument
        fields = ['LinkName', 'Url', 'ShowOnPublicWebsite',  'ShowOnInternalWebsite']
        
class TeamSiteDocumentsForm(forms.ModelForm):
      Document = forms.FileField(required=False,widget=forms.FileInput(attrs={'class': 'form-control-file'}))
      FileName = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      ShowOnPublicWebsite = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
      ShowOnInternalWebsite = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
      
    
      class Meta:
        model = TeamDocument
        fields = ['Document', 'FileName', 'ShowOnPublicWebsite',  'ShowOnInternalWebsite']
        
class TeamRosterForm(forms.ModelForm):
      FirstName = forms.CharField(required=False,label="First Name",widget=forms.TextInput(attrs={'class': 'form-control'}))
      MiddleName = forms.CharField(required=False, label="Middle Name",widget=forms.TextInput(attrs={'class': 'form-control'}))
      LastName = forms.CharField(required=False, label="Last Name",widget=forms.TextInput(attrs={'class': 'form-control'}))
      JerseyNumber = forms.CharField(required=False, label="Jersey Number",widget=forms.TextInput(attrs={'class': 'form-control'}))
      ThrowingHand = forms.ChoiceField(required=False,label="Throwing Hand",choices=THROWING_BATTING_HAND_LIST, widget=forms.Select(attrs={'class':'form-control'}))
      BattingHand = forms.ChoiceField(required=False,label="Batting Hand",choices=THROWING_BATTING_HAND_LIST, widget=forms.Select(attrs={'class':'form-control'}))
      ProfileImage =forms.ImageField(required=False,label="Profile Image",widget=forms.FileInput(attrs={'class': 'form-control-file'}))
      class Meta:
        model=TeamRoster
        fields = ['FirstName', 'MiddleName', 'LastName', 'JerseyNumber','ThrowingHand','BattingHand','ProfileImage']
        exclude =["Team"]
        
class TeamFanInviteForm(forms.ModelForm):
      EmailContact = forms.CharField(required = False, label="Invitee Email Address", widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      class Meta:
        model=TeamFanInviteRequest
        fields = ['EmailContact']
        exclude =['RequestStatus', 'DateCreated', 'DateApprovedRejected', 'InviteCode']        
        
class TeachCoachForm(forms.ModelForm):
      CoachName =  forms.CharField(required=False, disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'})) 
      CoachTitle = forms.CharField(required=False, disabled=False, widget=forms.TextInput(attrs={'class': 'form-control'})) 
      
      class Meta:
        model=TeamCoach
        fields = ['CoachName', 'CoachTitle']
        
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #self.fields['SportType'].queryset = TeamType.objects.all()
             
class TeamPracticeForm(forms.ModelForm):
      FieldLocation = forms.CharField(required=False,label="Field Location",widget=forms.TextInput(attrs={'class': 'form-control'}))
      AssignedTeam = forms.ModelChoiceField(required=False,disabled=True, queryset=Team.objects.all(), widget=forms.Select(attrs={'class': 'form-control '}))  
      StartGameDateTime = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],label="Start Practice Time", required=False,widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
      EndGameDateTime = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],label="End Practice Time",required=False,widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
      AdditionalInfo = forms.CharField(required=False,label="Additonal Practice Info",widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      class Meta:
        model=TeamPractice
        fields=['FieldLocation', 'AssignedTeam', 'StartGameDateTime', 'EndGameDateTime' ,'AdditionalInfo'] 
        
class TeamGameForm(forms.ModelForm):
      HomeTeam = forms.ModelChoiceField(required=False, queryset=Team.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))  
      AwayTeam = forms.ModelChoiceField(required=False, queryset=Team.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
      StartGameDateTime = forms.DateTimeField(label="Start Time", required=False,widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
      EndGameDateTime = forms.DateTimeField(label="End Time (Estimated)", required=False,widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
      Location = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      class Meta:
        model=TeamGame
        fields=['HomeTeam', 'AwayTeam', 'StartGameDateTime', 'EndGameDateTime' ,'Location'] 
        
class GamePlayerForm(forms.ModelForm):
      AssignedGame = forms.ModelChoiceField(required=False, queryset=TeamGame.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))  
      AssignedTeam=forms.ModelChoiceField(required=False, queryset=Team.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))  
      FirstName = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      MiddleName = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      LastName = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'})) 
      # FullName = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      JerseyNumber = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      ThrowingHand = forms.ChoiceField(required=False,choices=THROWING_BATTING_HAND_LIST, widget=forms.Select(attrs={'class':'form-control'}))
      BattingHand = forms.ChoiceField(required=False,choices=THROWING_BATTING_HAND_LIST, widget=forms.Select(attrs={'class':'form-control'}))
      BattingOrder = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      FieldPosition = forms.ChoiceField(required=False,choices=FIELD_POSITION_LIST, widget=forms.Select(attrs={'class':'form-control'}))
      PlayerID = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      
      
      class Meta:
        model=GamePlayer
        fields=['AssignedGame', 'AssignedTeam', 'FirstName', 'MiddleName' ,'LastName','JerseyNumber','ThrowingHand','BattingHand','BattingOrder','FieldPosition'] 
        exclude=['FullName', 'PlayerID']
        
class BatterGameStatForm(forms.ModelForm):
  
      Position = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      AssignedPlayer = forms.ModelChoiceField(required=False, queryset=GamePlayer.objects.all(), widget=forms.Select(attrs={'class': 'form-control'})) 
      AtBats = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Runs = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Hits = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      RBI = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BaseOnBalls = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      StrikeOuts=forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BattingAverage = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      OBP= forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      
      class Meta:
        model=BatterGameStat
        fields=['Position', 'AssignedPlayer', 'AtBats', 'Runs' ,'Hits','RBI','BaseOnBalls','StrikeOuts','BattingAverage','OBP'] 
        
class PitcherGameStatForm(forms.ModelForm):

      AssignedPlayer = forms.ModelChoiceField(required=False, queryset=GamePlayer.objects.filter(FieldPosition="P").all(), widget=forms.Select(attrs={'class': 'form-control'})) 
      InningsPitch = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Hits = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Runs = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      EarnRuns = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BaseOnBalls = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      StrikeOuts = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BattersFaced = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      EarnRunAverage = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Loss = forms.BooleanField(required=False)
      Won = forms.BooleanField(required=False)
      
      
      class Meta:
        model=PitcherGameStat
        fields=['AssignedPlayer', 'InningsPitch', 'Hits', 'Runs' ,'EarnRuns','BaseOnBalls','StrikeOuts','BattersFaced','EarnRunAverage','Loss', 'Won'] 
        
class TeamBatterStatTotalForm(forms.ModelForm):

      AssignedGame = forms.ModelChoiceField(required=False, queryset=TeamGame.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))  
      AssignedTeam = forms.ModelChoiceField(required=False, queryset=Team.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))   
      AtBats = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Runs = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Hits = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      RBI = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BaseOnBalls = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      StrikeOuts=forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BattingAverage = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      OBP= forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'})) 
      
      
      
      class Meta:
        model=TeamBatterStatTotal
        fields=['AssignedGame', 'AssignedTeam', 'AtBats', 'Runs' ,'Hits','RBI','BaseOnBalls','StrikeOuts','BattingAverage','OBP'] 

class TeamPitcherStatTotalForm(forms.ModelForm):

      AssignedGame = forms.ModelChoiceField(required=False, queryset=TeamGame.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))  
      AssignedTeam = forms.ModelChoiceField(required=False, queryset=Team.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))   
      InningsPitch = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Hits = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      Runs = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      EarnRuns = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BaseOnBalls=forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      StrikeOuts = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      BattersFaced= forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'})) 
      EarnRunAverage= forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
      
      class Meta:
        model=TeamPitcherStatTotal
        fields=['AssignedGame', 'AssignedTeam', 'InningsPitch', 'Hits' ,'Runs','EarnRuns','BaseOnBalls','StrikeOuts','BattersFaced','EarnRunAverage'] 
