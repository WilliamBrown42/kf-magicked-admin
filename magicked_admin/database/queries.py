"""
Start the process of moving queries to a seperate file.
Also might work on creating private methods for certain queries
Double check the spacing is correct on the strings
"""

class Queries:
    def __init__:
        self.cur = cur

    """
    Some of these will be super simple and will
    seem overkill to have a method but as query complexity
    increases and whatnot it will make it easier to manage.
    Need to look at how to deal w/ multi args for column
    """

    def _select_single:
        """Private method for simple selections used in !kills, !dosh, etc.
        Args: column
        """
        return

    def _select_average:
        """Private method for averaging selections
        Args: column
        # TODO: Add table
        """
        query = ('SELECT AVG({})'
                'FROM players'
                ).format(column)
        return query

    def _select_sum:

    def _select_max:

    def _select_min:
        
    def _select_rank:
        """Private method for rank based selections.
        Args: column
        TODO: Combine into one query and fix args
        """
        subquery = ("SELECT count(*) "
                    "FROM players "
                    "AS player2 "
                    "WHERE player2.kills >= player1.kills"
                    )
        query = "SELECT player1.*,({}) "
                "AS kill_rank "
                "FROM players AS player1 "
                "WHERE player1.username=?"
                ).format(subquery)
        return query

    # Example query, may vary, possibly format and return in proper form for
    # whatever command it is?
    def query_command(self):
        lock.acquire(True)
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][0]

    def rank_kills(self, username):
        subquery = "SELECT count(*) FROM players AS player2 WHERE player2.kills >= player1.kills"
        query = "SELECT player1.*,({}) AS kill_rank FROM players AS player1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    def rank_dosh(self, username):
        subquery = "SELECT count(*) FROM players as player2 WHERE player2.dosh >= player1.dosh"
        query = "SELECT  player1.*,({}) AS dosh_rank FROM  players AS player1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    def rank_death(self, username):
        subquery = "SELECT count(*) FROM players as player2 WHERE player2.deaths <= player1.deaths"
        query = "SELECT player1.*,({}) AS death_rank FROM  players AS player1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    def rank_kd(self, username):
        subquery = "SELECT count(*) FROM players as p2 WHERE p2.kills / p2.deaths >= p1.kills / p1.deaths"
        query = "SELECT p1.*,({}) AS kd_rank FROM  players AS p1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    def rank_time(self, username):
        subquery = "SELECT count(*) FROM players as player2 WHERE player2.time_online >= player1.time_online"
        query = "SELECT player1.*,({}) AS time_rank  FROM  players AS player1 WHERE p1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    # SUM(dosh_spent) Add in later.
    def server_dosh(self):
        lock.acquire(True)
        self.cur.execute('SELECT SUM(dosh) FROM players')
        all_rows = self.cur.fetchall()
        lock.release()
        # Errors out when you call it with 0 with "NoneType"
        if all_rows and all_rows[0][0]:
            return int(all_rows[0][0])
        else:
            return 0

    def server_kills(self):
        lock.acquire(True)
        self.cur.execute('SELECT SUM(kills) FROM players')
        all_rows = self.cur.fetchall()
        lock.release
        # Errors out when you call it with 0 with "NoneType"
        if all_rows and all_rows[0][0]:
            return int(all_rows[0][0])
        else:
            return 0

    def top_kills(self):
        lock.acquire(True)
        self.cur.execute('SELECT username, kills FROM players ORDER BY kills DESC')
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows

    def top_dosh(self):
        lock.acquire(True)
        self.cur.execute('SELECT username, dosh FROM players ORDER BY dosh DESC')
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows

    def player_dosh(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (dosh) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_dosh_spent(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (dosh_spent) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_kills(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (kills) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_deaths(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (deaths) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_logins(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (logins) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_time(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (time_online) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_health_lost(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (health_lost) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0
