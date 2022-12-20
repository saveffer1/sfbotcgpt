import discord
from discord import app_commands
from discord.ext import commands
from src import responses
from src import log
from ast import alias
from youtube_dl import YoutubeDL

logger = log.setup_logger(__name__)

config = responses.get_config()

isPrivate = False

class aclient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /help")
        
async def send_message(message, user_message):
    await message.response.defer(ephemeral=isPrivate)
    try:
        response = '> **' + user_message + '** - <@' + \
            str(message.user.id) + '>\n\n'
        response = f"{response}{user_message}{await responses.handle_response(user_message)}"
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            if "```" in response:
                # Split the response if the code block exists
                parts = response.split("```")
                # Send the first message
                await message.followup.send(parts[0])
                # Send the code block in a seperate message
                code_block = parts[1].split("\n")
                formatted_code_block = ""
                for line in code_block:
                    while len(line) > 1900:
                        # Split the line at the 50th character
                        formatted_code_block += line[:1900] + "\n"
                        line = line[1900:]
                    formatted_code_block += line + "\n"  # Add the line and seperate with new line

                # Send the code block in a separate message
                if (len(formatted_code_block) > 2000):
                    code_block_chunks = [formatted_code_block[i:i+1900]
                                         for i in range(0, len(formatted_code_block), 1900)]
                    for chunk in code_block_chunks:
                        await message.followup.send("```" + chunk + "```")
                else:
                    await message.followup.send("```" + formatted_code_block + "```")

                # Send the remaining of the response in another message

                if len(parts) >= 3:
                    await message.followup.send(parts[2])
            else:
                response_chunks = [response[i:i+1900]
                                   for i in range(0, len(response), 1900)]
                for chunk in response_chunks:
                    await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception as e:
        await message.followup.send("> **Error: แม่งเอ๊ยเกิดอะไรสักอย่างผิดพลาด, ไว้ลองใหม่ดูนะ!**")
        logger.exception(f"Error while sending message: {e}")


async def send_start_prompt(client):
    import os
    import os.path

    config_dir = os.path.abspath(__file__ + "/../../")
    prompt_name = 'starting-prompt.txt'
    prompt_path = os.path.join(config_dir, prompt_name)
    try:
        if os.path.isfile(prompt_path) and os.path.getsize(prompt_path) > 0:
            with open(prompt_path, "r") as f:
                prompt = f.read()
                logger.info(f"Send starting prompt with size {len(prompt)}")
                responseMessage = await responses.handle_response(prompt)
                if (config['discord_channel_id']):
                    channel = client.get_channel(int(config['discord_channel_id']))
                    await channel.send(responseMessage)
            logger.info(f"Starting prompt response: {responseMessage}")
        else:
            logger.info(f"No {prompt_name}. Skip sending starting prompt.")
    except Exception as e:
        logger.exception(f"Error while sending starting prompt: {e}")


def run_discord_bot():
    client = aclient()

    @client.event
    async def on_ready():
        await send_start_prompt(client)
        await client.tree.sync()
        logger.info(f'{client.user} is now running!')

    @client.tree.command(name="chat", description="ป่ะคุยกับ chat gpt ได้เลย")
    async def chat(interaction: discord.Interaction, *, message: str):
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
        await send_message(interaction, user_message)

    @client.tree.command(name="private", description="เข้าสู่โหมดส่งข้อความส่วนตัว")
    async def private(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if not isPrivate:
            isPrivate = not isPrivate
            logger.warning("\x1b[31mSwitch to private mode\x1b[0m")
            await interaction.followup.send("> **Info:  ต่อไปจะตอบกลับทางข้อความส่วนตัว. ถ้าจะกลับไปโหมดส่งข้อความสาธารณะให้ใช้, `/public`**")
        else:
            logger.info("You already on private mode!")
            await interaction.followup.send("> **Warn: คุณอยู่ในโหมดส่วนตัวแล้ว.  ถ้าจะกลับไปโหมดส่งข้อความสาธารณะให้ใช้, `/public`**")

    @client.tree.command(name="public", description="เข้าสู่โหมดส่งข้อความสาธารณะ")
    async def public(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send("> **Info: Next, ต่อไปจะตอบกลับข้อความภายในช่องแชต. หากจะส่งข้อความส่วนตัวให้ใช้, `/private`**")
            logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
        else:
            await interaction.followup.send("> **Warn: คุณอยู่ในโหมดส่งข้อความสาธารณะ. ถ้าจะกลับไปโหมดส่วนตัวให้ใช้, `/private`**")
            logger.info("You already on public mode!")

    @client.tree.command(name="help", description="แสดงคำสั่งเกี่ยวกับ saveffer bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(":star:**ชุดคำสั่ง** \n    `/chat [message]` คุยกับ ChatGPT!\n  `/private` เข้าสู่โหมดส่งข้อความส่วนตัว\n  `/public` เข้าสู่โหมดส่งข้อความสาธารณะ \n    visit saveffer1: https://github.com/saveffer1")
        logger.info("\x1b[31mSomeone need help!\x1b[0m")
    
    @client.tree.command(name="invite", description="เชิญบอทเข้าเซิฟเวอร์")
    async def invite(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("https://discord.com/api/oauth2/authorize?client_id=1054600054498926613&permissions=59392&scope=bot")
        logger.info("\x1b[31mSomeone use invite cmd!\x1b[0m")
    
    #say command
    @client.tree.command(name="say", description="บอทจะพูดตามที่คุณพิมพ์")
    async def say(interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(message)
        logger.info("\x1b[31mSomeone use say cmd!\x1b[0m")
        
    #play music command
    @client.tree.command(name="play", description="เล่นเพลง")
    #write the join voice channel and play music code here
    #send the link to the music
    async def play(interaction: discord.Interaction, url: str):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("ทำยากจังขี้เกียจทำต่อละ: https://youtu.be/dQw4w9WgXcQ")
        logger.info("\x1b[31mSomeone use play cmd!\x1b[0m")

    TOKEN = config['discord_bot_token']
    client.run(TOKEN)
