"""История снимков коэффициентов и прогрузов (нужна для графиков и бэктеста)."""
import sqlite3
from .providers.base import Odds, MoneyFlow


class DB:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS odds_snap(
            ts DATETIME DEFAULT CURRENT_TIMESTAMP, match_id TEXT, bookmaker TEXT,
            home REAL, draw REAL, away REAL);
        CREATE TABLE IF NOT EXISTS flow_snap(
            ts DATETIME DEFAULT CURRENT_TIMESTAMP, match_id TEXT, source TEXT,
            home_pct REAL, draw_pct REAL, away_pct REAL, volume REAL);
        """)

    def save_odds(self, o: Odds):
        self.conn.execute("INSERT INTO odds_snap(match_id,bookmaker,home,draw,away) VALUES(?,?,?,?,?)",
                          (o.match_id, o.bookmaker, o.home, o.draw, o.away))
        self.conn.commit()

    def save_flow(self, f: MoneyFlow):
        self.conn.execute("INSERT INTO flow_snap(match_id,source,home_pct,draw_pct,away_pct,volume) VALUES(?,?,?,?,?,?)",
                          (f.match_id, f.source, f.home_pct, f.draw_pct, f.away_pct, f.volume))
        self.conn.commit()
