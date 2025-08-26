#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extremos_sqlite.py
Mostra jogo mais antigo e mais recente (com odds e placar) numa tabela SQLite.

Uso:
  python extremos_sqlite.py
  python extremos_sqlite.py --db database.sqlite --table betfront
"""

import argparse
import sqlite3
import config as cfg

def show(label, row):
    if not row:
        print(f"{label}: não encontrado")
        return
    data, hora, partida, gm, gv, o1, ox, o2, dt_raw = row
    placar = f"{gm}-{gv}" if gm is not None and gv is not None else "N/D"
    print(f"{label}: {data} {hora} | {partida} | Placar: {placar} | Odds (1-X-2): {o1}, {ox}, {o2} | DT raw: {dt_raw}")

def main():
    ap = argparse.ArgumentParser(description="Extremos temporais (mais antigo/recente) no SQLite.")
    ap.add_argument("--db", type=str, default=cfg.SQLITE_DB, help="Arquivo SQLite.")
    ap.add_argument("--table", type=str, default=cfg.SQLITE_TABLE, help="Tabela.")
    args = ap.parse_args()

    with sqlite3.connect(args.db) as conn:
        cur = conn.cursor()

        oldest = cur.execute(f"""
            SELECT DATE(DATETIME) AS data, TIME(DATETIME) AS hora, MATCH, FTG1, FTG2,
                   HOME_CLOSING, DRAW_CLOSING, AWAY_CLOSING, DATETIME
            FROM {args.table}
            WHERE DATETIME IS NOT NULL
            ORDER BY DATETIME ASC
            LIMIT 1;
        """).fetchone()

        newest = cur.execute(f"""
            SELECT DATE(DATETIME) AS data, TIME(DATETIME) AS hora, MATCH, FTG1, FTG2,
                   HOME_CLOSING, DRAW_CLOSING, AWAY_CLOSING, DATETIME
            FROM {args.table}
            WHERE DATETIME IS NOT NULL
            ORDER BY DATETIME DESC
            LIMIT 1;
        """).fetchone()

    show("Mais antigo", oldest)
    show("Mais recente", newest)

if __name__ == "__main__":
    main()
