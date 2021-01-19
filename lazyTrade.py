import discord
import config
import requests
import json
from bs4 import BeautifulSoup


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
    print(soup.prettify())
    return stock_price


def cap(message):
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
        cols = soup.findAll(class_ = "Ta(c) Pstart(10px) Miw(60px) Miw(80px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor)")[0].text
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
        #call our cap webscraper function
        market_cap = cap(message)
        #send the message to the channel
        await message.channel.send(f"Market cap for {stock.upper()} is ${market_cap} currently.")

    elif message.content.startswith('!help'):
        help_list = """
        List of commands:
            hello
            good
            bye
            inspire me
            !clear
            !price <<ticker>>
            """

        await message.channel.send(help_list)


client.run(config.KEY)
