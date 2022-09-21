import discord
from chat import Conversation
from time import sleep
import random
import os

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
conv = Conversation()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):

    text = None

    # If bot is mentioned
    if message.mentions:
        if message.mentions[0].id == bot.user.id:

            # Reset cool down and return 
            if conv.cool_down == 0:
                conv.cool_down = 5
                return None

            # If another bot/user is mentioned
            if len(message.mentions) == 2:
                # conv.respond_to = message.mentions[1]
                print(message.mentions[1])
                # print(conv.respond_to)
                seed = "hello dude"
                response = conv.generate_response(seed)
                await message.channel.send(f"<@!{message.mentions[1].id}> {response}")
                return None

            # Mentioned by name
            if message.content[3:21] == str(message.mentions[0].id):
                # Extract text
                text = message.content[23:]
            else:
                # Mentioned by reply
                text = message.content

    # If no text is provided in either case -> return error
    if not text:
        return None

    # If command
    if text.split()[0] == "-model":
        model = text.split()[1]
        if model in ["large", "medium", "small"]:
            response = await message.channel.send("Switching models...")
            conv.switch_model(model)
            return await response.edit(content="Done!")
        else:
            return message.reply("Legal models are: large, medium, small")

    # If proper response
    else:
        # Check if bot, decrement cool down
        if message.author.bot: 
            conv.cool_down -= 1
            sleep(random.uniform(0.8, 2)) 

        response = conv.generate_response(text)
        # Reply with generated response
        await message.reply(response)


bot.run(TOKEN)