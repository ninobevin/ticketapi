from fastapi import APIRouter, Request, Header, HTTPException,Query
from models.tickets import Ticket
from database.ticket_database import ticket_collection
from faker import Faker
from examples.location_random import LocationRand 
import random
from datetime import datetime, timezone,timedelta
from typing import Optional


router = APIRouter()
faker = Faker()
random_location = LocationRand()
MANILA_TZ = timezone(timedelta(hours=8))



async def is_ticket_duplicated(ticket : Ticket):


    var_duration = 24 
    duration = datetime.utcnow() - timedelta(hours=var_duration)
    count = await ticket_collection.count_documents({"uuid" : ticket.uuid ,"created_at": {"$gte": duration}})
    
    if count > 0 :
        raise HTTPException(status_code=409,detail=f"Sorry you have pending ticket in the last 24 hours.")

@router.get("/get_my_ticket/{uuid}")
async def get_my_ticket(
            uuid: str,
            from_time: Optional[datetime] = Query(None, alias="from"),
            to_time: Optional[datetime] = Query(None, alias="to")
        ):
    
    var_duration = 24 # time duration para dai madoble ang ticket within 24hrs

    duration = datetime.utcnow() - timedelta(hours=var_duration)

    # Query MongoDB
    pending_tickets_cursor = ticket_collection.find(
        {"uuid": uuid, "created_at": {"$gte": duration}}
    )
    ticket_history_cursor = ticket_collection.find(
        {"uuid": uuid, "created_at": {"$lt": duration}}
    )

    # Convert cursor to list and map to Ticket model
    pending_tickets = [Ticket(**ticket) async for ticket in pending_tickets_cursor]
    ticket_history = [Ticket(**ticket) async for ticket in ticket_history_cursor]
    return {"ticket_history": ticket_history, "pending_ticket": pending_tickets}


@router.get("/get_all_ticket")
async def get_all_ticket(
            from_time: Optional[datetime] = Query(None, alias="from"),
            to_time: Optional[datetime] = Query(None, alias="to"),
            status: Optional[int] = Query(None, alias="status")
        ):
   
   
    print(f"From Time: {from_time}")
    print(f"To Time: {to_time}")


    # Query MongoDB
    all_tickets_cursor = ticket_collection.find(
        {"created_at": {"$gte": from_time,"$lte": to_time},"status" : status}
    )



    # Convert cursor to list and map to Ticket model
    all_ticket = [Ticket(**ticket) async for ticket in all_tickets_cursor]

    tickets = []
    for ticket in all_ticket:
        tz = ticket.created_at.astimezone(MANILA_TZ).isoformat()
        ticket.created_at = ticket.created_at.astimezone(MANILA_TZ).isoformat()  # Convert timezone
       
        # print(f"{tz}")
        tickets.append(ticket)
        
    return {"all_ticket": tickets}



@router.get("/")
async def get_tickets():
    return {"message": "Development Mode"}

@router.post("/create")
async def create_ticket(ticket : Ticket,request : Request):
    await is_ticket_duplicated(ticket)
    ticket_collection.insert_one(ticket.dict())
    return {"message" : f"new ticket with uuid {ticket.uuid} is inserted."}




@router.get("/range")
async def get_range(longitude : float,latitude : float):


    result = await find_nearby_tickets(longitude,latitude)
    all_ticket = [Ticket(**ticket) async for ticket in result]
    coordinates = [ [ticket.location.coordinates[0],ticket.location.coordinates[1]] for ticket in all_ticket ]
    return {"ticket" : coordinates}

async def find_nearby_tickets(lon, lat, max_distance=500):
    return ticket_collection.find({
        "location": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]  # Must be [longitude, latitude]
                },
                "$maxDistance": max_distance  # 500 meters
            }
        }
    })