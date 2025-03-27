from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from ..core.config import settings

security = HTTPBearer()

class StackAuthMiddleware:
    def __init__(self):
        self.project_id = settings.stack_project_id
        self.publishable_key = settings.stack_publishable_client_key
        self.secret_key = settings.stack_secret_server_key

    async def __call__(self, request: Request, call_next):
        # Skip auth for public endpoints
        if request.url.path in ["/docs", "/redoc", "/health"]:
            return await call_next(request)

        try:
            # Get the authorization header
            credentials: Optional[HTTPAuthorizationCredentials] = await security(request)
            if not credentials:
                raise HTTPException(status_code=401, detail="No authorization token provided")

            # Verify the JWT token
            token = credentials.credentials
            try:
                payload = jwt.decode(
                    token,
                    self.secret_key,
                    algorithms=["HS256"]
                )
                
                # Add user info to request state
                request.state.user = payload
                
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")

            return await call_next(request)

        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e)) 