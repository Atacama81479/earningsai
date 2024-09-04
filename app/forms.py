from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FileField
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
    query = StringField('Chat')
    submit = SubmitField('Submit')

class MultipleChatForm(FlaskForm):
    query = StringField('Chat')
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

class EditCompanynameForm(FlaskForm):
    companyname = SelectField(u'Company 1', validate_choice=False)
    companyname2 = SelectField(u'Company 2', validate_choice=False)
    companyname3 = SelectField(u'Company 3', validate_choice=False)
    submit = SubmitField('Submit')

class AddCompanynameForm(FlaskForm):
    companyname = StringField('Company Name')
    namespace_name = StringField('Namespace Name')
    submit = SubmitField('Submit')

class AddCompanyData(FlaskForm):
    presentation = FileField('Earnings Presentation')
    press_release = FileField('Earnings Press Release')
    konsens = FileField('Company Konsens Data')
    isin = StringField('Company ISIN')
    company_name  = StringField('Company Name')
    submit = SubmitField('Submit')