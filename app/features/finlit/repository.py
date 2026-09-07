from __future__ import annotations 
import json 
import math 
import uuid 
from datetime import date ,datetime ,timedelta 
from sqlalchemy import ForeignKey ,String ,Text ,Uuid ,select 
from sqlalchemy .orm import Mapped ,Session ,mapped_column ,relationship 
from app .core .db import Base ,TimestampsMixin ,UUIDMixin ,iso_utc ,utcnow 
class FinProfile (UUIDMixin ,TimestampsMixin ,Base ):
    __tablename__ ="finlit_profiles"
    user_id :Mapped [str ]=mapped_column (String (64 ),unique =True ,index =True )
    pre_score :Mapped [float ]=mapped_column (default =0.0 )
    post_score :Mapped [float ]=mapped_column (default =0.0 )
    sim_balance :Mapped [float ]=mapped_column (default =100.0 )
    sim_debt :Mapped [float ]=mapped_column (default =0.0 )
    sim_confidence :Mapped [float ]=mapped_column (default =0.0 )
    sim_decisions :Mapped [int ]=mapped_column (default =0 )
    sim_quality_sum :Mapped [float ]=mapped_column (default =0.0 )
    last_activity :Mapped [date ]=mapped_column (default =date .today )
    streak :Mapped [int ]=mapped_column (default =0 )
    def to_dict (self )->dict :
        quality =(
        round (self .sim_quality_sum /self .sim_decisions ,3 )
        if self .sim_decisions 
        else 0.0 
        )
        return {
        "id":str (self .id ),
        "pre_score":self .pre_score ,
        "post_score":self .post_score ,
        "score_gain":round (max (0.0 ,self .post_score -self .pre_score ),1 ),
        "streak":self .streak ,
        "sim":{
        "balance":round (self .sim_balance ,2 ),
        "debt":round (self .sim_debt ,2 ),
        "confidence":round (self .sim_confidence ,1 ),
        "decisions":self .sim_decisions ,
        "quality":quality ,
        },
        }
class ModuleProgress (UUIDMixin ,Base ):
    __tablename__ ="finlit_module_progress"
    user_id :Mapped [str ]=mapped_column (String (64 ),index =True )
    module_id :Mapped [str ]=mapped_column (String (64 ),index =True )
    best_score :Mapped [float ]=mapped_column (default =0.0 )
    attempts :Mapped [int ]=mapped_column (default =0 )
    completed :Mapped [bool ]=mapped_column (default =False )
    completed_at :Mapped [datetime |None ]=mapped_column (default =None )
    def to_dict (self )->dict :
        return {
        "module_id":self .module_id ,
        "best_score":self .best_score ,
        "attempts":self .attempts ,
        "completed":self .completed ,
        "completed_at":iso_utc (self .completed_at )if self .completed_at else None ,
        }
class SimHistory (UUIDMixin ,Base ):
    __tablename__ ="finlit_sim_history"
    user_id :Mapped [str ]=mapped_column (String (64 ),index =True )
    scenario_id :Mapped [str ]=mapped_column (String (64 ))
    choice_id :Mapped [str ]=mapped_column (String (64 ))
    delta_json :Mapped [str ]=mapped_column (Text ,default ="{}")
    created_at :Mapped [datetime ]=mapped_column (default =utcnow )
    def to_dict (self )->dict :
        return {
        "id":str (self .id ),
        "scenario_id":self .scenario_id ,
        "choice_id":self .choice_id ,
        "delta":json .loads (self .delta_json )if self .delta_json else {},
        "created_at":iso_utc (self .created_at ),
        }
class GoalEntity (UUIDMixin ,TimestampsMixin ,Base ):
    __tablename__ ="finlit_goals"
    user_id :Mapped [str ]=mapped_column (String (64 ),index =True )
    name :Mapped [str ]=mapped_column (String (120 ))
    target :Mapped [float ]=mapped_column (default =0.0 )
    weekly :Mapped [float ]=mapped_column (default =0.0 )
    apy :Mapped [float ]=mapped_column (default =0.0 )
    status :Mapped [str ]=mapped_column (String (16 ),default ="active")
    contributions :Mapped [list ["Contribution"]]=relationship (
    back_populates ="goal",cascade ="all, delete-orphan"
    )
    def contributed (self )->float :
        return sum (c .amount for c in self .contributions )
    def to_dict (self )->dict :
        from app .features .finlit .core import months_to_target ,progress_pct ,target_date 
        contributed =self .contributed ()
        months =months_to_target (self .target ,self .weekly )
        return {
        "id":str (self .id ),
        "name":self .name ,
        "target":self .target ,
        "weekly":self .weekly ,
        "apy":self .apy ,
        "status":self .status ,
        "contributed":round (contributed ,2 ),
        "remaining":round (max (0.0 ,self .target -contributed ),2 ),
        "progress":progress_pct (contributed ,self .target ),
        "months_to_target":months ,
        "target_eta":(
        target_date (self .target ,self .weekly ).isoformat ()if months else None 
        ),
        "contributions":[c .to_dict ()for c in self .contributions ],
        "created_at":iso_utc (self .created_at ),
        }
