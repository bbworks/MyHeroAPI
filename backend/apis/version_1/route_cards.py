from typing import List
import re, unicodedata
from db.models.cards import Job
from db.repository.cards import create_new_job
from db.repository.cards import delete_job_by_id
from db.repository.cards import list_jobs
from db.repository.cards import retreive_job
from db.repository.cards import update_job_by_id
from db.session import get_db
from schemas.cards import JobCreate
from schemas.cards import ShowJob
from sqlalchemy.orm import Session
from db.models.users import User 
from apis.version_1.route_login import get_current_user_from_token
from fastapi import APIRouter, Header, Path, Query, status

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def api_introduction():
    return{"Guide": "Here are all of the different get requests you can make using this API."}


# -- Uses queries to find all cards within provided parameters
@router.get("/", status_code=status.HTTP_200_OK, tags=["All Cards"])
async def card_search(
        t: str | None = Query(
            default = None, 
            title = "Type", 
            description = "Query cards in database that have 'x' type. Types available: Attack, Asset, Action, Character, Foundation"
            ), 
        r: str | None =  Query(
            default = None, 
            title = "Rarity", 
            description = "Query cards in database that have 'x' rarity. Rarities available: Common, Uncommon, Rare, Ultra Rare, Starter Exclusive, Promo, Secret Rare"
            ), 
        sm: str  | None = Query(
            default = None, 
            title = "Symbol", 
            description = "Query cards in database that have 'x' symbol(s). Symbols available: Air, All, Chaos, Death, Earth, Evil, Fire, Good, Infinity, Life, Order, Void, Water"
            ),
        s: str | None = Header(
            default = None, 
            title = "Set", 
            description = "Query cards in database that are in 'x' set. Sets available: My Hero Academia, Crimson Rampage, Provisional Showdown"
            )):
    
    results = [] 

    for card in full_card_results:
        if t != None:
            if card.type_attributes["type"].upper() == t.upper():
                results.append(card)
        
        if r != None:            
            if card.rarity.upper() == r.upper():
                results.append(card)
        
        if sm != None:
            for symbol in card.symbols:
                if symbol.upper() == sm.upper():
                    results.append(card)

        if s != None:
            s = re.sub(" ","-", s)
            set = card.set
            set = re.sub(" ", "-", set)
            if set.upper() == s.upper():
                results.append(card)

    
    for card in full_prov_card_results:    
        if t != None:
            if card.type_attributes["type"].upper() == t.upper():
                results.append(card)
        
        if r != None:            
            if card.rarity.upper() == r.upper():
                results.append(card)
        
        if sm != None:
            for symbol in card.symbols:
                if symbol.upper() == sm.upper():
                    results.append(card)

        if s != None:
            s = re.sub(" ","-", s)
            set = card.set
            set = re.sub(" ", "-", set)
            if set.upper() == s.upper():
                results.append(card)
    return {"cards": sorted(results, key= lambda x:x.id)}


# -- Creates new provisional cards
#@router.post("/v1/users/me/cards", status_code=status.HTTP_201_CREATED, tags=["Normal Cards"])
#async def create_card(card: Card):
#    c = cards.put(card.dict())
#    return c

# -- List of all cards
@router.get("/cards", status_code=status.HTTP_200_OK, tags=["Normal Cards"])
async def card_list():
    return{"count": len(regular_cards), "card_list": sorted(regular_cards, key=lambda x: x.id, )}


# -- Searches for cards with either the card ID or the card Name
@router.get("/cards/{card_id}", status_code=status.HTTP_200_OK, tags=["Normal Cards"])
async def card_id(card_id: int = Path(ge=0)):
    for card in full_card_results:
        if card.id == card_id:
            return card

    return JSONResponse({"message": "card not found"}, status_code= status.HTTP_404_NOT_FOUND)

@router.get("/cards/{card_name}", tags=["Normal Cards"])
async def card_name(card_name: str):
    for card in full_card_results:
        regex_card = re.sub(" ", "_", card.name)
        print(regex_card)
        if regex_card.upper() == card_name.upper():
            return card
    return{"Data": "Not found"}


# -- Creates new provisional cards
#@router.post("/v1/users/me/prov-cards", status_code=status.HTTP_201_CREATED, tags=["Tournament Prize Cards"])
#async def create_prov_card(card: Card):
#    c = prov_cards.put(card.dict())
#    return c

# -- List of all provisional cards
@router.get("/prov-cards", status_code=status.HTTP_200_OK, tags=["Tournament Prize Cards"])
async def prov_card_list():
    return{"count": len(provisional_cards), "provisional_card_list": sorted(provisional_cards, key=lambda x: x.id)}


# -- Searches for provisional cards people win at tournaments with either the card ID or the card Name
@router.get("/prov-cards/{card_id}", status_code=status.HTTP_200_OK, tags=["Tournament Prize Cards"])
async def provisional_card_id(card_id: int = Path(ge=0)):
    for card in full_prov_card_results:
        if card.id == card_id:
            return card
    return{"Data": "Not found"}

@router.get("/prov-cards/{card_name}", status_code=status.HTTP_200_OK, tags=["Tournament Prize Cards"])
async def provisional_card_name(card_name: str):
    for card in full_prov_card_results:
        regex_card = re.sub(" ", "_", card.name)
        if regex_card.upper() == card_name.upper():
            return card
    return{"Data": "Not found"}