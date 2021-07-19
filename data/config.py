import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
DATABASE = str(os.getenv("DATABASE"))
admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")

POSTGRES_URL = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'

I18N_DOMAIN = 'exodus'
LOCALES_DIR = 'locales'


DEBUG = True


"""
WEBHOOK

Quick'n'dirty SSL certificate generation:

openssl genrsa -out webhook_pkey.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem

When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
with the same value in you put in WEBHOOK_HOST

"""
WEBHOOK_HOST = '127.0.0.1'  # '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_URL_PATH = '/.ssl'  # Part of URL

# This options needed if you use self-signed SSL certificate
# Instructions: https://core.telegram.org/bots/self-signed
WEBHOOK_SSL_CERT = './.ssl/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './.ssl/webhook_pkey.pem'  # Path to the ssl private key


WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"