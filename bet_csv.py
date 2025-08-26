#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bet_csv.py
Lê arquivos CSV (Football-Data), filtra por mandantes e adversários excluídos,
escolhe a melhor coluna de odds do mandante, simula apostas com stake fixa,
imprime jogo-a-jogo e resumo.

Uso:
  python bet_csv.py
  python bet_csv.py --files SP1_2425.csv SP1_2324.csv --teams "Real Madrid,Barcelona" --exclude "Ath Madrid,Valencia,Real Madrid" --stake 5 --max 20
"""

import argparse
from typing import Any, Dict, List
from utils import choose_home_odd, dict_reader_utf8_sig, key_dt_ddmmyy, profit_home_win
import config as cfg

def parse_csv_list(s: str) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()]

def parse_set(s: str) -> set:
    return set(parse_csv_list(s))

def main():
    ap = argparse.ArgumentParser(description="Apostas em CSV Football-Data (mandantes + exclusões).")
    ap.add_argument("--files", nargs="*", default=cfg.CSV_FILES, help="Lista de CSVs (Football-Data).")
    ap.add_argument("--teams", type=str, default=",".join(sorted(cfg.TIMES_MANDANTES)), help="Times mandantes (separados por vírgula).")
    ap.add_argument("--exclude", type=str, default=",".join(sorted(cfg.EXCLUIR_ADVERSARIOS)), help="Adversários excluídos (vírgula).")
    ap.add_argument("--stake", type=float, default=cfg.STAKE, help="Stake por aposta.")
    ap.add_argument("--max", type=int, default=cfg.MAX_PRINT if cfg.MAX_PRINT is not None else -1, help="Máximo a imprimir (padrão: todos).")
    ap.add_argument("--odds-pref", type=str, default=",".join(cfg.ODDS_HOME_PRIORIDADE), help="Ordem de preferência das colunas de odds (vírgula).")
    args = ap.parse_args()

    files = args.files
    teams = parse_set(args.teams)
    excludes = parse_set(args.exclude)
    stake = float(args.stake)
    max_print = None if args.max is None or args.max < 0 else int(args.max)
    odds_priority = parse_csv_list(args.odds_pref)

    linhas: List[Dict[str, Any]] = []

    for path in files:
        try:
            rd = dict_reader_utf8_sig(path)
            headers = rd.fieldnames or []
            for row in rd:
                home = (row.get("HomeTeam") or "").strip()
                away = (row.get("AwayTeam") or "").strip()
                if home not in teams:
                    continue
                if away in excludes:
                    continue

                # gols
                try:
                    fthg = int((row.get("FTHG") or row.get("HG") or "").strip())
                    ftag = int((row.get("FTAG") or row.get("AG") or "").strip())
                except Exception:
                    continue

                col_odd, odd_home = choose_home_odd(row, headers, odds_priority)
                if odd_home is None:
                    continue

                linhas.append({
                    "Src": path,
                    "Date": row.get("Date", ""),
                    "Time": row.get("Time", ""),
                    "HomeTeam": home,
                    "AwayTeam": away,
                    "FTHG": fthg,
                    "FTAG": ftag,
                    "OddCol": col_odd,
                    "OddHome": float(odd_home),
                })
        except FileNotFoundError:
            print(f"[AVISO] Arquivo não encontrado: {path}")
        except Exception as e:
            print(f"[AVISO] Erro lendo {path}: {e}")

    linhas.sort(key=lambda r: key_dt_ddmmyy(r["Date"], r["Time"]))

    print(f"Arquivos: {', '.join(files)}")
    print(f"Mandantes: {sorted(teams)} | Excluídos: {sorted(excludes)} | Stake={stake:.2f}")
    print(f"{'#':>3}  {'Data':10}  {'Hora':5}  {'Mandante':15}  {'Visitante':18}  {'Odd(H)':>7}  {'Placar':7}  {'Res':3}  {'Lucro':>9}  {'Acum':>9}  {'(col)'}")
    print("-" * 120)

    cum = 0.0
    wins = draws = losses = 0
    printed = 0

    for idx, r in enumerate(linhas, 1):
        gm, gv = r["FTHG"], r["FTAG"]
        lucro = profit_home_win(r["OddHome"], stake, gm, gv)
        cum += lucro
        if gm > gv:
            wins += 1; res = "W"
        elif gm == gv:
            draws += 1; res = "D"
        else:
            losses += 1; res = "L"

        if (max_print is None) or (printed < max_print):
            print(f"{idx:>3}  {r['Date']:10}  {r['Time'][:5]:5}  {r['HomeTeam'][:15]:15}  {r['AwayTeam'][:18]:18}  {r['OddHome']:7.2f}  {gm}-{gv:3}   {res:3}  {lucro:9.2f}  {cum:9.2f}  ({r['OddCol']})")
            printed += 1

    total = len(linhas)
    invest = total * stake if total else 0.0
    roi = (cum / invest * 100.0) if invest else 0.0
    wr = (wins / total * 100.0) if total else 0.0

    print("\nResumo:")
    print(f"Jogos: {total} | W: {wins}  D: {draws}  L: {losses}")
    print(f"Lucro líquido: {cum:.2f} | ROI: {roi:.2f}% | Winrate: {wr:.2f}%")

if __name__ == "__main__":
    main()
