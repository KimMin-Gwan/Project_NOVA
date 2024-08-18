import jwt

class JWTDecoder:
    def __init__(self):
        self.secret_key = "your_secret_key"
        self.argorithms = ["HS256"]

    def decode(self, token):
        decoded_payload = jwt.decode(token, self.secret_key, 
                                     algorithms=self.argorithms,
                                     options={"verify_exp":False}
                                     )
        payload = JWTPayload(email=decoded_payload['email'])

        return payload
    
class JWTPayload:
    def __init__(self, email, exp="0"):
        self.email=email
        self.exp=exp



    
