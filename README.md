# Chess
Chess web based multiplayer game

To play either uncomment the last line and comment the line above and open the address on another device on the lan.
Or to play on the same address open the address on two different browsers e.g. normal chrome and incognito or chrome and edge/firefox etc
This is to make sure the session data is different.

Note the server only deletes session data 60 seconds after a disconnect so unless you change t ==60 to t==0 you'll have to delete the files the flask-session folder before execution.
