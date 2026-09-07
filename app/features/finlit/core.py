from __future__ import annotations 
import math 
from dataclasses import dataclass ,field 
from datetime import date 
from typing import Any 
@dataclass (slots =True )
class SimState :
    balance :float =100.0 
    debt :float =0.0 
    confidence :float =0.0 
    decisions :int =0 
    quality_sum :float =0.0 
    @property 
    def quality (self )->float :
        return round (self .quality_sum /self .decisions ,3 )if self .decisions else 0.0 
    def to_dict (self )->dict [str ,float ]:
        return {
        "balance":round (self .balance ,2 ),
        "debt":round (self .debt ,2 ),
        "confidence":round (self .confidence ,1 ),
        "decisions":float (self .decisions ),
        "quality":self .quality ,
        }
@dataclass (slots =True )
class ChoiceOutcome :
    money :float =0.0 
    debt :float =0.0 
    confidence :float =0.0 
    quality :float =0.0 
    def apply (self ,state :SimState )->SimState :
        state .balance =max (0.0 ,state .balance +self .money )
        state .debt =max (0.0 ,state .debt +self .debt )
        state .confidence =max (0.0 ,min (100.0 ,state .confidence +self .confidence ))
        state .decisions +=1 
        state .quality_sum +=self .quality 
        return state 
def months_to_target (target :float ,weekly :float )->int |None :
    if target <=0 :
        return 0 
    if weekly <=0 :
        return None 
    monthly =weekly *52.0 /12.0 
    return max (1 ,math .ceil (target /monthly ))
def target_date (target :float ,weekly :float ,start :date |None =None )->date |None :
    months =months_to_target (target ,weekly )
    if months is None :
        return None 
    start =start or date .today ()
    year =start .year +(start .month -1 +months )//12 
    month =(start .month -1 +months )%12 +1 
    return date (year ,month ,min (start .day ,28 ))
def progress_pct (contributed :float ,target :float )->float :
    if target <=0 :
        return 0.0 
    return round (min (100.0 ,contributed /target *100.0 ),1 )
def grade_quiz (answers :list [tuple [str ,int ]],bank :dict [str ,Any ])->dict [str ,Any ]:
    correct =0 
    for qid ,chosen in answers :
        q =bank .get (qid )
        if q and chosen ==q ["answer_index"]:
            correct +=1 
    total =len (answers )
    return {
    "correct":correct ,
    "total":total ,
    "score":round (correct /total *100.0 ,1 )if total else 0.0 ,
    }
def outcome_delta (
money :float ,debt :float ,confidence :float ,quality :float 
)->ChoiceOutcome :
    return ChoiceOutcome (money =money ,debt =debt ,confidence =confidence ,quality =quality )
