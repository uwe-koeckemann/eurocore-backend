from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship


# class TeamRobotLink(SQLModel, table=True):
#     team_id: Optional[int] = Field(
#         default=None, foreign_key="team.id", primary_key=True
#     )
#     robot_id: Optional[int] = Field(
#         default=None, foreign_key="robot.id", primary_key=True
#     )
