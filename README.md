# Botnyan
Hello, I'm botnyan. Outgoing-webhook slackbot collaborates with Google Drive documents :cat:

## What's botnyan

This is [Outgoing-webhook slackbot](https://api.slack.com/outgoing-webhooks) collaborates with [Google Drive](http://drive.google.com) documents :cat:


Here is one of working screenshot:
![Slack screenshot](https://raw.githubusercontent.com/wiki/supistar/botnyan/screenshots/slack.png)

- botnyan has pairs of keyword and Google Drive document ID.
- If user says some keyword (in this case, I just said "パチン"), botnyan retrieves document contents from Google Drive corresponding to the keyword, then replies it :)
- botnyan will repond only if **message fully match the keyword**, because we do not want the unnecessary reation to some messages.

## How to install

You can install this on [heroku](https://www.heroku.com/home) instance.

### Install on heroku

#### Preparation

First, please install these packages.
- Git
- [Heroku toolbelt](https://toolbelt.heroku.com/)
- OpenSSL

#### Install steps

1. Create new application on your [heroku dashboard](https://dashboard.heroku.com/apps).

2. Clone this code on your machine.
  
  ```bash
  git clone git@github.com:supistar/Botnyan.git
  ```

3. Configure document settings
  
  - You can configure pairs of keyword and Google Drive document ID. For details, please see `settings.py` on project root directory.
    They has `Keyword` and `DocumentID` elements.
    - Keyword : Specify keyword to respond. You can specify keyword(s) by string or list.
    - DocumentID : Specify document ID of Google Drive. ID is placed on `https://docs.google.com/document/d/{DocumentID}`. 
  
4. Commit the changes of `settings.py`
  
  - This changes are used by heroku deployment, no need to push it on GitHub :)
  
  ```bash
  git add -u .
  git commit -m "Customize settings.py"
  ```

5. Add heroku configuration to current project
  
  ```bash
  heroku git:remote -a ${HerokuAppName}`
  ```

6. Deploy your application
  
  ```bash
  git push heroku master
  ```

7. Create a Google Service Account
  
  - Visit the Google Developer Console
  - Create new project or select existing your project.
  - Click `APIs & Auth` ->  `Credentials`
  - Click `Create new Client ID`
  - Create a `Service account` with `P12 Key` key type.
  - Retrieve p12 file after account creation.
  - Check your service account's `EMAIL ADDRESS` (This value will be used in subsequent step)
  
8. Incorporate Service account private key
  
  ```bash
  cd path/to/p12directory
  openssl pkcs12 -passin pass:notasecret -in privatekey.p12 -nocerts -passout pass:notasecret -out key.pem
  openssl pkcs8 -nocrypt -in key.pem -passin pass:notasecret -topk8 -out google-services-private-key.pem
  rm key.pem
  ```
  
9. Configure `Config Variables`
  
  ```bash
  heroku config:add SLACK_WEBHOOK_TOKEN=ExampleOfTokenValue
  heroku config:add GOOGLE_OWNER_EMAIL=*****@gmail.com
  heroku config:add GOOGLE_CLIENT_EMAIL=******************@developer.gserviceaccount.com
  heroku config:add GOOGLE_PRIVATE_KEY=`cat path/to/p12directory/google-services-private-key.pem`
  heroku config:add BOTNYAN_BASE_URL=https://mybotnyan.herokuapp.com
  ```
  
10. Run your botnyan
  
  ```bash
  heroku ps:scale web=1
  ```

### Configure Outgoing-webhooks on Slack

1. Open Outgoing WebHooks (https://yourteam.slack.com/services/new/outgoing-webhook)
2. Click `Add Outgoing WebHooks Integration`
3. Configure Integration settings
  - Trigger Word(s): Specify some keywords defined in your `settings.py`
  - URL(s): Specify `https://mybotnyan.herokuapp.com/api/slack/webhook`

## Limitations

- botnyan will respond to the public channel messages, not private channel.
  This limitation come from slack specification.

