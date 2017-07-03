from nacl import bindings

from nacl import exceptions as exc
from nacl._sodium import ffi, lib
from nacl.exceptions import ensure


from saltchannel.util.py import Singleton
from saltchannel.saltlib.saltlib_base import SaltLibBase
from saltchannel.saltlib.saltlib_base import BadSignatureException

class SaltLibPyNaCl(SaltLibBase, metaclass=Singleton):

    @staticmethod
    def isAvailable():
        return True

    # ret: pk, sk
    def crypto_sign_keypair_not_random(self, seed):
        if len(seed) != self.crypto_sign_SEEDBYTES:
            raise ValueError("Invalid seed")
        pk = ffi.new("unsigned char[]", self.crypto_sign_PUBLICKEYBYTES)
        sk = ffi.new("unsigned char[]", self.crypto_sign_SECRETKEYBYTES)
        rc = lib.crypto_sign_seed_keypair(pk, sk, seed)
        ensure(rc == 0,
               'Unexpected library error',
               raising=exc.RuntimeError)
        return (ffi.buffer(pk, self.crypto_sign_PUBLICKEYBYTES)[:],
                ffi.buffer(sk, self.crypto_sign_SECRETKEYBYTES)[:],
                )

    # ret: sm
    def crypto_sign(self, m, sk):
        return bindings.crypto_sign(m, sk)

    # ret: m
    def crypto_sign_open(self, sm, pk):
        try:
            return bindings.crypto_sign_open(sm, pk)
        except Exception as e:
            raise BadSignatureException(e)

    # ret: pk, sk
    def crypto_box_keypair_not_random(self, sk):
        if len(sk) != self.crypto_box_SECRETKEYBYTES:
            raise ValueError("Invalid secret key length")
        return bindings.crypto_scalarmult_base(sk), sk

    def crypto_hash(self, m):
        return bindings.crypto_hash(m)