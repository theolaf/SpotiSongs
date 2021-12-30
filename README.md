# About the project
**SpotiSongs** is a **Flask** webapp that helps you discover new music on Spotify.
It is currently a **WIP**. For now, the app merely shows the user their top 10 most listened songs and 10 last saved songs.

# Getting started

Clone the repo:
<code>git clone https://github.com/theolaf/SpotiSongs.git</code>

Install [Docker](https://www.docker.com/) then go to your [Spotify Dashboard](https://developer.spotify.com/dashboard) to register a new app and get your client ID and secret. Depending your Spotify app is in development mode, you need to authorize users manually. If you want to add more than 25 users to the app, you'll have to submit a quota extension to Spotify.<br/>
Add a .env file at the root of the repo containing the following:

	CLIENT_ID="YOUR_SPOTIFY_CLIENT_ID"
	CLIENT_SECRET="YOUR_SPOTIFY_CLIENT_SECRET"
	REDIRECT_URI="http://127.0.0.1:5000/api_callback"
	FLASK_SECRET="YOUR_FLASK_SECRET_KEY"

You can then run the following command to start the container:
<code>docker-compose up -d</code><br/>
Go to <code>http://localhost:5000/</code> to use the app.
