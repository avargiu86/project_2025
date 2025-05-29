from typing import List

from fastapi import APIRouter, Path, HTTPException, Query #APIRouter: classe che usiamo al posto di FastAPI quando costruiamo parti modulari dell'app. Path: funzione per specificare i parametri nell'URL. HTTPException: classe per gestire le eccezioni. Query: per dichiarare e validare parametri di query negli endpoint FastAPI.

from app.models.event import Event #import necessario per usare la classe Event definita nel package models nel file python event.py
from typing import Annotated #funzione Annotated --> serve per validare i dati
from pydantic import ValidationError #per gestire le eccezioni
from app.models.user import User #import necessario per usare la classe User definita nel package models nel file python user.py
from app.data.db import SessionDep
from sqlmodel import select, delete

router = APIRouter(prefix="/users") #tutti gli endpoint definiti dentro il router inizieranno con /events

@router.get("/") #Decoratore che specifica il metodo HTTP e il percorso. Definisce un endpoint GET relativo al prefisso router. Il prefisso è /events, quindi questo endpoint corrisponde a GET /events
def get_all_users(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort users by their username")]
) -> list[User]: #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint
    """Return the list of all events"""
    users = session.exec(select(User)).all()
    if sort:
        return sorted(users.values(), key=lambda user: user.username)
    else:
        return list(users.values()) #restituisce una lista di oggetti Event

#DA QUI!!!!
@router.post("/") #decoratore API che fornisc eun endpoint POST realtivo al prefisso /books (POST /books). Specifica il metodo HTTP e il percorso
def add_user(session: SessionDep, user: User): #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint
    #user: User dice a FastAPI di aspettarsi un oggetto JSON nel body della richiesta e di convertirlo automaticamente in un oggetto User utilizzando Pydantic
    """Adds a new user""" #questa descrizione appare nella documentazione /docs
    session.add(User.model_validate(user))
    session.commit()
    return "User successfully added"

@router.delete("/") #decoratore FastAPI che definisce un endpoint DELETE relativo al prefisso /events -> DELETE /events
def delete_all_users(session: SessionDep):  #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint
    """Delete all users""" #questa descrizione appare nella documentazione /docs
    session.exec(delete(User))
    session.commit()
    return "All useers successfully deleted"

@router.get("/{username}") #Decoratore che specifica il metodo HTTP e il percorso. Definisce un endpoint GET relativo al prefisso router. Il prefisso è /users, quindi questo endpoint corrisponde a GET /users/{username}
def get_event_by_username( #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint.
        session: SessionDep,
        username: Annotated[str, Path(description="The username of the user to get")] #Il tipo atteso per lo username è una stringa. Path aggiunge una descrizione visibile nella documentazione Swagger.
) -> User: #restituisce un oggetto di tipo User
        """Return the user with the given username"""
        user = session.get(User, username)
        if user: #gestiamo il caso in cui non esista un utente con lo username cercato nel path
            return user
        else:
            raise HTTPException(status_code=404, detail=f"The user with username {username} was not found") #404 -> la risorsa richiesta non esiste

@router.delete("/{username}") #decoratore FastAPI che definisce un endpoint DELETE con un parametro dinamico {username} nell'URL -> DELETE /users/{username}
def delete_user_by_username( #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint.
        session: SessionDep,
        username: Annotated[str, Path(description="The username of the user to delete")] #Il tipo atteso per lo username è una stringa. Path aggiunge una descrizione visibile nella documentazione Swagger.
):
    """Delete the user with the given username""" #questa descrizione appare nella documentazione /docs
    user = session.get(User, username)
    if not user: #se l'utente non esiste
        raise HTTPException(status_code=404, detail=f"The user with username {username} was not found") #404 -> la risorsa richiesta non esiste
    session.delete(user)
    session.commit()
    return f"User with username {username} successfully deleted"