from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm

# This will create custome OAuthPasswordRequestForm But not made yet quite good it leaks some information data to terminal

class OAuth2PasswordRequestFormField(OAuth2PasswordRequestForm):
    def __init__(self, password: str, grant_type: Optional[str] = None, username: Optional[str] = None, email: Optional[str] = None, scope: str = "", client_id: Optional[str] = None, client_secret: Optional[str] = None):
        if not username:
            username = ""
        super().__init__(grant_type=grant_type, username=username, password=password, scope=scope, client_id=client_id, client_secret=client_secret)
        self.email = email