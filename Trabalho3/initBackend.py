import subprocess
import os

cwd = os.getcwd()
backend = os.path.join(cwd, "Backend")

cmd = [
    "wt", "-w", "0", "-M",

    # Pane 1 (top-left): Promocao
    "cmd", "/k", f'cd /d "{backend}" && title Promocao && python -m Promocao.Promocao',

    ";",
    # Split horizontal → Pane 2 (top-right): Ranking
    "split-pane", "-H", "cmd", "/k", f'cd /d "{backend}" && title Ranking && python -m Ranking.Ranking',

    ";",
    # Move focus back to pane 1 (left)
    "move-focus", "left",

    ";",
    # Split vertical → Pane 3 (bottom-left): Notificacao
    "split-pane", "-V", "cmd", "/k", f'cd /d "{backend}" && title Notificacao && python -m Notificacao.Notificacao',

    ";",
    # Move to pane 2 (top-right)
    "move-focus", "up",
    ";",
    "move-focus", "right",

    ";",
    # Split vertical → Pane 4 (bottom-right): Getway
    "split-pane", "-V", "cmd", "/k", f'cd /d "{backend}" && title Getway && python -m Getway.Getway',
]

subprocess.Popen(cmd)
