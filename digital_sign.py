#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''All the fame and glory goes to...'''
__author__ = 'Jason Brown'
__email__  = 'jason.brown@aptiv.com'
__date__   = '20201012'

'''Import those modules!'''
from OpenSSL import crypto
from botocore.exceptions import ClientError
from os import system
import boto3, json, base64

def main():

    '''Connection to AWS Secrets Manager'''
    secret_name = 'prod/causer_ca/n3fips'
    region_name = 'us-east-2'

    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])

    '''Retrieve username:password from Secrets Manager and export it per CloudHSM requirements'''
    system('export n3fips_password=' + secret['username'] + ':' +secret['password'])

    privkey_file = open('privatekey.pem', 'r')
    privkey = privkey_file.read()
    privkey_file.close()
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, privkey)

    '''And this is where the magic happens'''
    '''Grab the file and sign it'''
    hashed = open('winners.csv', 'rb').read()
    signed = crypto.sign(pkey, hashed, 'sha256')
    signedb64 = base64.encodebytes(signed).decode()

    signature = open('signature.sig', 'w')
    signature.write(signedb64)
    signature.close()

if __name__ == '__main__':
    main()
