# Datei: main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# FastAPI App
app = FastAPI(
    title="NutriGuard API",
    description='Lebensmittelbeschreibung="Nährwert-Datenbank für Dialyse & Ernährungserkrankungen"',
    version="1.0.0"
)

# Lade deine CSV einmal beim Start
df = pd.read_csv("E:/VSProjekte/NutriGuard/prototyping/backend/data/dialysis.csv")

# In richtige Typen umwandeln (wichtig für JSON!)
df["kcal"] = pd.to_numeric(df["kcal"], errors="coerce")
df["protein"] = pd.to_numeric(df["protein"], errors="coerce")
df["nacl"] = pd.to_numeric(df["nacl"], errors="coerce")
df["kalium"] = pd.to_numeric(df["kalium"].astype(str).str.replace("*", "", regex=False), errors="coerce")
df["phosphate"] = pd.to_numeric(df["phosphate"].astype(str).str.replace("*", "", regex=False), errors="coerce")

# Pydantic-Modell für ein einzelnes Lebensmittel (für schöne Docs)
class FoodItem(BaseModel):
    category: str
    name: str
    kcal: float | None
    protein: float | None
    nacl: float | None
    kalium: float | None
    phosphate: float | None

# POST Endpoint – gibt alles als Array von Objekten zurück
@app.post("/api/foods", response_model=list[FoodItem])
async def get_all_foods():
    return JSONResponse(content=jsonable_encoder(df.to_dict(orient="records")))

# Optional: auch GET möglich machen (praktisch zum Testen)
@app.get("/api/foods", response_model=list[FoodItem])
async def get_all_foods_get():
    return JSONResponse(content=jsonable_encoder(df.to_dict(orient="records")))

# Starten mit: uvicorn main:app --reload