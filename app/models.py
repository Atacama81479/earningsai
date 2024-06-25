from app import db

class Prompts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    gsheetcell = db.Column(db.String(400), nullable=False)


class SummarySettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(80), nullable=False)
    gsheetname = db.Column(db.String(400), nullable=False)
    gsheetno = db.Column(db.String(400), nullable=False)
    indexname = db.Column(db.String(400), nullable=False)
    llm = db.Column(db.String(400), nullable=False)
    embedding = db.Column(db.String(400), nullable=False)
    rag_prompt = db.Column(db.String(400), nullable=False)

class ChatAnswer():
    content = ""
    context =[]
    value =""