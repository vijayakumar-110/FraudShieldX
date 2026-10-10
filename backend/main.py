from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import sqlite3, json, re
from urllib.parse import urlparse
DB='fraudshield.db'
app=FastAPI(title='FraudShield X API',version='1.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=False,allow_methods=['*'],allow_headers=['*'])
class AnalyzeRequest(BaseModel):
    message:str=Field(min_length=1,max_length=10000)
    source:str=Field(default='manual',max_length=50)
    sender:str|None=Field(default=None,max_length=100)
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init():
    c=conn(); c.execute('''CREATE TABLE IF NOT EXISTS detections(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT,source TEXT,sender TEXT,message TEXT,risk_score INTEGER,risk_level TEXT,category TEXT,indicators TEXT,urls TEXT)'''); c.commit(); c.close()
init()
def detect(text):
    s=text.lower(); score=0; inds=[]; cats=[]
    rules=[(['urgent','immediately','act now','last chance'],18,'Urgency'),(['otp','one time password','pin','cvv','password'],25,'Credential/OTP request'),(['account blocked','account suspended','kyc expired','verify your account'],22,'Account/KYC threat'),(['you won','congratulations','prize','lottery','reward'],18,'Prize/reward scam'),(['processing fee','registration fee','pay fee','job offer'],16,'Job/fee scam'),(['send money','transfer','pay now','payment required'],20,'Payment request'),(['investment','guaranteed return','double your money'],20,'Investment scam'),(['police','legal action','arrest','fine'],16,'Authority threat')]
    for terms,pts,label in rules:
        if any(t in s for t in terms): score+=pts; inds.append(label); cats.append(label)
    urls=re.findall(r'https?://[^\s<>\"]+',text)
    for u in urls:
        host=urlparse(u).hostname or ''
        if u.lower().startswith('http://'): score+=12; inds.append('Non-HTTPS URL')
        if any(k in host.lower() for k in ['verify','login','secure','claim','bonus','wallet']): score+=10; inds.append('Suspicious URL keyword')
        if host.count('-')>=3: score+=7; inds.append('Unusual domain structure')
    score=min(score,100); level='HIGH' if score>=60 else 'MEDIUM' if score>=30 else 'LOW'
    category=cats[0] if cats else 'No strong scam pattern detected'
    rec='Do not click links, share OTP/PIN/passwords, or send money. Verify through an official channel.' if level=='HIGH' else 'Pause and independently verify the sender, request, and link before acting.' if level=='MEDIUM' else 'No strong scam pattern was detected. Still verify unexpected requests before acting.'
    return {'risk_score':score,'risk_level':level,'category':category,'indicators':list(dict.fromkeys(inds)),'urls':urls,'recommendation':rec}
@app.get('/')
def root(): return {'name':'FraudShield X','status':'running'}
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/api/analyze')
def analyze(req:AnalyzeRequest):
    r=detect(req.message); c=conn(); c.execute('INSERT INTO detections(created_at,source,sender,message,risk_score,risk_level,category,indicators,urls) VALUES(?,?,?,?,?,?,?,?,?)',(datetime.now(timezone.utc).isoformat(),req.source,req.sender,req.message,r['risk_score'],r['risk_level'],r['category'],json.dumps(r['indicators']),json.dumps(r['urls']))); c.commit(); c.close(); return r
@app.get('/api/detections')
def detections(limit:int=50):
    c=conn(); rows=c.execute('SELECT * FROM detections ORDER BY id DESC LIMIT ?',(max(1,min(limit,200)),)).fetchall(); c.close()
    return [{**dict(x),'indicators':json.loads(x['indicators']),'urls':json.loads(x['urls'])} for x in rows]
