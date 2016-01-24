# Block Attack: UDP Server

> UDP Server is going to use `json` & follow below mentioned structure.
> 
> UDP Server is going to written using `socketserver.UDPServer` & `socketserver.ThreadingMixIn`.

**Note:** Need to ensure when a UDP packet is received. Only the packets with `timestamp > now` are being used to update game screen.

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
