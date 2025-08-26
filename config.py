# -*- coding: utf-8 -*-

# CSVs padrão (Football-Data)
CSV_FILES = [
    "SP1_2425.csv",
    "SP1_2324.csv",
    "SP1_2223.csv",
    "D1_2425.csv",
    "D1_2324.csv",
    "D1_2223.csv",
]

# Times mandantes para apostar (modo CSV)
TIMES_MANDANTES = {"Real Madrid", "Bayern Munich"}

# Adversários excluídos (clássicos/derbys etc.)
EXCLUIR_ADVERSARIOS = {
    "Barcelona", "Ath Madrid", "Valencia",
    "Real Madrid", "Dortmund", "Leverkusen"
}

# Stake padrão (unidades por aposta)
STAKE = 5.0

# Preferência de colunas de odds (vitória do mandante) nos CSVs
ODDS_HOME_PRIORIDADE = ["B365CH", "B365H", "PSH", "PH", "AvgH", "MaxH"]

# Quantidade padrão a imprimir (None = todos)
MAX_PRINT = None

# ==== SQLite (defaults) ====
SQLITE_DB = "database.sqlite"
SQLITE_TABLE = "betfront"
# Filtros padrão de odds no SQLite (aposta no mandante; visitante só como critério)
HOME_ODD_MAX = 1.5   # <=
AWAY_ODD_MIN = 5.0   # >
SQLITE_MAX_PRINT = 100
