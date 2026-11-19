"""Bounded public-documentation Fetch; no network without --execute."""
from __future__ import annotations
import argparse
import hashlib
import ipaddress
import json
import os
import urllib.error
import urllib.request
from datetime import datetime,timezone
from urllib.parse import urlsplit

HOSTS={'api-docs.deepseek.com','platform.claude.com','docs.github.com','context7.com'}
class Blocked(RuntimeError):pass
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise Blocked('REDIRECT_REJECTED')

def checked_url(url:str,allow_hosts:list[str])->str:
    if not 1<=len(url)<=8192:raise Blocked('URL_LENGTH')
    u=urlsplit(url);h=u.hostname or ''
    if u.scheme!='https' or u.username or u.password or u.query or u.fragment or u.port not in (443,None):
        raise Blocked('PUBLIC_HTTPS_WITHOUT_CREDENTIALS_QUERY_REQUIRED')
    if h=='localhost' or h.endswith(('.local','.localhost','.internal')):raise Blocked('PRIVATE_TARGET')
    try:ipaddress.ip_address(h)
    except ValueError:pass
    else:raise Blocked('IP_LITERAL_REJECTED')
    if h not in HOSTS|set(allow_hosts):raise Blocked('HOST_NOT_ALLOWED')
    if any(ord(c)<33 for c in url):raise Blocked('URL_CONTROL_CHARACTER')
    return url

def normalize(data:dict,url:str)->dict:
    if data.get('truncated') or data.get('incomplete'):raise Blocked('SOURCE_REPORTED_INCOMPLETE')
    title,content=data.get('title'),data.get('content')
    if not isinstance(title,str) or not isinstance(content,str) or not content.strip():raise Blocked('INVALID_MARKDOWN')
    if len(content.encode())>1_000_000:raise Blocked('MARKDOWN_TOO_LARGE')
    return {'title':title,'content':content,'source_url':url,'retrieved_at':datetime.now(timezone.utc).isoformat(),
            'sha256':hashlib.sha256(content.encode()).hexdigest(),'sha256_scope':'returned_markdown_utf8',
            'verification_status':'UNVERIFIED'}

def fetch(url:str,timeout:float,allow_hosts:list[str]|None=None)->dict:
    url=checked_url(url,allow_hosts or [])
    key=os.environ.get('DEEPSEEK_API_KEY')
    if not key:raise Blocked('CREDENTIAL_BINDING_MISSING')
    if len(key)>4096 or any(ord(c)<33 or ord(c)>126 for c in key):raise Blocked('INVALID_CREDENTIAL_FORMAT')
    if not 1<=timeout<=60:raise Blocked('INVALID_TIMEOUT')
    req=urllib.request.Request('https://api.deepseek.com/v1/tools/fetch',data=json.dumps({'url':url}).encode(),
        headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=timeout) as res:
            raw=res.read(2_000_001)
            if len(raw)>2_000_000:raise Blocked('RESPONSE_TOO_LARGE')
            data=json.loads(raw)
            if not isinstance(data,dict):raise Blocked('INVALID_RESPONSE')
            return normalize(data,url)
    except urllib.error.HTTPError as e:raise Blocked(f'PROVIDER_HTTP_{e.code}_NOT_RETRIED') from None
    except (urllib.error.URLError,OSError,TimeoutError):raise Blocked('NETWORK_NOT_RETRIED') from None
    except (ValueError,TypeError):raise Blocked('INVALID_HEADER_OR_PROVIDER_RESPONSE') from None

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--url',required=True)
    p.add_argument('--allow-host',action='append',default=[]);p.add_argument('--timeout',type=float,default=30)
    p.add_argument('--execute',action='store_true');p.add_argument('--acceptance',default='');a=p.parse_args()
    try:
        url=checked_url(a.url,a.allow_host)
        if not a.execute:
            print(json.dumps({'status':'DRY_RUN','endpoint':'https://api.deepseek.com/v1/tools/fetch','url':url}));return 0
        if not a.acceptance.strip():raise Blocked('ACCEPTANCE_REQUIRED')
        print(json.dumps({'status':'RESPONSE_RECEIVED','acceptance_criterion':a.acceptance,
                          'acceptance_status':'NOT_EVALUATED',**fetch(url,a.timeout,a.allow_host)},ensure_ascii=False));return 0
    except Blocked as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)}));return 2
    except (ValueError,TypeError):
        print(json.dumps({'status':'BLOCKED','reason':'INVALID_INPUT_OR_RESPONSE'}));return 2
if __name__=='__main__':raise SystemExit(main())
