from itertools import product
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from dbConn import conn

from datetime import date

app = FastAPI()

class Drivers(BaseModel):
    DriverLicense: int
    FirstName: str
    LastName: str


@app.get("/drivers/all/nomodel")
def get_all_drivers():
    cursor = conn.cursor()
    cursor.execute("SELECT DriverLicense, FirstName, LastName FROM Driver LIMIT 50")
    result = cursor.fetchall()
    return {"drivers": result}

@app.get("/drivers/all", response_model=List[Drivers])
def get_driver():
    cursor = conn.cursor()
    query = "SELECT DriverLicense, FirstName, LastName FROM Driver LIMIT 50"
    cursor.execute(query)

    item = cursor.fetchall()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item = [Drivers(DriverLicense=driveritem[0], FirstName=driveritem[1], LastName=driveritem[2]) for driveritem in item]
    return item

@app.get("/drivers/{driver_license}", response_model=Drivers)
def get_driver(driver_license: int):
    cursor = conn.cursor()
    query = "SELECT DriverLicense, FirstName, LastName FROM Driver WHERE DriverLicense=%s"
    cursor.execute(query, (driver_license,))
    
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"DriverLicense": item[0], "FirstName": item[1], "LastName": item[2]}
