from __future__ import annotations 
from fastapi import APIRouter ,Depends 
from pydantic import BaseModel ,Field 
from sqlalchemy .orm import Session 
from app .core .auth import User ,get_current_user 
from app .core .db import get_db 
from app .core .errors import NotFoundError ,ValidationFailedError 
from app .features .finlit import content ,repository ,service 
router =APIRouter (prefix ="/finance",tags =["finance"])
class AnswerIn (BaseModel ):
    question_id :str =Field (min_length =1 )
    chosen_index :int =Field (ge =0 ,le =5 )
class AssessIn (BaseModel ):
    kind :str =Field (pattern ="^(pre|post)$")
    answers :list [AnswerIn ]=Field (min_length =1 )
class GradeModuleIn (BaseModel ):
    answers :list [AnswerIn ]=Field (min_length =1 )
class SimulateIn (BaseModel ):
    scenario_id :str =Field (min_length =1 )
    choice_id :str =Field (min_length =1 )
class GoalIn (BaseModel ):
    name :str =Field (min_length =1 ,max_length =120 )
    target :float =Field (gt =0 )
    weekly :float =Field (ge =0 )
    apy :float =Field (default =0.0 ,ge =0 ,le =30 )
class ContributeIn (BaseModel ):
    amount :float =Field (gt =0 )
@router .get ("/overview")
def overview (
user :User =Depends (get_current_user ),db :Session =Depends (get_db )
)->dict :
    return service .overview (db ,str (user .id ))
@router .post ("/assess")
def assess (
payload :AssessIn ,
user :User =Depends (get_current_user ),
db :Session =Depends (get_db ),
)->dict :
    return service .assess (
    db ,str (user .id ),[a .model_dump ()for a in payload .answers ],payload .kind 
    )
@router .get ("/modules")
def modules (
user :User =Depends (get_current_user ),db :Session =Depends (get_db )
)->dict :
    progress =repository .module_progress (db ,str (user .id ))
    return {
    "modules":[
    {
    **content .module_dict (module ),
    "progress":(
    progress [module .module_id ].to_dict ()
    if module .module_id in progress 
    else None 
    ),
    }
    for module in content .MODULES .values ()
    ]
    }
@router .get ("/modules/{module_id}")
def module (
module_id :str ,
user :User =Depends (get_current_user ),
db :Session =Depends (get_db ),
)->dict :
    module =content .MODULES .get (module_id )
    if module is None :
        raise NotFoundError ("Module not found.")
    progress =repository .module_progress (db ,str (user .id ))
    return {
    **content .module_dict (module ),
    "quiz":content .quiz_public (module ),
    "progress":progress [module_id ].to_dict ()if module_id in progress else None ,
    }
@router .post ("/modules/{module_id}/grade")
def grade_module (
payload :GradeModuleIn ,
module_id :str ,
user :User =Depends (get_current_user ),
db :Session =Depends (get_db ),
)->dict :
    try :
        return service .grade_module (
        db ,str (user .id ),module_id ,[a .model_dump ()for a in payload .answers ]
        )
    except ValueError as exc :
        raise ValidationFailedError (str (exc ))from exc 
@router .get ("/sim")
def sim (user :User =Depends (get_current_user ),db :Session =Depends (get_db ))->dict :
    profile =repository .get_or_create_profile (db ,str (user .id ))
    return {
    "state":profile .to_dict ()["sim"],
    "wallet":{
    "balance":profile .sim_balance ,
    "debt":profile .sim_debt ,
    },
    "scenarios":[content .scenario_dict (s )for s in content .SCENARIOS .values ()],
    "history":[h .to_dict ()for h in repository .sim_history (db ,str (user .id ))],
    }
@router .post ("/simulate")
def simulate (
payload :SimulateIn ,
user :User =Depends (get_current_user ),
db :Session =Depends (get_db ),
)->dict :
    try :
        return service .simulate (
        db ,str (user .id ),payload .scenario_id ,payload .choice_id 
        )
    except ValueError as exc :
        raise ValidationFailedError (str (exc ))from exc 
@router .post ("/sim/reset")
def sim_reset (
user :User =Depends (get_current_user ),db :Session =Depends (get_db )
)->dict :
    return service .reset_sim (db ,str (user .id ))
@router .get ("/goals")
def goals (
user :User =Depends (get_current_user ),db :Session =Depends (get_db )
)->dict :
    return {"goals":[g .to_dict ()for g in repository .list_goals (db ,str (user .id ))]}
@router .post ("/goals",status_code =201 )
def create_goal (
payload :GoalIn ,
user :User =Depends (get_current_user ),
db :Session =Depends (get_db ),
)->dict :
    goal =repository .create_goal (
    db ,str (user .id ),payload .name ,payload .target ,payload .weekly ,payload .apy 
    )
    repository .touch_profile (db ,repository .get_or_create_profile (db ,str (user .id )))
    return goal .to_dict ()
@router .post ("/goals/{goal_id}/contribute")
def contribute (
goal_id :str ,
payload :ContributeIn ,
user :User =Depends (get_current_user ),
db :Session =Depends (get_db ),
)->dict :
    goal =repository .get_goal (db ,str (user .id ),goal_id )
    if goal is None :
        raise NotFoundError ("Goal not found.")
    repository .add_contribution (db ,goal ,payload .amount )
    repository .touch_profile (db ,repository .get_or_create_profile (db ,str (user .id )))
    return goal .to_dict ()
