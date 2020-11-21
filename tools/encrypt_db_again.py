#!/usr/bin/env python2


from pysqlcipher import dbapi2 as sqlite
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--db', help='the path of output_db.db', default='output_db.db')
parser.add_argument('--output', help='the path of output encrypted db file', default='output_encrypted_db.db')
parser.add_argument('--key', help='the key of EnMicroMsg.db', default='0123456')
args = parser.parse_args()


db = args.db
output = args.output
key = args.key
print "key='"+key+"'"

try:
    conn = sqlite.connect(db)
    c = conn.cursor()

    # c.execute("PRAGMA key = '" + '' + "';")
    # c.execute("PRAGMA cipher_use_hmac = OFF;")
    # c.execute("PRAGMA cipher_page_size = 1024;")
    # c.execute("PRAGMA kdf_iter = 4000;")
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")

    c.execute("ATTACH DATABASE '" + output + "' AS db KEY '" + key + "';")

    # https://www.zetetic.net/sqlcipher/sqlcipher-api/#sqlcipher_export
    c.execute("PRAGMA db.cipher_use_hmac = OFF;")
    c.execute("PRAGMA db.cipher_page_size = 1024;")
    c.execute("PRAGMA db.kdf_iter = 4000;")

    c.execute("SELECT sqlcipher_export('db');")
    c.execute("DETACH DATABASE db;")
    print "Decrypt and dump database to {} ... ".format(output)
    print key
    print('OK!!!!!!!!!')
except Exception as e:
    print(str(e))
finally:
    conn.close()
