# -*- coding: utf-8 -*-
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

baseurl = "https://127.0.0.1"

keys = [
    {"type": "RSA", "key": "keys/pyoidc_enc", "use": ["enc"]},
    {"type": "RSA", "key": "keys/pyoidc_sig", "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["enc"]}
]

multi_keys = [
    {"type": "RSA", "use": ["enc"], "name": "rsa_enc_1", "key": "keys/pyoidc_enc"},
    {"type": "RSA", "use": ["sig"], "name": "rsa_sig_1", "key": "keys/pyoidc_sig"},
    {"type": "RSA", "use": ["enc"], "name": "rsa_enc_2", "key": "keys/sec_enc"},
    {"type": "RSA", "use": ["sig"], "name": "rsa_sig_2", "key": "keys/sec_sig"},
    {"type": "EC", "crv": "P-256", "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["enc"]},
    {"type": "EC", "crv": "P-256", "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["enc"]}
]

KEYDEFS = [
    {"type": "RSA", "key": '', "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["sig"]}
]

FOS = ['swamid.se', 'surfnet.nl', 'aai.grnet.gr', 'heanet.ie']

GRPS = [
    "Discovery", "Dynamic Client Registration",
    "Response Type and Response Mode", "claims Request Parameter",
    "request_uri Request Parameter", "scope Request Parameter",
    "nonce Request Parameter", "Client Authentication",
    "ID Token", "Key Rotation", "Claims Types", "UserInfo Endpoint",
    "3rd-Party Init SSO",
    "RP Initiated BackChannel Logout", "RP Initiated FrontChannel Logout"
]

# Only Username and password.
AUTHENTICATION = {
    # "UserPassword": {"ACR": "PASSWORD", "WEIGHT": 1, "URL": SERVICE_URL}
    "NoAuthn": {"ACR": "PASSWORD", "WEIGHT": 1, "user": "diana"}
}

COOKIE = {
    #    'domain': '192.168.1.109'
    'name': 'pyoic',
    'ttl': 4 * 60  # 4 hours
}

SSO_TTL = 2*60

SYM_KEY = "SoLittleTime,Got"

SERVER_CERT = "certs/server.crt"
SERVER_KEY = "certs/server.key"
# CA_BUNDLE="certs/chain.pem"
CA_BUNDLE = None

CLIENT_DB = "clients"

# This is where a user should be involved but we skip that and go directly
# to logout
LOGOUT_PATH = 'logout'

CHECK_SESSION_IFRAME = "{}:{{}}/<PATH>/check_session_iframe".format(baseurl)

# =======  SIMPLE DATABASE ==============

USERINFO = "SIMPLE"

USERDB = {
    "diana": {
        "sub": "dikr0001",
        "name": "Diana Krall",
        "given_name": "Diana",
        "family_name": "Krall",
        "nickname": "Dina",
        "email": "diana@example.org",
        "email_verified": False,
        "phone_number": "+46 90 7865000",
        "address": {
            "street_address": "Umeå Universitet",
            "locality": "Umeå",
            "postal_code": "SE-90187",
            "country": "Sweden"
        },
    },
    "babs": {
        "sub": "babs0001",
        "name": "Barbara J Jensen",
        "given_name": "Barbara",
        "family_name": "Jensen",
        "nickname": "babs",
        "email": "babs@example.com",
        "email_verified": True,
        "address": {
            "street_address": "100 Universal City Plaza",
            "locality": "Hollywood",
            "region": "CA",
            "postal_code": "91608",
            "country": "USA",
        },
    },
    "upper": {
        "sub": "uppe0001",
        "name": "Upper Crust",
        "given_name": "Upper",
        "family_name": "Crust",
        "email": "uc@example.com",
        "email_verified": True,
    }
}
