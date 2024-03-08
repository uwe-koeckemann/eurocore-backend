# EuroCore Backend

API for the EuroCore including end-points to manage coopetitions.
Used to track teams, robots, and modules for running a coopetition.

## How to Run

- Optional: Create conda environment

        conda create --name eurocore python=3.8
        conda activate eurocore
            
- Install requirements

        pip install -r requirements.txt
        
- Start API server

        uvicorn euro_core_backend.main:app --reload

- Try API in web-browser by opening URL indicated by `uvicorn` (http://localhost:8000/docs)

- The database is currently SQLite and will be stored in a file called `database.db` in this folder

# Ideas / TODO

- Safe-delete for tag, relation_type, and entry
- Delete-everywhere for tag, relation_type, and entry

# Data Classes (Database Tables)

## Entry

Can represent a module, a team, a library, a map, a service on the web, a tutorial, a datasheet, a paper, or anything 
else deemed useful. Uses tags to describe the type of content and what we can do with it.

- Name
- URL
- Description
- Tags

## Tag

Property of an entry. Can represent a standard, file format, type of entry (e.g., Team), robotics key-words. 

*Naming convention:* upper case words, seperated by underscore (_) if needed. Example:

- Map
- Robot_Manipulation
- SLAM

## Relation Type

Possible relationship between entries and its inverse. Topics will be used as headers on the web.

- Name
- Inverse name
- Topic
- Inverse topic

*Naming convention:* lower case words, seperated by underscore (_) if needed. Example:

- offers
- offered_by
- used_by
- tutorial_of

## Relation

Instance of a relation. Connects a relation type to two entries. 

- Relation type id: key of the relation type
- From id: key of the source entry
- To id: key of the target entry

## Team Tokens

Links a team entry to a token counter for a coopetition.

## Module Offer

Links a team entry to a module entry as an offer in a coopetion.

- team_id
- module_id
- cost: token cost of the module
- integration_support: indicates if offering team offers integration support
- integration_cost: token cost of integration support

# Module Usage

Indicates that a team used a module offer by another team.

- consumer_team_id
- module_offer_id
- bought: if the module was bought
- bought_support: if support was bought
- using: if the module is in use
- rating: a rating
- review: a review (up for 500 characters)

# Implementation Notes

## Splitting Data Classes

Data classes are split into up to three classes (depending on the need). For instance for `Entry` we have:

- `EntryBase`: basic data used for creation (does not include the database key
  which will be created for us)
- `Entry`: inherits from `RobotBase` only adding robot_id as a primary key. This
  class will be the actual table
- `EntryUpdate`: all fields are optional so we can update any part of an entry
  without having to specify the old values

# Resources

- Fast API documentation: https://fastapi.tiangolo.com/
- SQLModel documentation: https://sqlmodel.tiangolo.com/

# Acknowledgments

This work is part of the euROBIN project funded by the European Union's Horizon
Europe Framework Programme under grant agreement No 101070596. See
https://www.eurobin-project.eu/
