import json 
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


# For generating the PEM key 
from Crypto.Util.asn1 import DerSequence
# from Crypto.PublicKey import RSA
from binascii import a2b_base64


# For generating a "x509" certificate
from cryptography import x509 
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import uuid
"""
<---------------------- Steps ---------------------->
1. You generate a private/public key pair 

2. You create a request for a certificate, which is signed by your key (to 
prove that you own the key). 

3. You give the certificate signing request (CSR) to a Cirtificate Authority (CA)
(don't give them your private key). 

4. The CA validates that you own the resource (e.g. domain) that you want a 
certificate for. 

5. The CA gives you a certificate, signed by them, which identifies your public key, 
and the resource you are authenticated for. 

6. You configure your server to use that certificate, combined with your private key, 
to serve traffic. 


"""


def generatePEM():
    key = RSA.generate(2048)
    pv_key_string = key.exportKey()
    with open("private.pem","w") as prv_file: 
        print("{}".format(pv_key_string.decode()), file = prv_file)
    
    pb_key_string = key.exportKey()
    with open("public.pem","w") as pub_file: 
        print("{}".format(pb_key_string.decode()), file = pub_file)



def generateCert():
    key = rsa.generate_private_key(

    public_exponent=65537,

    key_size=2048,
    )

    # Write our key to disk for safe keeping

    with open("key.pem", "wb") as f:

        f.write(key.private_bytes(

            encoding=serialization.Encoding.PEM,

            format=serialization.PrivateFormat.TraditionalOpenSSL,

            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),

        ))

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"), 
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Maryland"), 
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Baltimore"),  
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"opencord"), 
        x509.NameAttribute(NameOID.COMMON_NAME, u"opencord.chat"),  
     ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # Our certificate will be valid for 10 days 
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = 10)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), 
        critical = False, 
    ).sign(key, hashes.SHA256()) # Sign our certificate with our private key 

    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

def csr(key):

    custom_extension = x509.Extension(
        oid = 
        
    )
    
    # Certificate signing request 
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Provide various details about who we are. 
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"), 
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Maryland"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Baltimore"), 
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Opencord"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"opencord.chat") 
    ])).add_extension(
        x509.SubjectAlternativeName([
            # Describe what sites we want this certificate for 
            x509.DNSName(u"opencord.chat"), 
            x509.DNSName(u"www.opencord.chat")
        ]), 
        critical = False,
    ).sign(key, hashes.SHA256())
    
    # Write our CSR out to disk
    with open('csr.pem', 'wb') as f: 
        f.write(csr.public_bytes(serialization.Encoding.PEM))
     
def signKey():
    pass

def loadCert(name):
    file = open(name, 'rb')
    cert = x509.load_pem_x509_certificate(file.read())

    print(f"UUID: {uuid.uuid4()}")
    print(f"Cert: {cert.issuer}")
    print(f"Serial number: {cert.serial_number}")
    print(f"Public key: {cert.public_key()}")
    print(f"Subject: {cert.subject}")
    print(f"Validity Period (before): {cert.not_valid_before}")
    print(f"Validity Period (after): {cert.not_valid_after}")
    print(f"Signature algorithm: {cert.signature_algorithm_oid}")
    print("\n")


if __name__ == '__main__':
    # generatePEM()
    generateCert()
    # loadCert("google-com.pem")
    # loadCert("totallycritical-com.pem")
    loadCert("cert.pem")

