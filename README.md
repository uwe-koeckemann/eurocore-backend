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

        uvicorn main:app --reload

- Try API in web-browser by opening URL indicated by `uvicorn` (http://localhost:8000/docs)

# Ideas / TODO

- Safe-delete for tag, relation_type, and entry
- Delete-everywhere for tag, relation_type, and entry

# Data Classes

Most data classes are split into three classes. For instance for `Entry` we have:

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
