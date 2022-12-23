# saveffer
## The renewed discord bot

## สำคัญมาก ถ้าจะโคลนโปรเจ็คไปให้แก้ config.json ก่อนเพราะในนั้นเป็นคีย์ที่ใช้รันบอทจริงตอนนี้

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
[![Invite](https://discord.com/api/oauth2/authorize?client_id=1054600054498926613&permissions=59392&scope=bot)

sfbotcgpt is the one of my discord bot that combine many projects from github into one.

## Features

- /chat to use chat-gpt3
- /draw to draw an image with dall-e mini
- /multidraw to draw 3x3 image in one time
- /help to check other feature

## Installation

sfbotcgpt requires server to run this bot

Install all dependencies and start the script.                                             
Th version
```sh
tested python version == 3.11
1.ติดตั้ง python library
  pip install -r requirements.txt
2.ขอ API จาก open ai(โทเค็นจะย้อนมาดูไม่ได้อีก เอาเก็บไว้ที่ไหนสักที่ให้ดีๆ)
  https://beta.openai.com/account/api-keys
3.สร้างบอท
  https://discordapp.com/developers/applications/
4.ตั้งชื่อและใส่รูปให้บอท(ไม่ทำจะไม่ได้โทเค็น)
5.เขียน description ให้บอท(ไม่ทำจะไม่ได้โทเค็น)
6.ไปที่ bot -> add bot
7.กด reset token
8.กด copy(โทเค็นจะย้อนมาดูไม่ได้อีก เอาเก็บไว้ที่ไหนสักที่ให้ดีๆ)
9.เอาของทั้งข้อ 2 และ ข้อ 8 ไปใส่ใน ไฟล์ที่โหลดมาชื่อ config.json(มีเขียนกำกับอยู่ว่าต้องใส่อันไหน)
10.ในเว็บบอทดิสคอร์ดให้ไปที่ oauth2 -> url generator ติ๊ก bot ติ๊ก admin แล้ว copy code เชิญด้านล่างมาเปิด จะเป็นการเชิญบอทเข้าดิส
11.ในเว็บบอทดิสคอร์ดกลับไปที่เมนู bot ตรง Privileged Gateway Intents มีให้เปิดอยู่ 3 อัน เปิดแม่งให้หมด
12.run python code ได้เลยชื่อไฟล์ main.py
จบปิ๊ง
```

En google translate version
```sh
tested python version == 3.11
1. Install python library
   pip install -r requirements.txt
2.Request API from open ai(The token will not be able to view again Keep it somewhere good)
   https://beta.openai.com/account/api-keys
3. Create a bot
   https://discordapp.com/developers/applications/
4. Set a name and put a picture for the bot (do not do it will not get a token)
5. Write a description for the bot (don't do it, you won't get a token)
6. go to bot -> add bot
7.Press reset token
8. Press copy(The token will not be able to look back again. Keep it somewhere good)
9. Take items from item 2 and item 8 to put in the downloaded file named config.json(it is written which one to put)
10. In web bot discord, go to oauth2 -> url generator, tick bot, tick admin and copy the invitation code below to open. This will invite the bot to the disk.
11. In the web bot discord, go back to the bot menu at Privileged Gateway Intents, there are 3 open. Open them all.
12.run python code, the filename is main.py
end.
```

## Cloned feature bot credit

| Features | Projects | Github |
| ------ | ------ | ------ |
| Chat Bot | Chat GPT | https://github.com/Zero6992/chatGPT-discord-bot |
| Image Drawing | Dall-E Mini |https://github.com/rawandahmad698/Dalle-Discord |
| 3D Drawing | In some day, I hope. | ------ |
| Youtube music Player | In some day, I hope. | ------ |


## Enjoy
