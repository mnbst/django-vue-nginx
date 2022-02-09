# docker+django+vue+nginx

## CONCEPT
- こちらはローカルホストだけで使用することを想定しております。
  - モバイル向けのインドネシア語の語学アプリに使うデータベース構築のために作りました。

- 語学アプリについては、インドネシア単語の詳細画面で用例としてyoutube動画が再生される仕様を考えています。
  - そのためにyoutube動画と単語の紐付け作業を自動化する必要がありました。

- ブラウザ上でスクレイピング作業の進度をリアルタイムで可視化できるようにしました。
  - 自動化できない部分に関しては手作業で修正できるようにvue.jsで実装しました。

- 起動にはGoogleのクレデンシャルが必要になります。

## SETUP

```
cd frontend
npm install
```
env/.env.dev
を以下のようにする

```
DEBUG=1
SECRET_KEY=!0$5@7$m5n1-hz+p!vm30#@8cahlm2w4waa=p0o6q8s6=7u-v0
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
DEVELOPER_KEY={グーグルデベロッパーキー}
```
DEVELOPER_KEY → [api key](https://developers.google.com/youtube/v3/getting-started)

### dev 

```
docker-compose -f docker-compose.yml up -d --build
``` 
app/backend/settings.pyでDEBUG_CELERY=Trueとすればceleryタスクをでバックできます。
http://localhost:8000/

#### ユーザー作成

```
docker-compose exec django python manage.py createsuperuser
```
### prod 
```
docker-compose -f docker-compose.prod.yml up -d --build
``` 


http://localhost:1337/ 

![title](画面収録.gif)
