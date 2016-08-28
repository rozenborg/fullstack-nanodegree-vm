#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("""DELETE FROM swisspairings;""") # swisspairs are cleared as well every time matches are
    c.execute("""DELETE FROM matches;""")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("""DELETE FROM players;""")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("""SELECT count(*) FROM players;""")
    count = c.fetchone()
    db.close()
    return count[0] # the number of players is called from the tuple generated with c.fetchone()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("""INSERT INTO players (name) VALUES (%s)""", (name,)) # I believe this is query parameterization to prevent SQL injection. Please correct me if I am wrong and/or suggest alternative methods.
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("""SELECT * FROM playerswinsmatches;""")
    standings = c.fetchall()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    # winner and loser must match primary key for players that have already been registered
    c.execute("""INSERT INTO matches (winner, loser) VALUES (%s, %s)""", (winner, loser,)) # I believe this is query parameterization to prevent SQL injection. Please correct me if I am wrong and/or suggest alternative methods.
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # this swiss pairing algorithm makes use of the ordering of standings by wins, and simply assigns the odd players with the even players subsequent to them in the list

    db = connect()
    c = db.cursor()
    c.execute("""DELETE FROM swisspairings;""") # old pairings are deleted and we start fresh each time.
    i = 0
    standings = playerStandings()
    query = """INSERT INTO swisspairings (id1, name1, id2, name2) values (%s, %s, %s, %s)""" # I believe this is query parameterization to prevent SQL injection. Please correct me if I am wrong and/or suggest alternative methods.
    while i < len(standings):
        c.execute(query, (standings[i][0], standings[i][1], standings[i + 1][0], standings[i + 1][1], ))
        db.commit()
        i += 2
    c.execute("""SELECT * FROM swisspairings;""")
    pairings = c.fetchall()
    return pairings #returns a tuple with the resultant pairings.
