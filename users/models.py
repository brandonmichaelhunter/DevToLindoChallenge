import os
from django.db import models
from django.contrib.auth.models import User, Group
from PIL import Image
import uuid
import datetime

# Extending User Model Using a One-To-One Link
class TeamType(models.Model):
      TeamTypeID = models.AutoField(primary_key=True)
      Type=models.CharField(max_length=100)
      
      def __str__(self):
          return "{}".format(self.Type)
class Sport(models.Model):
      SportID = models.AutoField(primary_key=True)
      Name = models.CharField(max_length=100, null=False)
      
      def __str__(self):
          return "{}".format(self.Name)

class Profile(models.Model):
    class ThrowingBattingHand(models.TextChoices):
        RIGHT = 'R'
        LEFT = 'L'
        BOTH='B'
    class Grade(models.TextChoices):
        FRESHMAN = 'FR'
        SOPHOMORE = 'SO'
        JUNIOR = 'JR'
        SENIOR = 'SR'
        GRADUATE = 'GR'
    class UserTypeList(models.TextChoices):
          PARENT='P'
          COACH='C'
          PLAYER='PL'
          PARENTCOACH='PC'      
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    BirthDate = models.DateField(null=True)
    PrimaryEmail = models.EmailField(null=True, unique=False)
    SecondaryEmail = models.EmailField(null=True, unique=False)
    PrimaryPhone = models.CharField(max_length=12, null=True)
    SecondPhone = models.CharField(max_length=12, null=True)
    City = models.CharField(max_length=2000,null=True)
    State = models.CharField(max_length=2000,null=True)
    Zip = models.CharField(max_length=2000,null=True)
    ThrowingHand = models.CharField(max_length=2000, choices=ThrowingBattingHand.choices, default=ThrowingBattingHand.RIGHT,)
    BattingHand = models.CharField(max_length=2000, choices=ThrowingBattingHand.choices, default=ThrowingBattingHand.RIGHT,)
    ShootingHand = models.CharField(max_length=2000, choices=ThrowingBattingHand.choices, default=ThrowingBattingHand.RIGHT,)
    UserType = models.CharField(max_length=2000, choices=UserTypeList.choices, default=UserTypeList.PLAYER,)
    YearInSchool = models.CharField(max_length=200, choices=Grade.choices, default=Grade.FRESHMAN, null=True)
    
    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class SiteStyle(models.Model):
      SiteStyleID = models.AutoField(primary_key=True)
      Style = models.CharField(max_length=1000)
      Active = models.BooleanField(default=False)
class Team(models.Model):
      
      
      class SeasonList(models.TextChoices):
          FALL='FALL'
          SPRING ='SPRING'
          SUMMER='SUMMER'
          WINTER='WINTER'    
      TeamID = models.AutoField(primary_key=True)
      TeamName = models.CharField(max_length=100)
      PrimaryEmail = models.EmailField(unique=False)
      SecondaryEmail = models.EmailField(null=True, unique=False)
      PrimaryPhone = models.CharField(max_length=12, null=True)
      SecondaryPhone = models.CharField(max_length=12, null=True)
      City = models.CharField(max_length=2000,null=True)
      State = models.CharField(max_length=2000,null=True)
      Zip = models.CharField(max_length=2000,null=True)
      SportType = models.ForeignKey(TeamType, on_delete=models.CASCADE)
      TeamLogo = models.ImageField(default='default.jpg', upload_to='team_logos')
      CurrentSeason = models.CharField(max_length=2000, choices=SeasonList.choices, default=SeasonList.FALL,)
      DateCreated = models.DateTimeField(auto_now=True)
      CurrentYear = models.CharField(max_length=4, default=datetime.date.today().year)
      
      def __str__(self):
          return "{}".format(self.TeamName)
      
      # resizing images
      def save(self, *args, **kwargs):
          self.CurrentYear = datetime.date.today().year
          self.DateCreated = datetime.datetime.now()
          super().save()

          img = Image.open(self.TeamLogo.path)

          if img.height > 100 or img.width > 100:
             new_img = (100, 100)
             img.thumbnail(new_img)
             img.save(self.TeamLogo.path)

