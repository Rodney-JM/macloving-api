from fastapi import HTTPException, status

#Exception base
class AppException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

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
        
class InvalidTokenError(AppException):
    def __init__(self, detail: str = "Acesso negado"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)
        
class InvalidCredentialsError(AppException):
    def __init__(self, detail: str = "Email ou senha incorretos", status_code = status.HTTP_401_UNAUTHORIZED):
        super().__init__(detail, status_code)

class ConflictError(AppException):
    def __init__(self, detail: str = "Conflito de dados."):
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail
            )

#regra de negocio
class BusinessRuleError(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        ) 
        
class CoupleRequiredError(AppException):
    def __init__(self):
        super().__init__(
            detail="Você precisa estar vinculado a um parceiro para usar essa funcionalidade",
            status_code=status.HTTP_403_FORBIDDEN
        )

class AlreadyInCoupleError(AppException):
    def __init__(self):
        super().__init__(
            detail="Você já está em um relacionamento ativo",
            status_code=status.HTTP_409_CONFLICT
        )
class SurpriseLockError(AppException):
    def __init__(self):
        super().__init__(
            detail="Essa surpresa ainda está bloqueada e não pode ser aberta",
            status_code=status.HTTP_403_FORBIDDEN
        )

#upload

class InvalidFileTypeError(AppException):
    def __init__(self, allowed: list[str]):
        super().__init__(
            detail=f"Tipo de arquivo não permitido. Aceitos: {', '.join(allowed)}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        
class FileTooLargeError(AppException):
    def __init__(self, max_mb: int):
        super().__init__(
            detail=f"Arquivo muito grande. Tamanho máximo: {max_mb}MB",
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        )
        
        
class StorageError(AppException):
    def __init__(self, detail: str = "Erro ao processar arquivo."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
        
#rate limit 
class RateLimitError(AppException):
    def __init__(self):
        super().__init__(
            detail="Muitas requisições. Tente novamente em breve",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
        
#Subscription

class PremiumRequiredError(AppException):
    def __init__(self, feature: str = "essa funcionalidade"):
        super().__init__(
            f"O plano Premium é necessário para usar {feature}."
            "Faça upgrade em Configurações -> Assinatura.",
            status.HTTP_402_PAYMENT_REQUIRED
        )

class SubscriptionLimitError(AppException):
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_402_PAYMENT_REQUIRED)

class ActiveSubscriptionError(AppException):
    def __init__(self):
        super().__init__(
            "Você já possui uma assinatura ativa. Gerencie-a pelo portal do cliente.",
            status.HTTP_409_CONFLICT
        )

class StripeWebhookError(AppException):
    def __init__(self, detail: str = "Webhook inválido"):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)