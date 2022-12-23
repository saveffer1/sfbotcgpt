# saveffer
## The renewed discord bot
invite link: https://discord.com/api/oauth2/authorize?client_id=1054600054498926613&permissions=59392&scope=bot

## สำคัญมาก ถ้าจะโคลนโปรเจ็คไปให้แก้ config.json ก่อนเพราะในนั้นเป็นคีย์ที่ใช้รันบอทจริงตอนนี้

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

sfbotcgpt is the one of my discord bot that combine many projects from github into one.

## Features

- /chat to use chat-gpt3
- /draw to draw an image with dall-e mini
- /multidraw to draw 3x3 image in one time
- /help to check other feature

## Installation

sfbotcgpt requires server to run this bot

Install the dependencies and start the script.

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
## Cloned feature bot credit

| Features | Projects | Github |
| ------ | ------ | ------ |
| Chat Bot | Chat GPT | https://github.com/Zero6992/chatGPT-discord-bot |
| Image Drawing | Dall-E Mini |https://github.com/rawandahmad698/Dalle-Discord |
| 3D Drawing | In some day, I hope. | ------ |
| Youtube music Player | In some day, I hope. | ------ |


## Enjoy
