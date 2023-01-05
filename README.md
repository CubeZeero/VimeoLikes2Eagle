# VimeoLikes2Eagle

Tool to send all Vimeo likes to [Eagle](https://eagle.cool) library!

Vimeoでライクした動画をすべて[Eagle](https://eagle.cool)へ追加するツールです

## How to use

1. exeを起動
2. Vimeoアカウントを連携させます
3. 自動でLikesがEagleへ保存されます

## Build

1. `pip install -r requirements.txt` で必須ライブラリをインストール
2. VimeoのDeveloperページから `Client ID` と `Client Secret` を取得
3. 取得したキーを `apikey_sample.py` へ登録
4. `apikey_sample.py` を `apikey.py` へリネーム
5. `version_sample` にバージョン記述
6. `version_sample.py` を `version.py` へリネーム
7. `vimeolikes_2_eagle.py` を実行し動作確認
8. `dist` フォルダを作成
9. `build.py` を実行

