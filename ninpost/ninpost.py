import sys
import tkinter as tk
import tkinter.filedialog as filedialog
from typing import Optional, Tuple
from .csv_to_json import SpreadSheet
from .json_to_html import generate_html
from .css import css
from pathlib import Path
import json
import tomllib
from argparse import ArgumentParser
from subprocess import run
parser = ArgumentParser()
parser.add_argument('address', nargs='?')
parser.add_argument('-c', '--config', default='config.toml')
parser.add_argument('-k', '--apikey', default='')
args = parser.parse_args()

def init():
    path = Path('.')
    with open(path / 'config.toml', 'w') as fp:
        fp.write('''dirname = 'output'
browser = 'firefox'
address = '○○市○○1丁目0-0'
myPost = '0000000'
myName = '葉書 太郎'
apikey = ''
''')
    with open(path / 'address.csv', 'w') as fp:
        fp.write('''"post","address","familyName","name","title","name","title","name","title","relation","content","prompt","enable"
"0090233","都道府県","名字","名前","様","連名","様","連名","君","間柄","手紙の内容","プロンプト","1"''')

if (not Path('address.csv').exists()) and (not Path('config.toml').exists()):
    init()

with open(args.config, 'rb') as fp:
    config = tomllib.load(fp)
apikey = args.apikey if args.apikey else config['apikey']

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

def make_html(path, key=''):
    spreadsheet = SpreadSheet(path).as_dict()
    num = len([j for j in spreadsheet if j["enable"]=='1'])
    res = [generate_html(j, config, num, key=key) for j in spreadsheet if j["enable"]=='1']
    dirpath = Path(config['dirname'])
    for num, html in enumerate(res):
        (dirpath / f'{num}.html').write_text(html)
    (dirpath / 'main.css').write_text(css)
    dirpath = Path(config['dirname'])
    run([config['browser'], dirpath / '0.html'])

class App:
    def __init__(self, master: tk.Tk):
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
        make_html(path, key=apikey)


def main():
    dirpath = Path(config['dirname'])
    if dirpath.exists():
        for p in dirpath.glob('*'):
            p.unlink()
        dirpath.rmdir()
    dirpath.mkdir()
    if args.address:
        make_html(args.address, key=apikey)
    else:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
