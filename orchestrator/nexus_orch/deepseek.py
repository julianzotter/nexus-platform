"""Bounded DeepSeek requests with explicit mode; no credential logging."""
from __future__ import annotations
import json
import urllib.error
import urllib.request
from typing import Any
from .credentials import CredentialError, resolve_key

BASE='https://api.deepseek.com'
class DeepSeekError(RuntimeError):
    pass

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req:Any,fp:Any,code:int,msg:str,headers:Any,newurl:str)->None:
        raise DeepSeekError('DEEPSEEK_REDIRECT_REJECTED')

def request_json(path:str,key:str,payload:dict[str,Any]|None=None,timeout:float=45)->dict[str,Any]:
    if path not in ('/models','/chat/completions','/v1/tools/fetch'):
        raise DeepSeekError('ENDPOINT_NOT_ALLOWED')
    if not 1<=timeout<=60:raise DeepSeekError('INVALID_TIMEOUT')
    data=None if payload is None else json.dumps(payload).encode()
    req=urllib.request.Request(BASE+path,data=data,headers={
        'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='GET' if payload is None else 'POST')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=timeout) as res:
            raw=res.read(2_000_001)
            if len(raw)>2_000_000:raise DeepSeekError('RESPONSE_TOO_LARGE')
            value=json.loads(raw)
            if not isinstance(value,dict):raise DeepSeekError('INVALID_RESPONSE')
            return value
    except urllib.error.HTTPError as exc:
        raise DeepSeekError(f'DEEPSEEK_HTTP_{exc.code}') from None
    except (urllib.error.URLError,OSError,TimeoutError,ValueError):
        raise DeepSeekError('DEEPSEEK_NETWORK_OR_RESPONSE_ERROR') from None

def complete(cfg:dict[str,Any],prompt:str,system:str,key:str)->dict[str,Any]:
    if cfg.get('model') not in ('deepseek-flash','deepseek-v4-pro'):raise DeepSeekError('MODEL_NOT_ALLOWED')
    if cfg.get('base_url','').rstrip('/')!=BASE:raise DeepSeekError('BASE_URL_NOT_ALLOWED')
    mode=cfg.get('thinking',{}).get('type')
    effort=cfg.get('reasoning_effort')
    if mode not in ('enabled','disabled') or effort not in ('none','low','high','max'):
        raise DeepSeekError('EXPLICIT_THINKING_AND_EFFORT_REQUIRED')
    if (mode=='disabled')!=(effort=='none'):raise DeepSeekError('THINKING_EFFORT_CONFLICT')
    cap=cfg.get('max_tokens',2048)
    if type(cap) is not int or not 1<=cap<=4096:raise DeepSeekError('INVALID_OUTPUT_CAP')
    if not prompt.strip() or len(prompt)+len(system)>32000:raise DeepSeekError('INVALID_INPUT_SIZE')
    messages=([{'role':'system','content':system}] if system else [])+[{'role':'user','content':prompt}]
    payload={'model':cfg['model'],'messages':messages,'thinking':{'type':mode},
             'reasoning_effort':effort,'max_tokens':cap,'stream':False}
    data=request_json('/chat/completions',key,payload,cfg.get('timeout',45))
    choices=data.get('choices')
    if not isinstance(choices,list) or len(choices)!=1 or not isinstance(choices[0],dict):
        raise DeepSeekError('INVALID_CHOICES')
    choice=choices[0];message=choice.get('message',{})
    if not isinstance(message,dict):raise DeepSeekError('INVALID_MESSAGE')
    if choice.get('finish_reason')!='stop' or message.get('tool_calls'):
        raise DeepSeekError('NON_TEXT_OR_INCOMPLETE_RESPONSE')
    text=message.get('content')
    if not isinstance(text,str) or not text.strip():raise DeepSeekError('EMPTY_TEXT')
    return {'text':text,'citations':[],'model':data.get('model',cfg['model']),
            'usage':data.get('usage'),'verification_status':'UNVERIFIED'}

def models_probe(store:str|None='dsh')->dict[str,Any]:
    try:
        key=resolve_key('DEEPSEEK_API_KEY',store)
        data=request_json('/models',key)
        rows=data.get('data')
        if not isinstance(rows,list):raise DeepSeekError('INVALID_MODELS_RESPONSE')
        return {'status':'AUTHENTICATED','http_status':200,
                'models':[r['id'] for r in rows if isinstance(r,dict) and isinstance(r.get('id'),str)]}
    except (CredentialError,DeepSeekError) as exc:
        reason=str(exc)
        return {'status':'BLOCKED','http_status':401 if reason=='DEEPSEEK_HTTP_401' else None,'reason':reason}
