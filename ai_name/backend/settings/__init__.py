from datetime import timedelta

DB_URI = "mysql+aiomysql://root:123456@127.0.0.1:3306/ai_name?charset=utf8mb4"

MAIL_USERNAME="2369980279@qq.com"
MAIL_PASSWORD="vlqghaxzqccbeagc"
MAIL_FROM="2369980279@qq.com"
MAIL_PORT=587
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="ai_name"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False

JWT_SECRET_KEY="asfdshbdt342"
JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=72)
JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=7)