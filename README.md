# ninpost
CSVから葉書印刷できるやつ。
vimキーバインドの年賀状の宛名印刷ソフト。CSVとかJSONとかから宛名を作って、そこから宛名を印刷するhtmlファイルを作ります。

# 依存
python依存。

# インストール

```sh
pip install git+https://github.com/uesseru/ninpost
```

# 使い方
まず、起動します。
```bash
ninpost
```

すると、下記の二つのファイルが作られます。

- address.csv
- config.toml

このaddress.csvに色々書きこみます。手紙の内容も書けます。
config.tomlの内容も、まぁ、設定です。適当に書き替えてください。あとは適当に

```bash
ninpost address.csv
```

で、output.htmlというのが出力されます。これを開くと葉書がブラウザで表示されます。
これ、キーボードの右左矢印やhlで中の宛名を切り替えられます。

さらに、複数の住所録のCSVを作ったら複数読ませられます。

```bash
ninpost address.csv address2.csv
```

これ、キーボードの上下矢印やjkで中の宛名を切り替えられます。

pを押したら印刷、iを押したら手紙の内容ですね。
手紙の内容の方はhtml形式で書けます。

```bash
ninpost address.csv
```
# オプション
- -c/--config    default='config.toml'
  + 設定ファイルの場所
- -g/--gui    action='store_true'
  + GUIで起動する。
- -b/--browser    action='store_true'
  + ブラウザを起動する。もし-oが"-"なら無効になる。
- -o/--output    default='out.html'
  + 出力するファイル名。もし"-"なら標準出力に出力する。-bが有効ならそれを無効にする。
- -i/--input
  + 標準入力を使う場合。
