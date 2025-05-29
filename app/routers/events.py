from typing import List

from fastapi import APIRouter, Path, HTTPException, Query #APIRouter: classe che usiamo al posto di FastAPI quando costruiamo parti modulari dell'app. Path: funzione per specificare i parametri nell'URL. HTTPException: classe per gestire le eccezioni. Query: per dichiarare e validare parametri di query negli endpoint FastAPI.
from app.models.event import Event, EventCreate, EventPublic #import necessario per usare la classe Event definita nel package models nel file python event.py
from typing import Annotated #funzione Annotated --> serve per validare i dati
from pydantic import ValidationError #per gestire le eccezioni
from app.models.user import User #import necessario per usare la classe User definita nel package models nel file python user.py
from sqlmodel import select, delete
from app.data.db import SessionDep
router = APIRouter(prefix="/events") #tutti gli endpoint definiti dentro il router inizieranno con /events

@router.get("/") #Decoratore che specifica il metodo HTTP e il percorso. Definisce un endpoint GET relativo al prefisso router. Il prefisso è /events, quindi questo endpoint corrisponde a GET /events
def get_all_events(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort events by id")]=False
) -> list[EventPublic]: #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint
    """Return the list of all events"""
    events = session.exec(select(Event)).all()
    if sort:
        return sorted(events.value(), key=lambda event: event.id)
    else:
        return list(events.values()) #restituisce una lista di oggetti Event

@router.post("/") #decoratore API che fornisc eun endpoint POST realtivo al prefisso /books (POST /books). Specifica il metodo HTTP e il percorso
def add_event(session: SessionDep, event: EventCreate): #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint
    #event: Event dice a FastAPI di aspettarsi un oggetto JSON nel body della richiesta e di convertirlo automaticamente in un oggetto Event utilizzando Pydantic
    """Adds a new event to the database""" #questa descrizione appare nella documentazione /docs
    session.add(Event.model_validate(event))
    session.commit()
    return "Event successfully added"

@router.delete("/") #decoratore FastAOI che definisce un endpoint DELETE relativo al prefisso /events -> DELETE /events
def delete_all_events(session: SessionDep):  #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint
    """Delete all events""" #questa descrizione appare nella documentazione /docs
    session.exec(delete(Event))
    session.commit()
    return "All events successfully deleted"

@router.get("/{id}") #Decoratore che specifica il metodo HTTP e il percorso. Definisce un endpoint GET relativo al prefisso router. Il prefisso è /events, quindi questo endpoint corrisponde a GET /events/{id}
def get_event_by_id( #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint.
        session: SessionDep,
        id: Annotated[int, Path(description="The id of the event to get")] #il tipo atteso per l'id è un intero. Path aggiunge una descrizione visibile nella documentazione Swagger.
        ) -> EventPublic: #restituisce un oggetto di tipo evento
        """Return the event with the given id"""
        event = session.get(Event, id)
        if event:
            return event
        else:
            raise HTTPException(status_code=404, detail=f"The event with ID {id} was not found") #404 -> la risorsa richiesta non esiste


@router.post("/{id}/register") #decoratore FastAPI che definisce un endìpoint POST (POST /events/{id}/register) con un parametro dinamico id nell'URL
def register_user( #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint.
        session: SessionDep,
        id: Annotated[int, Path(description="The id of the event the user wants to register for")], #il tipo atteso per l'id è un intero. Path aggiunge una descrizione visibile nella documentazione Swagger.
        user: User, #oggetto di classe User inviato nel body della richiesta
        username=None,
        name=None,
        email=None
):
    """Register a user to the event with the given ID""" #questa descrizione appare nella documentazione /docs
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail=f"The event with ID {id} was not found")
    user.username = username.username
    user.name = name.name
    user.email = email.email
    session.add(user)
    session.commit()
    return "User successfully registered"


@router.put("/{id}")
def update_event( #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint.
    session: SessionDep,
    id: Annotated[int, Path(description="The id of the event to update")], #il tipo atteso per l'id è un intero. Path aggiunge una descrizione visibile nella documentazione Swagger.
    new_event: EventCreate,
): #restituisce un oggetto di tipo event
    """Update the event with the given id""" #questa descrizione appare nella documentazione /docs
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404,detail=f"The event with ID {id} was not found")
    event.title = new_event.title
    event.description = new_event.description
    event.data = new_event.data
    event.location = new_event.location
    session.add(event)
    session.commit()
    return "Event successfully updated"

@router.delete("/{id}") #decoratore FastAPI che definisce un endpoint DELETE  con un parametro dinamico {id} nell'URL -> DELETE /events/{id}
def delete_event_by_id( #endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint.
        session: SessionDep,
        id: Annotated[int, Path(description="The id of the event to delete")] #il tipo atteso per l'id è un intero. Path aggiunge una descrizione visibile nella documentazione Swagger.
):
    """Delete the event with the given id""" #questa descrizione appare nella documentazione /docs
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail=f"The book with ID {id} was not found") #404 -> la risorsa richiesta non esiste
    session.delete(event)
    session.commit()
    return "Event successfully deleted"