class TeamStyle(models.Model):
      TeamStyleID = models.AutoField(primary_key=True)
      SiteTheme = models.ForeignKey(SiteStyle, on_delete=models.CASCADE, default='', related_name="SiteTheme")
      
      def __str__(self):
        return self.SiteTheme.Style
      
class TeamWebsite(models.Model):
      
      class SiteStyleOptionList(models.TextChoices): 
          Default='default'
          Cerulean='cerulean'
          Cosmo='cosmo'
          Cyborg='cyborg'
          Darkly='darkly'
          Flatly='flatly'
          Journal='journal'
          Litera='litera'
          Lumen='lumen'
          Lux='lux'
          Materia='materia'
          Minty='minty'
          Morph='morph'
          Pulse='pulse'
          Quartz='quartz'
          Sandstone='sandstone'
          Simplex='simplex'
          Sketchy='sketchy'
          Slate='slate'
          Solar='solar'
          Spacelab='spacelab'
          Superhero='superhero'
          United='united'
          Vapor='vapor'
          Yeti='yeti'
          Zephyr='zephyr'
          
      TeamWebsiteID = models.AutoField(primary_key=True)
      TeamName = models.ForeignKey(Team, on_delete=models.CASCADE)
      HeaderImage = models.ImageField(default='default.jpg', upload_to='teamsite_images')
      SiteTitle = models.CharField(max_length=100)
      MissionStatement = models.TextField()
      ShowRoster = models.BooleanField(default=False)
      ShowCoaches = models.BooleanField(default=False)
      ShowPlayerMedia = models.BooleanField(default=False)
      ShowGamesAndStats = models.BooleanField(default=False)
      IsPublicSite = models.BooleanField(default=False)
      SiteStyleOption = models.CharField(max_length=200, choices=SiteStyleOptionList.choices, default=SiteStyleOptionList.Default, null=True,)
      
      def __str__(self):
        return self.TeamName.TeamName

      # resizing images
      def save(self, *args, **kwargs):
          super().save()

          img = Image.open(self.HeaderImage.path)

          if img.height > 100 or img.width > 100:
             new_img = (100, 100)
             img.thumbnail(new_img)
             img.save(self.HeaderImage.path)
             
class TeamDocument(models.Model):
      TeamDocumentID = models.AutoField(primary_key=True)
      Document = models.FileField(default='default.jpg', upload_to='team_files')
      FileName = models.CharField(max_length=100, default="")
      ShowOnPublicWebsite = models.BooleanField(default=False)
      ShowOnInternalWebsite = models.BooleanField(default=False)
      SiteID = models.ForeignKey(TeamWebsite, on_delete=models.CASCADE)
      
      
      def get_docfile_name(self):
          if not self.Document:
            return "test"
          file_path = self.Document.name
          return "test"#os.path.basename(file_path)

class TeamWebsiteExternalLink(models.Model):
      LinkID = models.AutoField(primary_key=True)
      LinkName = models.CharField(null=True, max_length=1000)
      Url = models.CharField(null=True, max_length=1000)
      ShowOnPublicWebsite = models.BooleanField(default=False)
      ShowOnInternalWebsite = models.BooleanField(default=False)
      SiteID = models.ForeignKey(TeamWebsite, on_delete=models.CASCADE)

class TeamMedia(models.Model):
     
      class MediaTypeList(models.TextChoices): 
          Image='Image'
          Video='Video'
  
      TeamMediaID = models.AutoField(primary_key=True)
      MediaTitle = models.CharField(max_length=1000)
      MediaDescription = models.TextField(max_length=5000)
      MediaFile = models.FileField(upload_to="team_media")
      MediaType = models.CharField(max_length=200, choices=MediaTypeList.choices, default=MediaTypeList.Image, null=True,)
      SiteID = models.ForeignKey(TeamWebsite, on_delete=models.CASCADE)
      
      def __str__(self):
        return self.MediaTitle
      
      def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.MediaFile.path)
      
