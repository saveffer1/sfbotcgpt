import discord
from discord import app_commands
from discord.ext import commands
from src import responses
from src import log
from ast import alias

from src.Classes import Dalle

# Builtin
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Union

logger = log.setup_logger(__name__)

config = responses.get_config()

isPrivate = False

class aclient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /draw | /help")
        
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

def del_dir(target: Union[Path, str], only_if_empty: bool = False):
    target = Path(target).expanduser()
    if not target.is_dir():
        raise RuntimeError(f"{target} is not a directory")

    for p in sorted(target.glob('**/*'), reverse=True):
        if not p.exists():
            continue
        p.chmod(0o666)
        if p.is_dir():
            p.rmdir()
        else:
            if only_if_empty:
                raise RuntimeError(f'{p.parent} is not empty!')
            p.unlink()
    target.rmdir()

async def create_collage(ctx: discord.Interaction, query: str, source_image: Image, images: list) -> str:
        width = source_image.width
        height = source_image.height
        font_size = 30
        spacing = 16
        text_height = font_size + spacing
        
        im = Image.open(images[0].path)
        im.thumbnail((width, height))
        with Image.new('RGB', (width, height + text_height), (255, 255, 255)) as new_im:
            new_im.paste(im, (0, text_height))
            img_draw = ImageDraw.Draw(new_im)
            fnt = ImageFont.load_default()
            img_draw.text((1, 0), query, font=fnt, fill=(0, 0, 0))
            new_im.save(f"./generated/{ctx.user.id}/art.png")
            new_im.close()
            im.close()
        return f"./generated/{ctx.user.id}/art.png"

async def create_multcollage(ctx: discord.Interaction, query: str, source_image: Image, images: list) -> str:
        width = source_image.width
        height = source_image.height
        font_size = 30
        spacing = 16
        text_height = font_size + spacing
        new_im = Image.new('RGBA', (width * 3 + spacing * 2, height * 3 + spacing * 2 + text_height),
                            (0, 0, 0, 0))

        index = 0
        for i in range(0, 3):
            for j in range(0, 3):
                im = Image.open(images[index].path)
                im.thumbnail((width, height))
                new_im.paste(im, (i * (width + spacing),
                             text_height + j * (height + spacing)))
                index += 1

        img_draw = ImageDraw.Draw(new_im)
        fnt = ImageFont.load_default()
        img_draw.text((1, 0), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((0, 1), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((1, 2), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((2, 1), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((0, 0), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((0, 2), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((2, 0), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((2, 2), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((1, 1), query, font=fnt, fill=(255, 255, 255))
        new_im.save(f"./generated/{ctx.author.id}/art.png")
        return f"./generated/{ctx.author.id}/art.png"

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
    
    @client.tree.command(name="draw", description="สร้างรูปจากสิ่งที่พิมพ์")
    async def draw(ctx: discord.Interaction, *, query: str) -> None:
        await ctx.response.defer(ephemeral=False)
        # Check if query is empty
        if not query:
            await ctx.followup.send("sfbot: เกิดข้อผิดพลาด\nโปรดใส่สิ่งที่ต้องการให้วาดลงไปด้วย.")
            return

        # Check if query is too long
        if len(query) > 100:
            await ctx.followup.send("sfbot: เกิดข้อผิดพลาด\nสิ่งที่ขอมันยาวเกินไป! (สูงสุด: 100 ตัวอักษร)")
            return

        print(f"[-] {ctx.user.name} asked to draw {query}")

        message = await ctx.followup.send(f"กำลังทำคำขอให้ {ctx.user.name} (นี่อาจจะใช้เวลามากกว่า 2 นาที)"" ```" + query + "```")

        try:
            dall_e = await Dalle.DallE(prompt=f"{query}", author=f"{ctx.user.id}")
            generated = await dall_e.generate()

            if len(generated) > 0:
                first_image = Image.open(generated[0].path)
                generated_collage = await create_collage(ctx, query, first_image, generated)

                # Prepare the attachment
                file = discord.File(generated_collage, filename="art.png")
                await ctx.followup.send(file=file)

                # Delete the message
                await message.delete()

        except Dalle.DallENoImagesReturned:
            await ctx.followup.send("sfbot ไม่รู้จัก {query}.")
        except Dalle.DallENotJson:
            await ctx.followup.send("API Serialization Error, โปรดลองอีกครั้ง.")
        except Dalle.DallEParsingFailed:
            await ctx.followup.send("Parsing Error, โปรดลองอีกครั้ง.")
        except Dalle.DallESiteUnavailable:
            await ctx.followup.send("API Error, โปรดลองอีกครั้ง.")
        except Exception as e:
            if e == UnicodeEncodeError:
                await ctx.followup.send("ระบบวาดตอนนี้ไม่เข้าใจภาษาอื่น, ขอร้องอย่าพยายามไอ้พวกเหี้ย.")
            else:
                await ctx.followup.send("เซิร์ฟล่มไปแล้ว, โปรดลองอีกครั้ง.")
                await ctx.followup.send(repr(e))
        finally:
            # Delete the author folder in ./generated with author id, if exists
            del_dir(f"./generated/{ctx.user.id}")
    
    @client.tree.command(name="multidraw", description="วาดหลายรูปพร้อมกัน")
    async def draw(ctx: discord.Interaction, *, query: str) -> None:
        await ctx.response.defer(ephemeral=False)
        # Check if query is empty
        if not query:
            await ctx.followup.send("sfbot: เกิดข้อผิดพลาด\nโปรดใส่สิ่งที่ต้องการให้วาดลงไปด้วย.")
            return

        # Check if query is too long
        if len(query) > 100:
            await ctx.followup.send("sfbot: เกิดข้อผิดพลาด\nสิ่งที่ขอมันยาวเกินไป! (สูงสุด: 100 ตัวอักษร)")
            return

        print(f"[-] {ctx.user.name} asked to draw {query}")

        message = await ctx.followup.send(f"กำลังทำคำขอให้ {ctx.user.name} (นี่อาจจะใช้เวลามากกว่า 2 นาที)"" ```" + query + "```")

        try:
            dall_e = await Dalle.DallE(prompt=f"{query}", author=f"{ctx.user.id}")
            generated = await dall_e.generate()

            if len(generated) > 0:
                first_image = Image.open(generated[0].path)
                generated_collage = await create_multcollage(ctx, query, first_image, generated)

                # Prepare the attachment
                file = discord.File(generated_collage, filename="art.png")
                await ctx.followup.send(file=file)

                # Delete the message
                await message.delete()

        except Dalle.DallENoImagesReturned:
            await ctx.followup.send("sfbot ไม่รู้จัก {query}.")
        except Dalle.DallENotJson:
            await ctx.followup.send("API Serialization Error, โปรดลองอีกครั้ง.")
        except Dalle.DallEParsingFailed:
            await ctx.followup.send("Parsing Error, โปรดลองอีกครั้ง.")
        except Dalle.DallESiteUnavailable:
            await ctx.followup.send("API Error, โปรดลองอีกครั้ง.")
        except Exception as e:
            if e == UnicodeEncodeError:
                await ctx.followup.send("ระบบวาดตอนนี้ไม่เข้าใจภาษาอื่น, ขอร้องอย่าพยายามไอ้พวกเหี้ย.")
            else:
                await ctx.followup.send("เซิร์ฟล่มไปแล้ว, โปรดลองอีกครั้ง.")
                await ctx.followup.send(repr(e))
        finally:
            # Delete the author folder in ./generated with author id, if exists
            del_dir(f"./generated/{ctx.user.id}")

    TOKEN = config['discord_bot_token']
    client.run(TOKEN)
