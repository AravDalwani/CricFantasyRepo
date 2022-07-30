from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Match
from .views import views
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from .form_contact import ContactForm, PredForm
from http.client import responses
import requests
import random
from datetime import datetime
import math

def getList(dict):
    return dict.keys()

def conditional_change(prediction, old_score, new_score, bet):
    if new_score >= old_score:
        if prediction == 'Increase':
            Match.query.filter_by(id=bet.id).update(dict(result=1))
            print(True)
        else:
            print(False)
            Match.query.filter_by(id=bet.id).update(dict(result=0))
    else:
        if prediction == 'Decrease':
            Match.query.filter_by(id=bet.id).update(dict(result=1))
        else:
            Match.query.filter_by(id=bet.id).update(dict(result=0))

def prediction_change(prediction, old_value, new_value, threshold_new, bet):
    if (new_value - old_value) >= threshold_new:
        if prediction == 'Increase':
            Match.query.filter_by(id=bet.id).update(dict(result=1))
            print(True)
        else:
            print(False)
            Match.query.filter_by(id=bet.id).update(dict(result=0))
    else:
        if prediction == 'Decrease':
            Match.query.filter_by(id=bet.id).update(dict(result=1))
        else:
            Match.query.filter_by(id=bet.id).update(dict(result=0))


auth = Blueprint("auth", __name__)
mail = Mail()

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")


        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                print("Logged in!")
                return redirect(url_for('auth.success'))
            else:
                flash('Password is incorrect.', category='error')
                print('Password is incorrect.')
        else:
            flash('Email does not exist.', category='error')
            print('Email does not exist.')

    return render_template("login.html", user=current_user)

def send_message(message):
    print(message.get('name'))

    msg = Message(message.get('subject'), sender = message.get('email'),
            recipients = ['newpythontestapp@gmail.com'],
            body= message.get('message')
    )
    mail.send(msg)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
            print('Email is already in use.')
        elif username_exists:
            flash('Username is already in use.', category='error')
            print('Username is already in use.')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
            print('Password don\'t match!')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
            print('Username is too short.')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
            print('Password is too short.')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
            print("Email is invalid.")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            print('User created!')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/")
def index():
    return render_template("index.html")

