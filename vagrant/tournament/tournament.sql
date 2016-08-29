-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (

-- This creates a simple table of players with a auto-generated serial id and a player name.

  id serial PRIMARY KEY,
  name text
  );

CREATE TABLE matches (

-- This creates a table of matches with an auto-generated matchid (which is not used as a primary key currently,
-- but is set up to be one incase the program is expanded in a way that would involve referencing individual matches)
-- as well as a list of winner and loser for each match. Currently, ties are not allowed.

  matchid serial PRIMARY KEY,
  winner INT REFERENCES players(id),
  loser INT REFERENCES players(id)
  );

CREATE VIEW playermatchrawlist AS (

-- This is a view which is used to simplify the creation of playerswinsmatches below.
-- It compiles a list of all winners and losers from the matches table for easy tallying of how many matches a player has played.
-- Any advice on how to eliminate this view and count the matches a player has played in without this intermediate step,
-- without overcomplicating the playerswinsmatches function below are welcome.

  SELECT winner
  AS playerid
  FROM matches
  UNION ALL
  SELECT loser
  FROM matches
  );

CREATE VIEW playerswinsmatches as (

-- This table is a list of all players (by id and name) along with a count of their number of wins and total matches played, ordered by # of wins.

  SELECT players.id,
  players.name,
  COUNT(matches.winner) as wins,
  COUNT(playermatchrawlist) as matches
  FROM players
  LEFT JOIN matches
  ON players.id = matches.winner
  LEFT OUTER JOIN playermatchrawlist
  ON players.id = playermatchrawlist.playerid
  GROUP BY players.id ORDER BY wins DESC
  );