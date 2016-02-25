# Block Attack: The Servers

There are two servers we will be using on the backend.   

* **HTTP Server**
  
  * Maintain connected Users
  * List connected Users
  * Login with a username

* **UDP Server**
  * Connect and maintain game state

## How to handle change from HTTP to TCP/UDP for game.
Once the user sends a `/connect`, and returns the `game_id` in response.
Then the client needs to start a TCP/UDP connection with game id and rest of required details.
