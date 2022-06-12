from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import databases
import sqlalchemy

DATABASE_URL = "postgresql://vpdkizvonqmbbh:28afd484c151b423fc65e29fa2f2511d35bf8057b248b176666783d95227acf0@ec2-54-227-248-71.compute-1.amazonaws.com:5432/d24q63i1f77asb"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

mahasiswa = sqlalchemy.Table(
    "mahasiswa",
    metadata,
    sqlalchemy.Column("npm", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("nama", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.get("/read/{npm}")
async def read_npm(npm: str):
    query = mahasiswa.select().where(mahasiswa.c.npm == npm)
    result = await database.fetch_one(query)
    return {"status":"OK", "NPM":npm, "Nama":result.nama}

