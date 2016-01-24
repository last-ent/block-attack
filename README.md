# Block Attack

## Game UI

```ascii
                                                                          
                                                                          
                                                                          
         **************************************************************   
         *                                    .........|              *   
         *                                    .  Next .|  Opponent's  *   
         *                                    .-------.|   Screen     *   
         *                                    . U | O .|              *   
         *                                    .   |   .|              *   
         *                                    .   |   .|              *   
         *                                    .........|              *   
         *                                             |              *   
         *                                             |              *   
         *                                             |              *   
         *                                             |              *   
         *                                             |              *   
         *                                             |              *   
         *                                             |              *   
         *                                             |              *   
         *                           Blocks            |              *   
         *                     @@@@@@@@@@@@@@@@@@@@@@@@|              *   
         *-------Line----------@@@@@@@@@@@@@@@@@@@@@@@@|-----Line-----*   
         *                     @@@@@@@@@@@@@@@@@@@@@@@@|              *   
         * B    Blocks         @@@@@@@@@@@@@@@@@@@@@@@@|              *   
         *@@   @@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@|              *   
         *@@   @@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@|              *   
         **************************************************************   
         ========~~~~~====~~~~~=====~~~~~======~~~~~===================   
         =       ~ I ~    ~ R ~     ~ S ~      ~ N ~                  =   
         ========~~~~~====~~~~~=====~~~~~======~~~~~===================   

Line     -> Beyond this line, Opponent's powers won't work. (2 squares above least block filled line.)
B/Blocks -> Normal Tetris Blocks.
Next     -> Shows next block.
   |> U  -> Your block
   |> O  -> Opponent's block

Opponent's Incoming Block == OIB
Powers   -> Signified by the letters in ` ~ `. Works against the opponent.
   |> I  -> Invert OIB
   |> R  -> Swap OIB with a random shape.
   |> S  -> Swap OIB with User selected shape (A drop down appears when S is clicked.) 
   |> N  -> Shift block's position to left or right. (User selected/random?)
```

## Server & Server Commands

### User Server :: HTTP

*All requests have Authorization Token.*

* `/users`

  *List all the users connected to server.*
  
  |> Response (GET) :: json -> ` [{'username': ___, 'status': ___ }, ...] `

* `/connect`

  *Start game with given opponent.*

  |> POST :: json -> `{'username': ___, 'opponent': ___}`

  |> Response (POST) :: json -> ` {'status': ___ }`

* `/login`

  *Log into server with given username.*

  |> POST :: json -> `{'username': ___}`

  |> Response (POST) :: json -> ` {'status': ___ }`

### Game Server

* **Game Start**
    
    * Request :: json ->
      ```json
      {
        "command": "connect",
        "self": ___,
        "opponent": ___
      }
      ```

    * Response :: json ->
      ```json
      {
        "timestamp": ___,
        "command": "game_start",
        "game_name": ___,
        "self": ___,
        "opponent": ___,
        "user_blocks": ___,
        "opponent_blocks": ___,
        "next_block": ___,
        "time_left": ___,
        "user_score": ___,
        "opponent_score: ___,
        "powers_available": ___
      }
      ```

* **Game Continuation**
    
    * Request :: json ->
      ```json
      {
        "timestamp": ___,
        "command": "game_flux",
        "game_name": ___,
        "user_blocks": ___,
        "opponent_blocks": ___,
        "power_used": ___,
        "user_score": ___,
        "powers_available": ___
      }
      ```

    * Response :: json ->
      ```json
      {
        "timestamp": ___,
        "command": "game_flux",
        "game_name": ___,
        "user_blocks": ___,
        "opponent_blocks": ___,
        "power_used": ___,
        "power_applied": ___,
        "next_block": ___,
        "time_left": ___,
        "user_score": ___,
        "opponent_score": ___
        "powers_available": ___
      }
      ```

* **Game Conclusion**
    
    * Request :: json ->
      ```json
      {
        "timestamp": ___,
        "command": "game_flux",
        "game_name": ___,
        "user_blocks": ___,
        "opponent_blocks": ___,
        "power_used": ___,
        "user_score": ___
      }
      ```

    * Response :: json ->
      ```json
      {
        "timestamp": ___,
        "command": "game_end",
        "winner": ___,
        "score": ___,
        "reason": ___
      }
      ```