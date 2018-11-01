Multiplayer Snake Game - gRPC version
===

This is a multiplayer snake game that works over a network. It uses pygame for graphical user interface, user
interaction and timing, even on the server (thus you need X forwarding if the server is remote). The server also has
a GUI that shows the server's view of the game. This is a server-authoritative game: the server is the sole authority
for all game information. It responds to events from the clients, but as network delays may occur, the server may end
up with a different decision than the client.

This game is a developed as part of a research project and it is not meant for commercial use. It has bugs and the
entire user experience is very limited (and buggy).

Contribution
---
Contributors are welcome to open pull requests and email yotamhc (at) berkeley . edu.

License
---
Please see LICENSE file.
