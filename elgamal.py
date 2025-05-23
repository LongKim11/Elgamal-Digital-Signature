from Crypto.Util import number as num
from random import randint
from math import gcd

""" Module for generating ElGamal Digital Signature Scheme systems, keys,
    Signing documents, and veryfing signatures.
"""

def generate_system(key_length, hash_function):
    """ Generates an ElGamal system

        Parameters:
        key_length (int): bits of length of prime number p
        hash_function (HASH): a hash function (from hashlib) to hash the message

        Returns:
        Dictionary: {
            "N": bit length of prime
            "p": generated prime
            "H": hash function
            "g": chosen generator of Z*p
        }
    """
    # Generating safe prime
    p = 4
    while not num.isPrime(p):
        pp = num.getPrime(key_length-1)
        p = pp*2+1

    # Choosing a generator
    g = randint(2, p-1)
    while (p-1)%g == 1:
        g = randint(2, p-1)

    system = {
        "N": key_length,
        "p": p,
        "H": hash_function,
        "g": g  
    }
    return system

def generate_keys(system):
    """ Generates a pair of keys for an ElGamal DS system

        Parameters:
        system (dictionary):    an ElGamal system (generated by generate_system)

        Returns:
        int, int:   a pair of keys - private key, public key (x, y)
    """
    x = randint(1, system["p"]-2)
    y = pow(system["g"], x, system["p"])

    return x, y

def sign(system, message, private_key):
    """ Signs a message (document) using an ElGamal DS system and private key

        Parameters:
        system (dictionary):    an ElGamal system (generated by generate_system)
        message (str):          a message to be signed
        private_key (int):      private key to be used to sign the message

        Returns:
        int, int:   a signature pair - (r, s)
    """
    # Hashing the message
    H = system["H"].copy()
    H.update(message.encode())
    hash = int(H.hexdigest(), 16)

    s = 0
    while s == 0:
        # Find relatively prime to p-1 k
        k = randint(2,system["p"])
        while gcd(k, system["p"]-1) != 1:
            k = randint(2,system["p"])
        
        # Calculate the signature pair
        r = pow(system["g"], k, system["p"])
        s = ((hash - private_key*r) * num.inverse(k, system["p"]-1))%(system["p"]-1)

    return r,s

        

def verify(system, message, signature, public_key):
    """ Verifies an ElGamal signature

        Parameters:
        system (dictionary):    an ElGamal system (generated by generate_system)
        message (str):          a message that was signed
        signature (int, int):   a signature pair (r, s)
        public_key (int):       a public key from the pair used to sign the document

        returns:
        bool:   validity of the signature - True if valid, False otherwise
    """
    # Check correctnes of signature
    if signature[0] <= 0 or signature[1] <= 0 or signature[0] >= system["p"] or signature[1] >= (system["p"]-1):
        return False
    
    # Hashing the message
    H = system["H"].copy()
    H.update(message.encode())
    hash = int(H.hexdigest(), 16)

    # Check validity of signature
    l = pow(system["g"], hash, system["p"])
    r = pow(public_key, signature[0], system["p"]) * pow(signature[0], signature[1], system["p"]) % system["p"]

    return l == r