@auth.route('/success', methods=['GET', 'POST'])
def success():

    headers = {
        'X-RapidAPI-Key': "6dc8a9fa2dmshd76336d1779068ap174c41jsn3a631cdb3743",
        'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
        }
    
    seriesName_upcoming_new = []
    start_times_new = []
    match_status_new = []
    match_details_arr_new = []
    match_ID_new = []

    team_1_data = []
    team_2_data = []

    #Link to scrape data about ongoing matches

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    response = requests.request("GET", url, headers=headers)
    information = response.json()

    game_types = [0, 1, 2]
    try:
        for game_type in game_types:

            data = information['typeMatches'][game_type]['seriesMatches'] 

            series_list = [] #Different ongoing Series
            match_details = [] #Different ongoing Matches

            for series_current in data:

                #Some Necessary Data Formatting and Series Finding
                try:
                    curr_series_data = series_current['seriesAdWrapper']
                except:
                    pass

                try:
                    series_list.append([curr_series_data['seriesName'], curr_series_data['seriesId']])
                    storage = curr_series_data['seriesName']
                    curr_series_data = curr_series_data['matches']
                except:
                    pass
                
                for matchSet in curr_series_data:
                    if (matchSet['matchInfo']['matchFormat'] == 'T20') and (matchSet['matchInfo']['state'] != 'Complete'):
                        seriesName_upcoming_new.append(storage)
                        match_status_new.append('Live')
                        match_details_fire = matchSet['matchInfo']['team1']['teamName'] + str(" ") + str("vs") + str(" ") + matchSet['matchInfo']['team2']['teamName']
                        match_details_arr_new.append(match_details_fire)
                        #Getting current Match ID

                        dt_object = datetime.fromtimestamp(int(matchSet['matchInfo']['startDate'])/1000)
                        start_times_new.append(str(dt_object))
                        match_ID_new.append(int(matchSet['matchInfo']['matchId']))

                        a = matchSet['matchScore']['team1Score']

                        try:
                            b = matchSet['matchScore']['team2Score']
                        except:
                            b = {}


                        team_1_data.append([matchSet['matchInfo']['team1']['teamName'], a])
                        team_2_data.append([matchSet['matchInfo']['team2']['teamName'], b])

    except:
        pass

    list_types = ['international', 'league']

    for match_type in list_types:
        url_curr = "https://cricbuzz-cricket.p.rapidapi.com/schedule/v1/" + str(match_type) 
        response = requests.request("GET", url_curr, headers=headers)
        information = response.json()
        series_types_new = information['matchScheduleMap'][0]['scheduleAdWrapper']['matchScheduleList']

        for series in series_types_new:
            matches_in_series = series['matchInfo']

            for curr_match_name in matches_in_series:
                if curr_match_name['matchFormat'] == 'T20':
                    seriesName_upcoming_new.append(series['seriesName'])
                    dt_object = datetime.fromtimestamp(int(curr_match_name['startDate'])/1000)
                    start_times_new.append(str(dt_object))
                    match_status_new.append('Upcoming')
                    match_details_fire = curr_match_name['team1']['teamName'] + str(" ") + str("vs") + str(" ") + curr_match_name['team2']['teamName']
                    match_details_arr_new.append(match_details_fire)
                    match_ID_new.append(str(""))

    global Details
    global required_1
    global required_2

    if request.method == 'POST':
        Details = int(request.form.get("Details"))
        index_pos = match_ID_new.index(Details)
        required_1 = team_1_data[index_pos]
        required_2 = team_2_data[index_pos]
        return redirect(url_for('auth.scorecard'))


    return render_template('success.html', seriesName_upcoming_new=seriesName_upcoming_new, 
    start_times_new = start_times_new,
    match_status_new = match_status_new,
    match_details_arr_new = match_details_arr_new,
    len = len(match_details_arr_new),
    match_ID_new = match_ID_new
    )

