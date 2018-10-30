Multiplayer Snake Game
===

This is a multiplayer snake game that works over a network. It uses pygame for graphical user interface, user
interaction and timing, even on the server (thus you need X forwarding if the server is remote). The server also has
a GUI that shows the server's view of the game. This is a server-authoritative game: the server is the sole authority
for all game information. It responds to events from the clients, but as network delays may occur, the server may end
up with a different decision than the client.

This game is a developed as part of a research project and it is not meant for commercial use. It has bugs and the
entire user experience is very limited (and buggy).

How to Use
---
### Start server:
```
python server.py SHOW
```
(The ```SHOW``` argument makes the server show a window with the global game view. Even without this argument, the server loads as a window (hidden), so you should have an X server running)

Exit by pressing ESC for more than 3 seconds.

### Start client:
```
python client.py [AUTO] [server address]
```
By default, the client connects to localhost as the server address, unless another address is given in command line. The ```AUTO``` argument makes the client play automatically. It does not make it super intelligence, but it avoids screen bounds and tries to eat as much food as possible. AUTO clients do not try to avoid hitting themselves, nor do they try to eat each other (although this may happen accidentally). The AUTO mode was devloped for debugging purposes, not for some AI effort...

Contribution
---
Contributors are welcome to open pull requests and email yotamhc (at) berkeley . edu.

License
---
Please see LICENSE file.
