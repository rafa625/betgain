# Bet Analysis Toolkit

Ferramentas em Python para análise de apostas usando datasets do Football-Data (CSV) e bancos SQLite.  
Simula apostas com stake fixa, imprime jogo a jogo e mostra resumo (lucro, ROI, winrate).

---

## Instalação

Clone o repositório:

    git clone https://github.com/rafa625/betgain.git
    cd betgain

**Não requer instalação de pacotes externos** (apenas Python 3.8+).

---

## Estrutura do Repositório

    repo/
    ├─ bet_csv.py          # Apostas em mandantes a partir de CSVs do Football-Data
    ├─ bet_sqlite.py       # Apostas em mandantes filtrando odds a partir de banco SQLite
    ├─ extremos_sqlite.py  # Mostra jogo mais antigo e mais recente no banco SQLite
    ├─ utils.py            # Funções auxiliares (datas, odds, lucro, etc.)
    ├─ config.py           # Configurações padrão (stake, times, arquivos, filtros)
    └─ README.md

Coloque seus arquivos CSV e o banco SQLite na raiz do projeto ou ajuste os caminhos em `config.py`.

---

## 1) Pré-requisitos

- Python 3.8+  
- Somente bibliotecas padrão (não requer pip install)

### Dados de entrada esperados

- **CSV (Football-Data):**  
  - Colunas mínimas:
    - `Date` (dd/mm/yy), `Time`, `HomeTeam`, `AwayTeam`
    - `FTHG` (Full Time Home Goals) ou `HG`, `FTAG` (Full Time Away Goals) ou `AG`
    - Pelo menos uma coluna de odds para vitória do mandante entre: `B365CH`, `B365H`, `PSH`/`PH`, `AvgH`, `MaxH`
- **SQLite:**
  - Banco: `database.sqlite`
  - Tabela: `betfront`
  - Campos: `DATETIME`, `MATCH`, `FTG1` (mandante), `FTG2` (visitante), `HOME_CLOSING`, `DRAW_CLOSING`, `AWAY_CLOSING`

---

## 2) Configuração (config.py)

Parâmetros padrão centralizados:

- `CSV_FILES`: lista de arquivos CSV (ex.: SP1_2425.csv, D1_2324.csv…)
- `TIMES_MANDANTES`: times em casa nos quais apostar (ex.: {"Real Madrid", "Bayern Munich"})
- `EXCLUIR_ADVERSARIOS`: adversários a evitar (clássicos/derbys)
- `STAKE`: stake fixa por aposta (unidades)
- `ODDS_HOME_PRIORIDADE`: ordem de preferência das colunas de odds home (ex.: B365CH → B365H → PSH → PH → AvgH → MaxH)
- `MAX_PRINT`: limite de linhas exibidas (None = todas)

SQLite:
- `SQLITE_DB`, `SQLITE_TABLE`
- `HOME_ODD_MAX` (mandante ≤), `AWAY_ODD_MIN` (visitante >)
- `SQLITE_MAX_PRINT`

Você pode alterar diretamente no `config.py` ou sobrescrever via linha de comando (veja abaixo).

---

## 3) Uso Rápido

### 3.1 CSV → `bet_csv.py`

Executar com configurações do `config.py`:

    python bet_csv.py

Sobrescrever opções na linha de comando:

    python bet_csv.py --files SP1_2425.csv SP1_2324.csv \
      --teams "Real Madrid,Barcelona" \
      --exclude "Ath Madrid,Valencia,Real Madrid" \
      --stake 5 \
      --max 20 \
      --odds-pref "B365CH,B365H,AvgH,MaxH"

O script:
- Lê os CSVs
- Filtra jogos onde `HomeTeam` está em `--teams`
- Ignora jogos se `AwayTeam` está em `--exclude`
- Escolhe automaticamente a primeira coluna de odds válida na prioridade fornecida
- Calcula lucro por jogo: vitórias ganham (odd−1)×stake; empate/derrota perdem stake
- Imprime linha a linha e um resumo (Jogos, W/D/L, Lucro, ROI, Winrate)

### 3.2 SQLite → `bet_sqlite.py`

Executar com defaults do `config.py`:

    python bet_sqlite.py

Sobrescrever opções:

    python bet_sqlite.py --db database.sqlite --table betfront \
      --home-max 1.5 --away-min 8.0 --stake 1 --limit 200

O script:
- Busca jogos com `HOME_CLOSING` ≤ home-max e `AWAY_CLOSING` > away-min
- Simula aposta no mandante (mesma regra de lucro acima)
- Imprime jogo a jogo e resumo

### 3.3 Extremos temporais → `extremos_sqlite.py`

    python extremos_sqlite.py
    python extremos_sqlite.py --db database.sqlite --table betfront

Mostra o jogo mais antigo e o mais recente do banco (data/hora, placar, odds).

#### Exemplo de saída do extremos_sqlite.py

    Mais antigo: 18/08/2024 21:30 | Real Madrid vs Villarreal | Placar: 2-1 | Odds (1-X-2): 1.45, 4.20, 7.00 | DT raw: 2024-08-18 21:30:00
    Mais recente: 25/05/2025 18:00 | Bayern Munich vs Dortmund | Placar: 3-0 | Odds (1-X-2): 1.50, 4.00, 6.50 | DT raw: 2025-05-25 18:00:00

---

## 4) Exemplos de Saída (trechos)

Saída típica de aposta:

    #  Data       Hora  Mandante        Visitante          Odd(H)  Placar  Res     Lucro      Acum  (col)
    ------------------------------------------------------------------------------------------------------
     1  18/08/2024  21:30  Real Madrid     Villarreal          1.45    2-1    W       2.25       2.25  (B365CH)
     2  25/08/2024  20:00  Real Madrid     Valencia            1.60    1-1    D      -5.00      -2.75  (B365H)
    ...
    Resumo:
    Jogos: 34 | W: 26  D: 5  L: 3
    Lucro líquido: 21.50 | ROI: 12.65% | Winrate: 76.47%

---

## 5) Dicas & Troubleshooting

- **CSV com separador/encoding diferente:** os arquivos do Football-Data padrão funcionam direto; se necessário, ajuste a leitura em `utils.dict_reader_utf8_sig`.
- **Colunas de odds ausentes:** a prioridade tenta várias; se nenhuma existir, a linha é ignorada.
- **Datas:** esperadas em dd/mm/yy. Se vier outro formato, adapte `utils.key_dt_ddmmyy`.
- **Consistência de stake:** você pode padronizar alterando no `config.py` ou usando `--stake`.
- **Onde colocar os arquivos:** coloque os CSVs e o banco SQLite na raiz do projeto ou ajuste os caminhos em `config.py`.

---

## 6) Organização e Extensões

- **DRY:** lógica comum (data/odd/lucro) está em `utils.py`.
- **Ajuste fino de filtros via CLI**, sem editar código.
- **Extensões possíveis:**
  - Novos filtros (ex.: por temporada, por janelas de datas)
  - Outras métricas (EV teórico, Kelly, distribuição por linhas de handicap)
  - Relatórios em CSV/Markdown (atualmente só imprime na tela)

---

## 7) Contato & Contribuição

Sugestões, dúvidas ou interesse em contribuir? Abra uma issue ou envie um pull request!

---

## 8) Licença

Uso livre para análise pessoal/educacional. Respeite os termos dos datasets (Football-Data) e de quaisquer fontes de dados utilizadas.

