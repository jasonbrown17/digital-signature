#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''All the fame and glory goes to...'''
__author__ = 'Jason Brown'
__email__  = 'jason@jasonbrown.us'
__date__   = '20201013'

'''Import those modules!'''
from OpenSSL import crypto
from os import system
import json, base64

def main():

    privkey_file = open('privatekey.pem', 'r')
    privkey = privkey_file.read()
    privkey_file.close()
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, privkey)

    '''And this is where the magic happens'''
    '''Grab the file and sign it'''
    hashed = open('', 'rb').read()
    signed = crypto.sign(pkey, hashed, 'sha256')
    signedb64 = base64.encodebytes(signed).decode()

    signature = open('', 'w')
    signature.write(signedb64)
    signature.close()

if __name__ == '__main__':
    main()