class TeamRoster(models.Model):
      class ThrowingBattingHand(models.TextChoices):
            RIGHT = 'R'
            LEFT = 'L'
            BOTH='B'
        
      TeamPlayerID = models.AutoField(primary_key=True)
      FirstName = models.CharField(default="", max_length=1000)
      MiddleName = models.CharField(default="", max_length=1000)
      LastName = models.CharField(default="", max_length=1000)
      FullName = models.CharField(max_length=1000, default="")
      Team=models.ForeignKey(Team, on_delete=models.CASCADE)
      JerseyNumber = models.CharField(max_length=10, default="")
      ThrowingHand = models.CharField(max_length=2000, choices=ThrowingBattingHand.choices, default=ThrowingBattingHand.RIGHT,)
      BattingHand = models.CharField(max_length=2000, choices=ThrowingBattingHand.choices, default=ThrowingBattingHand.RIGHT,)
      ProfileImage = models.ImageField(default='default.jpg', upload_to='player_profile_images')
      def __str__(self):
          return "{} {} {} - {}".format(self.FirstName, self.MiddleName, self.LastName, self.Team.TeamName)
      
      def save(self, *args, **kwargs):
          if(self.MiddleName == ""):
             self.Fullname = "{} {}".format(self.FirstName, self.LastName)
          else:
             self.FullName = "{} {} {}".format(self.FirstName, self.MiddleName, self.LastName)
             
          super().save()

          img = Image.open(self.ProfileImage.path)

          if img.height > 100 or img.width > 100:
             new_img = (100, 100)
             img.thumbnail(new_img)
             img.save(self.ProfileImage.path)

class TeamMember(models.Model):
      class MemberTypeList(models.TextChoices):
            PARENT='PARENT'
            COACH='COACH'
      
      TeamMemberID = models.AutoField(primary_key=True)
      MemberType = models.CharField(max_length=2000, choices=MemberTypeList.choices, default=MemberTypeList.PARENT,)
      MemberUser = models.ForeignKey(User, on_delete=models.CASCADE)
      AssignedTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
      TeamOwner = models.BooleanField(default=False)
      def __str__(self):
          return "{} {} {}".format(self.MemberUser.first_name, self.MemberUser.last_name, self.AssignedTeam.TeamName) 
class TeamFan(models.Model):
      class FanType(models.TextChoices):
            PARENT = 'PARENT'
            FAN = 'FAN'
      TeamFanID = models.AutoField(primary_key=True)
      FanUser = models.ForeignKey(User, on_delete=models.CASCADE)
      AssignedTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
      
      def __str__(self):
          return "{} {}".format(self.FanUser.first_name, self.FanUser.last_name)
class TeamFanInviteRequest(models.Model):
      class RequestStatusList(models.TextChoices):
            OPEN = 'OPEN'
            PENDING = 'PENDING'
            APPROVED = 'APPROVED'
            REJECTED='REJECTED'
      class MemberTypeList(models.TextChoices):
            PARENT='PARENT'
            COACH='COACH'
                  
      TeamFanInviteRequest = models.AutoField(primary_key=True)
      EmailContact = models.CharField(max_length=1000)
      RequestStatus = models.CharField(max_length=2000, choices=RequestStatusList.choices, default=RequestStatusList.OPEN,) 
      DateCreated = models.DateField(auto_created=True)
      DateApprovedRejected = models.DateField(auto_now=True)
      InviteCode = models.CharField(default = "", max_length=2000)
      AssignedTeam = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
      MemberType = models.CharField(max_length=2000, choices=MemberTypeList.choices, default=MemberTypeList.PARENT,)

      def __str__(self):
          return self.EmailContact     
class PlayerMedia(models.Model):
      PlayerMediaID = models.AutoField(primary_key=True)
      SelectedTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
      SelectedPlayer = models.ForeignKey(TeamRoster, on_delete=models.CASCADE)     
      TeamMediaItem = models.ForeignKey(TeamMedia, on_delete=models.CASCADE) 
       
      def __str__(self):
          return self.SelectedPlayer.FullName

