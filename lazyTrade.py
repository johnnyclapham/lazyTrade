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
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']+" -"+json_data[0]['a']
    return(quote)


def get_price(message):
        l={}
        u=list()

        #Splitting the input from !price to read input text from user.
        stock = message.content.split(' ')[1]
        print(stock)

        url = "https://finance.yahoo.com/quote/"
        full_url = url + stock + "/key-statistics?p=" + stock
        r = requests.get(full_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(full_url)
        print(soup.title)

        #search by unique description. For stock price it is the following
        stock_price = soup.findAll(class_ = "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text

        #!!!
        all_data = soup.find_all("tbody")
        #print('all_data: \n\n'+ str(all_data)+'\n\n')

        results = soup.find_all('tbody',attrs={'class':'Bxz(bb) H(36px) BdY Bdc($seperatorColor) fi-row Bgc($hoverBgColor):h'})
        print(len(stock_price))


        client.send_message(message.channel, f"The stock price for {stock.upper()} is ${stock_price} currently.")






@client.event
async def on_ready():
    print('Bot with userid: {0.user} connected'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello '+str(message.author)+'!'+' how are you?')
    if message.content.startswith('good'):
        await message.channel.send('Really? That is excellent news.')
    if message.content.startswith('bye'):
        await message.channel.send('until next time!')
    if message.content.startswith('inspire me'):
        quote = get_quote()
        await message.channel.send(quote)
    if message.content.startswith('!price'):
        #get_price(message)
        #stock_bot(message)
        #await message.channel.send()
        l={}
        u=list()

        #Splitting the input from !price to read input text from user.
        stock = message.content.split(' ')[1]
        print(stock)

        url = "https://finance.yahoo.com/quote/"
        full_url = url + stock + "/key-statistics?p=" + stock
        r = requests.get(full_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(full_url)
        print(soup.title)

        stock_price = soup.findAll(class_ = "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
        #message.channel.send( f"The stock price for {stock.upper()} is ${stock_price} currently.")

        #!!!
        all_data = soup.find_all("tbody")
        #print('all_data: \n\n'+ str(all_data)+'\n\n')

        results = soup.find_all('tbody',attrs={'class':'Bxz(bb) H(36px) BdY Bdc($seperatorColor) fi-row Bgc($hoverBgColor):h'})
        print(len(stock_price))


        await message.channel.send(f"The stock price for {stock.upper()} is ${stock_price} currently.")








    if message.content.startswith('!help'):
        await message.channel.send('List of commands:\n hello \n good \n bye \n inspire me ')



client.run(config.KEY)
