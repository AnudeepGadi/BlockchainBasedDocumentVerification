from tinyec import registry
import secrets

def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y)

curve = registry.get_curve('secp521r1')
studentPrivKey = secrets.randbelow(curve.field.n)
studentPubKey = studentPrivKey * curve.g
verifierPrivKey = secrets.randbelow(curve.field.n)
verifierPubKey = verifierPrivKey * curve.g

print("STUDENT_PRIVATE_KEY=",studentPrivKey)
print("VERIFIER_PRIVATE_KEY=",verifierPrivKey)
print("STUDENT_PUBLIC_KEY=",compress(studentPubKey))
print("VERIFIER_PUBLIC_KEY=",compress(verifierPubKey))

