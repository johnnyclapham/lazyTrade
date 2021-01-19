import discord
import config
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


'''
Simple bare-bones discord bot for further development.
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
def scrape(message,row_to_fetch):
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
    if message.author == client.user:
        return
    elif message.content.startswith('hello'):
        await message.channel.send('Hello '+str(message.author)+'!'+' how are you?')

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

    #this is our market cap webscraper conditional
    elif message.content.startswith('!breakdown'):
        #get ticker from message
        stock = message.content.split(' ')[1]
        #call our cap webscraper function
        stock_price = get_price(message)
        market_cap = scrape(message,0)
        ent_value = scrape(message,1)
        trailpe = scrape(message,2)
        forwardpe = scrape(message,3)
        peg_stat = scrape(message,4)
        psttm = scrape(message,5)
        pbmrq = scrape(message,6)
        entvalrev = scrape(message,7)
        entvalebitda = scrape(message,8)

        #send the message to the channel
        await message.channel.send(f"""Statistics from finance.yahoo.com at {datetime.now()}
        {stock.upper()} Breakdown:
        ```
        Stock price               ${stock_price}
        Market cap                ${market_cap}
        Enterprise Value          ${ent_value}
        Trailing P/E              ${trailpe}
        Forward P/E               ${forwardpe}
        PEG Ratio (5 yr expected) ${peg_stat}
        Price/Sales (ttm)         ${psttm}
        Price/Book (mrq)          ${pbmrq}
        Enterprise Value/Revenue  ${entvalrev}
        Enterprise Value/EBITDA   ${entvalebitda}```""")

    elif message.content.startswith('!help'):
        help_list = """
        List of commands:
            hello
            good
            bye
            inspire me
            !clear
            !price <<ticker>>
            !peg <<ticker>>
            !breakdown <<ticker>>
            """

        await message.channel.send(help_list)


client.run(config.KEY)



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
