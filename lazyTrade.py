import discord
import config
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import os #for repl.it
import time



'''
Simple discord bot for further development
Deploys web-scraping to provide financial data
Created for Python 3.7+
@author johnnyclapham 2021
'''

client = discord.Client()




def get_quote():
    #returns a random quote
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']+" -"+json_data[0]['a']

    return(quote)

def get_price(message):

    #Splitting the input from !price to read input text from user.
    stock = message.content.split(' ')[1]

    #concatenate url string
    url = "https://finance.yahoo.com/quote/"
    full_url = url + stock + "/key-statistics?p=" + stock
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #find stock price from html and return
    stock_price = soup.findAll(class_ = "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
    print(len(stock_price))
    #print(soup.prettify())
    return stock_price



#row_to_fetch corresponds to which row index on table
#I.e 0 is market cap, 1 is enterprize value, 2 is Trailing P/E
def scrape(message,row_to_reach):
    #create a list for our data to exist
    data_list = list()

    #Splitting the input from !price to read input text from user.
    stock = message.content.split(' ')[1]

    #concatenate url string
    url = "https://finance.yahoo.com/quote/"
    full_url = url + stock + "/key-statistics?p=" + stock
    print(full_url)
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #find table body
    rows = soup.find('tbody')

    #loop thru from row index 0 to end point (9 rows on valuation measures
    #https://finance.yahoo.com/quote/AAPL/key-statistics/)
    for currow in range(row_to_reach):
        #append each row to our python list
        data_list.append(soup.findAll(class_ = "Ta(c) Pstart(10px) Miw(60px) Miw(80px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor)")[currow].text)

    return data_list


def oldscrape(message,row_to_fetch):#old scraping function. kept for testing.
    l={}
    u=list()
    #Splitting the input from !price to read input text from user.
    stock = message.content.split(' ')[1]

    #concatenate url string
    url = "https://finance.yahoo.com/quote/"
    full_url = url + stock + "/key-statistics?p=" + stock
    print(full_url)
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #find table rows
    rows = soup.find('tbody')
    print(len(rows))
    #for each row, find the specific column
    for row in rows:
        cols = soup.findAll(class_ = "Ta(c) Pstart(10px) Miw(60px) Miw(80px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor)")[row_to_fetch].text
        print(len(cols))

    return cols


@client.event
async def on_ready():
    print('Bot with userid: {0.user} connected'.format(client))


@client.event
async def on_message(message):
    message.content=message.content.lower()
    if message.author == client.user:
        return

    elif message.content.startswith('!help'):
        help_list = """
        ```List of commands:
            hello
            good
            bye
            inspire me
            !clear
            !price <<ticker>>
            !peg <<ticker>>
            !scrape <<ticker>>
            !oldscrape <<ticker>>
            ```"""
        await message.channel.send(help_list)

    elif message.content.startswith('hello'):
        await message.channel.send('Hello '+str(message.author)+'!'+' how are you?')
    elif message.content.startswith('!host'):
        try:
            await message.channel.send('lazyTrade currently hosted by '+str(config.RUNNER))
        except:
            await message.channel.send('lazyTrade currently hosted by '+str(os.getenv('HOST')))

    elif message.content.startswith('good'):
        await message.channel.send('Really? That is excellent news.')

    elif message.content.startswith('bye'):
        await message.channel.send('until next time!')

    elif message.content.startswith('inspire me'):
        quote = get_quote()
        await message.channel.send(quote)

    elif message.content.startswith('!clear'):
        await message.channel.purge(limit=5)
        #await message.channel.send('Channel refreshed. All contents deleted. Type !help for options.')
        await message.channel.send('5 messages cleared.')

    elif message.content.startswith('!refreshxlcrazy'):
        await message.channel.purge(limit=1000)
        #await message.channel.send('Channel refreshed. All contents deleted. Type !help for options.')
        await message.channel.send('Channel refreshed.')

    #this is our stock price webscraper conditional
    elif message.content.startswith('!price'):
        #get ticker from message
        stock = message.content.split(' ')[1]
        #call our get price webscraper function
        stock_price = get_price(message)
        #send the message to the channel
        await message.channel.send(f"The stock price for {stock.upper()} is ${stock_price} currently.")

    #this is our market cap webscraper conditional
    elif message.content.startswith('!mc'):
        #get ticker from message
        stock = message.content.split(' ')[1]
        #call our cap webscraper function using 0 as row index
        market_cap = scrape(message,0)
        #send the message to the channel
        await message.channel.send(f"Market cap for {stock.upper()} is ${market_cap} currently.")

    #this is our market cap webscraper conditional
    elif message.content.startswith('!peg'):
        #get ticker from message
        stock = message.content.split(' ')[1]
        #call our cap webscraper function using 4 as row index
        peg_stat = scrape(message,4)
        #send the message to the channel
        await message.channel.send(f"PEG Ratio (5 yr expected) for {stock.upper()} is ${peg_stat} currently.")




    #batch webscrape
    elif message.content.startswith('!scrape'):
        start_timer = time.time() #start timer for testing
        stock = message.content.split(' ')[1] #get ticker from message

        try:#get data for rows 0-9 from page
            data = scrape(message,9)
        except:
            await message.channel.send(f"""Whoops! Something went wrong for ticker {stock.upper()}.""")
            return

        #call our cap webscraper function / index = row number
        stock_price     = get_price(message)
        market_cap      = data[0]
        ent_value       = data[1]
        trailpe         = data[2]
        forwardpe       = data[3]
        peg_stat        = data[4]
        psttm           = data[5]
        pbmrq           = data[6]
        entvalrev       = data[7]
        entvalebitda    = data[8]

        end_timer = time.time() #stop timer for testing
        time_elapsed = end_timer - start_timer

        #send the message to the channel
        await message.channel.send(f"""Statistics from finance.yahoo.com at {datetime.now()} using new
        {stock.upper()} Breakdown:
        Found in {str(time_elapsed)[:4]} seconds```
        Stock price               ${stock_price}
        Market cap                ${market_cap}
        Enterprise Value          ${ent_value}
        Trailing P/E               {trailpe}
        Forward P/E                {forwardpe}
        PEG Ratio (5 yr expected)  {peg_stat}
        Price/Sales (ttm)         ${psttm}
        Price/Book (mrq)          ${pbmrq}
        Enterprise Value/Revenue  ${entvalrev}
        Enterprise Value/EBITDA   ${entvalebitda}```""")




    #old batch web scrape
    elif message.content.startswith('!oldscrape'):
        #timecode
        oldstart_timer = time.time()
        #get ticker from message
        stock = message.content.split(' ')[1]

        try:
            #call our cap webscraper function
            stock_price = get_price(message)
            market_cap = oldscrape(message,0)
            ent_value = oldscrape(message,1)
            trailpe = oldscrape(message,2)
            forwardpe = oldscrape(message,3)
            peg_stat = oldscrape(message,4)
            psttm = oldscrape(message,5)
            pbmrq = oldscrape(message,6)
            entvalrev = oldscrape(message,7)
            entvalebitda = oldscrape(message,8)
        except:
            await message.channel.send(f"""Whoops! Something went wrong for ticker {stock.upper()}.""")
            return

        oldend_timer = time.time()
        old_time_elapsed = oldend_timer - oldstart_timer

        #send the message to the channel
        await message.channel.send(f"""Statistics from finance.yahoo.com at {datetime.now()} using old
        {stock.upper()} Breakdown:
        Found in {str(old_time_elapsed)[:4]} seconds```
        Stock price               ${stock_price}
        Market cap                ${market_cap}
        Enterprise Value          ${ent_value}
        Trailing P/E               {trailpe}
        Forward P/E                {forwardpe}
        PEG Ratio (5 yr expected)  {peg_stat}
        Price/Sales (ttm)         ${psttm}
        Price/Book (mrq)          ${pbmrq}
        Enterprise Value/Revenue  ${entvalrev}
        Enterprise Value/EBITDA   ${entvalebitda}```""")








#main

try:
    client.run(config.KEY)              #for local usage
except:
    client.run(os.getenv('KEY'))        #for repl.it















################BELOW FUNCTIONS CURRENTLY NOT IN USE#######################
#
# def cap(message):
#     l={}
#     u=list()
#     #Splitting the input from !price to read input text from user.
#     stock = message.content.split(' ')[1]
#
#     #concatenate url string
#     url = "https://finance.yahoo.com/quote/"
#     full_url = url + stock + "/key-statistics?p=" + stock
#     print(full_url)
#     r = requests.get(full_url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#
#     #find table rows
#     rows = soup.find('tbody')
#     print(len(rows))
#     #for each row, find the specific column
#     for row in rows:
#         cols = soup.findAll(class_ = "Ta(c) Pstart(10px) Miw(60px) Miw(80px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor)")[0].text
#         print(len(cols))
#
#     return cols
#
# def peg(message):
#     l={}
#     u=list()
#     #Splitting the input from !price to read input text from user.
#     stock = message.content.split(' ')[1]
#
#     #concatenate url string
#     url = "https://finance.yahoo.com/quote/"
#     full_url = url + stock + "/key-statistics?p=" + stock
#     print(full_url)
#     r = requests.get(full_url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#
#     #find table rows
#     rows = soup.find('tbody')
#     print(len(rows))
#     #for each row, find the specific column
#     for row in rows:
#         cols = soup.findAll(class_ = "Ta(c) Pstart(10px) Miw(60px) Miw(80px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor)")[4].text
#         print(len(cols))
#
#     return cols
