# About the project
**SpotiSongs** is a **Flask** webapp that helps you discover new music on Spotify.
It is currently a **WIP**. For now, the app merely shows the user their top 10 most listened songs and 10 last saved songs.

# Getting started

Clone the repo:
<code>git clone https://github.com/theolaf/SpotiSongs.git</code>

Then you'll need to install Docker.
Add a file called docker-compose.yml to the root of the repo containing the following:

	version: '3'
	services:
	  spotisongs:
	    build: .
	    ports:
	      - "5000:5000"
	    volumes:
	      - .:/src
	    environment:
	      CLIENT_ID: "YOUR_SPOTIFY_CLIENT_ID"
	      CLIENT_SECRET: "YOUR_SPOTIFY_CLIENT_SECRET"
	      REDIRECT_URI: "http://127.0.0.1:5000/api_callback"
	      FLASK_SECRET: "YOUR_FLASK_SECRET_KEY"

You can then run the following command:
<code>docker-compose up -d</code>