class PlayerContact(models.Model):
    
      class ContactTypeList(models.TextChoices):
            Family = 'Family'
            Emergency = 'Emergency'
            BOTH='Both'
            
      PlayerFamilyContactID = models.AutoField(primary_key=True)
      FamilyMember = models.ForeignKey(TeamFan, on_delete=models.CASCADE)
      Player = models.ForeignKey(TeamRoster, on_delete=models.CASCADE)
      ContactType = models.CharField(max_length=2000, choices=ContactTypeList.choices, default=ContactTypeList.Family,)
      
      def __str__(self):
          return "{} {} {} - {}".format(self.Player.FirstName, self.Player.MiddleName, self.Player.LastName)
      
      
class TeamCoach(models.Model):
      TeamCoachID = models.AutoField(primary_key=True)
      Coach = models.ForeignKey(User, on_delete=models.CASCADE)
      Team=models.ForeignKey(Team, on_delete=models.CASCADE)
      IsHeadCoach=models.BooleanField(default=False)
      CoachTitle = models.CharField(max_length=1000, default="")
      #Role=models.ForeignKey(Group, on_delete=models.CASCADE)
      
      def __str__(self):
          return "{} {} - {}".format(self.Coach.first_name, self.Coach.last_name, self.Team.TeamName)
      
class UserRelationship(models.Model):
      UserRelationshipID = models.AutoField(primary_key=True)
      User1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="Parent")
      User2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="Child")
      
      def __str__(self):
          return "{} {} Connected To {} {}".format(self.User1.user.first_name, self.User1.user.last_name, self.User2.user.first_name, self.User2.user.last_name)
    

class AccessRequestQueue(models.Model):
      
      class MemberTypeList(models.TextChoices):
            PARENT='PARENT'
            COACH='COACH'
      
      class RequestStatusList(models.TextChoices):
            OPEN = 'OPEN'
            PENDING = 'PENDING'
            APPROVED = 'APPROVED'
            REJECTED='REJECTED'
                  
      AccessRequestQueueID = models.AutoField(primary_key=True)
      Requestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Requestor_User")
      Approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Approve_User")
      TeamRequested = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team_Requested")
      MemberType  = models.CharField(max_length=2000, choices=MemberTypeList.choices, default=MemberTypeList.PARENT,)
      DateTimeCreated = models.DateField(auto_created=True, default=datetime.datetime.now)
      DateTimeModified = models.DateField( default=datetime.datetime.now)
      RequestStatus = models.CharField(max_length=2000, choices=RequestStatusList.choices, default=RequestStatusList.OPEN,) 
      
      # def __str__(self):
      #     return "{} {} Connected To {} {}".format(self.RequestorUser.user.first_name, self.RequestorUser.user.last_name, self.RequestorUser.user.first_name, self.RequestorUser.user.last_name)
    
      # def save(self, *args, **kwargs):
      #     self.RequestCreated = datetime.datetime.now()
      #     self.RequestModified = datetime.datetime.now()
      #     super().save()

class TeamPractice(models.Model):
      TeamPracticeID = models.AutoField(primary_key=True)
      FieldLocation = models.CharField(max_length=5000)
      AssignedTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
      StartGameDateTime = models.DateTimeField(default=datetime.datetime.today)
      EndGameDateTime = models.DateTimeField(default=datetime.datetime.today)
      AdditionalInfo = models.TextField(max_length=8000)  
      
class TeamGame(models.Model):
      TeamGameID = models.AutoField(primary_key=True)
      Start_Game_DateTime = models.DateTimeField(default=datetime.datetime.today)
      End_Game_DateTime = models.DateTimeField(default=datetime.datetime.today)
      HomeTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Home_Team")
      AwayTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Away_Team")
      Location = models.CharField(max_length=5000, default="")
      
   
