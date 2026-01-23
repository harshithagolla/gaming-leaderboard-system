# populate_data.py
import argparse
import random
import time
import math
import pymysql

def batched_insert(cursor, base_query, rows, batch_size=10000):
    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i+batch_size]
        values_str = ",".join(["(" + ",".join(cursor.connection.escape(v) for v in r) + ")" for r in chunk])
        cursor.execute(base_query + values_str)

def gen_users(n):
    for i in range(1, n+1):
        yield (f"user_{i}",)

def gen_game_sessions(n_sessions, n_users):
    modes = ['solo','team']
    for _ in range(n_sessions):
        user_id = random.randint(1, n_users)
        score = random.randint(100, 10000)
        mode = random.choice(modes)
        # timestamp left to default (server time)
        yield (user_id, score, mode)

def main(args):
    conn = pymysql.connect(host=args.host, port=args.port, user=args.user, password=args.password, db=args.db,
                           autocommit=False, charset='utf8mb4')
    cur = conn.cursor()
    users = args.users
    sessions = args.sessions
    print(f"Inserting {users} users...")
    batch = 5000
    user_rows = []
    count = 0
    # insert users in batches
    for u in gen_users(users):
        user_rows.append(u)
        if len(user_rows) >= batch:
            vals = ",".join(cur.connection.escape(v[0]) for v in user_rows)
            # build multi-row insert
            q = "INSERT INTO users (username) VALUES " + ",".join(f"({cur.connection.escape(u[0])})" for u in user_rows)
            cur.execute(q)
            conn.commit()
            user_rows = []
            count += batch
            print(f"Inserted {count} users")
    if user_rows:
        q = "INSERT INTO users (username) VALUES " + ",".join(f"({cur.connection.escape(u[0])})" for u in user_rows)
        cur.execute(q)
        conn.commit()
        print(f"Inserted {count + len(user_rows)} users")

    # Insert sessions in batches
    print(f"Inserting {sessions} game sessions (this may take a while)...")
    batch = 10000
    sess_rows = []
    inserted = 0
    gen = gen_game_sessions(sessions, users)
    for sess in gen:
        sess_rows.append(sess)
        if len(sess_rows) >= batch:
            values = ",".join(f"({cur.connection.escape(r[0])},{cur.connection.escape(r[1])},{cur.connection.escape(r[2])})" for r in sess_rows)
            q = "INSERT INTO game_sessions (user_id, score, game_mode) VALUES " + values
            cur.execute(q)
            conn.commit()
            inserted += len(sess_rows)
            print(f"Inserted {inserted} sessions")
            sess_rows = []
    if sess_rows:
        values = ",".join(f"({cur.connection.escape(r[0])},{cur.connection.escape(r[1])},{cur.connection.escape(r[2])})" for r in sess_rows)
        q = "INSERT INTO game_sessions (user_id, score, game_mode) VALUES " + values
        cur.execute(q)
        conn.commit()
        inserted += len(sess_rows)
        print(f"Inserted {inserted} sessions")

    # Populate leaderboard by aggregating SUM(score) per user
    print("Aggregating total_score into leaderboard...")
    # NOTE: Use efficient single SQL: insert into leaderboard (user_id, total_score) select user_id, SUM(score) ...
    cur.execute("INSERT INTO leaderboard (user_id, total_score) SELECT user_id, SUM(score) as total_score FROM game_sessions GROUP BY user_id")
    conn.commit()
    print("Leaderboard populated.")

    cur.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=3306)
    parser.add_argument('--user', default='root')
    parser.add_argument('--password', default='')
    parser.add_argument('--db', default='leaderboard_db')
    parser.add_argument('--users', type=int, default=200000)
    parser.add_argument('--sessions', type=int, default=1000000)
    args = parser.parse_args()
    main(args)
