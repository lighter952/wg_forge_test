from passlib.context import CryptContext


myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])
hash1 = myctx.hash("joshua")
print(myctx.verify("joshua", hash1))

print(myctx.hash('johndoe'))