class GamePlayer(models.Model):
      class ThrowingBattingHand(models.TextChoices):
            RIGHT = 'R'
            LEFT = 'L'
            BOTH='B'
      
      class FieldPositionList(models.TextChoices):
            FIRSTBASE = '1B'
            SECONDBASE = '2B'
            SHORTSTOP='SS'
            THIRDBASE = '3B'
            LEFTFIELD= 'LF'
            CENTERFIELD='CF'
            RIGHTFIELD='RG'
            DESIGNATEDHITTER='DH'
            PITCHER='P'
            CATCHER='C'
      GameTeamPlayerID = models.AutoField(primary_key=True)
      AssignedGame = models.ForeignKey(TeamGame, on_delete=models.CASCADE)
      AssignedTeam=models.ForeignKey(Team, on_delete=models.CASCADE)
      FirstName = models.CharField(default="", max_length=1000)
      MiddleName = models.CharField(default="", max_length=1000)
      LastName = models.CharField(default="", max_length=1000)
      FullName = models.CharField(max_length=1000, default="")
      
      JerseyNumber = models.CharField(max_length=10, default="")
      ThrowingHand = models.CharField(max_length=2000, choices=ThrowingBattingHand.choices, default=ThrowingBattingHand.RIGHT,)
      BattingHand = models.CharField(max_length=2000, choices=ThrowingBattingHand.choices, default=ThrowingBattingHand.RIGHT,)
      BattingOrder = models.IntegerField(default=0)
      FieldPosition = models.CharField(max_length=2000, choices=FieldPositionList.choices, default=FieldPositionList.DESIGNATEDHITTER,)
      PlayerID = models.IntegerField(default=0)
      
class BatterGameStat(models.Model):
      BatterGameStatID = models.AutoField(primary_key=True)
      Position = models.CharField(max_length=40)
      AssignedPlayer = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
      AtBats = models.IntegerField(default=0)
      Runs = models.IntegerField(default=0)
      Hits = models.IntegerField(default=0)
      RBI = models.IntegerField(default=0)
      BaseOnBalls = models.IntegerField(default=0)
      StrikeOuts=models.IntegerField(default=0)
      BattingAverage = models.IntegerField(default=0)
      OBP= models.IntegerField(default=0)
     
class PitcherGameStat(models.Model):
      PitcherGameStatID = models.AutoField(primary_key=True)
      AssignedPlayer = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
      InningsPitch = models.IntegerField(default=0)
      Hits = models.IntegerField(default=0)
      Runs = models.IntegerField(default=0)
      EarnRuns = models.IntegerField(default=0)
      BaseOnBalls = models.IntegerField(default=0)
      StrikeOuts = models.IntegerField(default=0)
      BattersFaced = models.IntegerField(default=0)
      EarnRunAverage = models.IntegerField(default=0)
      Loss = models.BooleanField(default=False)
      Won = models.BooleanField(default=False)
      
class TeamBatterStatTotal(models.Model): 
      TeamBatterStatTotalID = models.AutoField(primary_key=True)
      AssignedGame = models.ForeignKey(TeamGame, on_delete=models.CASCADE)
      AssignedTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
      AtBats = models.IntegerField(default=0)
      Runs = models.IntegerField(default=0)
      Hits = models.IntegerField(default=0)
      RBI = models.IntegerField(default=0)
      BaseOnBalls = models.IntegerField(default=0)
      StrikeOuts=models.IntegerField(default=0)
      BattingAverage = models.IntegerField(default=0)
      OBP= models.IntegerField(default=0)     
      
class TeamPitcherStatTotal(models.Model): 
      PitcherGameStatID = models.AutoField(primary_key=True)
      AssignedGame = models.ForeignKey(TeamGame, on_delete=models.CASCADE)
      AssignedTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
      InningsPitch = models.IntegerField(default=0)
      Hits = models.IntegerField(default=0)
      Runs = models.IntegerField(default=0)
      EarnRuns = models.IntegerField(default=0)
      BaseOnBalls = models.IntegerField(default=0)
      StrikeOuts = models.IntegerField(default=0)
      BattersFaced = models.IntegerField(default=0)
      EarnRunAverage = models.IntegerField(default=0)

      

      