@login_required
@auth.route('/scorecard', methods=['GET', 'POST'])
def scorecard():

    headers = {
        'X-RapidAPI-Key': "6dc8a9fa2dmshd76336d1779068ap174c41jsn3a631cdb3743",
        'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
        }

    #Link to scrape data about ongoing matches

    #Batsmen Bowler Data for a Single Game

    batsmen_team_one = []
    batsmen_team_two = []
    bowlers_team_one = []
    bowlers_team_two = []

    #Meta Data for Each Team - Total Runs, Name, etc
    url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/" + str(Details) + "/scard"

    responsetest_ = requests.request("GET", url, headers=headers)

    information_match = responsetest_.json()

    cycle_number  = 0

    team_currently_batting = []
    team_currently_bowling = []
    team_1_full = [] 
    team_2_full = [] 

    #Batsmen Bowler Data for a Game
    team_1_full.append(required_1)
    team_2_full.append(required_2)

    for team_number_ID in information_match['scoreCard']:  
        for data_point in team_number_ID['batTeamDetails']['batsmenData']:
            curr_batsmen = team_number_ID['batTeamDetails']['batsmenData'][data_point]
            if cycle_number == 0:
                batsmen_team_one.append([curr_batsmen['batName'], curr_batsmen['isCaptain'], curr_batsmen['isKeeper'], curr_batsmen['runs'],curr_batsmen['balls'], curr_batsmen['strikeRate'], curr_batsmen['boundaries'],curr_batsmen['sixers'], curr_batsmen['wicketCode'], curr_batsmen['bowlerId'], curr_batsmen['fielderId1'], curr_batsmen['outDesc']])
            else:
                batsmen_team_two.append([curr_batsmen['batName'], curr_batsmen['isCaptain'], curr_batsmen['isKeeper'], curr_batsmen['runs'],curr_batsmen['balls'], curr_batsmen['strikeRate'], curr_batsmen['boundaries'],curr_batsmen['sixers'], curr_batsmen['wicketCode'], curr_batsmen['bowlerId'], curr_batsmen['fielderId1'], curr_batsmen['outDesc']])

        for data_point in team_number_ID['bowlTeamDetails']['bowlersData']:
            curr_bowler = team_number_ID['bowlTeamDetails']['bowlersData'][data_point]

            if cycle_number == 0:
                bowlers_team_two.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])
            else:
                bowlers_team_one.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])

        cycle_number += 1

    team_1_full.append(batsmen_team_one)
    team_2_full.append(batsmen_team_two)
    team_1_full.append(bowlers_team_one)
    team_2_full.append(bowlers_team_two)

    team_currently_batting = team_1_full
    team_currently_bowling = team_2_full

    if (len(team_2_full[1]) != 0):
        team_currently_batting = team_2_full
        team_currently_bowling = team_1_full

    team_batting = team_currently_batting[0][0]
    batsmen_1 = 'None'
    batsmen_2 = 'None'
    batsmen_1_runs= 0
    batsmen_2_runs= 0
    batsmen_1_balls= 0
    batsmen_1_sr= 0
    batsmen_2_sr= 0
    batsmen_2_balls= 0
    batsmen_1_sixes= 0
    batsmen_2_sixes= 0
    batsmen_1_fours= 0
    batsmen_2_fours= 0

    team_bowling = team_currently_bowling[0][0]
    bowler_name= 'None'
    bowler_overs= 0
    bowler_runs= 0
    bowler_wickets= 0
    bowler_maidens= 0
    bowler_econ= 0
    bowler_no_ball= 0
    bowler_wides= 0

    global questions_general
    global questions_general_overs
    global special_questions
    global question_number
    global question

    count_batter = 0 

    team_batting_stats = team_currently_batting[0][1]['inngs1']

    team_batting_runs = team_batting_stats['runs']
    team_batting_overs = team_batting_stats['overs']

    global over_number

    over_number = math.floor(team_batting_overs)

    try:
        team_batting_wickets = team_batting_stats['wickets']
    except:
        team_batting_wickets = 0 

    for batter in team_currently_batting[1]:

        if count_batter == 2:
            break

        if (batter[-1] == 'batting') and (batsmen_1 == 'None') and (count_batter == 0):
            batsmen_1 = str(batter[0])
            batsmen_1_runs = int(batter[3])
            batsmen_1_balls = int(batter[4])
            batsmen_1_sr = float(batter[5])
            batsmen_1_fours = int(batter[6])
            batsmen_1_sixes = int(batter[7])
            count_batter += 1
            batsmen_1_ = True

        elif (batter[-1] == 'batting') and (batsmen_2 == 'None') and (count_batter == 1):
            batsmen_2 = str(batter[0])
            batsmen_2_runs = int(batter[3])
            batsmen_2_balls = int(batter[4])
            batsmen_2_sr = float(batter[5])
            batsmen_2_fours = int(batter[6])
            batsmen_2_sixes = int(batter[7])
            count_batter += 1
            batsmen_1_ = True

    for bowler in team_currently_bowling[2]:

        if (float(bowler[3]) % 1) != 0:
            bowler_name = str(bowler[0])
            bowler_overs = float(bowler[3])
            bowler_runs = int(bowler[5])
            bowler_wickets = int(bowler[6])
            bowler_maidens = int(bowler[4])
            bowler_econ = float(bowler[7])
            bowler_no_ball = int(bowler[8])
            bowler_wides = int(bowler[9])
            break
            
    try:
        if (43 < batsmen_1_runs < 47):
            batsmen = batsmen_1
        elif (43 < batsmen_2_runs < 47):
            batsmen = batsmen_2
        else:
            batsmen = 'None'
    except:
        pass

    wicket_number = team_batting_wickets + 1
    target_runs = int(team_batting_runs) + 60
    off_balls = bowler_no_ball + bowler_wides

    global option1
    global option2
    global threshold

    thresholds_general  = [-1, 2, 1, 2, 1, 1, 1, -1]
    thresholds_general_overs = [40, 7, 2, 1, -1] 
    thresholds_special = [50, 100, 50, 100]

    options_questions_general = [['Increase', 'Decrease'], ['2 or Above', 'Under 2'], ['1 or Above', 'Under 1'], ['2 or Above', 'Under 2'], ['Yes', 'No'], ['Yes', 'No'], ['Yes', 'No'], ['Increase', 'Decrease']]
    options_questions_general_overs = [['Over 40', 'Under 40'], ['7 or Above', 'Under 7'], ['2 or Above', 'Under 2'], ['Yes', 'No'], ['Yes', 'No']]
    options_special_questions = [
        ['Yes', 'Yes', 'Yes', 'Yes', 'Over 50'],
        ['No', 'No', 'No', 'No', 'Under 50']]

    questions_general = ['How will the strike rate of {} of {} change in the next over'.format(batsmen_1, batsmen_1_sr),'How many fours will batsman {} hit in the next over?'.format(batsmen_2), 'How many sixes will batsman {} hit in the next over?'.format(batsmen_1), 'How many wides will bowler {} bowl in his next over?'.format(bowler_name), 'Will {} take a wicket in the over'.format(bowler_name), 'Currently bowled {} wides, will {} bowl another one this over?'.format(off_balls, bowler_name), 'Currently bowled {} maidens, will {} bowl another one this over?'.format(bowler_maidens, bowler_name), 'How will the economy of {} of {} change in the next over'.format(bowler_name, bowler_econ)]

    questions_general_overs = ['How many runs will team {} make in the next 5 overs?'.format(team_batting), 'How many fours will batsman {} hit in the next 5 overs'.format(batsmen_2), 'How many wickets will {} take in the next five overs'.format(bowler_name), 'Will team {} lose its {} wicket in the next five overs'.format(team_batting, wicket_number), 'Will team {} cross {} in the next 5 overs'.format(team_batting, target_runs)]

    special_questions = ['Will team {} cross 50 runs in the next over?'.format(team_batting), 'Will team {} cross 100 runs in the next over?'.format(team_batting), 'Will {} score a half century in the next over?'.format(batsmen), 'Will {} score a century in the next over?'.format(batsmen), 'How many runs will the next partnership between batsman {} and {} be?'.format(batsmen_1, batsmen_2)]

    global question

    if team_batting_overs < 15:
        question = [*questions_general, *questions_general_overs]
        options = [*options_questions_general, *options_questions_general_overs]
        thresholds = [*thresholds_general, *thresholds_general_overs]
    else:
        question = questions_general
        options = options_questions_general
        thresholds = thresholds_general

    question_number = random.randint(0, len(question) - 1)
    
    question = question[question_number]
    option1 = options[question_number][0]
    option2 = options[question_number][1]
    threshold = thresholds[question_number]

    special_question = 0

    match_curr_id = int(Details)

    if 40 < team_batting_runs < 45:
        question = special_questions[0]
        threshold = thresholds_special[0]
        special_question = 1
        option1 = options_special_questions[0][0]
        option2 = options_special_questions[1][0]
    elif 90 < team_batting_runs < 95:
        question = special_questions[1]
        threshold = thresholds_special[1]
        special_question = 2
        option1 = options_special_questions[0][1]
        option2 = options_special_questions[1][1]
    elif (43 < batsmen_1_runs < 47) or (43 < batsmen_2_runs < 47):
        question = special_questions[2]
        threshold = thresholds_special[2]
        special_question = 3
        option1 = options_special_questions[0][2]
        option2 = options_special_questions[1][2]
    elif (93 < batsmen_1_runs < 96) or (93 < batsmen_2_runs < 96):
        question = special_questions[3]
        threshold = thresholds_special[3]
        special_question = 4
        option1 = options_special_questions[0][3]
        option2 = options_special_questions[1][3]

    link_current_match = "https://www.cricbuzz.com/live-cricket-scores/" + str(match_curr_id)

    global values_stored
    global type

    if (special_question == 1):
        values_stored = team_batting_runs
        type = 'Threshold'
    elif (special_question == 2):
        values_stored = team_batting_runs
        type = 'Threshold'
    elif (special_question == 3):
        if batsmen == 'batsmen_1':
            values_stored = batsmen_1_runs
        else:
            values_stored = batsmen_2_runs
        type = '1'
    elif (special_question == 4):
        if batsmen == 'batsmen_1':
            values_stored = batsmen_1_runs
        else:
            values_stored = batsmen_2_runs
        type = '1'
    elif (question_number == 0):
        values_stored = batsmen_1_sr
        type = '1'  
    elif (question_number == 1):
        values_stored = batsmen_2_fours
        type = '1'
    elif (question_number == 2):
        values_stored = batsmen_1_sixes
        type = '1'
    elif (question_number == 3):
        values_stored = bowler_wides
        type = '1'
    elif (question_number == 4):
        values_stored = bowler_wickets
        type = '1'
    elif (question_number == 5):
        values_stored = off_balls
        type = '1'
    elif (question_number == 6):
        values_stored = bowler_maidens
        type = '1'
    elif (question_number == 7):
        values_stored = bowler_econ
        type = '5'
    elif (question_number == 8):
        values_stored = team_batting_runs
        type = '5'
    elif (question_number == 9):
        values_stored = batsmen_2_runs
        type = '5'
    elif (question_number == 10):
        values_stored = bowler_wickets
        type = '5'
    elif (question_number == 11):
        values_stored = team_batting_wickets
        type = '5'
    elif (question_number == 12):
        values_stored = target_runs
        type = '5'

    return render_template('scorecard.html', batsmen_1 = batsmen_1,
    batsmen_2 = batsmen_2,
    batsmen_1_runs = batsmen_1_runs,
    batsmen_2_runs = batsmen_2_runs,
    batsmen_1_balls = batsmen_1_balls,
    batsmen_1_sr = batsmen_1_sr,
    batsmen_2_sr = batsmen_2_sr,
    batsmen_2_balls = batsmen_2_balls,
    batsmen_1_sixes = batsmen_1_sixes,
    batsmen_2_sixes = batsmen_2_sixes,
    batsmen_1_fours = batsmen_1_fours,
    batsmen_2_fours = batsmen_2_fours,
    link = link_current_match,
    user=current_user)
    
