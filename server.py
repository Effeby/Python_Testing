import json
from flask import Flask,render_template,request,redirect,flash,url_for
from  datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

today = datetime.now()

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    comp = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    return render_template('index.html', clubs = clubs, competitions = comp)

#Route pour la page acceuil de chaque club
@app.route('/showSummary',methods=['POST'])
def showSummary():
    comp = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    club = next((club for club in clubs if club['email'] == request.form['email']), None)
    if club:
        return render_template('welcome.html',club=club,competitions=comp)
    else:
        flash("Email introuvable, veuillez entrer un mail valide !")
        return redirect(url_for('index'))


#Route pour réserver les tickets
@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

#Rooute pour les calcules sur la reservation des tickets
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    comp = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    #verification du nombre de point si c'est insuffisant alors ça affiche Point insuffisabt!
    if int(club['points']) < int(placesRequired):
        flash('Points insuffisant!')
        return redirect(request.referrer)
    elif int(placesRequired) > int(competition['numberOfPlaces']):
        flash('Probleme de surreservation')
        return redirect(request.referrer)
    else:
        #calcule pour que le nombre de point et les places diminuent en fonction du nombre de place réservé
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points']= int(club['points']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=comp)

#TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))