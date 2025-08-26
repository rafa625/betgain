#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bet_sqlite.py
Consulta SQLite (tabela com odds e placares), filtra por odds do mandante/visitante,
simula apostas no mandante (stake fixa), imprime jogo-a-jogo e resumo.

Uso:
  python bet_sqlite.py
  python bet_sqlite.py --db database.sqlite --table betfront --home-max 1.5 --away-min 8 --stake 1 --limit 200
"""

import argparse
import sqlite3
import zipfile
import os
from utils import profit_home_win
import config as cfg
from config import SQLITE_DB

def extrair_database_zip(zip_path="database.zip", db_name=SQLITE_DB):
    if not os.path.exists(zip_path):
        print(f"Arquivo {zip_path} não encontrado.")
        return

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if db_name in zip_ref.namelist():
            zip_ref.extract(db_name, ".")
            print(f"{db_name} extraído com sucesso.")
        else:
            print(f"{db_name} não encontrado em {zip_path}.")

def main():
    ap = argparse.ArgumentParser(description="Apostas via SQLite (filtros de odds).")
    ap.add_argument("--db", type=str, default=cfg.SQLITE_DB, help="Arquivo SQLite.")
    ap.add_argument("--table", type=str, default=cfg.SQLITE_TABLE, help="Tabela.")
    ap.add_argument("--home-max", type=float, default=cfg.HOME_ODD_MAX, help="Mandante <= este valor.")
    ap.add_argument("--away-min", type=float, default=cfg.AWAY_ODD_MIN, help="Visitante > este valor (filtro).")
    ap.add_argument("--stake", type=float, default=cfg.STAKE, help="Stake por aposta.")
    ap.add_argument("--limit", type=int, default=cfg.SQLITE_MAX_PRINT, help="Limite de linhas a exibir (ORDER BY DATETIME).")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    rows = cur.execute(f"""
        SELECT 
            DATE(DATETIME)    AS data,
            MATCH             AS partida,
            HOME_CLOSING      AS odd_home,
            DRAW_CLOSING      AS odd_draw,
            AWAY_CLOSING      AS odd_away,
            FTG1              AS gm,
            FTG2              AS gv
        FROM {args.table}
        WHERE 
            HOME_CLOSING <= ? AND
            AWAY_CLOSING  >  ? AND
            FTG1 IS NOT NULL AND FTG2 IS NOT NULL
        ORDER BY DATETIME
        LIMIT ?;
    """, (args.home_max, args.away_min, args.limit)).fetchall()

    conn.close()

    print(f"DB: {args.db} | Tabela: {args.table} | Filtro: home <= {args.home_max} & away > {args.away_min} | Stake={args.stake:.2f}")
    print(f"{'#':>3}  {'Data':10}  {'Partida':40}  {'OddHome':>7}  {'OddAway':>7}  {'Placar':7}  {'Res':3}  {'Lucro':>9}  {'Acum':>9}")
    print("-" * 110)

    cum = 0.0
    wins = draws = losses = 0

    for i, (data, partida, odd_home, odd_draw, odd_away, gm, gv) in enumerate(rows, 1):
        lucro = profit_home_win(float(odd_home), float(args.stake), int(gm), int(gv))
        cum += lucro
        if gm > gv:
            wins += 1; res = "W"
        elif gm == gv:
            draws += 1; res = "D"
        else:
            losses += 1; res = "L"

        print(f"{i:>3}  {data:10}  {partida[:40]:40}  {float(odd_home):7.2f}  {float(odd_away):7.2f}  {gm}-{gv:3}   {res:3}  {lucro:9.2f}  {cum:9.2f}")

    total = len(rows)
    invest = total * args.stake if total else 0.0
    roi = (cum / invest * 100.0) if invest else 0.0
    wr = (wins / total * 100.0) if total else 0.0

    print("\nResumo:")
    print(f"Jogos: {total} | W: {wins}  D: {draws}  L: {losses}")
    print(f"Lucro líquido: {cum:.2f} | ROI: {roi:.2f}% | Winrate: {wr:.2f}%")

if __name__ == "__main__":
    extrair_database_zip()
    main()
