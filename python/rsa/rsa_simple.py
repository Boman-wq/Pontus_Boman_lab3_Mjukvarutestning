import math
#
# RSA algoritmen (Rivest, Shamir, Adleman, 1978) PKCS#3
# Välj två stora primtal (bara delbara med 1) P och Q. 
# Hitta deras produkt n = PQ
# Beräkna m = (P-1)(Q-1)
# Välj ett relativt prima (gemensam nämnare med m som är 1) tal e mindre än m och större än 1. 
# Formeln blir då: d = 1/e mod m där e är den publika och d den privata exponenten. 
# Den publika nyckeln är paret n och e och den privata nyckeln är paret n och d. 
# Faktorerna P och Q måste hållas hemliga eller förstöras
#
# Simple RSA algorithm test
#
def main():

    # Menu
    while 1:
        print("""
    1. Set Public Key 
    2. Encode
    3. Decode
    4. Non-interactive Test
    0. Quit
    Your choice? """, end = "")

        choice = int(input())
        if not choice:
            return
        if choice == 1:
            n, e, d = set_keys()
        if choice == 2:
            if not n:
                n = int(input("Public Key: "))
                e = int(input("e: "))
            encode(n, e)
        if choice == 3:
            if not d:
                n, e, d = set_keys()
            decode(d, n)
        if choice == 4:
            non_interactive_test()


# Calculate for when (dd * e) % m returns the rest number 1 => we found d
def get_d(e, m):
    dd = 0
    while ((dd * e) % m) != 1:
        dd = dd + 1
    return dd


def set_keys():
    """This fuction asks for 2 primes. 
    It sets a public key and an encoding number, 'e'."""
    P = int(input("P: "))
    Q = int(input("Q: "))
    n = P * Q
    m = (P - 1) * (Q - 1)
    e = get_e(m)
    d = get_d(e, m)
    while d < 0:
        d += m
    print("N =", n, ", m =", m, "\ne =", e, ", d =", d)
    return [n, e, d]   


def get_e(m):
    """Finds an e coprime with m."""
    e = 2
    while gcd(e, m) != 1:
        e += 1
    return e


def gcd(a,b):
    """Euclid's Algorithm: Takes two integers and returns gcd."""
    while b > 0:
        a, b = b, a % b
    return a


def encode(n, e):
    """This function asks for a number and encodes it using 'n' and 'e'."""
    while 1:
        c = int(input("Number to encode (0 to go back): "))
        if not c:
            return
        print(pow(c, e, n))


def decode(d, n):
    """This function asks for a number and decodes it using 'd' and 'n'."""
    while 1:
        c = int(input("Number to decode (0 to go back): "))
        if not c:
            return
        else:
            print(pow(c, d, n))      

# Non-interactive test
def non_interactive_test():
    print("Non-interactive test")
    # Select a secret first prime
    P = 11
    # Select a secret second prime
    Q = 7
    # public and private modulo number is 
    # N = P * Q = 77
    n = P * Q
    
    # Calculate m or (n) = (P-1) * (Q -1) = 60
    m = (P-1) * (Q -1)

    # Choose a public exponent prime number e which must be less than m and larger than 1
    e = 17
    
    # Calculate the private exponent number d = 1/e mod m
    d = get_d(e, m)
    # print ("d: " + str(d))
    print("N =", n, ", m =", m, "\ne =", e, ", d =", d)

    # Public key pair is n and e. 
    # Private key pair is n and d.

    # Char we want to encrypt, c1 must be less than n (plaintext < n)
    c1 = 8
    print ("original char: " + str(c1))

    # Formula for encryption: encrypt(plaintext) = plaintext^e mod n, (plaintext < n)
    cipher = pow(c1, e) % n
    print("cipher char: "+ str(cipher))

    # Formula for decryption: decrypt(ciphertext) = cipher^d mod n
    c2 = pow (cipher, d) % n
    print("decrypted char: " + str(c2))

    print("--result--")
    print("Are they equal? " + str(c1 == c2))
    
if __name__ == "__main__":
    main()
