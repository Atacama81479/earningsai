from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms. validators import DataRequired, Length



class AddQueryForm(FlaskForm):
    id = IntegerField('Enter ID', validators=[DataRequired()])
    queryname = StringField('Enter Query Name', validators=[DataRequired(), Length(1, 400)])
    querycontent = StringField('Enter Query', validators=[DataRequired(), Length(1, 400)])
    submit = SubmitField('Submit')


class EditQueryForm(FlaskForm):
    querycontent = StringField('Edit Prompt Query')
    cell = StringField('Edit Spread Cell')
    submit = SubmitField('Submit')


class ChatForm(FlaskForm):
    query = StringField('Chat' )
    submit = SubmitField('Submit')

class EditSettingsForm(FlaskForm):
    companyname = StringField('Edit Company Name')
    gsheetname = StringField('Edit Sheet Name')
    gsheetno = StringField('Edit Sheet Number')
    indexname = StringField('Edit Pinecone Index Name')
    llm = StringField('OpenAi Modell')
    embedding = StringField('OpenAi Embedding')
    RAG_Prompt = StringField('RAG Prompt')
    submit = SubmitField('Submit')