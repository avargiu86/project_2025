from pydantic import EmailStr
from sqlmodel import SQLModel, Field #la classe SQLModel per i modelli ORM/Pydantic, la funzione Field per applicare dei vincoli sui dati

class User(SQLModel, table=True): #Definizione della classe User. Diventa sia un modello Pydantic sia un mappatura di tabella ORM.
    #table=True specifica che si tratta di un modello relazionale, oltre che di un modello Pydantic -> Dice a SQLModel di generare anche la tabella corrispondente del databse.
    username: str = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=1) #campo obligatorio, minimo 1 parola e massimo 30
    email: EmailStr = Field(...) #campo obbligatorio, minimo una parola
