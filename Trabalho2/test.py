import subprocess
import os

cwd = os.getcwd()

cmd = [
    "wt", "-w", "0", "-M",

    # Pane 1 (inicial)
    "cmd", "/k", f'cd /d "{cwd}" && title processo1 && python processoFile.py processo1 9091',

    ";",
    # Divide horizontal → cria pane 2 (direita)
    "split-pane", "-H", "cmd", "/k", f'cd /d "{cwd}" && title processo2 && python processoFile.py processo2 9092',

    ";",
    # Volta para pane 1 (esquerda)
    "move-focus", "left",

    ";",
    # Divide vertical → cria pane 3 (baixo esquerdo)
    "split-pane", "-V", "cmd", "/k", f'cd /d "{cwd}" && title processo3 && python processoFile.py processo3 9093',

    ";",
    # Vai para pane 2 (direita superior)
    "move-focus", "up",
    ";",
    "move-focus", "right",

    ";",
    # Divide vertical → cria pane 4 (baixo direito)
    "split-pane", "-V", "cmd", "/k", f'cd /d "{cwd}" && title processo4 && python processoFile.py processo4 9094',
]

subprocess.Popen(cmd)