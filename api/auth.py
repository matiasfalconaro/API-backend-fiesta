from fastapi import (HTTPException,
                     Request,
                     Security)
from fastapi.security.api_key import (APIKeyHeader)
from config import settings
from starlette.status import HTTP_403_FORBIDDEN


api_key_header = APIKeyHeader(name=settings.API_KEY_NAME,
                              auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header),
                      request: Request = None):
    """
    
    """
    api_key_query = request.query_params.get(settings.API_KEY_NAME)
    
    if (api_key_header == settings.API_KEY or
        api_key_query == settings.API_KEY):
        return api_key_header
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail="No se pudieron validar las credenciales")
