from typing import List

from fastapi import APIRouter, Path, HTTPException, Query #APIRouter: classe che usiamo al posto di FastAPI quando costruiamo parti modulari dell'app. Path: funzione per specificare i parametri nell'URL. HTTPException: classe per gestire le eccezioni. Query: per dichiarare e validare parametri di query negli endpoint FastAPI.
from app.models.event import Event #import necessario per usare la classe Event definita nel package models nel file python event.py
from typing import Annotated #funzione Annotated --> serve per validare i dati
from pydantic import ValidationError #per gestire le eccezioni

from app.models.registration import Registration
from app.models.user import User #import necessario per usare la classe User definita nel package models nel file python user.py
from app.data.db import SessionDep
from sqlmodel import select, delete

router = APIRouter(prefix="/registrations") #tutti gli endpoint definiti dentro il router inizieranno con /events

@router.get("/") #Decoratore che specifica il metodo HTTP e il percorso. Definisce un endpoint GET relativo al prefisso router. Il prefisso è /registrations, quindi questo endpoint corrisponde a GET /registrations
def get_all_registrations(
        session: SessionDep,
        sort: Annotated[bool, Query(descrption="Sort registrations by event id")]=False
) -> list[Registration]: #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint
    """Return the list of all registrations"""
    registration = session.exec(select(Registration)).all()
    return registration

@router.delete("/registrations") #decoratore FastAPI che definisce un endpoint DELETE con 2 parametri dinamici {username} e {event_id} nell'URL -> DELETE /registrations/?username={username}&event_id={event_id}
def delete_registration_by_username_and_event_id ( #Endpoint/path function = funzione associata all'endpoint. Definisce la funzione di risposta all'endpoint.
        id: Annotated[int, Query(description="The id of the event to delete")], #il tipo atteso per l'id è un intero. Path aggiunge una descrizione visibile nella documentazione Swagger.
        username: Annotated[str, Query(description="The username of the person to delete")],
        session: SessionDep
):
    """Delete the registration with the given event id and the given username""" #questa descrizione appare nella documentazione /docs
    registration = session.exec(
        select(Registration).where(Registration.username == username, Registration.id == id)).first()
    if not registration:
        raise HTTPException(status_code=404, detail=f"No registration find for user {username} or event {id}")  # 404 -> la risorsa richiesta non esiste
    session.delete(registration)
    session.commit()
    return f"Registration of {username} for event {id} deleted successfully"

