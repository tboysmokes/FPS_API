from supervised import Head2Head, homeAdvantage, pastfivematch, similarOpponent, loop, put_in_list
from flask import Flask, request, jsonify



app = Flask(__name__)
app.config['SECRET_KEY'] = "TYPESHII"


@app.route('/Head2Head', methods=['GET', 'POST'])
def H2H():
    if request.method == 'POST':
        data = request.get_json()
        team1 = data['team1']
        team2 = data['team2']

        prediction_list, neededData = Head2Head(teamid=team1, team2id=team2)

        match_outcome = loop(neededData['match_outcome'])
        event_date = loop(neededData['event_date'])
        team1id = loop(neededData['team1_id'])
        team2id = loop(neededData['team2_id'])

        return jsonify({'datalist': list(prediction_list), 'match_outcome': match_outcome, 'event_date': event_date, 'team2_id': team2id, 'team1_id': team1id})
    

@app.route('/pastfivematch', methods=['GET', 'POST'])
def lastfivematch():
    if request.method == 'POST':
        data = request.get_json()
        teamid = data['team1']
        prediction, neededData = pastfivematch(teamid=teamid)
        OpponentName = loop(neededData['team2_id'])
        MatchDate = loop(neededData['event_date'])
        MatchOutcome = loop(neededData['match_outcome'])
        win, loss, draw = put_in_list(prediction)
        return jsonify({'win': win, 'loss': loss, 'draw': draw, 'opponent': OpponentName, 'date': MatchDate, 'outcome': MatchOutcome})
    

@app.route('/homeadvantage', methods=['GET', 'POST'])
def homeadvantages():
    if request.method == 'POST':
        data = request.get_json()
        teamid = data['team1']
        prediction, neededData = homeAdvantage(teamid=teamid)
        OpponentName = loop(neededData['team2_id'])
        MatchDate = loop(neededData['event_date'])
        MatchOutcome = loop(neededData['match_outcome'])
        win, loss, draw = put_in_list(prediction)
        return jsonify({'win': win, 'loss': loss, 'draw': draw, 'opponent': OpponentName, 'date': MatchDate, 'outcome': MatchOutcome})
    

@app.route('/similaropponent', methods=['GET', 'POST'])
def sameopponent():
    if request.method == 'POST':
        data = request.get_json()
        team1 = data['team1']
        team2 = data['team2']
        team1prediction, team2prediction, datalist, similarTeams = similarOpponent(teamid=team1, team2id=team2)
        win, loss, draw = put_in_list(team1prediction)
        win1, loss1, draw1 = put_in_list(team2prediction)
        return jsonify({'team1': {'win': win, 'loss': loss, 'draw': draw},
                        'team2': {'win': win1, 'loss': loss1, 'draw': draw1},
                        'opponent': {'name': similarTeams, 'date': datalist}})

if __name__ == "__main__":
    app.run(debug=True)