# Block Attack: HTTP Server

> HTTP Server is going to follow REST protocol. All requests have Authorization Token

> The HTTP Server is going to be written with `flask` & `flask-restful`.

* `/users`

  *List all the users connected to server.*
  
  |> Response (GET) :: json -> ` [{'username': ___, 'status': ___ }, ...] `

* `/connect`

  *Start game with given opponent.*

  |> POST :: json -> `{'username': ___, 'opponent': ___}`

  |> Response (POST) :: json -> ` {'game_id': ___ }`
  |> Response (POST) :: json -> ` {'error': 'Unable to create the match' }`

* `/login`

  *Log into server with given username.*

  |> POST :: json -> `{'username': ___}`

  |> Response (POST) :: str -> `User succesfully logged in.`


