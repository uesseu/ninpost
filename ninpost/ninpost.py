import sys
from typing import Optional, Tuple
from .csv_to_json import SpreadSheet
from .json_to_html import generate_html
from pathlib import Path
import json
import tomllib
from argparse import ArgumentParser
from subprocess import run
import tkinter as tk
import tkinter.filedialog as filedialog
from subprocess import run

parser = ArgumentParser(
    prog='ninpost',
    description='vimキーバインドの年賀状の宛名印刷ソフト。CSVとかJSONとかから宛名を作って、そこから宛名を印刷するhtmlファイルを作ります。'
)

parser.add_argument('address', nargs='*')
parser.add_argument(
    '-c', '--config', default='config.toml',
    help='設定ファイルの場所'
)
parser.add_argument(
    '-g', '--gui', action='store_true',
    help='GUIで起動する。'
)
parser.add_argument(
    '-b', '--browser', action='store_true',
    help='ブラウザを起動する。もし-oが"-"なら無効になる。'
)
parser.add_argument(
    '-o', '--output',
    help='出力するファイル名。もし"-"なら標準出力に出力する。-bが有効ならそれを無効にする。',
    default='out.html'
)
parser.add_argument(
    '-i', '--input', action='store_true',
    help='標準入力を使う場合。',
)
args = parser.parse_args()


if not args.address:
    parser.print_help()


def init():
    path = Path('.')
    with open(path / 'config.toml', 'w') as fp:
        fp.write('''browser = 'firefox'
address = '○○市○○1丁目0-0'
myPost = '0000000'
myName = '葉書 太郎'
''')
    with open(path / 'address.csv', 'w') as fp:
        fp.write('''"post","address","familyName","name","title","name","title","name","title","relation","content","prompt","enable"
"0090233","都道府県","名字","名前","様","連名","様","連名","君","間柄","手紙の内容","プロンプト","1"''')

if (not Path('address.csv').exists()) and (not Path('config.toml').exists()):
    init()

with open(args.config, 'rb') as fp:
    config = tomllib.load(fp)

def browse_file(
    title: str = "Select a file",
    initialdir: Optional[str] = None,
    filetypes: Optional[Tuple[Tuple[str, str], ...]] = None,
    parent: Optional[object] = None
) -> str:
    created_root = False
    if parent is None:
        root = tk.Tk()
        root.withdraw()
        parent = root
        created_root = True

    if filetypes is None:
        filetypes = (("All Files", "*.*"),)

    path = filedialog.askopenfilename(
        parent=parent,
        title=title,
        initialdir=initialdir,
        filetypes=filetypes
    )

    if created_root:
        try:
            parent.destroy()
        except Exception:
            pass
    return path

def make_html(path) -> str:
    spreadsheet = [SpreadSheet(p).as_dict() for p in path]
    return generate_html(spreadsheet, config)

class App:
    def __init__(self, master: 'tk.Tk'):
        self.master = master
        master.title("NinPost")
        self.label = tk.Label(master, text="住所録を開いてください")
        self.label.pack(padx=10, pady=10)
        self.button = tk.Button(master, text="住所録を開く", command=self.browse)
        self.button.pack(padx=10, pady=10)
        self.path: str = ""

    def browse(self):
        path = browse_file(
            parent=self.master, title="住所録を開く",
            filetypes=(("csv", "*.csv"),)
        )
        if path:
            self.label.config(text=f"はがきをつくるよ！")
        else:
            self.label.config(text="No file selected")
        make_html(path)


def main():
    if args.address:
        result = make_html(args.address)
        if args.output.strip() == '-':
            print(result)
        else:
            Path(args.output).write_text(result)
            if args.browser:
                run([config['browser'], args.output])
    elif args.gui:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
