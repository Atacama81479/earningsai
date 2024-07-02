import os
import json
import pygsheets
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough


def Createsummary(settings, query_set):

    load_dotenv()
    Gcredentialpath = os.getenv('PATH_TO_CREDENTIALS') 
    gsheetnr = int(settings.gsheetno)
    gsheetname = settings.gsheetname
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    print("Retrieving...")

    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings)
    
    
    print(gsheetname) 

    print("Testing LLM...")
    query = "how was q1 of alfen?"
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input = {})


    print("setting up Vectorstore...")
    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings)

    print("connect with google...")
    gc = pygsheets.authorize(service_file= Gcredentialpath)
    sheet= gc.open(gsheetname)


    wks = sheet[gsheetnr]
    

    print("creating rag_chain...")
                
    template =  """
    """+ rag_promt+"""

    {context}

    Question: {question}

    Helpful Answer:
    """
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = ( 
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()} 
        | custom_rag_prompt
        | llm
    )



    
    print("creating Summary...")

    #Ausblick



    for x in query_set:
        company = companyname
        query= str(x.content)
        query = query.format(company)
    

        gsheetcell = x.gsheetcell
        res = rag_chain.invoke(query)
        wks.update_value( gsheetcell, res.content)

    return "Summary created"

    #Incomestatement



def askchat(settings, query):
    load_dotenv()
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm

    query= str(query)
    query = query.format(companyname)


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)




    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings.companyname)


    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings)



                
    template =  """
    """+ rag_promt+"""

    {context}

    Question: {question}

    Helpful Answer:
    """
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = ( 
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()} 
        | custom_rag_prompt
        | llm
    )


    print(rag_chain)
    print(query)

    res = rag_chain.invoke(query)

    print(res)

    return res

