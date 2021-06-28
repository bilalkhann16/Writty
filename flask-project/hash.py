#trying to fugure out how to use hashing in Python.
s = "subhan1234"
import hashlib
#hash =  (int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**8)
hash = str(hash(s))
# decode = hash.decode(encoding='UTF-8',errors='strict')
print (hash)