![](static/images/full_site_logo.png)

<sub>Project background and idea history will be updated soon</sub>

Currently, (August 2022) you can find and use my project on free Heroku server: 

https://fifa-draft.herokuapp.com/


**TLTR:**

The site allows you to create your dream team lineups in FIFA game. The idea is that when you get bored of playing the same rigid line-ups this app gives you the opportunity to change that. Group members choose players to their teams from all players over 79 (it can be changed) overall points available in FIFA 22 in a predetermined order one player at a time until the teams are full. **Line-ups must be set manually in the FIFA game settings.** There is an option for fixed and serpentine drafts.
Quick guide:

1. Create a Group, then a Team, and invite your friends to join your Group,

2. when everyone has a Team in your Group, draw the draft order,

3. the order in which players are selected changes automatically according to the order drawn,

4. players are selected through the "Pick players" button at the top of the page, select the team you want to select a player for, and then click Add player. The player selected by one person in the Group will not appear in the list again,

5. next person need to pick a player, repeat until the lineup is full,

6. if it is not your turn, you can add a player to the pending list who will be automatically selected when it is your turn,

7. complete the Excel file with the match schedule,

8. meet your friends and let the best one win!




# Installation:
1. Clone this repository: <code>git clone git@github.com:Grzegorz-Oledzki/fifa_draft_project.git</code>
2. Install requirements: <code>pip install -r requirements.txt</code>
3. Set up your database. If you want to use local database go to draft_fifa folder > settings.py and comment lines 88 to 97, and uncomment lines 98 to 103.
4. Type:
<code>python manage.py migrate</code>
<code>python manage.py createsuperuser</code>
And finally:
<code>python manage.py runserver</code>
5. Download players list from
<code>https://docs.google.com/spreadsheets/d/1xOSDGC8MhbUNWA6OeNcWmpOjFRkPzLYb/edit?usp=sharing&ouid=107358397983377935642&rtpof=true&sd=true </code>
6. Import players from .xlsx file on <code>http://127.0.0.1:8000/admin/players/player/ </code> 
7. Invite your friends and play! 

Screenshots: 

Home:
![img.png](static/images/img.png)
Players list:
![img_1.png](static/images/img_1.png)

When it was your turn:
![img_2.png](static/images/img_2.png)
Team view:
![img_3.png](static/images/img_3.png)