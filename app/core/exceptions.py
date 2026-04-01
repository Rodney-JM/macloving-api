from fastapi import HTTPException, status

#Exception base
class AppException(HTTPException):
    pass

class NotFoundError(AppException):
    def __init__(self, resource: str = "Recurso"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} não encontrado.",
        )
        
class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Não autenticado."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )
        
class ForbiddenError(AppException):
    def __init__(self, detail: str = "Acesso negado."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ConflictError(AppException):
    def __init__(self, detail: str = "Conflito de dados."):
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail
            )

class BusinessRuleError(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        ) 
        
        
class StorageError(AppException):
    def __init__(self, detail: str = "Erro ao processar arquivo."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )