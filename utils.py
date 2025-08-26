# -*- coding: utf-8 -*-
import csv
from typing import Any, Dict, List, Optional, Tuple

def parse_float(x: Any) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None

def choose_home_odd(row: Dict[str, str], headers: List[str], priority: List[str]) -> Tuple[str, Optional[float]]:
    for col in priority:
        if col in headers:
            val = parse_float(row.get(col, ""))
            if val is not None:
                return col, val
    return "", None

def key_dt_ddmmyy(date_str: str, time_str: str) -> Tuple[int, int, int, str]:
    """
    Ordena datas no formato dd/mm/yy; se falhar, joga pro fim.
    Retorna (YYYY, MM, DD, HH:MM).
    """
    t = (time_str or "00:00")[:5]
    try:
        dd, mm, yy = date_str.split("/")
        yy_i = int(yy); yy_i = 2000 + yy_i if yy_i < 100 else yy_i
        return (yy_i, int(mm), int(dd), t)
    except Exception:
        return (9999, 12, 31, t)

def result_from_score(gm: int, gv: int) -> str:
    if gm > gv:
        return "W"
    if gm == gv:
        return "D"
    return "L"

def profit_home_win(odd_home: float, stake: float, gm: int, gv: int) -> float:
    res = result_from_score(gm, gv)
    if res == "W":
        return (odd_home - 1.0) * stake  # ganho líquido
    return -stake  # empate/derrota

def dict_reader_utf8_sig(path: str) -> csv.DictReader:
    return csv.DictReader(open(path, "r", encoding="utf-8-sig", newline=""))
