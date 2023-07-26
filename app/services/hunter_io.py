import httpx

from app.exceptions import VerifyEmailError
from app.settings import settings


async def get_email_data_by_hunter_io(email: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_IO_KEY}'
        )
    if response.status_code == 401:
        errors = [error['details'] for error in response.json().get('errors', [])]
        raise VerifyEmailError(
            f'Ответ от сервера верификации Email`а вернулся с ошибкой: {"; ".join(errors)}'
        )
    if response.status_code != 200:
        raise VerifyEmailError(f'Не удалось получить ответ от сервера верификации Email`а')
    return response.json()


async def verifying_email(email: str) -> bool:
    response = await get_email_data_by_hunter_io(email=email)
    return response['data']['status'] == 'valid'

