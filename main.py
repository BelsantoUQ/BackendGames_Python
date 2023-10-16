from fastapi import Depends, Body, Path, Query, FastAPI, HTTPException
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from Player import PlayerInfo
from controller import DataStore
from jwt import encode as jwt_encode, decode, InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta
import secrets

clave_secreta = secrets.token_hex(16)
app = FastAPI()
app.title = "Belsanto Software - Games API"
app.version = "0.0.1"
dataController = DataStore()
class Player(BaseModel):
    plyid : Optional[int] = None
    plyscore : str = Field(default="N/A", max_length=155)
    plygame : str = Field(max_length=255)
    plylife : str = Field(default="N/A", max_length=155)
    plygames : float = Field(ge=0)
    plypos : str = Field(default="N/A", max_length=155)
    plyrot : str = Field(default="N/A", max_length=155)
    plypowerups : int = Field(ge=0, le = 100)
    plyname : str = Field(max_length=50)
    plyemail : Optional[str] = Field(default="N/A", max_length=155)
    plypass : Optional[str] = Field(default="N/A", max_length=155)

security = HTTPBearer()

def verificar_token(token: str = Depends(security)):
    try:
        payload = decode(token.credentials, clave_secreta, algorithms=["HS256"])
        usuario = payload["usuario"]
        expiracion = datetime.utcfromtimestamp(payload["exp"])
        if expiracion > datetime.utcnow():
            return usuario
        else:
            raise HTTPException(status_code=401, detail="Token expirado")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get('/', tags=['home'])
def message( usuario: str = Depends(verificar_token)):
    return {"message": "API Restful de juegos - Creado por Belsanto: https://belsanto.site/"}

@app.post('/login', tags=['autenticación'])
def login(usuario: str, contrasena: str):
    try:
        if usuario == 'admin' and contrasena == 'admin':
            token = jwt_encode({
                'usuario': usuario,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, clave_secreta, algorithm='HS256')
            return {
            'mensaje': 'Inicio de sesión exitoso',
            'token': token
        }
        else:
            raise HTTPException(status_code=401, detail='Credenciales inválidas')
    except Exception as e:
        return {'error': str(e)}

@app.get('/games', tags=['games'])
def get_games():
    if len(dataController.get_games) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron juegos.")
    return dataController.get_games

