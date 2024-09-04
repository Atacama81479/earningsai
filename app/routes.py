from flask import render_template, flash
from app import app
from app.forms import AddQueryForm, EditQueryForm, EditSettingsForm, ChatForm,MultipleChatForm, EditCompanynameForm, AddCompanynameForm, AddCompanyData
from app.ai  import Createsummary, askchat, askchat2
from app.models import Prompts, SummarySettings, ChatAnswer, CompanyNames
from app import db
from app.dataupload import companyfileupload,store_pdf_from_variable
import json
import random
import uuid
import tempfile

@app.route("/hello")
def hello_world():

    return render_template('base.html')



@app.route('/edit', methods=['GET', 'POST'])
def edit():

    print("YES")
    all_prompts=Prompts.query.all()

    form = EditQueryForm()
    
    return render_template('edit.html', form=form, all_prompts=all_prompts)



@app.route('/edit/<id>', methods=['GET', 'POST'])
def editprompt(id):

    print("this is the ID"+ id)
    prompt = Prompts.query.filter_by(id=id).first_or_404()
    form = EditQueryForm()

    
    print(prompt)

    if form.validate_on_submit():
        prompt.content = form.querycontent.data
        prompt.gsheetcell = form.cell.data
        db.session.commit()
        flash('Your changes have been saved.')

    return render_template('editprompt.html', form=form, prompt=prompt)

@app.route('/', methods=['GET', 'POST'])
def createsummary():
    settings= SummarySettings.query.filter_by(id=1).first_or_404()
    companynames = CompanyNames.query.all()
    return render_template('createsummary.html', settings=settings, companynames =companynames)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    form = ChatForm()
    settings= SummarySettings.query.filter_by(id=1).first_or_404()
    res= ChatAnswer
    if form.validate_on_submit():
        query = form.query.data
        print(query)
        answer = askchat(settings, query)
        print(answer)
        res.content = answer.content
        
    return render_template('chat.html', settings=settings, form = form, res = res)

@app.route('/chat2', methods=['GET', 'POST'])
def chat2():
    settings= SummarySettings.query.filter_by(id=1).first_or_404()
    form = MultipleChatForm()
    
    res= ChatAnswer

    if form.validate_on_submit():
        query = form.query.data
        answer = askchat2(settings, query)
        res.content = answer.content
        
    return render_template('chat.html', settings=settings, form = form, res = res)




@app.route('/created', methods=['GET', 'POST'])
def created():
    query_set= Prompts.query.all()
    settings= SummarySettings.query.filter_by(id=1).first_or_404()

    Createsummary(settings, query_set)
    print("Summary created successful")
    return render_template('created.html')


@app.route('/editsettings', methods=['GET', 'POST'])
def updatesettings():
    settings= SummarySettings.query.filter_by(id=1).first_or_404()
    form = EditSettingsForm()

    if form.validate_on_submit():
        settings.companyname = form.companyname.data
        settings.gsheetname = form.gsheetname.data
        settings.gsheetno = form.gsheetno.data
        settings.indexname = form.indexname.data
        settings.llm = form.llm.data
        settings.embedding = form.embedding.data
        settings.rag_prompt = form.RAG_Prompt.data

        db.session.commit()

    return render_template('updatesettings.html', settings=settings, form = form)

@app.route('/updatecompanies', methods=['GET', 'POST'])
def updatecompanyname():
    company_names= CompanyNames.query.all()
    cn=[]
    for x in company_names:
        cn.append(x.namespace_name)

    form = EditCompanynameForm()
    form.companyname.choices = cn
    form.companyname2.choices = cn
    form.companyname3.choices = cn

   
    settings= SummarySettings.query.filter_by(id=1).first_or_404()

    if form.validate_on_submit():
        settings.companyname = form.companyname.data
        settings.companyname2 = form.companyname2.data
        settings.companyname3 = form.companyname3.data

        db.session.commit()

    return render_template('updatecompany.html', settings=settings, form =form)

@app.route('/addcompany', methods=['GET', 'POST'])
def addcompany():
    form = AddCompanynameForm()

    if form.validate_on_submit():
        uid = uuid.uuid1()
        newCompany = CompanyNames(id = uid,
                      name=form.companyname.data,
                      namespace_name=form.namespace_name.data)
        db.session.add(newCompany)
        db.session.commit()

    return render_template('addcompany.html', form =form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = AddCompanyData()
    settings= SummarySettings.query.filter_by(id=1).first_or_404()

    if form.validate_on_submit():
        uid = uuid.uuid1()
        presentation=form.presentation.data
        pressrelease=form.press_release.data
        konsens=form.konsens.data
        isin=form.isin.data
        company_name=form.company_name.data
       
        
        presentation_path=store_pdf_from_variable(presentation)
        companyfileupload(presentation_path,settings,isin,company_name)

        pressrelease_path=store_pdf_from_variable(pressrelease)
        companyfileupload(pressrelease_path,settings,isin,company_name)

        if konsens is not None:
         konsens_path=store_pdf_from_variable(konsens)
         companyfileupload(konsens_path,settings,isin,company_name)

    return render_template('addcompany.html', form =form)