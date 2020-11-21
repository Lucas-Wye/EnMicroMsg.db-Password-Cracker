#!/usr/bin/env python2

from pysqlcipher import dbapi2 as sqlite
import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('--db', help='the path of EnMicroMsg.db', default='EnMicroMsg.db')
parser.add_argument('--output', help='the path of output db file', default='output_db.db')
parser.add_argument('--imei', help='imei', default='100003000945586')
parser.add_argument('--uin', help='uin', default='1234567890')
parser.add_argument('--key', help='key')
args = parser.parse_args()

def get_key():
    IMEI=args.imei
    uin=args.uin
    key = hashlib.md5((IMEI+uin).encode()).hexdigest()[:7]
    return key

key = args.key if args.key else get_key()
print('pass: ', key)

db = args.db
output = args.output
try:
    conn = sqlite.connect(db)
    c = conn.cursor()

    c.execute("PRAGMA key = '" + key + "';")
    c.execute("PRAGMA cipher_use_hmac = OFF;")
    c.execute("PRAGMA cipher_page_size = 1024;")
    c.execute("PRAGMA kdf_iter = 4000;")
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")

    c.execute("ATTACH DATABASE '" + output + "' AS db KEY '';")
    c.execute("SELECT sqlcipher_export('db');")
    c.execute("DETACH DATABASE db;")
    print "Decrypt and dump database to {} ... ".format(output)
    print key
    print('OK!!!!!!!!!')
except Exception as e:
    print(str(e))
finally:
    conn.close()