def askchat2(settings, query):
    load_dotenv()
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm
    context = str("""Greetings and welcome to the Jabil Third Quarter of Fiscal Year 20 24 Earnings Call. At this time, all participants are in a listen only mode. A brief question and answer session will follow the formal presentation. As a reminder, this conference is being recorded. It is now my pleasure to introduce your host, Adam Berry, Vice President of Investor Relations. Thank you. You may begin.

    Good morning, and thank you for joining Jabil's Q3 fiscal 2024 earnings call. Joining me on today's call are Chief Financial Officer, Greg Hebert and Chief Executive Officer, Mike Dastoor. Over the next few minutes, we will review the following: review our Q3 results, provide an update on current demand, and preview our 7th annual virtual investor briefing. Before we begin, please note that today's call is being webcast live. And during our prepared remarks, we will be referencing slides. To follow along with the slides, please visit jabil.com within the Investor Relations portion of the website. At the conclusion of today's call, the entirety of today's presentation will be posted for audio playback. I'd now ask that you view the slides on the website and follow along with our presentation, beginning with the forward looking statement. During this conference call, we will be making forward looking statements, including among other things, those regarding the anticipated outlook for our business. These statements are based on current expectations, forecasts and assumptions involving risks and uncertainties that could cause actual outcomes and results to differ materially. An extensive list of these risks and uncertainties are identified in our annual report on Form 10 ks for the fiscal year ended August 31, 2023 and other filings with the SEC.

    Jabil disclaims any intention or obligation to update or revise any forward looking statements, whether as a result of new information, future events or otherwise. With that, I'll now hand the call over to Greg.

    Thanks, Adam. Good morning, everyone. It's a great privilege to be a part of the call today. I like to begin this morning by walking through our Q3 results, where the team delivered approximately $6,800,000,000 in revenue, $265,000,000 above the midpoint of the guidance range on better than expected growth in our connected devices and networking and storage end markets. Core operating income for the quarter came in at $350,000,000 or 5.2 percent of revenue, an improvement of 40 basis points year over year. Net interest expense for Q3 came in better than expected at $64,000,000 This was due to lower levels of inventory during the quarter, reflecting improved working capital management by the team. From a gas perspective, operating income was $261,000,000 and our GAAP diluted earnings per share was 1.06 dollars Core diluted earnings per share was $1.89 $0.04 above the midpoint of our guidance range. Now turning to our performance by segment in the quarter. Revenue for the DMS segment came in at $3,400,000,000 $65,000,000 above our expectations, driven by better than expected growth within our connected devices business, offset slightly by the lower than anticipated revenue in our Automotive and Healthcare businesses. On a year over year basis, our DMS segment revenue was down approximately 23%, driven primarily by the mobility divestiture.

    Core operating margins for the segment came in at 4.6%, 50 basis points higher than the same quarter from a year ago, reflective of the ongoing mix shift within our DMS business. Revenue for our EMS segment came in at $3,400,000,000 approximately $200,000,000 above our expectations, driven by higher than anticipated revenue in our networking and storage end markets in the quarter. Compared to the prior year quarter, EMS revenue was down roughly 18%, driven mainly by lower revenue in end markets like 5 gs, Renewable Energy and Digital Print, offset slightly by good growth in cloud. For the quarter, core margins for the EMS segment came in at 5.7%, up 20 basis points year over year. Next, I'd like to begin with an update on our cash flow and balance sheet metrics. Inventory at the end of Q3 came in 6 days lower sequentially at 81 days. Net of inventory deposits from our customers, inventory days were 58, which was a quarter on quarter improvement of 4 days. As a result of the team's good working capital management in the quarter, our Q3 cash flows from operations came in quite strong at $515,000,000 while net capital expenditures totaled $100,000,000 resulting in $450,000,000 in adjusted free cash flow during the quarter.

    In Q3, we repurchased 3,700,000 shares for approximately $500,000,000 leaving us with approximately $700,000,000 remaining on our current $2,500,000,000 share repurchase authorization as of May 31. We remain fully committed to completing the share repurchase authorization by the end of FY 2024. We exited Q3 with a healthy and solid balance sheet with debt to core EBITDA levels of approximately 1.2 times and cash balances of approximately $2,500,000,000 And as a management team, we are fully committed to maintaining our investment grade credit profile. With that, let's turn to the next slide for our Q4 guidance. For Q4, we expect total company revenue to be in the range of $6,300,000,000 to $6,900,000,000 Core operating income for Q4 is estimated to be in the range of $365,000,000 to $425,000,000 GAAP operating income is expected to be in the range of $285,000,000 to $355,000,000 Core diluted earnings per share is estimated to be in the range of $2.03 to $2.43 GAAP diluted earnings per share is expected to be in the range of $1.40 to 1.88 Net interest expense in the 4th quarter is estimated to be approximately $67,000,000 And our core tax rate for Q4 is expected to be 20%. Before moving to our full year guidance on the next slide, I'd like to provide a brief update on our net interest expense and core tax rate beyond FY 2024.

    Now anticipate interest rates to remain elevated and expect our net interest expense to remain at FY 2024 levels in FY 2025 and be approximately $275,000,000 And for core tax rate in FY 'twenty five, we anticipate our core tax rate will be impacted by Pillar 2 global minimum tax legislation. We will be required to adopt this only in FY 2025. We are evaluating the impact this will have as we sit today, we anticipate our core tax rate in FY 2025 to be in the range of 22% to 24%. Now moving on to full year guidance on the next slide. For the year, we continue to expect $28,500,000,000 in revenue in the face of what continues to be a very dynamic demand environment. Compared with our thoughts in March, our expectations for growth in our automotive and transportation business has softened further. In particular, the market in China has been impacted due to overcapacity resulting in a surplus of cars affecting local demand there. And new global EV platforms that we originally expected to begin launching in the next 100 days or so have now shifted out several quarters. On the healthcare side, we see softness in medical devices, which we expect will create a headwind to revenue in the near term.

    These declines were offset by strength in connected devices and our AI data center end markets, which today are reported across industrial, cloud and networking end markets. All other end markets are largely in line with previous expectations. Given this updated end market outlook, let's move to the next slide to review our FY 'twenty four guidance. We continue to expect core margins for the year to come in at 5.6 percent, a 60 basis point improvement over the prior year. We also expect to deliver EPS of $8.40 for the year. And importantly, we remain committed to generating over $1,000,000,000 in adjusted free cash flow this year. With that, I'd like to thank you for your time this morning and your interest in Jabil. I'll now turn the call over to Mike.

    Thanks, Greg. Good morning and thank you for joining our call today. Before I jump into my prepared remarks, a couple of comments. I am truly humbled by the trust placed in me by Mark and the Jabil Board. For the past 24 years, Jabil has the company's journey from $3,000,000,000 in $2,000,000 to $28,000,000,000 is a true testament to the care we offer our customers. As CEO, I'm excited and carry a tremendous amount of gratitude to steward an amazing team. As Greg highlighted, the team has executed well in FY 2024 amid a dynamic environment. Consider this, we divested our mobility business, a key strategic decision. We're capturing growth in the AI data center space and we're working towards our commitment to repurchase $2,500,000,000 of our shares, all while dealing with end market softness in renewables, EVs and semi cap equipment, which we expect to be short term in nature. Yet when you take a step back and put it all together, the company remains resilient and on track. And we expect to deliver on key metrics, including 5.6% core margins and strong free cash flow in excess of $1,000,000,000 on $28,500,000,000 of revenue. More importantly, we remain well positioned to benefit from many of the world's powerful trends in areas like AI data center infrastructure, healthcare, pharma solutions and automated warehousing to name a few.

    At the end of the day, the world needs complex manufacturing to enable innovation in nearly everything we do in our everyday lives. Jabil is at the forefront of providing solutions around a rapidly evolving technology landscape with complex supply chains in an ever changing geopolitical environment. As a management team, it's incumbent upon us to ensure we're focused on the right end markets with the most innovative customers, thereby delivering incredible solutions. And I think it's safe to say we're right in the middle of that ecosystem today. Moving ahead, we'll continue to reshape our diversified portfolio and remain focused on growing new and existing value added businesses, driving margins and generating free cash flow. Let me share where I've been spending my time over the last 6 to 8 weeks. I've been focused on our customers, our investors, our suppliers and our people. Some of the key takeaways are as follows. From a structure standpoint, I've chosen an organizational approach that has served us well over the last decade with an intense focus on speed, precision and solutions. This focused approach, I believe targets our ability serve each distinct market effectively by creating domain expertise in our core areas and better positions Jabil for growth.

    From a capital allocation standpoint, we will remain committed to returning value to our shareholders by prioritizing organic investments in our business and aggressively pursuing share buybacks at attractive valuation levels. This balanced approach ensures that we can reward our shareholders while simultaneously investing in next generation capabilities. All the while, we will take care of our customers and suppliers while treating our people here at Jabil with respect. Turning to the business side of things. As you recall on May 20th, we choose to rescind our FY 'twenty five guidance. And it's worth noting, there was no singular issue that led to that CUP decision, but rather three key factors. For starters, many of the end markets we serve remain soft and the timing of recovery in these end markets remains unclear, particularly in EVs and semi cap equipment. We also expect to accelerate reshaping our portfolio away from end markets and geographies with less attractive risk and financial outcomes. As a result, our revenue in FY '25 may be negatively impacted by approximately $800,000,000 However, this will set us up to be a much stronger company in the years to come. And lastly, in FY 2025, we now expect interest expense and the tax rate to be higher due to a push out of interest rate card expectations and the global minimum tax that Greg noted earlier.

    Over the next couple of months, the management team will be spending a lot of time reviewing our plans for FY 'twenty five and beyond. And in September, I fully anticipate providing a full year outlook per usual with our normal color and commentary surrounding our strategy, the end markets we serve and our anticipated capital allocation methodology for the year. From an end market standpoint, you will hear how we've aligned technology driven capabilities in our intelligent infrastructure business to help not only hyperscalers, but also silicon providers accelerate their own technology. Our manufacturing model leverages our automation capabilities to navigate the rapid growth in AI demand. How we're prioritizing growth in certain end markets like healthcare and energy infrastructure. How we're helping retailers automate solutions in both the retail environment as well as warehousing to robotics. We'll also offer color on the businesses we anticipate deemphasizing in the future. And of course, we'll do our best to provide our expectations around a roadmap for the timing of recovery in key areas like renewables, semi cap, electric vehicles, connected devices and 5 gs. And when you put this all together, we'll describe how the seasonality has changed and how the capital intensity of our business has improved and the subsequent free cash flows we will generate given our new mix of business.

    I am confident that the roadmap we developed will propel Jabil towards an even brighter future. I can assure you that all of these actions will remain squarely focused on driving margins higher in the long run and generating robust sustainable cash flow, all while taking care of our customers, suppliers and people. Jabil's success is not the result of individual efforts, but rather a collective achievement of our entire team. Looking ahead, I'm excited about the long term trajectory of the company. We have a strong track record, a talented and dedicated leadership team and a clear vision for the future. Together, we will continue to drive innovation, deliver value to our shareholders and execute for our customers. Before handing the call over to Adam, I would like to take a moment to say thank you to the entire Jabil team for your commitment and dedication to our customers, communities and to each other. Thank you for your time and for your interest in Jabil. I'll now hand the call over to Adam.

    Thanks Mike, Greg, and congratulations to each of you on well deserved new roles. I look forward to working alongside both of you. Before we move into our Q and A session, I'd like to take a few minutes to broadly summarize some of our key messages you heard today. First off, our fiscal 'twenty four outlook is on track with the update we provided in March and subsequently reiterated in May. Notably, this includes $8.40 in core EPS, 5.6% core margins and $1,000,000,000 plus in free cash flow. And as we move through Q4, we fully anticipate completing the balance of our $2,500,000,000 share repurchase authorization. As we turn our attention to the end markets, we remain fully committed to our year over year growth plans in our AI data center end markets in both fiscal 2024 and 2025, which today are reported across our cloud, networking and industrial end markets. At the same time, we're actively evaluating our portfolio to see if there's any opportunity to further optimize as Mike just described. And for early modeling purposes, please keep in mind that our seasonality in fiscal 2025 will be reflective of the mobility divestiture. As such, our quarterly earnings progression will be more like that of our EMS business, where we typically earn 40% in the first half of the year and 60% in the second half of the year.

    Interest expense in fiscal 'twenty five, although rate dependent, is shaping up to be approximately $275,000,000 And our core tax rate is expected to increase from fiscal 2024 to fiscal 2025 as a result of Pillar 2 global minimum tax legislation. And finally, and just generally speaking, Jabil remains extremely well positioned to benefit from a recovery in many of the end markets that have proven to be headwinds in fiscal 'twenty four. And while the timing remains uncertain, the ultimate recovery will lead to solid revenue growth, further margin expansion and even more cash flow generation on an already installed capacity. We look forward to updating you on these matters and more on our 7th annual investor briefing, which is tentatively scheduled for September 26. Operator, we're now ready for Q and A.

    Thank you. The floor is now open for questions.

    QNA

    Today's first question is coming from Ruplu Bhattacharya. Please go ahead.

    Hi. Thanks for taking my questions. Mike and Greg, congrats on your new assignments. Mike, what do you see as the biggest opportunity for Jabil over the next year? And what do you see as the biggest risk? And Greg, similar question to you as CFO, what are your main focus areas for the next year?

    Thanks, Ruplu. I think you're aware I've been CFO for 6 years. And during this time, my focus areas have always been and always will continue to be margins and free cash flow and utilization of that free cash flow for buyback purposes. We still do think we're undervalued. So that's a key area of capital allocation that will continue well with the focus on margins, continuous focus on free cash flow. We're in all the right sort of end markets as well. So from an opportunity standpoint, are there end markets that we're not in? Yes, we'll be looking into that. That's one of the reasons we're structured the way we are in the new organization. But right now, yes, there's some softness in some of our end markets. But over the long term, these end markets are ripe for recovery. And I'm not suggesting that happens in the next 1 or 2 quarters. I think we have seen some of that shifting the recovery shifting to the right. Overall, from an opportunity perspective, I think the key is when does this whole AI proliferation in almost everything we do. So we're a hardware company. AI is going to require hardware refreshes across the board and we're paying in almost all the right end markets.

    So I do expect that entire AI proliferation to be a tailwind for us. So that happened in the next 1 or 2 quarters, perhaps not. Right now it's more data center focused. But over the long run, I do expect that to proliferate across the entire range of end markets we serve. From a risk standpoint, Ruffalo, I think it's the timing of the recovery. I think there's various anecdotes outside externally, internally, some would suggest things some would suggest things are recovering a little bit slower than we anticipated. Some suggest that it might be okay. So we'll take this time over the next 3 or 4 months to figure out our plan. That was one of the reasons we rescinded our FY 'twenty five guidance and we'll provide much more color on our analyst briefing in at the end of September. Yes. Hi, Ruplu. This is Greg. Just to reiterate some of the things Mike just said, definitely expanding operating margins, it will be a key focus, continuing to generate strong free cash flows as you saw quite a strong Q3 we had. And then return capital to shareholders, we continue to be super thoughtful on this and believe share repurchase is still a great use of our cash for Jabil.

    Okay, got it. Mike, you talked about AI. I mean, when I look at things, AI is getting to be a very competitive space. And so how do you see Jabil's investments in AI trending over the next few years? And do you think margins on the AI side trend lower or higher than the rest of the business given the increased competition?

    So I think you're absolutely right. There is a large amount of competition, Ruffalo. Today, if you think about where we play in AI, it's mainly around the server equipment. As we look at data center, building infrastructure, we're looking at power, we're looking at cooling, We're looking at value add services around some of these data center pieces as well. So there will be a margin sort of will slow down, but it'll start picking up again over time as we start expanding around an AI data center driven strategy. So we're looking at other pieces in the periphery along the lines of silicon photonics. We're looking at OSAT packaging. So there's a whole bunch of things that we look at from an AI perspective. And I think margin does it's not going to go jump up quite a bit right now, but it'll go down and come back up pretty fast.

    Okay. Maybe I'll try and sneak one more in. You talked about some weakening of the auto and the healthcare space. And also on semi cap, I think you've said that it's weaker than expected. When do you expect a recovery in these? And if revenues continue to be weak, what are some of the levers you have to continue to drive margins and free cash flow? I think you've said margins are a focus. So what are some of the levers you have on the margin and free cash flow side even if revenues are weak? Thanks for taking my questions.

    Right. So let me try and answer your auto question first. I think in auto we are seeing some weakness particularly as it relates to China. I think there's an oversupply situation there. That does impact manufacturing for us local to local and local to Asia, sorry, local for export purposes as well. So we're seeing some push out in the whole EV recovery space because of this situation in China. From a semi cap standpoint, we I think our initial expectation was a full scale recovery in December or January in December 2024 or January 2025. That's pushing out a little bit to the right. And I think you'll see a little bit of a weird situation there where China is a dominant player right now. There is sell through into China, but a lot of that sell through is coming from existing inventory. So we expect a Jabil impact to start around the middle of calendar year 2020 5. From a margin standpoint, Ruplu, we do expect all of these end markets to start coming back at some point or the other. So it's not a we're not in a full blown recession where we go and completely close down facilities and take down costs because we lose out when the recovery does come through.

    So you might see some level of temporary margin impact there, but overall trajectory and our position when the recovery starts will extremely strong. And I'll give you an example. I think today we're probably capacitized for about $30,000,000,000 $33,000,000,000 of revenue. And if you look at in FY 2025, obviously, it'd be considerably lower than that. So we'll have a little bit of surplus capacity. We do want to take that out. I don't think the answer is take capacity out.

    I think we're going to wait for that recovery to come back and there might be some level of temporary margin impact, but long term really well positioned.

    Okay. Thanks for all the details. Congrats again on the new assignments.

    Thanks, Ru.

    Thank you. The next question is coming from Steven Fox of Fox Advisors. Please go ahead.

    Hi, good morning and congrats Mike and Greg on your appointments. I guess I had two questions. First of all, just following up on these last comments, Mike, I mean the guidance for Q4 implies you hit that magical 6% operating margin number. So I'm just curious if you could put that number into context. You just described a lot of seasonality and some mixed markets. So like how sustainable is 6% as more of a Q4 number versus like something that's ongoing you think out the next year? And then I had a follow-up.

    Yes. So thanks, Dave. First of all, I do think there is an amount of seasonality that we see in almost every single Q4. So you'll see margins go up because of that for sure. And I think Adam highlighted even FY 2020 5 when we think about that, we expect the second half going forward second half to be much more than the first half of the year because of our mobility divestiture. There is some level still of fixed cost recoveries and when you have fixed cost recoveries, but no revenue flowing through, there is definitely a bit of a margin impact. I do think I don't think 6% is what we're going to be seeing. It's not sustainable in Q1. If you look at historical seasonality, Q1 things go down, Q2 is consistent with Q1. And then we see another sort of Q3 and Q4 uptick in margins. So 6%, I would say, had a little bit of one offs in it and is not sustainable for the first half of the year, but Q3, Q4 of next year, you'll see similar sort of seasonality from a margin perspective.

    Great. That's helpful. And then in terms of your prepared remarks, I guess there's one area I was hoping you could dig into a little bit. You mentioned with your second point, some reshaping geographically end market is on the table now for next year. Can you just sort of expand on what you saw in your last 6 to 8 weeks that makes you want to sort of, I guess, change strategy just incrementally a little bit? Thanks.

    Sure. So Steve, I've always been focused on margins and free cash flow. I think you've seen that over the last 6 years. We continue to prioritize margins and cash flow. If we see some level of accounts where the 1 or 2 of these metrics don't shape up too well, we're looking at it from a reshaping our portfolio sort of away from some of those end markets and geographies as well with less sort of attractive risk and financial outcomes. So it's spread out a little bit. I would look at legacy networking as one of the areas where you see this the legacy networking going down. You will see the AI piece replacing some of that. So you'll see an increase in AI, but you'll see a little bit of a decrease on the legacy networking piece as well. Again, this positions us really well. So I'm not saying margins will jump up in 2025 because of this, but over the long term in FY 2026 and beyond, the margin structure will improve along with better cash flows. I think Greg talked about free cash flows coming in really strong in Q3. We continue to be focused on our free cash flows going forward because that's where we think the valuation lies is in the free cash flow.

    Great. That's helpful. Thank you.

    Thank you. The next question is coming from George Wang of Barclays. Please go ahead.

    Congrats on the new role. So I have 2 parts. Firstly, you mentioned the 3Q driven by connected devices and the networking storage. You also raised the 4 year forecast subsequently for the 2 segments. Just can you talk about kind of what's driving better kind of results and outlook for the connected devices and networking? Just is this a kind of industry growth or kind of share gains?

    I think it's probably neither of those. It was a little bit of conservative forecasting from our perspective. If you see connected devices over the last maybe a couple of years. Post COVID, it's been a little bit down and we've always sort of tried to make sure that our forecasts are accurate. In this particular instance, the numbers came in. I don't think we're seeing a big jump up in the end market, but I think the whole impact in Q3 was mainly because of the conservative forecasting that we sort of anticipate.

    Got you. Just a quick follow-up, if can. I just want to confirm, it's still RMB6 1,000,000,000 AI revenue for FY 'twenty five. You guys talked about in the prepared market, didn't really change the forecast. So I just want to confirm it's still RMB6 1,000,000,000. But also like I just want to hone in on the power and the cooling. You guys talked about some of the value added, obviously, power cooling has been massive shortage with higher margins. So can you talk about your differentiation and some of the initiatives on table from Jabil standpoint to capture the coming inherent sort of shortage and the kind of the demand associated with power and cooling in the data center?

    Let me hit the power and cooling question first. One of the things we are seeing in the data center space, the legacy data centers are going through a retrofit. And that retrofit, we were looking at capabilities there where we can offer services to data centers from a cooling distribution unit perspective. If you look at new deployments, the legacy ones are more liquid to air. The newer deployments are liquid to liquid cooling. We have internal capabilities around that. And be continuing to look at small capability driven transactions in that space as well. The key here is to expand our service around server integration and into the whole data center building infrastructure as well. And we I think that will be a big differentiator. Okay. Thank you. Thanks, Joe.

    Thank you. The next question is coming from Matt Sheerin of Stifel. Please go ahead.

    Yes. Thanks. Good morning, everyone. I wanted to drill down a little bit more on your commentary on networking, the strength, but also the customer base. You indicated that you may walk away from some of the legacy business. I'm guessing you're talking about the traditional OEM market. But I know that you've got a growing data center and hyper scale customer base, particularly on the server side. But are you also working with those customers on network products like switches? And could you tell us exactly what you're doing for those partners on the networking side?

    Yes. So I think that's a great question. I think you're absolutely right. It's the legacy piece from the networking side that we're sort of walking away from a lot of that is being replaced anyways by future forward looking AI, liquid cool sort of switches. We're definitely getting involved in that. We're looking at if you look at our silicon photonics piece, we're looking at the whole transceiver business, which gets attached to that space quite a bit as well. So overall networking and storage, think of it as a transition where we're transitioning from a legacy network to a new era of networking and switching. And we're going to be playing heavily on the new networking and switching. At the same time, the legacy business will go down a bit.

    Okay. And then in the networking side, we're seeing some of your peers have an ODM model where they're actually doing custom work for customers and others are building to customers' design. Are you going through both routes or mostly on the more traditional EMS side?

    Well, I think it will be a hybrid. We're not going full OEM at this stage. Definitely going to continue in the EMS space. Historically, we've stayed away from competing directly with our customers and we'll continue to do that, Matt.

    Okay, great. Thank you. And just turning to the balance sheet and your forecast for that higher interest net interest expense next year are basically flattish. Could you just talk through the capital allocation? I know you've done aggressive buybacks significant, but why not take down some of the short term borrowings or some of your debt to reduce that? And also, if you look at your inventory, inventory days, they've come down a lot, but they're still well above where they were post pandemic. So is there work to be done in terms of inventory or the working capital to bring that net interest expense down?

    Yes. Hi, this is Greg. So yes, I think there's a few parts to that question. I'd say first on interest expense and share buyback, we definitely look at the 2 combined and making sure we have the most effective EPS results from that. Interest expense, we do see rates continuing to stay elevated for most of the calendar 2024 and into 2025. So being conservative on that number. From working capital perspective, I think we've been doing a really good job. We do see our debt inventory in the 55 to 60 day range. And do we and we do see some cyclicality of that during the year and inter quarter. So obviously, this quarter, we had a good number that hit. But one thing to remind you as well, we do have inventory deposits that does offset some of that pickup when we do just look at our gross DII coming down. So we're continuing to be very focused on net inventory and getting it down closer to 55%, but there is some dollars share authorization in Q4. We do need a new Board authorization as we go into 2025. So stay tuned for that, but looking to get our WASSO into the $110,000,000 to $113,000,000 range by the end of FY 2025.

    And Matt, if I can just add provide some more color on the interest. If you go back to FY 2023, so not this year, but previous years, our interest was in the range of $150,000,000 I think if you look over time, it was in that range. I'm not suggesting we go back to $150,000,000 Today it's at $275,000,000 But as interest rates start coming down and we have a full year impact of that more towards the end of our calendar year 2025, you'll see interest start going down quite a bit as well because 275 is not going to be the norm. It's going to continue to go downwards. It won't go back to $1.50 but a low 200s is highly possible. And all of that just drops directly to the EPS line.

    Got it. Okay. Thank you for that. And just if I can just sneak in a last question regarding that $800,000,000 headwind you talked about for next year, most of that coming from and demand weakness. But is there a part of that also coming from deselecting customers, as you said, as you prune the portfolio. Could you break that down for us?

    All of that comes from deselecting, not deselecting, but renegotiating with customers. It's coming down. I think the number I provided was $800,000,000 That is part of our strategy. Like I mentioned before, margins and free cash flow continue to be front and center of everything we do. And we just it's reshaping our portfolio sort of away from end markets and geographies with less attractive risk and financial outcomes. So it's all that I think I mentioned legacy networking being one of the big ones there. So it's all driven by literally reshaping the numbers. I think if you look at all the other end markets, they are more than soft. I'd say the recovery the timing of that recovery has been pushed out is continuing to be pushed out a little bit. So the other end markets will be down, but there is no reshaping going on around that and that $800,000,000 that I referenced was purely a reshaping number. There will be some level of revenue impact as the timing of recovery gets shifted to the right as well.

    That's very helpful to clarify. And I would imagine that $800,000,000 revenue is that margin and return profile is below your company average. So that would be accretive in other words to the business.

    Absolutely. I'm not again, I'm not suggesting FY '25 will see a big accretion because of that. I talked about us being capacitized for $32,000,000,000 $33,000,000,000 of revenue. Our revenues are going to be considerably short of that. So we will have a little bit of open capacity, but we need that capacity when things start to recover. And I think it will be very shortsighted of us to go and address that incremental capacity that we have today. So yes, there will be margin accretion in these businesses overall from a company standpoint. Just keep in mind that there is a little bit of an overcapacity situation right now as well. But think of that as an opportunity. When situation right now as well. But think of that as an opportunity. When things start coming back, it will have a big margin impact. And does that happen towards the end of 2025? Does that happen in FY 2026? We just don't know right now. And that's why we've asked for a little bit more time and that's why we withdrew our FY 20 25 guidance. We will provide more color in at the end of September to the best of our abilities.

    Got it. Okay. Thanks so much.

    Thank you. The next question is coming from Mark Delaney of Goldman Sachs. Please go ahead.

    Yes. Good morning and thanks for taking my questions. First, a follow-up on the 800 $1,000,000 of revenue that the company is looking to deselect. Can you help us better understand what the margin profile is of that? I know you said it's below the corporate average, but is it just above breakeven, low single digits, slightly below corporate average? Any more color on the EBIT margin associated with the $800,000,000 would be helpful.

    It's south of Enterprise margin. It's not just the margin. We look at the free cash flow profile as well that both of those metrics are critical for our success. I think the one of the things we're looking at is risk as well. So obviously the financial metrics have to tie out. The risk has to tie out as well, risk in different parts of the world, risk in the end markets that are seeing a downward trend or being replaced by a new perspective. So it's all of that work and the margin will be south as I was mentioning on the previous question from Matt. Don't expect margins to jump up from 25% because of this. There is a little bit of an overcapacity situation. So the margin does get impacted and it's over time. I do expect maybe towards the end of FY20 25 or even in FY2026 to see a pickup in margin because of this. So it's a mid to long term payback or a return.

    Helpful color. Thanks for that, Mike. And then my second question was around hybrids. You mentioned in the presentation that you have some ability to grow with hybrids, not just with bevs. Can you double click a little bit more, talk to us around where Jabil is participating in hybrids? And to what extent you have the design wins that would support growth in hybrids as some of the traditional OEMs are planning to grow faster in hybrids over the next few years? Thanks.

    So I think when I talked about EVs, I think the point I was trying to make was that we're almost agnostic to whether it's EVs that succeed or hybrids that succeed. And I think if you look at some of the 3 or 4 areas that we participate in, I think it's software defined vehicles. That applies across combustion, hybrids and EVs. If you look at the battery management systems and everything to do with the battery, It equally applies to EVs and hybrids. If you look at some of the connectivity piece, again, it applies to all 3 categories of automotive. And then if you look at automated driving with optics, cameras, with a whole bunch of ADAS technologies, again agnostic to which technology wins out. We still think EVs is right for a comeback. I think it's seeing some temporary sort of impact due to price, due to battery range. Just couple of those issues being resolved and EVs will be back again. But the point I was trying to make is look, we're going to have a EV or a hybrid. When EVs go down and hybrids go up, there'll always be a little bit of a timing difference as we win programs in the hybrid space for them to come online.

    But the long term trajectory for our EV business is actually quite agnostic in terms of which technology wins out.

    Thank you.

    Thank you. The next question is coming from Samik Chatterjee of JPMorgan. Please go ahead.

    Hi. Thanks for taking my question. This is NP on for Samik Chatterjee. So I just wanted to ask like you had included outlook around connected devices, networking storage, 5 gs, cloud, etcetera. So a lot of AI revenue is recognized in these end markets, I believe. So I just wanted to check how much of the increase in the outlook is because of AI versus traditional recovery in the end markets? And I have a follow-up.

    So in the other end markets, I think Greg talked about the 3 that are impacting us today from an AI perspective. On the other end markets, I think it's a little too early for us to start sort of assuming AI pieces in there. I think AI is definitely coming. AI is definitely going to impact all of those end markets. Hardware refresh cycles will take place in a number of our end markets, but our assumptions won't bake that inward right now. As we see it coming forward, we will start putting some of that in. But the answer direct answer to your question is there's very little. There's almost no AI in any of the other end markets at this stage. Okay. And another one will be on operating expenses. I believe since the revenues were quite higher than the midpoint of the guidance this quarter, but operating expenses, which is something which I believe drove the operating margins to be below the midpoint of guidance. So what exactly was driving the higher operating expenses? And what's your confidence on bringing this to track for strong 6% margin next quarter? Thank you.

    Yes. Hi, Sameek. It's really a mix that we're seeing recently. So we again, some seasonality to that, but all that is related to mix.

    Samik, did you have additional questions?

    Thank you. There's no questions.

    Thanks, Devin.

    The next question is coming from David Vogt of UBS. Please go ahead.

    Hi, this is Andrew on for David. I wanted to ask a question about your wireless business. As we've moved past the elections in India, have you seen any signs that that business might pick back up?

    At this stage, not really. I think there's been a mass scale deployment of 5 gs already in India. I think there's definitely I think there's a hope today monetize that and move forward after they've seen some returns. So they're almost I think there's 75%, 80% sort of rolled out. I don't think we have some big assumptions of post election recovery in India at this stage.

    Got it. And I just also wanted to follow-up on the comments about the softness you saw in the healthcare segment. I think you said it was in the medical devices part of that business. I'm just wondering if you could expand on what was driving that softness? Is it macro? What are you seeing there?

    So when we say softness, just note that it's just one of the 4 or 5 things that we do in the entire healthcare space. I think if you look at the GLP-one drugs, they're off the charts. They just keep going higher and higher and higher. There's no and we're really well positioned to play in that space. There is a counter sort of impact, obviously, that impacts surgeries, medical devices. But there's a whole bunch of other things that we do as well from a diagnostic orthopedic standpoint, from a pharma solutions standpoint, from other medical devices. So it's smaller impact. I wouldn't Greg called it out. I think it was an issue specifically for our FY 2024. We're seeing some short term headwinds there because of that. But don't forget the GLP-one piece will continue to grow. I think the only sort of constraint is capacity, putting that capacity in place, which takes a little bit of time due to the heavy automation that's involved on the GLP-one piece.

    Thank you.

    Thank you. At this time, I would like to turn the floor back over to management for any additional or closing comments.

    That's it for this call. Thank you very much. If you have any further questions, please reach out. We will be happy to talk. Thank you.

    Ladies and gentlemen, this concludes today's event. You may disconnect your lines or log off the webcast at this time and enjoy the rest of your day.



    NEWS RELEASE

    Jabil Posts Third Quarter Results
    6/20/2024
    ST. PETERSBURG, Fla.--(BUSINESS WIRE)-- Today, Jabil Inc. (NYSE: JBL), reported preliminary, unaudited nancial
    results for its third quarter of scal year 2024.
    “It's clear that Jabil has navigated a period of signi cant transformation this scal year: a year in which we divested
    our Mobility business, captured growth in the AI datacenter space, and experienced softness across multiple endmarkets,” said CEO Mike Dastoor. “Despite these moving pieces, we remain on track to deliver 5.6% in core margins
    and $8.40 of core diluted EPS in FY24, while generating more than $1 billion in adjusted free cash ow. At the same
    time, we’ve been working towards our commitment to repurchase $2.5 billion of our shares. And importantly, in the
    mid-to-longer-term we remain well-positioned to bene t from many of the world’s powerful trends in areas like
    datacenter power and cooling, electric and hybrid vehicles, healthcare and pharma solutions, semi-cap equipment,
    and automated warehousing to name a few,” he concluded.

    Third Quarter of Fiscal Year 2024 Highlights:

    • Net revenue: $6.8 billion
    • U.S. GAAP operating income: $261 million
    • U.S. GAAP diluted earnings per share: $1.06
    • Core operating income (Non-GAAP): $350 million
    • Core diluted earnings per share (Non-GAAP): $1.89

    Fourth Quarter of Fiscal Year 2024 Outlook:

    • Net revenue
    • U.S. GAAP operating income
    • U.S. GAAP diluted earnings per share
    • Core operating income (Non-GAAP)(1)
    • Core diluted earnings per share (Non-GAAP)(1)

    $6.3 billion to $6.9 billion
    $285 million to $355 million
    $1.40 to $1.88 per diluted share
    $365 million to $425 million
    $2.03 to $2.43 per diluted share

    1

    __________________
    (1) Core operating income and core diluted earnings per share exclude anticipated adjustments of $12 million for amortization of intangibles (or
    $0.09 per diluted share) and $18 million for stock-based compensation expense and related charges (or $0.14 per diluted share) and $50 million
    to $40 million (or $0.40 to $0.32 per diluted share) for restructuring, severance and related charges.

    Fiscal Year 2024 Outlook:

    • Net revenue
    • Core operating margin (Non-GAAP)
    • Core diluted earnings per share (Non-GAAP)
    • Adjusted free cash ow (Non-GAAP)

    $28.5 billion
    5.6%
    $8.40 per diluted share
    $1+ billion

    (De nitions: “U.S. GAAP” means U.S. generally accepted accounting principles. Jabil de nes core operating
    income as U.S. GAAP operating income less amortization of intangibles, stock-based compensation expense and
    related charges, restructuring, severance and related charges, distressed customer charges, loss on disposal of
    subsidiaries, settlement of receivables and related charges, impairment of notes receivable and related charges,
    goodwill impairment charges, business interruption and impairment charges, net, gain from the divestiture of
    businesses, acquisition and divestiture related charges, plus other components of net periodic bene t cost. Jabil
    de nes core earnings as core operating income, less loss on debt extinguishment, loss (gain) on securities, other
    components of net periodic bene t cost, income (loss) from discontinued operations, gain (loss) on sale of
    discontinued operations and certain other expenses, net of tax and certain deferred tax valuation allowance
    charges. Jabil de nes core diluted earnings per share as core earnings divided by the weighted average number of
    outstanding diluted shares as determined under U.S. GAAP. Jabil de nes adjusted free cash ow as net cash
    provided by (used in) operating activities less net capital expenditures (acquisition of property, plant and equipment
    less proceeds and advances from sale of property, plant and equipment). Jabil reports core operating income, core
    earnings, core diluted earnings per share and adjusted free cash ow to provide investors an additional method for
    assessing operating income, earnings, diluted earnings per share and free cash ow from what it believes are its
    core manufacturing operations. See the accompanying reconciliation of Jabil’s core operating income to its U.S.
    GAAP operating income, its calculation of core earnings and core diluted earnings per share to its U.S. GAAP net
    income and U.S. GAAP earnings per share and additional information in the supplemental information.)

    Forward Looking Statements: This release contains forward-looking statements, including those regarding

    our anticipated nancial results for our third quarter of scal year 2024 and our guidance for future nancial
    performance in our fourth quarter of scal year 2024 (including, net revenue, U.S. GAAP operating income, U.S.
    GAAP diluted earnings per share, core operating income (Non-GAAP), core diluted earnings per share (Non-GAAP)
    results and the components thereof, including but not limited to amortization of intangibles, stock-based
    compensation expense and related charges and restructuring, severance and related charges); and our full year
    2024 (including net revenue, core operating margin (Non-GAAP), core diluted earnings per share (Non-GAAP) results
    and Adjusted Free Cash Flow (Non-GAAP)) and our plans to repurchase stock. The statements in this release are
    based on current expectations, forecasts and assumptions involving risks and uncertainties that could cause actual
    outcomes and results to di er materially from our current expectations. Such factors include, but are not limited to:
    our determination as we nalize our nancial results for our third quarter of scal year 2024 that our nancial
    results and conditions di er from our current preliminary unaudited numbers set forth herein; unexpected costs or
    unexpected liabilities that may arise from the Mobility transaction; scheduling production, managing growth and
    capital expenditures and maximizing the e ciency of our manufacturing capacity e ectively; managing rapid
    declines or increases in customer demand and other related customer challenges that may occur; the e ect of
    COVID-19 on our operations, sites, customers and supply chain; our dependence on a limited number of
    customers; our ability to purchase components e ciently and reliance on a limited number of suppliers for critical
    2

    components; risks arising from relationships with emerging companies; changes in technology and competition in
    our industry; our ability to introduce new business models or programs requiring implementation of new
    competencies; competition; transportation issues; our ability to maintain our engineering, technological and
    manufacturing expertise; retaining key personnel; risks associated with international sales and operations,
    including geopolitical uncertainties; energy price increases or shortages; our ability to achieve expected pro tability
    from acquisitions; risk arising from our restructuring activities; issues involving our information systems, including
    security issues; regulatory risks (including the expense of complying, or failing to comply, with applicable
    regulations; risk arising from design or manufacturing defects; risk arising from compliance, or failure to comply,
    with environmental, health and safety laws or regulations and intellectual property risk); nancial risks (including
    customers or suppliers who become nancially troubled; turmoil in nancial markets; tax risks; credit rating risks;
    risks of exposure to debt; currency uctuations; and asset impairment); changes in nancial accounting standards
    or policies; risk of natural disaster, climate change or other global events; and risks arising from expectations
    relating to environmental, social and governance considerations. Additional factors that could cause such
    di erences can be found in our Annual Report on Form 10-K for the scal year ended August 31, 2023 and our
    other lings with the Securities and Exchange Commission. We assume no obligation to update these forwardlooking statements.

    Supplemental Information Regarding Non-GAAP Financial Measures: Jabil provides supplemental,

    non-GAAP nancial measures in this release to facilitate evaluation of Jabil’s core operating performance. These
    non-GAAP measures exclude certain amounts that are included in the most directly comparable U.S. GAAP
    measures, do not have standard meanings and may vary from the non-GAAP nancial measures used by other
    companies. Management believes these “core” nancial measures are useful measures that facilitate evaluation of
    the past and future performance of Jabil’s ongoing operations on a comparable basis.
    Jabil reports core operating income, core earnings, core diluted earnings per share and adjusted free cash ows to
    provide investors an additional method for assessing operating income, earnings, earnings per share and free cash
    ow from what it believes are its core manufacturing operations. Among other uses, management uses non-GAAP
    nancial measures to make operating decisions, assess business performance and as a factor in determining
    certain employee performance when determining incentive compensation.
    The Company determines an annual normalized tax rate (“normalized core tax rate”) for the computation of the
    non-GAAP (core) income tax provision to provide better consistency across reporting periods. In estimating the
    normalized core tax rate annually, the Company utilizes a full-year nancial projection of core earnings that
    considers the mix of earnings across tax jurisdictions, existing tax positions, and other signi cant tax matters. The
    Company may adjust the normalized core tax rate during the year for material impacts from new tax legislation or
    material changes to the Company’s operations.
    Detailed de nitions of certain of the core nancial measures are included above under “De nitions” and a
    reconciliation of the disclosed core nancial measures to the most directly comparable U.S. GAAP nancial
    measures is included under the heading “Supplemental Data” at the end of this release.

    Meeting and Replay Information: Jabil will hold a conference call today at 8:30 a.m. ET to discuss its earnings
    for the third quarter of scal year 2024. To access the live audio webcast and view the accompanying slide
    presentation, visit the Investor Relations section of Jabil’s website, located at https://investors.jabil.com. An
    archived replay of the webcast will also be available after completion of the call.

    About Jabil: At Jabil (NYSE: JBL), we are proud to be a trusted partner for the world's top brands, o ering

    3

    comprehensive engineering, manufacturing, and supply chain solutions. With over 50 years of experience across
    industries and a vast network of over 100 sites worldwide, Jabil combines global reach with local expertise to deliver
    both scalable and customized solutions. Our commitment extends beyond business success as we strive to build
    sustainable processes that minimize environmental impact and foster vibrant and diverse communities around the
    globe. Discover more at www.jabil.com.

    JABIL INC. AND SUBSIDIARIES
    CONDENSED CONSOLIDATED BALANCE SHEETS
    (in millions)

    Current assets:
    Cash and cash equivalents
    Accounts receivable, net
    Contract assets
    Inventories, net
    Prepaid expenses and other current assets
    Assets held for sale
    Total current assets
    Property, plant and equipment, net
    Operating lease right-of-use asset
    Goodwill and intangible assets, net
    Deferred income taxes
    Other assets
    Total assets

    May 31, 2024
    (unaudited)

    ASSETS

    LIABILITIES AND EQUITY

    Current liabilities:
    Current installments of notes payable and long-term debt
    Accounts payable
    Accrued expenses
    Current operating lease liabilities
    Liabilities held for sale
    Total current liabilities
    Notes payable and long-term debt, less current installments
    Other liabilities
    Non-current operating lease liabilities
    Income tax liabilities
    Deferred income taxes
    Total liabilities
    Commitments and contingencies
    Equity:
    Jabil Inc. stockholders’ equity:
    Preferred stock
    Common stock
    Additional paid-in capital
    Retained earnings
    Accumulated other comprehensive loss
    Treasury stock, at cost
    Total Jabil Inc. stockholders’ equity
    Noncontrolling interests
    Total equity
    Total liabilities and equity

    $

    $
    $

    $

    August 31, 2023

    2,457
    3,382
    1,121
    4,439
    1,494
    —
    12,893
    2,963
    366
    810
    129
    288
    17,449

    $

    —
    5,398
    5,929
    96
    —
    11,423
    2,879
    331
    285
    112
    143
    15,173

    $

    —
    —
    2,881
    5,632
    (18)
    (6,219)
    2,276
    —
    2,276
    17,449

    $

    $

    1,804
    3,647
    1,035
    5,206
    1,109
    1,929
    14,730
    3,137
    367
    763
    159
    268
    19,424
    —
    5,679
    5,515
    104
    1,397
    12,695
    2,875
    319
    269
    131
    268
    16,557
    —
    —
    2,795
    4,412
    (17)
    (4,324)
    2,866
    1
    2,867
    19,424

    JABIL INC. AND SUBSIDIARIES
    CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS
    (in millions, except for per share data)
    (Unaudited)
    4

    Net revenue
    Cost of revenue
    Gross pro t
    Operating expenses:
    Selling, general and administrative
    Research and development
    Amortization of intangibles
    Restructuring, severance and related charges
    Gain from the divestiture of businesses
    Acquisition and divestiture related charges
    Operating income
    Interest and other, net
    Income before income tax
    Income tax expense
    Net income
    Net income attributable to noncontrolling interests, net of tax
    Net income attributable to Jabil Inc.
    Earnings per share attributable to the stockholders of Jabil Inc.:
    Basic
    Diluted
    Weighted average shares outstanding:
    Basic
    Diluted

    Three months ended
    May 31, 2024 May 31, 2023

    $

    Nine months ended
    May 31, 2024 May 31, 2023

    6,765 $
    6,157
    608

    8,475 $
    7,778
    697

    $

    268
    9
    12
    55
    —
    3
    261
    60
    201
    72
    129
    —
    129 $

    307
    8
    7
    —
    —
    —
    375
    69
    306
    73
    233
    —
    233 $

    890
    29
    27
    252
    (944)
    64
    1,695
    197
    1,498
    248
    1,250
    —
    1,250

    $

    911
    25
    24
    45
    —
    —
    1,096
    204
    892
    229
    663
    —
    663

    $
    $

    1.08 $
    1.06 $

    1.76 $
    1.72 $

    10.01
    9.86

    $
    $

    4.96
    4.86

    119.9
    121.7

    132.3
    135.1

    21,919
    19,906
    2,013

    $

    124.9
    126.9

    26,244
    24,143
    2,101

    133.6
    136.4

    JABIL INC. AND SUBSIDIARIES
    CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS
    (in millions)
    (Unaudited)
    Cash ows provided by operating activities:
    Net income
    Depreciation, amortization, and other, net
    Gain from the divestiture of businesses
    Change in operating assets and liabilities, exclusive of net assets acquired
    Net cash provided by operating activities
    Cash ows provided by (used in) investing activities:
    Acquisition of property, plant and equipment
    Proceeds and advances from sale of property, plant and equipment
    Cash paid for business and intangible asset acquisitions, net of cash
    Proceeds from the divestiture of businesses, net of cash
    Other, net
    Net cash provided by (used in) investing activities
    Cash ows used in nancing activities:
    Borrowings under debt agreements
    Payments toward debt agreements
    Payments to acquire treasury stock
    Dividends paid to stockholders
    Net proceeds from exercise of stock options and issuance of common stock under employee stock
    purchase plan
    Treasury stock minimum tax withholding related to vesting of restricted stock
    Other, net
    Net cash used in nancing activities
    E ect of exchange rate changes on cash and cash equivalents
    Net increase in cash and cash equivalents
    Cash and cash equivalents at beginning of period
    Cash and cash equivalents at end of period

    Nine months ended
    May 31, 2024
    May 31, 2023
    $

    $

    1,250
    557
    (944)
    318
    1,181

    $

    663
    752
    —
    (367)
    1,048

    (660)
    115
    (90)
    2,108
    (6)
    1,467

    (860)
    180
    (30)
    —
    (28)
    (738)

    1,895
    (1,987)
    (1,824)
    (32)

    3,556
    (3,369)
    (442)
    (34)

    31
    (68)
    (4)
    (1,989)
    (6)
    653
    1,804
    2,457

    27
    (36)
    (6)
    (304)
    (4)
    2
    1,478
    1,480

    $

    5

    JABIL INC. AND SUBSIDIARIES
    SUPPLEMENTAL DATA
    RECONCILIATION OF U.S. GAAP FINANCIAL RESULTS TO NON-GAAP MEASURES
    (in millions, except for per share data)
    (Unaudited)
    Three months ended
    Nine months ended
    May 31, 2024 May 31, 2023 May 31, 2024 May 31, 2023
    $
    261 $
    375 $
    1,695 $
    1,096
    Operating income (U.S. GAAP)
    Amortization of intangibles
    Stock-based compensation expense and related charges
    Restructuring, severance and related charges(1)
    Net periodic bene t cost
    Business interruption and impairment charges, net(2)
    Gain from the divestiture of businesses(3)
    Acquisition and divestiture related charges(3)
    Adjustments to operating income

    Core operating income (Non-GAAP)
    Net income attributable to Jabil Inc. (U.S. GAAP)

    $

    Core earnings (Non-GAAP)

    $
    $
    $

    12
    3
    55
    2
    14
    —
    3
    89
    350

    $

    Adjustments to operating income
    Net periodic bene t cost
    Adjustments for taxes

    Diluted earnings per share (U.S. GAAP)
    Diluted core earnings per share (Non-GAAP)
    Diluted weighted average shares outstanding (U.S. GAAP & NonGAAP)

    129
    89
    (2)
    14
    230
    1.06
    1.89

    7
    18
    —
    4
    —
    —
    —
    29
    404

    $
    $

    $

    233
    29
    (4)
    11
    269
    1.72
    1.99

    $
    $
    $

    121.7

    $
    $
    $
    $

    135.1

    27
    72
    252
    7
    14
    (944)
    64
    (508)
    1,187

    24
    80
    45
    11
    —
    —
    —
    160
    1,256

    $

    1,250
    (508)
    (7)
    51
    786
    9.86
    6.20

    $

    663
    160
    (11)
    32
    844
    4.86
    6.18

    $
    $
    $

    126.9

    136.4

    __________________
    (1) Charges recorded during the three months and nine months ended May 31, 2024, related to the 2024 Restructuring Plan.
    (2) Charges recorded during the three months and nine months ended May 31, 2024, related to costs associated with product quality liabilities.
    (3) We completed the divestiture of our mobility business and recorded a pre-tax gain of $944 million, subject to certain post-closing adjustments
    that are still being nalized. We incurred transaction and disposal costs in connection with the sale of approximately $64 million during the nine
    months ended May 31, 2024.

    JABIL INC. AND SUBSIDIARIES
    SUPPLEMENTAL DATA
    ADJUSTED FREE CASH FLOW
    (in millions)
    (Unaudited)
    Net cash provided by operating activities (U.S. GAAP)

    $

    Adjusted free cash ow (Non-GAAP)

    $

    Acquisition of property, plant and equipment (“PP&E”)(1)
    Proceeds and advances from sale of PP&E(1)

    __________________
    (1) C t i
    t

    i

    t i PP&E ith

    A

    i

    PP&E

    i

    th

    h

    t i

    Nine months ended
    May 31, 2024
    May 31, 2023
    1,181
    (660)
    115
    636

    i iti

    $

    1,048
    (860)
    180
    368

    $

    f PP&E Wh

    t

    6

    (1) Certain customers co-invest in PP&E with us. As we acquire PP&E, we recognize the cash payments in acquisition of PP&E. When our customers
    reimburse us and obtain control, we recognized the cash receipts in proceeds and advances from the sale of PP&E.

    Investor Contact
    Adam Berry
    Senior Vice President, Investor Relations and Communications
    Adam_Berry@jabil.com

    Media Contact
    Timur Aydin
    Senior Director, Enterprise Marketing and Communications
    Timur_Aydin@jabil.com
    Source: Jabil, Inc.

    7

    THIRD QUARTER
    FISCAL YEAR 2024
    RESULTS

    June 20, 2024

    Forward Looking Statement
    Forward Looking Statements: This presentation contains forward-looking statements, including those regarding our anticipated financial results for our third
    quarter of fiscal year 2024; our guidance for future financial performance in our fourth quarter of fiscal year 2024 (including, net revenue, segment revenue,
    U.S. GAAP operating income, U.S. GAAP diluted earnings per share, core operating income (Non-GAAP), net interest expense, core tax rate (Non-GAAP), core
    diluted earnings per share (Non-GAAP) results and the components thereof); our full year 2024 (including revenue by end market, net revenue, core operating
    margin (Non-GAAP), core earnings per share (Non-GAAP) results and the components thereof, and free cash flow); and our 2025 tax rate and interest expense;
    those related to our outlook for secular trends and end markets; our expectations regarding growth in AI solutions; our financial priorities; and our expectations
    with respect to stock repurchase activities. The statements in this presentation are based on current expectations, forecasts and assumptions involving risks
    and uncertainties that could cause actual outcomes and results to differ materially from our current expectations. Such factors include, but are not limited to:
    our determination as we finalize our financial results for our third quarter of fiscal year 2024 that our financial results and conditions differ from our current
    preliminary unaudited numbers set forth herein; unexpected costs or unexpected liabilities that may arise from the sale of our Mobility business; scheduling
    production, managing growth and capital expenditures and maximizing the efficiency of our manufacturing capacity effectively; managing rapid declines or
    increases in customer demand and other related customer challenges that may occur; the effect of COVID-19 on our operations, sites, customers and supply
    chain; our dependence on a limited number of customers; our ability to purchase components efficiently and reliance on a limited number of suppliers for
    critical components; risks arising from relationships with emerging companies; changes in technology and competition in our industry; our ability to introduce
    new business models or programs requiring implementation of new competencies; competition; transportation issues; our ability to maintain our engineering,
    technological and manufacturing expertise; retaining key personnel; risks associated with international sales and operations, including geopolitical
    uncertainties; energy price increases or shortages; our ability to achieve expected profitability from acquisitions; risk arising from our restructuring activities;
    issues involving our information systems, including security issues; regulatory risks (including the expense of complying, or failing to comply, with applicable
    regulations; risk arising from design or manufacturing defects; risk arising from compliance, or failure to comply, with environmental, health and safety laws or
    regulations and intellectual property risk); financial risks (including customers or suppliers who become financially troubled; turmoil in financial markets; tax
    risks; credit rating risks; risks of exposure to debt; currency fluctuations; and asset impairment); changes in financial accounting standards or policies; risk of
    natural disaster, climate change or other global events; and risks arising from expectations relating to environmental, social and governance considerations.
    Additional factors that could cause such differences can be found in our Annual Report on Form 10-K for the fiscal year ended August 31, 2023 and our other
    filings with the Securities and Exchange Commission. We assume no obligation to update these forward-looking statements.

    2

    Third Quarter FY 2024
    Income Highlights
    THREE MONTHS ENDED
    May 31,
    2024

    2023

    $6,765

    $8,475

    U.S. GAAP operating income

    $261

    $375

    U.S. GAAP net income

    $129

    $233

    U.S. GAAP diluted earnings per share

    $1.06

    $1.72

    Core operating income (non-GAAP)1

    $350

    $404

    Core earnings (non-GAAP)1

    $230

    $269

    Core diluted earnings per share (non-GAAP)1

    $1.89

    $1.99

    (In millions, except for per share data)

    Net revenue

    1

    See U.S. GAAP to non-GAAP reconciliation in appendix.

    3

    Third Quarter FY 2024
    Segment Results
    DIVERSIFIED MANUFACTURING SERVICES (DMS)
    ▪ Net Revenue decrease 23% y/y
    ▪ Core margin* (non-GAAP) of 4.6%

    ELECTRONICS MANUFACTURING SERVICES (EMS)
    ▪ Net Revenue decrease of 18% y/y
    ▪ Core margin* (non-GAAP) of 5.7%

    EMS
    50%

    $6.8B

    REVENUE

    DMS
    50%

    TOTAL COMPANY
    ▪ Net Revenue decrease of 20% y/y
    ▪ Core margin* (non-GAAP) of 5.2%

    * Core margin defined as core operating income divided by net revenue │ See U.S. GAAP to non-GAAP definitions and reconciliations located at https://investors.jabil.com/

    4

    Third Quarter FY 2024
    Cash Flow Highlights
    THREE MONTHS
    ENDED
    MAY 31,

    2024

    ($ millions)

    Net cash provided by operating activities
    Acquisition of property, plant and equipment
    Proceeds and advances from sale of property,
    plant and equipment
    Net capital expenditures1

    $515
    ($106)
    $6
    ($100)

    Adjusted free cash flow (non-GAAP)2

    $415

    Core EBITDA (non-GAAP)1

    $513

    Share repurchases

    $499

    1

    See U.S. GAAP to non-GAAP reconciliation in appendix and U.S. GAAP to non-GAAP definitions located at https://investors.jabil.com/
    2 See U.S. GAAP to non-GAAP reconciliation on Form 8-K filed on June 20, 2024.

    5

    Fourth Quarter FY24
    Guidance
    Segment Revenue Guidance

    Q4 FY23

    Q4 FY24E

    Diversified Manufacturing Services

    $4.44B

    $3.4B

    Electronics Manufacturing Services

    $4.02B

    $3.2B

    Consolidated Guidance
    Net revenue
    U.S. GAAP operating income

    Q4 FY24E
    $6.3B - $6.9B
    $285M - $355M

    U.S. GAAP diluted earnings per share

    $1.40 - $1.88

    Core operating income (non-GAAP)1

    $365 - $425M

    Net interest expense2
    Core tax rate (non-GAAP)3
    Core diluted earnings per share (non-GAAP)1

    $67M
    20%
    $2.03 - $2.43

    See U.S. GAAP to non-GAAP reconciliation on Form-8K filed on June 20, 2024.
    interest expense = interest expense, net + loss on sale of AR
    3 The core tax rate (non-GAAP) is a normalized annual income tax rate with regard to core earnings. See U.S. GAAP to non-GAAP definitions located at https://investors.jabil.com/
    1

    2 Net

    6

    FY24 Revenue by End-Market
    $ in billions

    Revenue by End-Market

    FY23

    FY24E

    Y/Y % ∆

    Auto & Transportation

    $4.4

    $4.6

    5%

    Healthcare & Packaging

    $5.6

    $5.5

    -2%

    Networking & Storage

    $3.1

    $2.7

    -13%

    Industrial & Semi-Cap

    $4.4

    $3.7

    -16%

    Digital Print & Retail

    $3.1

    $2.6

    -16%

    Connected Devices

    $4.0

    $3.2

    -20%

    5G Wireless & Cloud

    $6.1

    $4.5

    -26%

    Mobility

    $4.0

    $1.7

    Jabil

    $34.7

    $28.5

    Cloud transitioning to a consignment model
    Divested in December 2023

    7

    Our Outlook
    FY24 Financial Plan

    NET REVENUE

    $

    CORE OP MARGIN 1

    28.5

    5.6%

    BILLION

    CORE EPS 1

    $

    8.40

    FREE CASH FLOW 1

    1+

    $

    BILLION

    MANAGEMENT’S OUTLOOK FOR FY24

    1

    See U.S. GAAP to non-GAAP definitions and reconciliations located at https://investors.jabil.com/

    8

    Business Update

    Our Outlook
    FY24 Financial Plan

    NET REVENUE

    $

    CORE OP MARGIN 1

    28.5

    5.6%

    BILLION

    CORE EPS 1

    $

    8.40

    FREE CASH FLOW 1

    1+

    $

    BILLION

    MANAGEMENT’S OUTLOOK FOR FY24

    1

    See U.S. GAAP to non-GAAP definitions and reconciliations located at https://investors.jabil.com/

    10

    Our Portfolio
    Diversified and Resilient

    Healthcare &
    Packaging

    Digital Print
    & Retail
    Networking &
    Storage

    AI Data Center Infrastructure
    Automated Warehousing

    Connected
    Devices

    Auto &
    Transportation

    Industrial &
    Semi-Cap

    Pharma Solutions

    5G Wireless
    & Cloud

    11

    Value Creation For Shareholders
    Financial Priorities

    EXPAND
    OPERATING
    MARGINS

    INCREASE
    EARNINGS
    PER SHARE

    GENERATE
    STRONG CASH
    FLOWS

    RETURN
    CAPITAL TO
    SHAREHOLDERS

    ALIGNED & FOCUSED ON DRIVING CONSISTENT CASH FLOWS & PROFITABILIT Y

    See U.S. GAAP to non-GAAP definitions located at https://investors.jabil.com/

    12

    FY25 Considerations

    Timing of
    End-Market
    Recovery

    Optimizing
    Portfolio

    Interest
    & Tax

    13

    FY25 Investor Briefing
    • Well-positioned to support AI growth
    • Transitioning from legacy datacenters to AI
    tailored solutions
    • Evaluating certain businesses to optimize
    portfolio
    • Provide update for timing of recovery in key
    areas like renewables, semi-cap, EV’s,
    connected devices, and 5G

    14

    THANK YOU
    for your commitment
    and dedication
    to our customers,
    communities, and
    each other.

    15

    In Summary
    • FY24 remains on track

    • Expect to complete $2.5 billion share repurchase authorization in Q4 FY24
    • Fully committed to growth in AI data centers
    • Optimizing portfolio
    • Updated seasonality on new mix of business
    • Expect FY25 net interest expense to be $275 million
    • FY25 core tax rate expected to be 22% to 24%

    16

    APPENDIX
    GAAP TO NON-GAAP
    RECONCILIATIONS

    JABIL INC. AND SUBSIDIARIES
    OPERATING INCOME, EBITDA and NET INCOME NON-GAAP RECONCILIATION
    (in millions, except for per share data)
    (Unaudited)

    Three months ended
    May 31, 2024
    Operating income (U.S. GAAP)

    $

    Amortization of intangibles
    Stock-based compensation expense and related charges
    Restructuring, severance and related charges
    Net periodic benefit cost

    Nine months ended

    May 31, 2023
    261

    $

    May 31, 2024
    375

    $

    May 31, 2023

    1,695

    $

    1,096

    12

    7

    27

    24

    3

    18

    72

    80

    55

    —

    252

    45

    7

    11

    2

    4

    Business interruption and impairment charges, net

    14

    —

    14

    —

    Gain from the divestiture of businesses

    —

    —

    (944)

    —

    3

    —

    64

    —

    89

    29

    (508)

    160

    Acquisition and divestiture related charges
    Adjustments to operating income
    Core operating income (Non-GAAP)

    $

    350

    $

    404

    $

    1,187

    $

    1,256

    Core operating income (Non-GAAP)

    $

    350

    $

    404

    $

    1,187

    $

    1,256

    Depreciation expense

    163

    224

    499

    671

    Core EBITDA (Non-GAAP)

    $

    513

    $

    628

    $

    1,686

    $

    1,927

    Net income attributable to Jabil Inc. (U.S. GAAP)

    $

    129

    $

    233

    $

    1,250

    $

    663

    Adjustments to operating income

    89

    29

    (508)

    160

    Net periodic benefit cost

    (2)

    (4)

    (7)

    (11)

    Adjustments for taxes

    14

    11

    51

    32

    Core earnings (Non-GAAP)

    $

    230

    $

    269

    $

    786

    $

    844

    Diluted earnings per share (U.S. GAAP)

    $

    1.06

    $

    1.72

    $

    9.86

    $

    4.86

    Diluted core earnings per share (Non-GAAP)

    $

    1.89

    $

    1.99

    $

    6.20

    $

    6.18

    Diluted weighted average shares outstanding (U.S. GAAP and Non-GAAP)

    121.7

    135.1

    Days in inventory

    81 days

    84 days

    Days in inventory, net

    58 days

    62 days

    126.9

    136.4

    Supplemental Information

    19
    """)

    def fullcontext():
        return context
    query= str(query)
    query = query.format(companyname)


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)




    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings.companyname)


    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings)
                
    fullquery =  """Use the following pieces of context to answer the question at the end. If you dont know the answer just say that you dont know it, dont try to make up an answer. If the question is empty just provide a empty string, dont guess. Act as a financial analyst providing concise valuable information to the portfolio manager. pay high attention to thruth of every information in the answer, if you are not sure better leave it out. double check the answer for any false information. """+ query+""" 
    """+ context + """ 
    Question:"""+query+""" 
Helpful answer: """

    


    chain = PromptTemplate.from_template(template=fullquery) | llm
    res = chain.invoke(input = {})

    print(res)

    return res


