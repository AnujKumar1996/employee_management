from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

class Error(BaseModel):
    '''
    Text that provides mode details and corrective actions related to
    the error. This can be shown to a client user.
    '''
    
    message         : Optional[str] = Field(default=None,description = 'Text that provides mode details and corrective actions related to the error. This can be shown to a client user.')
    reason          : str = Field(max_length = 255,description = 'Text that explains the reason for the error. This can be shown to a client user.')
    referenceError  : Optional[HttpUrl] = Field(default=None,description = 'URL pointing to documentation describing the error.')

class Error404Code(str, Enum):
    NOT_FOUND  = 'notFound'


class Error404(Error):
    '''
        The following error code:
            - notFound: A current representation for the target resource 
            not found.
    '''
    code : Error404Code


class InternalError(str, Enum):
    INTERNAL_ERROR = 'internalError'

        
class Error500(Error):
    '''
        The following error code:

        - internalError: Internal server error - the server encountered
        an unexpected condition that prevented it from fulfilling the
        request.
    '''
    code : InternalError    
    
    