@auth.route("/contact", methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_message(request.form)
        return redirect('/')

    return render_template("contact.html", form=form)

@login_required
@auth.route('/propbetting', methods=['POST', 'GET'])
def propbetting():
    if request.method == 'POST':
        input_user = request.form.get("Option")
        print(input_user)
        new_match = Match(matchid=Details, prop=question, input = input_user, resolved = False, player_id = current_user.id, curr_data = values_stored, type = type, threshold = threshold, over_number = over_number)
        db.session.add(new_match)
        db.session.commit()

        return redirect(url_for('auth.success'))        

    return render_template('betting.html', question = question, option1 = option1, option2 = option2, user=current_user)


@login_required
@auth.route('/checkbet', methods=['POST', 'GET'])
def checkbet():
    bet_total = Match.query.filter_by(player_id = current_user.id).all()
    for bet in bet_total:
        if bet.resolved == False:

            headers = {
                'X-RapidAPI-Key': "6dc8a9fa2dmshd76336d1779068ap174c41jsn3a631cdb3743",
                'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
                }

            #Link to scrape data about ongoing matches

            #Batsmen Bowler Data for a Single Game

            batsmen_team_one = []
            batsmen_team_two = []
            bowlers_team_one = []
            bowlers_team_two = []

            #Meta Data for Each Team - Total Runs, Name, etc
            url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/" + str(Details) + "/scard"

            responsetest_ = requests.request("GET", url, headers=headers)

            information_match = responsetest_.json()

            cycle_number  = 0

            team_currently_batting = []
            team_currently_bowling = []
            team_1_full = [] 
            team_2_full = [] 

            #Batsmen Bowler Data for a Game
            team_1_full.append(required_1)
            team_2_full.append(required_2)

            for team_number_ID in information_match['scoreCard']:  
                for data_point in team_number_ID['batTeamDetails']['batsmenData']:
                    curr_batsmen = team_number_ID['batTeamDetails']['batsmenData'][data_point]
                    if cycle_number == 0:
                        batsmen_team_one.append([curr_batsmen['batName'], curr_batsmen['isCaptain'], curr_batsmen['isKeeper'], curr_batsmen['runs'],curr_batsmen['balls'], curr_batsmen['strikeRate'], curr_batsmen['boundaries'],curr_batsmen['sixers'], curr_batsmen['wicketCode'], curr_batsmen['bowlerId'], curr_batsmen['fielderId1'], curr_batsmen['outDesc']])
                    else:
                        batsmen_team_two.append([curr_batsmen['batName'], curr_batsmen['isCaptain'], curr_batsmen['isKeeper'], curr_batsmen['runs'],curr_batsmen['balls'], curr_batsmen['strikeRate'], curr_batsmen['boundaries'],curr_batsmen['sixers'], curr_batsmen['wicketCode'], curr_batsmen['bowlerId'], curr_batsmen['fielderId1'], curr_batsmen['outDesc']])

                for data_point in team_number_ID['bowlTeamDetails']['bowlersData']:
                    curr_bowler = team_number_ID['bowlTeamDetails']['bowlersData'][data_point]

                    if cycle_number == 0:
                        bowlers_team_two.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])
                    else:
                        bowlers_team_one.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])

                cycle_number += 1

            team_1_full.append(batsmen_team_one)
            team_2_full.append(batsmen_team_two)
            team_1_full.append(bowlers_team_one)
            team_2_full.append(bowlers_team_two)

            team_currently_batting = team_1_full
            team_currently_bowling = team_2_full

            if (len(team_2_full[1]) != 0):
                team_currently_batting = team_2_full
                team_currently_bowling = team_1_full
            
            url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/44156/overs"

            response_test = requests.request("GET", url, headers=headers)

            information_match_new = response_test.json()

            team_currently_batting[0][1]['inngs1']['runs'] = information_match_new['batTeam']['teamScore']
            team_currently_batting[0][1]['inngs1']['overs'] = information_match_new['overs']
            team_currently_batting[0][1]['inngs1']['wickets'] = information_match_new['batTeam']['teamWkts']

            team_batting = team_currently_batting[0][0]
            batsmen_1 = 'None'
            batsmen_2 = 'None'
            batsmen_1_runs= 0
            batsmen_2_runs= 0
            batsmen_1_balls= 0
            batsmen_1_sr= 0
            batsmen_2_sr= 0
            batsmen_2_balls= 0
            batsmen_1_sixes= 0
            batsmen_2_sixes= 0
            batsmen_1_fours= 0
            batsmen_2_fours= 0

            team_bowling = team_currently_bowling[0][0]
            bowler_name= 'None'
            bowler_overs= 0
            bowler_runs= 0
            bowler_wickets= 0
            bowler_maidens= 0
            bowler_econ= 0
            bowler_no_ball= 0
            bowler_wides= 0

            count_batter = 0 

            team_batting_stats = team_currently_batting[0][1]['inngs1']

            team_batting_runs = team_batting_stats['runs']
            team_batting_overs = team_batting_stats['overs']


            try:
                team_batting_wickets = team_batting_stats['wickets']
            except:
                team_batting_wickets = 0 

            for batter in team_currently_batting[1]:

                if count_batter == 2:
                    break

                if (batter[-1] == 'batting') and (batsmen_1 == 'None') and (count_batter == 0):
                    batsmen_1 = str(batter[0])
                    batsmen_1_runs = int(batter[3])
                    batsmen_1_balls = int(batter[4])
                    batsmen_1_sr = float(batter[5])
                    batsmen_1_fours = int(batter[6])
                    batsmen_1_sixes = int(batter[7])
                    count_batter += 1

                elif (batter[-1] == 'batting') and (batsmen_2 == 'None') and (count_batter == 1):
                    batsmen_2 = str(batter[0])
                    batsmen_2_runs = int(batter[3])
                    batsmen_2_balls = int(batter[4])
                    batsmen_2_sr = float(batter[5])
                    batsmen_2_fours = int(batter[6])
                    batsmen_2_sixes = int(batter[7])
                    count_batter += 1

            for bowler in team_currently_bowling[2]:

                if (float(bowler[3]) % 1) != 0:
                    bowler_name = str(bowler[0])
                    bowler_overs = float(bowler[3])
                    bowler_runs = int(bowler[5])
                    bowler_wickets = int(bowler[6])
                    bowler_maidens = int(bowler[4])
                    bowler_econ = float(bowler[7])
                    bowler_no_ball = int(bowler[8])
                    bowler_wides = int(bowler[9])
                    break
            
            try:
                if (43 < batsmen_1_runs < 47):
                    batsmen = batsmen_1
                elif (43 < batsmen_2_runs < 47):
                    batsmen = batsmen_2
                else:
                    batsmen = 'None'
            except:
                pass
            
            print(math.floor(team_batting_overs) - bet.over_number)
            print(bet.over_number)
            print(math.floor(team_batting_overs))
            if (math.floor(team_batting_overs) - bet.over_number) == 1:
                Match.query.filter_by(id=bet.id).update(dict(resolved=1))
                db.session.commit()
                print("working")
                if (special_questions == 3):
                    if batsmen == 'batsmen_1':
                        batsmen_stored = batsmen_1_runs
                    else:
                        batsmen_stored = batsmen_2_runs
                    prediction_change(bet.input, bet.curr_data, batsmen_stored, threshold, bet)
                if (special_questions == 4):
                    if batsmen == 'batsmen_1':
                        batsmen_stored = batsmen_1_runs
                    else:
                        batsmen_stored = batsmen_2_runs
                    prediction_change(bet.input, bet.curr_data, batsmen_stored, threshold, bet)
                elif (question_number == 0):
                    conditional_change(bet.input, bet.curr_data, batsmen_1_sr, bet)
                elif (question_number == 1):
                    prediction_change(bet.input, bet.curr_data, batsmen_1_fours, threshold, bet)
                elif (question_number == 2):
                    prediction_change(bet.input, bet.curr_data, batsmen_1_sixes, threshold, bet)
                elif (question_number == 3):
                    prediction_change(bet.input, bet.curr_data, bowler_wides, threshold, bet)
                elif (question_number == 4):
                    prediction_change(bet.input, bet.curr_data, bowler_wickets, threshold, bet)
                elif (question_number == 5):
                    prediction_change(bet.input, bet.curr_data, bowler_wides, threshold, bet)
                elif (question_number == 6):
                    prediction_change(bet.input, bet.curr_data, bowler_maidens, threshold, bet)
                elif (question_number == 7):
                    conditional_change(bet.input, bet.curr_data, bowler_econ, bet)
            if (math.floor(team_batting_overs) - bet.over_number) == 5:
                Match.query.filter_by(id=bet.id).update(dict(resolved=1))
                db.session.commit()
                if (question_number == 8):
                    prediction_change(bet.input, bet.curr_data, team_batting_runs, threshold, bet)
                elif (question_number == 9):
                    prediction_change(bet.input, bet.curr_data, batsmen_2_runs, threshold, bet)
                elif (question_number == 10):
                    prediction_change(bet.input, bet.curr_data, bowler_wickets, threshold, bet)
                elif (question_number == 11):
                    prediction_change(bet.input, bet.curr_data, team_batting_wickets, threshold, bet)
            if (special_questions == 1):
                prediction_change(bet.input, bet.curr_data, team_batting_runs, threshold, bet)
                Match.query.filter_by(id=bet.id).update(dict(resolved=1))
            elif (special_questions == 2):
                prediction_change(bet.input, bet.curr_data, team_batting_runs, threshold, bet)
                Match.query.filter_by(id=bet.id).update(dict(resolved=1))
            
    return render_template('scorecard.html')

    '''
    bet_placed_arr = []
    bet_status_arr = []
    bet_details_arr = []
    bet_id_arr = []
    bet_result_arr = []
        
    bet_total = Match.query.filter_by(player_id = current_user.id).all()
    for bets_all_player in bet_total:
        bet_id_arr.append(bets_all_player.id)
        bet_details_arr.append(bets_all_player.prop)
        bet_placed_arr.append(bets_all_player.input)
        bet_status_arr.append(bets_all_player.resolved)
        if(bet_result_arr.)


    return render_template('checkbet.html', question = question, option1 = option1, option2 = option2, user=current_user)

        '''

  