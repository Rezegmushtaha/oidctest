from func import set_discovery_issuer
from func import set_webfinger_resource
from jwkest import BadSignature
from oic.exception import IssuerMismatch
from oic.exception import PyoidcError

from otest.func import set_op_args
from otest.func import set_request_args

from oidctest.op.oper import AccessToken
from oidctest.op.oper import Discovery
from oidctest.op.oper import Registration
from oidctest.op.oper import SubjectMismatch
from oidctest.op.oper import SyncAuthn
from oidctest.op.oper import UpdateProviderKeys
from oidctest.op.oper import UserInfo
from oidctest.op.oper import Webfinger
from oidctest.testfunc import expect_exception
from oidctest.testfunc import resource
from oidctest.testfunc import set_jwks_uri

__author__ = 'roland'

ORDDESC = ["rp-discovery", "rp-registration",
           "rp-response_type", "rp-response_mode",
           "rp-token_endpoint", "rp-id_token",
           "rp-userinfo", "rp-claims", "rp-claims-request",
           "rp-request_uri", "rp-scope", "rp-nonce", "rp-key-rotation"]

FLOWS = {
    "rp-discovery-webfinger-url": {
        "sequence": [(Webfinger, {set_webfinger_resource: {}})],
        "desc": "Can Discover Identifiers using URL Syntax",
        "profile": ".T..",
    },
    "rp-discovery-webfinger-acct": {
        "sequence": [(Webfinger, {resource: {"pattern": "acct:{}@{}"},
                                  set_webfinger_resource: {}})],
        "desc": "Can Discover Identifiers using acct Syntax",
        "profile": ".T..",
    },
    "rp-discovery-openid-configuration": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}})
        ],
        "profile": "..T.",
        "desc": "Uses openid-configuration Discovery Information"
    },
    # "rp-discovery-issuer-not-matching-config": {
    #     "sequence": [
    #         (Webfinger, {set_webfinger_resource: {}}),
    #         (Discovery, {expect_exception: IssuerMismatch})
    #     ],
    #     "profile": "..T.",
    #     "desc": "Retrieve openid-configuration information for OpenID
    # Provider from the .well-known/openid-configuration path. Verify that
    # the issuer in the openid-configuration matches the one returned by
    # WebFinger"
    # },
    "rp-discovery-jwks_uri-keys": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}})
        ],
        "profile": "..T.",
        "desc": "Can read and understand jwks_uri",
        "tests": {
            "providerinfo-has-jwks_uri": {},
            "bare-keys": {}
        }
    },
    "rp-discovery-issuer-not-matching-config": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {},
                         expect_exception: IssuerMismatch})
        ],
        "profile": "..T.",
        "desc": "Will detect a faulty issuer claim in OP config"
    },
    "rp-registration-dynamic": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration
        ],
        "profile": "...T",
        "desc": "Uses Dynamic Registration"
    },
    "rp-registration-redirect_uris": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {set_request_args: {"redirect_uris": [""]},
                            expect_exception: PyoidcError}),
            Registration
        ],
        "profile": "...T",
        "desc": "Sends redirect_uris value which only contains a empty string "
                "while doing a registration request. Then send a valid "
                "redirect_uris list"
    },
    "rp-registration-uses-https-endpoints": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration,
             {set_request_args: {"redirect_uris": ["http://test.com"]},
              expect_exception: PyoidcError}),
        ],
        "profile": "I,IT,CI,CT,CIT...T",
        "desc": "Sends a redirect_uri endpoint which does not use https. The "
                "a valid redirect_uri is sent to the OP"
    },
    "rp-registration-well-formed-jwk": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {set_request_args: {"jwks": {
                "keys": [{
                    "use": "sig",
                    "n":
                        "tAAzYdbiWDAKI8Q3s1crQRuVp0QXpyGgnzx_sGItC2rhdug68gE9v5mfK-7SJCBpuZXzX1YevJ25B0LhNQSWqvb6gYwlNHs33G8VmSzjpqFazItnhKMPnEehCXmPl7iFi8VV0NCC5_uH9xP61TClWsE8B7i4CV6y9B0hZI22p2M",
                    "e": "AQAB",
                    "kty": "RSA",
                    "kid": "a1"
                }]},
                "id_token_signed_response_alg": "RS256",}}),
            (SyncAuthn, {set_op_args: {"response_type": ["id_token"]}}),
        ],
        "profile": "...T",
        "desc": ""
    },
    "rp-response_type-code": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn
        ],
        "profile": "C...",
        "desc": "Can Make Request with 'code' Response Type"
    },
    "rp-response_type-id_token": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration,
             {set_request_args: {"id_token_signed_response_alg": "RS256"}}),
            SyncAuthn
        ],
        "desc": "Can Make Request with 'id_token' Response Type",
        "profile": "I...",
    },
    "rp-response_type-id_token+token": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration,
             {set_request_args: {"id_token_signed_response_alg": "RS256"}}),
            SyncAuthn
        ],
        "profile": "IT...",
        "desc": "Can Make Request with 'id_token token' Response Type"
    },
    "rp-response_mode-form_post": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration,
             {set_request_args: {"id_token_signed_response_alg": "RS256"}}),
            (SyncAuthn, {set_request_args: {"response_mode": ["form_post"]}})
        ],
        "profile": "I,IT,CI,CT,CIT,...",
        "desc": "Can Make Request with response_mode=form_post"
    },
    "rp-authentication-client_secret_basic": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn,
            (AccessToken,
             {set_op_args: {"authn_method": "client_secret_basic"}})
        ],
        "profile": "C,CI,CIT...",
        "desc": "Can Make Access Token Request with 'client_secret_basic' "
                "Authentication"
    },
    "rp-authentication-client_secret_post": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration,
             {set_request_args: {
                 "token_endpoint_auth_method": "client_secret_post"}}),
            SyncAuthn,
            (AccessToken,
             {set_op_args: {"authn_method": "client_secret_post"}})
        ],
        "profile": "C,CI,CIT...",
        "desc": "Can Make Access Token Request with 'client_secret_post' "
                "Authentication"
    },
    "rp-authentication-client_secret_jwt": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration,
             {set_request_args: {
                 "token_endpoint_auth_method": "client_secret_jwt"}}),
            SyncAuthn,
            (AccessToken,
             {set_op_args: {"authn_method": "client_secret_jwt"}})
        ],
        "profile": "C,CI,CIT...",
        "desc": "Can Make Access Token Request with 'client_secret_jwt' "
                "Authentication"
    },
    "rp-authentication-private_key_jwt": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "token_endpoint_auth_method": "private_key_jwt"},
                set_jwks_uri: None
            }),
            SyncAuthn,
            (AccessToken,
             {set_request_args: {"authn_method": "private_key_jwt"}})
        ],
        "profile": "C,CI,CIT...",
        "desc": "Can Make Access Token Request with 'private_key_jwt' "
                "Authentication"
    },
    "rp-id_token-sig-rs256": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "id_token_signed_response_alg": "RS256"
                }
            }),
            (SyncAuthn, {set_op_args: {"response_type": ["id_token"]}}),
        ],
        "profile": "I...T",
        "desc": "Accept Valid Asymmetric ID Token Signature"
    },
    "rp-id_token-sig-hs256": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "id_token_signed_response_alg": "HS256"
                }
            }),
            (SyncAuthn, {set_op_args: {"response_type": ["id_token"]}})
        ],
        "profile": "I...T",
        "desc": "Accept Valid Symmetric ID Token Signature"
    },
    "rp-id_token-bad-sig-rs256": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "id_token_signed_response_alg": "RS256"
                }
            }),
            (SyncAuthn, {
                set_op_args: {"response_type": ["id_token"]},
                expect_exception: BadSignature
            }),
        ],
        "profile": "I...T",
        "desc": "Reject Invalid Asymmetric ID Token Signature"
    },
    "rp-id_token-bad-sig-es256": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "id_token_signed_response_alg": "ES256"
                }
            }),
            (SyncAuthn, {
                set_op_args: {"response_type": ["id_token"]},
                expect_exception: BadSignature
            })
        ],
        "profile": "I...T",
        "desc": "Reject Invalid Asymmetric ID Token Signature"
    },
    "rp-id_token-bad-sig-hs256": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "id_token_signed_response_alg": "HS256"
                }
            }),
            (SyncAuthn, {
                set_op_args: {"response_type": ["id_token"]},
                expect_exception: BadSignature
            })
        ],
        "profile": "I...T",
        "desc": "Reject Invalid Symmetric ID Token Signature"
    },
    "rp-id_token-sig+enc": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "id_token_signed_response_alg": "HS256",
                    "id_token_encrypted_response_alg": "RSA1_5",
                    "id_token_encrypted_response_enc": "A128CBC-HS256"},
                set_jwks_uri: None
            }),
            (SyncAuthn, {set_op_args: {"response_type": ["id_token"]}}),
        ],
        "profile": "I...T",
        "desc": "Can Request and Use Signed and Encrypted ID Token Response",
    },
    "rp-id_token-sig-none": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {"id_token_signed_response_alg": "none"}
            }),
            (SyncAuthn, {set_op_args: {"response_type": ["code"]}}),
            AccessToken
        ],
        "profile": "C,CT,CIT...T",
        "desc": "Can Request and Use unSigned ID Token Response"
    },
    "rp-userinfo-bad-sub-claim": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn,
            AccessToken,
            (UserInfo, {expect_exception: SubjectMismatch})
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Reject UserInfo with Invalid Sub claim"
    },
    "rp-claims-request-id_token": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            (SyncAuthn, {set_request_args: {
                "claims": {
                    "id_token": {
                        "auth_time": {
                            "essential": True
                        },
                        "email": {
                            "essential": True
                        },
                    }
                }
            }}),
            AccessToken
        ],
        "profile": "...",
        "desc": "The Relying Party can ask for a specific claim using the "
                "'claims' request parameter. The claim should be returned in "
                "an ID Token"
    },
    "rp-claims-request-userinfo": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            (SyncAuthn, {
                set_request_args: {
                    "claims": {
                        "userinfo": {
                            "email": {
                                "essential": True
                            },
                        }
                    }
                },
            }),
            AccessToken,
            UserInfo
        ],
        "profile": "C,IT,CI,CT,CIT...",
        "desc": "The Relying Party can ask for a specific claim using the "
                "'claims' request parameter. The claim should be returned in "
                "a UserInfo response",
    },
    "rp-scope-openid": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            (SyncAuthn, {set_request_args: {"scope": ["wrong"]}}),
        ],
        "profile": "...",
        "desc": "The Relying Party should always add the openid scope value "
                "while sending an Authorization Request.",
    },
    "rp-scope-userinfo-claims": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            (SyncAuthn,
             {set_request_args: {"scope": ["openid", "email", "profile"]}}),
            AccessToken,
            UserInfo
        ],
        "profile": "IT,CT,CIT...",
        "desc": "The Relying Party should be able to request claims using "
                "Scope Values",
    },
    "rp-userinfo-bearer-body": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn,
            AccessToken,
            (UserInfo, {
                set_request_args: {
                    "behavior": "token_in_message_body"
                }
            })
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Accesses UserInfo Endpoint with form-encoded body method"
    },
    "rp-userinfo-bearer-header": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn,
            AccessToken,
            (UserInfo, {
                set_request_args: {
                    "behavior": "use_authorization_header"
                }
            })
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Accesses UserInfo Endpoint with Header Method "
    },
    "rp-userinfo-enc": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "userinfo_encrypted_response_alg": "RSA1_5",
                    "userinfo_encrypted_response_enc": "A128CBC-HS256"
                },
                set_jwks_uri: None
            }),
            SyncAuthn,
            AccessToken,
            UserInfo
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Can Request and Use Encrypted UserInfo Response "
    },
    "rp-userinfo-sig+enc": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "userinfo_signed_response_alg": "RS256",
                    "userinfo_encrypted_response_alg": "RSA1_5",
                    "userinfo_encrypted_response_enc": "A128CBC-HS256"
                },
                set_jwks_uri: None
            }),
            SyncAuthn,
            AccessToken,
            UserInfo
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Can Request and Use Signed and Encrypted UserInfo Response"
    },
    "rp-userinfo-sign": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            (Registration, {
                set_request_args: {
                    "userinfo_signed_response_alg": "RS256",
                },
                set_jwks_uri: None
            }),
            SyncAuthn,
            AccessToken,
            UserInfo
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Can Request and Use Signed UserInfo Response"
    },
    "rp-claims-aggregated": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn,
            AccessToken,
            UserInfo
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Can handle aggregated user information"
    },
    "rp-claims-distributed": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn,
            AccessToken,
            UserInfo
        ],
        "profile": "C,CI,CT,CIT...",
        "desc": "Handles distributed user information"
    },
    "rp-nonce-invalid": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn
        ],
        "profile": "I,IT,CI,CIT...",
        "desc": "If a nonce value was sent in the Authentication Request the "
                "Relying Party must validate the nonce returned in the ID "
                "Token."
    },
    "rp-nonce-unless-code-flow": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            (SyncAuthn, {set_request_args: {"nonce": None}})
        ],
        "profile": "I,IT,CI,CIT...",
        "desc": "The Relying Party should always send a nonce as a request "
                "parameter while using implicit or hybrid flow. "
                "Since the server is suppose to return the nonce in the ID "
                "Token return from Authorization Endpoint, "
                "see ID Token required claims in hybrid flow or implicit "
                "flow. When using Code flow the the nonce is not "
                "required, see ID Token validation for code flow"
    },
    "rp-request_uri-enc": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            (SyncAuthn, {set_op_args: {"request_method": "file",
                                       "request_object_encryption_alg":
                                           "RSA1_5",
                                       "request_object_encryption_enc":
                                           "A128CBC-HS256",
                                       "local_dir": "./request_objects",
                                       "base_path":
                                           "https://localhost:8088/request_objects/"
                                       }})
        ],
        "profile": "...",
        "desc": "The Relying Party can pass a Request Object by reference "
                "using the request_uri parameter. "
                "Encrypt the Request Object using RSA1_5 and A128CBC-HS256 "
                "algorithms"
    },
    "rp-key-rotation-op-enc-key": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            (SyncAuthn, {
                set_op_args: {
                    "request_method": "request",
                    "request_object_encryption_alg": "RSA1_5",
                    "request_object_encryption_enc": "A128CBC-HS256"
                }
            }),
            UpdateProviderKeys,
            (SyncAuthn, {
                set_op_args: {
                    "request_method": "request",
                    "request_object_encryption_alg": "RSA1_5",
                    "request_object_encryption_enc": "A128CBC-HS256"
                }
            }),
        ],
        "profile": "...",
        "desc": "Support OP Encryption Key Rollover"
    },
    "rp-key-rotation-op-sign-key": {
        "sequence": [
            (Webfinger, {set_webfinger_resource: {}}),
            (Discovery, {set_discovery_issuer: {}}),
            Registration,
            SyncAuthn,
            SyncAuthn
        ],
        "profile": "I,IT,CI,CIT...",
        "desc": "Support OP Signing Key Rollover"
    }
}