class Contribution (UUIDMixin ,Base ):
    __tablename__ ="finlit_contributions"
    goal_id :Mapped [uuid .UUID ]=mapped_column (
    Uuid ,ForeignKey ("finlit_goals.id"),index =True 
    )
    amount :Mapped [float ]=mapped_column (default =0.0 )
    created_at :Mapped [datetime ]=mapped_column (default =utcnow )
    goal :Mapped [GoalEntity ]=relationship (back_populates ="contributions")
    def to_dict (self )->dict :
        return {
        "id":str (self .id ),
        "amount":self .amount ,
        "created_at":iso_utc (self .created_at ),
        }
def get_or_create_profile (db :Session ,user_id :str )->FinProfile :
    profile =db .scalar (select (FinProfile ).where (FinProfile .user_id ==user_id ))
    if profile is None :
        profile =FinProfile (user_id =user_id )
        db .add (profile )
        db .commit ()
        db .refresh (profile )
    return profile 
def touch_profile (db :Session ,profile :FinProfile )->None :
    today =date .today ()
    if profile .last_activity ==today :
        return 
    if profile .last_activity ==today -timedelta (days =1 ):
        profile .streak +=1 
    else :
        profile .streak =1 
    profile .last_activity =today 
    db .commit ()
def module_progress (db :Session ,user_id :str )->dict [str ,ModuleProgress ]:
    rows =db .scalars (select (ModuleProgress ).where (ModuleProgress .user_id ==user_id ))
    return {r .module_id :r for r in rows }
def upsert_module_score (
db :Session ,user_id :str ,module_id :str ,score :float ,passed :bool 
)->ModuleProgress :
    row =db .scalar (
    select (ModuleProgress ).where (
    ModuleProgress .user_id ==user_id ,ModuleProgress .module_id ==module_id 
    )
    )
    if row is None :
        row =ModuleProgress (
        user_id =user_id ,
        module_id =module_id ,
        attempts =0 ,
        best_score =0.0 ,
        completed =False ,
        )
        db .add (row )
    row .attempts +=1 
    row .best_score =max (row .best_score ,score )
    if passed :
        row .completed =True 
        row .completed_at =row .completed_at or utcnow ()
    db .commit ()
    db .refresh (row )
    return row 
def record_sim_decision (
db :Session ,user_id :str ,scenario_id :str ,choice_id :str ,delta :dict 
)->None :
    db .add (
    SimHistory (
    user_id =user_id ,
    scenario_id =scenario_id ,
    choice_id =choice_id ,
    delta_json =json .dumps (delta ),
    )
    )
    db .commit ()
def sim_history (db :Session ,user_id :str )->list [SimHistory ]:
    rows =db .scalars (
    select (SimHistory )
    .where (SimHistory .user_id ==user_id )
    .order_by (SimHistory .created_at .desc ())
    )
    return list (rows )
def list_goals (db :Session ,user_id :str )->list [GoalEntity ]:
    rows =db .scalars (
    select (GoalEntity )
    .where (GoalEntity .user_id ==user_id )
    .order_by (GoalEntity .created_at .desc ())
    )
    return list (rows )
def create_goal (
db :Session ,user_id :str ,name :str ,target :float ,weekly :float ,apy :float =0.0 
)->GoalEntity :
    goal =GoalEntity (user_id =user_id ,name =name ,target =target ,weekly =weekly ,apy =apy )
    db .add (goal )
    db .commit ()
    db .refresh (goal )
    return goal 
def get_goal (db :Session ,user_id :str ,goal_id :str )->GoalEntity |None :
    return db .scalar (
    select (GoalEntity ).where (
    GoalEntity .id ==uuid .UUID (goal_id ),GoalEntity .user_id ==user_id 
    )
    )
def add_contribution (db :Session ,goal :GoalEntity ,amount :float )->Contribution :
    row =Contribution (goal_id =goal .id ,amount =amount )
    db .add (row )
    db .commit ()
    db .refresh (row )
    return row 
