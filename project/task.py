from workers import celery
from jinja2 import Template
from weasyprint import HTML
from mail import send_email
import csv
from model import db, User as userdata ,Role, Song as songdata, Album as albumdata, Playlist as playlistdata, Rating as ratingdata

def format_report(template1,data,User="User"):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(data=data,User=User)


def pdf_report(data,User):
    msg = format_report("./templates/monthly.html",data=data,User=User)
    # print(msg)
    html = HTML(string=msg)
    # print(html)
    file_name = str(User)+"_IITM_Band"+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)  

@celery.task()
def monthly():
    creators=[]
    users = userdata.query.filter(userdata.roles.any(Role.name == 'creator')).all()
    for creator in users:
        email = creator.email
        username = creator.username
        creator_dict = {'Creator_email' : creator.email, "Creator_Name" : creator.username, "Creator_songs": [], "Creator_albums": []}
        for song in creator.song :
            song_dict = {'Song_Title' : song.title, 'Song_Artist' : song.artist, 'Song_Genere' : song.genre, 'Song_Releasedate' : song.releasedate}
            creator_dict['Creator_songs'].append(song_dict)
            print(song_dict)
        for album in creator.albums:
            album_dict ={'Album_title': album.title, 'Album_description': album.description}
            creator_dict['Creator_albums'].append(album_dict)
            print(album_dict)
        creators.append(creator_dict)
        pdf_report(creator_dict, username)
        with open('./templates/monthly.html','r') as f:
            template = Template(f.read())
        send_email(email,'Monthly Reminder',template.render(user=username, data = creator_dict),content="html", attachment="./"+str(username)+"_IITM_Band"+".pdf")
    return "Monthly reminder sent"


@celery.task()
def daily():
    users = userdata.query.filter(userdata.roles.any(Role.name == 'user')).all()
    for user in users:
        email = user.email
        username = user.username
        with open('./templates/daily.html','r') as f:
            template = Template(f.read())
        send_email(email,'Daily Reminder',template.render(user=username),content="html")
    return "Daily reminder sent"


@celery.task()
def exportjob(data,email,username):
    with open('./static/music.csv', 'w', encoding='utf8', newline='') as f:
        file = csv.DictWriter(f,fieldnames=data[0].keys(),restval='')
        file.writeheader()
        file.writerows(data)
    
    with open('./templates/music_csv.html','r') as f:
        template = Template(f.read())
    send_email(email,'Exported music Details',template.render(user=username,data=data),content="html",attachment="./static/music.csv")    
    return "Csv created for log." 