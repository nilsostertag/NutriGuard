# Datei: main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

DATA_PATH = "E:/VSProjekte/NutriGuard/prototyping/backend/data/dialysis.csv"
DATA_PATH_ENTRIES_DIALYSIS = "E:/VSProjekte/NutriGuard/prototyping/backend/data/entries_dialysis.csv"

origins = ["http://localhost:5173"]

# FastAPI App
app = FastAPI(
    title="NutriGuard API",
    description='Lebensmittelbeschreibung="Nährwert-Datenbank für Dialyse & Ernährungserkrankungen"',
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lade deine CSV einmal beim Start
df = pd.read_csv(DATA_PATH)

# In richtige Typen umwandeln (wichtig für JSON!)
df["kcal"] = pd.to_numeric(df["kcal"], errors="coerce")
df["protein"] = pd.to_numeric(df["protein"], errors="coerce")
df["nacl"] = pd.to_numeric(df["nacl"], errors="coerce")
df["potassium"] = pd.to_numeric(df["potassium"].astype(str).str.replace("*", "", regex=False), errors="coerce")
df["phosphate"] = pd.to_numeric(df["phosphate"].astype(str).str.replace("*", "", regex=False), errors="coerce")

# Pydantic-Modell für ein einzelnes Lebensmittel (für schöne Docs)
class FoodItem(BaseModel):
    food_id: int 
    name: str
    category: str
    kcal: float 
    protein: float 
    nacl: float 
    potassium: float 
    phosphate: float 

class FoodSubmission(BaseModel):
    datetime: str
    user_id: str
    food_id: int 
    amount: int

@app.post("/api/foods", response_model=list[FoodItem])
async def get_all_foods():
    return JSONResponse(content=jsonable_encoder(df.to_dict(orient="records")))

@app.post("/api/submitfood")
async def submit_food(food: FoodSubmission):
    df_temp = pd.DataFrame(food)
    df_temp = df_temp.transpose()
    df_temp.columns = df_temp.iloc[0]  # erste Zeile wird zu Spaltennamen
    df_temp = df_temp[1:]  # erste Zeile entfernen, da sie jetzt als Header dient
    #print(df_temp.columns)
    #print(df_temp)
    df_old = pd.read_csv(DATA_PATH_ENTRIES_DIALYSIS)
    #print(df_old)
    df = pd.concat([df_old, df_temp], ignore_index=True)
    #print(df)
    df.to_csv(DATA_PATH_ENTRIES_DIALYSIS, index=False)

@app.post("/api/registeruser", response_model=list[FoodItem])
async def get_all_foods():
    return JSONResponse(content=jsonable_encoder(df.to_dict(orient="records")))

@app.post("/api/confirmregistration", response_model=list[FoodItem])
async def get_all_foods():
    return JSONResponse(content=jsonable_encoder(df.to_dict(orient="records")))

# Starten mit: uvicorn main:app --reload