from flask import *
from flask_socketio import SocketIO,join_room,rooms
from flask_session import Session
from chess import board
from time import sleep
app = Flask(__name__)
boards = {}
deletelist = {}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'temporary'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)
@app.route('/')
def index():
    return render_template('wait.html')
@app.route('/game')
def game():
    if 'game' in session:
        deletelist[str(session['game'])+str(int(session['pieces']))]= False
        if boards[session['game']][0][1] !='b':
            return render_template('game.html')
    return redirect(url_for('index'))
@socketio.on('log')
def connection(request):
    if 'game' not in session:
        games = len(boards)
        if games!=0 and boards[games][0][1]=='b':
            join_room('waiting'+str(games))
            boards[games][0][1]= 'b'+str(games)
            session['pieces']= True
            session['game']= games
            session.modified = True
            socketio.emit('redirect', url_for('game'),room= 'waiting'+str(games))
        else:
            join_room('waiting'+str(games+1))
            boards[games+1]=[['w'+str(games+1),'b'],board()]
            session['pieces']= False
            session['game']= games+1
            session.modified = True
    else:
        deletelist[str(session['game'])+str(int(session['pieces']))]= False
        socketio.emit('redirect', url_for('game'),room= 'waiting'+str(session['game']))
@socketio.on('disconnect')
def disconnect():#check if session is empty-does it work
    if 'game' in session:
        def deletesession(sess,t):
            if deletelist[sess]==False:
                del deletelist[sess]
            elif t == 60:
                session.clear()
                print('SESSION CLEARED')
                del deletelist[sess]
            elif deletelist[sess]==True:
                sleep(1)
                deletesession(sess,t+1)
        deletelist[str(session['game'])+str(int(session['pieces']))]= True
        deletesession(str(session['game'])+str(int(session['pieces'])),0)
@socketio.on('move')
def update(request):
    move = request['data']
    if move =="initiation":
        join_room('game'+str(session['game']))
    game = boards[session['game']][1]
    game.play(move)
    socketio.emit('update',{'moves':game.legal_moves(),'board':game.grid,'square':move[2:],'checks':game.incheck()},room= 'game'+str(session['game']))

if __name__ == "__main__":
    socketio.run(app ,port=6454, debug=True)
    #socketio.run(app,host='0.0.0.0',port=5072, debug=True)