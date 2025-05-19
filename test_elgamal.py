import elgamal
from hashlib import sha256

""" Testing the elgamal module """

if __name__ == "__main__":
    # Documents to sign
    msgs = ["Introduction to information security - Elgamal digital signature"]
    msgs_fake = ["Introduction to information security - Elgamal digital signature1"]
    # Hash function
    hfun = sha256()
    # Bit Length
    N = 100

    # Testing the signatures for the documents
    for msg in msgs:
        print("")
        print("Message: ", msg)
        print()

        elgsys = elgamal.generate_system(N, hfun)
        print("Generated system:", elgsys)
        print()

        keys = elgamal.generate_keys(elgsys)
        print("Generated key pair (x, y): ", keys)
        print() 

        sig = elgamal.sign(elgsys, msg, keys[0])
        print("Generated signature pair (r, s):", sig)
        print()

        # is_valid = elgamal.verify(elgsys, msgs, sig, keys[1])
        is_valid = elgamal.verify(elgsys, msgs_fake[0], sig, keys[1])
        print("=> Is signature valid?", is_valid)
        
        print("----------------------------------------------------------------")