from pydantic import BaseModel  #per definire modelli di dati con validazione automatica
from datetime import datetime
from typing import Annotated #funzione Annotated: serve per validare i dati
from sqlmodel import SQLModel, Field #la classe SQLModel per i modelli ORM/Pydantic, la funzione Field per applicare dei vincoli sui dati

class EventBase(SQLModel): #superclasse con attributi comuni
    title: str
    description: str
    date: datetime
    location: str

class Event(EventBase, table=True):  #Definizione della classe Event. Diventa sia un modello Pydantic sia un mappatura di tabella ORM.
    #table=True specifica che si tratta di un modello relazionale, oltre che di un modello Pydantic -> Dice a SQLModel di generare anche la  tabella corrispondente del databse.
    id: int = Field(default=None, primary_key=True)

class EventCreate(EventBase): #Schema per creare un nuovo evento tramite API. Non include ID perchè il client non deve fornire la chiave primaria, verrà generata dal DB.
    pass

class EventPublic(EventBase): #Schema per restituire le info di un evento
    pass
