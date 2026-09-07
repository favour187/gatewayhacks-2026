from __future__ import annotations 
import math 
from typing import Any 
from sqlalchemy .orm import Session 
from app .features .finlit import content ,repository 
from app .features .finlit .core import outcome_delta 
def overview (db :Session ,user_id :str )->dict [str ,Any ]:
    profile =repository .get_or_create_profile (db ,user_id )
    progress =repository .module_progress (db ,str (user_id ))
    goals =repository .list_goals (db ,str (user_id ))
    modules =[
    {
    **content .module_dict (module ),
    "progress":(
    progress .get (module .module_id ).to_dict ()
    if module .module_id in progress 
    else None 
    ),
    }
    for module in content .MODULES .values ()
    ]
    return {
    "profile":profile .to_dict (),
    "modules":modules ,
    "modules_done":sum (
    1 for m in modules if m .get ("progress")and m ["progress"]["completed"]
    ),
    "modules_total":len (modules ),
    "goals":[g .to_dict ()for g in goals ],
    "sim_history_count":len (repository .sim_history (db ,str (user_id ))),
    }
def assess (
db :Session ,user_id :str ,answers :list [dict [str ,Any ]],kind :str 
)->dict [str ,Any ]:
    profile =repository .get_or_create_profile (db ,user_id )
    bank ={q ["question_id"]:q for q in content .ASSESSMENT }
    pairs =[(a ["question_id"],int (a ["chosen_index"]))for a in answers ]
    graded =_grade_bank (pairs ,bank )
    score =graded ["score"]
    if kind =="pre":
        profile .pre_score =max (profile .pre_score ,score )
    else :
        profile .post_score =max (profile .post_score ,score )
    db .commit ()
    return {"kind":kind ,**graded ,"profile":profile .to_dict ()}
def grade_module (
db :Session ,user_id :str ,module_id :str ,answers :list [dict [str ,Any ]]
)->dict [str ,Any ]:
    module =content .MODULES .get (module_id )
    if module is None :
        raise ValueError ("unknown module_id")
    bank ={q ["question_id"]:q for q in module .quiz }
    pairs =[(a ["question_id"],int (a ["chosen_index"]))for a in answers ]
    graded =_grade_bank (pairs ,bank )
    passed =graded ["score"]>=60.0 
    row =repository .upsert_module_score (
    db ,str (user_id ),module_id ,graded ["score"],passed 
    )
    repository .touch_profile (db ,repository .get_or_create_profile (db ,str (user_id )))
    explanations =[
    {
    "question_id":q ["question_id"],
    "chosen_index":next (
    (c for qid ,c in pairs if qid ==q ["question_id"]),None 
    ),
    "correct_answer":q ["options"][q ["answer_index"]],
    "explanation":q ["explanation"],
    }
    for q in module .quiz 
    ]
    return {
    "module_id":module_id ,
    "title":module .title ,
    "passed":passed ,
    "detail":graded ,
    "explanations":explanations ,
    "progress":row .to_dict (),
    }
def simulate (
db :Session ,user_id :str ,scenario_id :str ,choice_id :str 
)->dict [str ,Any ]:
    scenario =content .SCENARIOS .get (scenario_id )
    if scenario is None :
        raise ValueError ("unknown scenario_id")
    choice =next ((c for c in scenario .choices if c ["choice_id"]==choice_id ),None )
    if choice is None :
        raise ValueError ("unknown choice_id")
    profile =repository .get_or_create_profile (db ,str (user_id ))
    state =_state_from_profile (profile )
    outcome =outcome_delta (
    choice ["money"],choice ["debt"],choice ["confidence"],choice ["quality"]
    )
    state =outcome .apply (state )
    profile .sim_balance =state .balance 
    profile .sim_debt =state .debt 
    profile .sim_confidence =state .confidence 
    profile .sim_decisions =state .decisions 
    profile .sim_quality_sum =state .quality_sum 
    repository .touch_profile (db ,profile )
    repository .record_sim_decision (
    db ,
    str (user_id ),
    scenario_id ,
    choice_id ,
    {
    "money":outcome .money ,
    "debt":outcome .debt ,
    "confidence":outcome .confidence ,
    "quality":outcome .quality ,
    },
    )
    return {
    "scenario_id":scenario_id ,
    "choice_id":choice_id ,
    "label":choice ["label"],
    "explanation":choice ["explanation"],
    "delta":{
    "money":outcome .money ,
    "debt":outcome .debt ,
    "confidence":outcome .confidence ,
    "quality":outcome .quality ,
    },
    "state":state .to_dict (),
    "history":[h .to_dict ()for h in repository .sim_history (db ,str (user_id ))],
    }
def reset_sim (db :Session ,user_id :str )->dict [str ,Any ]:
    profile =repository .get_or_create_profile (db ,str (user_id ))
    profile .sim_balance =100.0 
    profile .sim_debt =0.0 
    profile .sim_confidence =0.0 
    profile .sim_decisions =0 
    profile .sim_quality_sum =0.0 
    db .commit ()
    return profile .to_dict ()
def _state_from_profile (profile :Any )->Any :
    from app .features .finlit .core import SimState 
    return SimState (
    balance =profile .sim_balance ,
    debt =profile .sim_debt ,
    confidence =profile .sim_confidence ,
    decisions =profile .sim_decisions ,
    quality_sum =profile .sim_quality_sum ,
    )
def _grade_bank (pairs :list [tuple [str ,int ]],bank :dict [str ,Any ])->dict [str ,Any ]:
    correct =0 
    for qid ,chosen in pairs :
        q =bank .get (qid )
        if q and chosen ==q ["answer_index"]:
            correct +=1 
    total =len (pairs )
    return {
    "correct":correct ,
    "total":total ,
    "score":round (correct /total *100.0 ,1 )if total else 0.0 ,
    }
