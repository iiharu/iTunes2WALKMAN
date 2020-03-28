# iTunes2WALKMAN
Copy iTunes music file and playlists

## 環境
- macOS Catalina (ver 10.15.3)
- Python 2.7.7

## 使い方
`Music.app`を開く.
メニューから, `ファイル` -> `ライブラリ` -> `ライブラリを書き出し...`を選択し, `ライブラリ.xml`を適当な場所に保存する.

次のように実行する.
WALKMANは`/Volumes/WALKMAN`にマウントされているものとする.
```
itunes2walkman.py path/to/xml
```

## TODO
- Python 3 対応
  デフォルトで入ってないと思ってた
