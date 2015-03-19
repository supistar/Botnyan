# Botnyan
Google Drive のドキュメントと連携する Outgoing-webhook ベースの slackbot、ボットニャンです :cat:

## What's botnyan

[Google Drive](http://drive.google.com) のドキュメントと連携する [Outgoing-webhook slackbot](https://api.slack.com/outgoing-webhooks) です :cat:

- 動作しているところのスクリーンショット
![Slack screenshot](https://raw.githubusercontent.com/wiki/supistar/botnyan/screenshots/slack.png)

- キーワードと Google Drive のドキュメント ID のペアをボットニャンに登録しておきます。
- Slack のチャットルームで設定したキーワードを発言すると（この場合は "バチン" と発言しています）、ボットニャンはそのキーワードに紐付いた Google Drive のドキュメント ID を元に、ドキュメントの内容を取得し発言します :)
- なお、ボットニャンは登録されたキーワードに **完全一致** した場合のみ反応します。

## インストール方法

ボットニャンは [heroku](https://www.heroku.com/home) のインスタンス上で動くようにできています。

### Heroku へのインストール

#### 前準備

インストールには下記のアプリケーションが必要になります。
- Git
- [Heroku toolbelt](https://toolbelt.heroku.com/)
- OpenSSL

#### インストール手順

1. 新しい Heroku アプリケーションの作成
  
  新しいアプリケーションを [heroku dashboard](https://dashboard.heroku.com/apps) から作成します。
  
2. ボットニャンのコードを取得
　
　下記のコマンドをターミナルに入力し、ボットニャンののコードを取得します。
  
  ```bash
  git clone git@github.com:supistar/Botnyan.git
  ```
  
3. キーワード・ドキュメント ID の設定
  
  取得したコード中の `settings.py` を編集し、キーワード・ドキュメント ID の設定を行います。
  
  - キーワードと Google Drive のドキュメント ID のペアを設定します。具体的な例はルートディレクトリにある `settings.py` ファイルを参照してください。
    ファイル中には `Keyword` と `DocumentID` の要素を設定します。
    - Keyword : 反応させたいキーワードを指定します。単一の文字列、もしくは文字列のリストが設定できます。
    - DocumentID : Google Drive のドキュメント ID を指定します。ID は ドキュメントを開いている際の URL 中 `https://docs.google.com/document/d/{DocumentID}` に含まれています。
  
4. キーワード・ドキュメント ID の変更を反映
  
  `settings.py` に加えた変更をコミットし反映させます。
  
  - この変更は Heroku へデプロイする際に必要です。GitHub へ Push する必要はありません :)
  
  ```bash
  git add -u .
  git commit -m "settings.py のカスタマイズ！"
  ```
  
5. Heroku のリポジトリ登録
  
  Heroku へデプロイするため、リポジトリの情報を登録します。
  
  ```bash
  heroku git:remote -a ${HerokuAppName}`
  ```
  
6. Heroku へデプロイ
  
  アプリケーションを Heroku へデプロイします。
  
  ```bash
  git push heroku master
  ```
  
7. Google のサービスアカウント作成
  
  次に、Google のサービスアカウントを作成します。
  このサービスアカウントは、ボットニャンから Google Drive へアクセスする際に必要なアカウントです。
  
  - Google Developer Console へアクセスします
  - 新規にプロジェクトを作成、もしくは既存のプロジェクトを選択します
  - `APIs & Auth` ->  `Credentials` を選択します
  - 次に `Create new Client ID` を選択します
  - `Service account` を選択し、アカウントを作成します。この際、キーのタイプに `P12 Key` を選択してください。
  - アカウントが作成された後、アクセスに必要な .p12 ファイルがダウンロードされます。
  - アカウント作成後、サービスアカウントの `EMAIL ADDRESS` を確認しておきます（この値は後ほど利用します）
  
8. サービスアカウント用の秘密鍵作成
  
  ターミナルへ下記を入力し、サービスアカウントで利用する秘密鍵を作成します。
  `path/to/p12directory`・`privatekey.p12` は環境にあわせて変更してください。
  
  ```bash
  cd path/to/p12directory
  openssl pkcs12 -passin pass:notasecret -in privatekey.p12 -nocerts -passout pass:notasecret -out key.pem
  openssl pkcs8 -nocrypt -in key.pem -passin pass:notasecret -topk8 -out google-services-private-key.pem
  rm key.pem
  ```
  
9. `Config Variables` の設定
  
  次にターミナルから `Config Variables` を設定します。
  これらの値は Heroku のダッシュボードからも入力できます。
  
  ```bash
  heroku config:add SLACK_WEBHOOK_TOKEN=ExampleOfTokenValue
  heroku config:add GOOGLE_OWNER_EMAIL=*****@gmail.com
  heroku config:add GOOGLE_CLIENT_EMAIL=******************@developer.gserviceaccount.com
  heroku config:add GOOGLE_PRIVATE_KEY=`cat path/to/p12directory/google-services-private-key.pem`
  heroku config:add BOTNYAN_BASE_URL=https://mybotnyan.herokuapp.com
  ```
  
10. ボットニャンの起動
  
  下記のコマンドをターミナルに入力し、ボットニャンを起動します
  
  ```bash
  heroku ps:scale web=1
  ```

### Slack 側の設定（Outgoing-webhooks）

1. Slack の Outgoing WebHooks (https://yourteam.slack.com/services/new/outgoing-webhook) 設定ページを開きます
2. `Add Outgoing WebHooks Integration` を選択します
3. Outgoing-webhooks インテグレーションの設定をします
  - Trigger Word(s): ボットニャンの `settings.py` で設定したキーワード全てを入力します。各キーワードは "," で区切ってください。
  - URL(s): `https://mybotnyan.herokuapp.com/api/slack/webhook` を指定します。mybotnyan のところは環境にあわせて変更してください。

## 制限事項

- ボットニャンはパブリックチャンネルに送信されたメッセージ（キーワード）のみに反応します。Slack 側の制限によりプライベートチャンネルでは動作しません。

