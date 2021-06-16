# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 18:05:25 2021

@author: HP
"""
"""***importing***"""
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Greedy
from discord import User

#intents=discord.Intents.default()
#intents.members=True

"""***setting prefix***"""
client = commands.Bot(command_prefix=">")#, intents=intents)

"""***lists to be used***"""
rules=["> no use of foul language.","respect every member","no vulgur content should be posted","Be particular about your deadlines"]  #if want to import from a text file 
filtered_words=['love','f***','girlfriend','hola']  #can also do by importing a text file

#f=open('rules.txt','r')
#rules=f.readlines()

"""***events***"""
@client.event
async def on_ready():
    print("bot is ready")

@client.event
async def on_message(message):
    for word in filtered_words:
        if word in message.content:
            await message.delete()
    
#    if ':'==message.content[0] and ':' == message.content[-1]:
#        emoji_name=message.content[1:-1]
#        for emoji in message.guild.emoji:
#            if emoji_name==emoji.name:
#                await message.channael.send(str(emoji))
#                await message.delete()
#                break
#    if "noice" in message.content:
#        await message.add_reaction("<:noice:id>")
   
    await client.process_commands(message)

#error handling 1.try except 2.eevnt
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('error')
        await ctx.message.delete()
    
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send('enter all the arguments')
        await ctx.message.delete()
        

"""***administrator commands***"""

#checking the rule 
@client.command(aliases=['rules'])
#async def hello(ctx):
 #   await ctx.send("Hi!")
async def rule(ctx,*,number):   #ctx stants for context   #ctx*number will help to read the number like rule1
    await ctx.send(rules[int(number)-1])
 

#clearing a message
@client.command(aliasis=['c'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit=amount)

#kicking a member    
@client.command(aliasis=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member,*,reason='No, reason provided'):
    #try:
    await member.send("you have been kicked"+reason)
    #except:
    await ctx.send('member has dm closed')
        
    await member.kick(reason=reason)

#banning a member    
@client.command(aliasis=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member,*,reason='No, reason provided'):
    await ctx.send(member.name+" have been banned"+reason)
    await member.ban(reason=reason)


#unban a member    
@client.command(aliasis=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member): #we are doing this becoz we will give the name of the member with its discriminator eg: >unban sheetal#2345
    banned_users = await ctx.guild.bans() #take u through the list of banned members
    member_name,member_disc= member.split('#')
    
    for banned_entry in banned_users:
        user=banned_entry.user
        if(user.name,user.discriminator)==(member_name,member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name+"has been unbanned")
            await member.send("u have been unbanned")
            return
        
    await ctx.send(member.name+"not found in the banned list")
    

#mute a member
@client.command(aliasis=['m'])
@commands.has_permissions(kick_members=True)   #mute ka alg se nhi hota isliye we r checking kick jo kick kr skta h vo mute bhi kr skega
async def mute(ctx,member:discord.Member):
    muted_role=ctx.guild.get_role(795903691981848586)
    await member.add_roles(muted_role)
    await ctx.send(member.mention+"has been muted")
    
#unmute a member
@client.command(aliasis=['um'])
@commands.has_permissions(kick_members=True)   #mute ka alg se nhi hota isliye we r checking kick jo kick kr skta h vo mute bhi kr skega
async def unmute(ctx,member:discord.Member):
    muted_role=ctx.guild.get_role(795903691981848586)
    await member.remove_roles(muted_role)
    await ctx.send(member.mention+"has been unmuted")
    

#checking a member
@client.command(aliases=['user','info'])
#@commands.has_permissions(kick_members=True)
async def whois(ctx,member:discord.Member):
    embed=discord.Embed(title = member.name,description = member.mention,color= discord.Colour.red())
    embed.add_field(name="ID", value = member.id , inline = True )
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url , text= f"requested by{ctx.author.name}")
    await ctx.send(embed=embed)
    
#
#@client.command()
#async def emoji(ctx):
#    await ctx.send("put an emjoi from emoji pedia ") #from emoji pedia we can directly use the emoji because the are universal
#    await ctx.send("<: name_of_emoji : emoji_id>") #custom emoji
#    await ctx.send("<a:emojiname:emojiid>") #for animated emoji


#images=[]
#@client.command()
#async def meme(ctx):
#    embed=discord.Embed(color=discord.colour.red())
#    random_link=random.choice(images)
#    embed.set_image(url=random_link)
#    await ctx.send(embed=embed)
    
#@client.command(aliases=["pl"])
#async def poll(ctx,*,msg):
#    channel=ctx.channel
#    try:
#        op1,op2 = msg.split("or")
#        txt = f"React with ✅ for {op1} or ❎ for {op2}"
#    except:
#        await channel.send("correct syntax: [choice1] or [choice2]")
#        return
#    
#    
#    embed = discord.Embed(title = "Poll",description = txt,colour=discord.Colour.blue())
#    message_ = await channel.send(embed=embed)
#    await message_.add_reaction("✅")
#    await message_.add_reaction("❎")
#    await ctx.message.delete()
    

"""***creating polls***"""

#creating poll for 2 options
@client.command(aliases=["pl"])
async def poll2(ctx,*,msg):
    channel=ctx.channel
    try:
        op1,op2 = msg.split("or")
        txt = f"React with the colors in front of the option : \n\n {op1} ---> ❤️ \n\n {op2} ---> 💛 \n\n"
    except:
        await channel.send("correct syntax: [choice1] or [choice2]")
        return
    
    
    embed = discord.Embed(title = "Poll",description = txt,colour=discord.Colour.blue())
    embed.set_footer(icon_url=ctx.author.avatar_url , text= f"\n Created by {ctx.author.name}")
    embed.set_thumbnail(url="https://www.seekpng.com/png/detail/25-253710_campaign-poll-images-thumbnails-vote-now-png.png")
    message_ = await channel.send(embed=embed)
    await message_.add_reaction("❤️")
    await message_.add_reaction("💛")
    await ctx.message.delete()    

#creating poll for 3 options
@client.command(aliases=["pl3"])
async def poll3(ctx,*,msg):
    channel=ctx.channel
    try:
        op1,op2,op3 = msg.split("or")
        txt = f"React with the colors in front of the option : \n\n {op1} ---> ❤️ \n\n {op2} ---> 💛 \n\n {op3} ---> 💚 \n\n"
    except:
        await channel.send("correct syntax: [choice1] or [choice2] or [choice3]")
        return
    
    
    embed = discord.Embed(title = "Poll",description = txt,colour=discord.Colour.blue())
    embed.set_footer(icon_url=ctx.author.avatar_url , text= f"\n Created by {ctx.author.name}")
    embed.set_thumbnail(url="https://www.seekpng.com/png/detail/25-253710_campaign-poll-images-thumbnails-vote-now-png.png")
    message1 = await channel.send(embed=embed)
    await message1.add_reaction("❤️")
    await message1.add_reaction("💛")
    await message1.add_reaction("💚")
    await ctx.message.delete()    


#creating poll for 4 options
@client.command(aliases=["pl4"])
async def poll4(ctx,*,msg):
    channel=ctx.channel
    try:
        op1,op2,op3,op4 = msg.split("or")
        txt = f"React with the colors in front of the option : \n\n {op1} ---> ❤️ \n\n {op2} ---> 💛 \n\n {op3} ---> 💚 \n\n {op4} ---> 💙 \n\n "
    except:
        await channel.send("correct syntax: [choice1] or [choice2] or [choice3] or [choice4]")
        return
    
    
    embed = discord.Embed(title = "Poll",description = txt,colour=discord.Colour.blue())
    embed.set_footer(icon_url=ctx.author.avatar_url , text= f"\n Created by {ctx.author.name}")
    embed.set_thumbnail(url="https://www.seekpng.com/png/detail/25-253710_campaign-poll-images-thumbnails-vote-now-png.png")
    message2 = await channel.send(embed=embed)
    await message2.add_reaction("❤️")
    await message2.add_reaction("💛")
    await message2.add_reaction("💚")
    await message2.add_reaction("💙")
    await ctx.message.delete()    


#creating poll for 5 options
@client.command(aliases=["pl5"])
async def poll5(ctx,*,msg):
    channel=ctx.channel
    try:
        op1,op2,op3,op4,op5 = msg.split("or")
        txt = f"React with the colors in front of the option : \n\n {op1} ---> ❤️ \n\n {op2} ---> 💛 \n\n {op3} ---> 💚 \n\n {op4} ---> 💙 \n\n {op5} ---> 🤎 \n\n"
    except:
        await channel.send("correct syntax: [choice1] or [choice2] or [choice3] or [choice4] or [choice5]")
        return
    
    
    embed = discord.Embed(title = "Poll",description = txt,colour=discord.Colour.blue())
    embed.set_footer(icon_url=ctx.author.avatar_url , text= f"\n Created by {ctx.author.name}")
    embed.set_thumbnail(url="https://www.seekpng.com/png/detail/25-253710_campaign-poll-images-thumbnails-vote-now-png.png")
    message3 = await channel.send(embed=embed)
    await message3.add_reaction("❤️")
    await message3.add_reaction("💛")
    await message3.add_reaction("💚")
    await message3.add_reaction("💙")
    await message3.add_reaction("🤎")
    await ctx.message.delete()    

        
"""***meeting card***"""
@client.command(aliases=['m'])
async def meeting(ctx,*,cmd):
    channel=ctx.channel
    try:
        time,date,link,topic=cmd.split('#')
        txt=f'📌 Time of the Meeting : {time}\n\n 📌 Date of the Meeting : {date} \n\n 📌 Link for the meeting : {link} \n\n 📌 Topic : {topic} \n\n react with ✅ to accept or ❎ to reject'
    except:
        await channel.send("correct syntax : time#date#link#topic")
        return
    
    embed = discord.Embed(title = "Meeting" , description = txt , colour=discord.Colour.red())
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Google_Meet_icon_%282020%29.svg/1245px-Google_Meet_icon_%282020%29.svg.png")
    embed.set_footer(text="\n\n By : Tech Hack Technologies")
    message_m=await channel.send(embed=embed)
    await message_m.add_reaction("✅")
    await message_m.add_reaction("❎")
    await ctx.msg.delete()
    #await ctx.send(embed=embed)


#@client.command(aliases=['td'])
#async def todolist(ctx,*,link):
#    
#   channel=ctx.channel
#   link_=link
#   txt=("Fill your todo list in the sheet attached \n\n 🖊️ What you have done yesterday? \n\n 🖊️ What you will be doing today? \n\n 🖊️ What is furthur plan for tomorrow? \n\n 🖊️ Is there anything that is hurdling you ?")
#    
#   embed=discord.Embed(title = "TO-DO-LIST" , description = txt , colour=discord.Colour.red())
#   embed.add_field(name="Sheet Link", value = link_ , inline = True )
#   embed.set_footer(text="\n\n By : Tech Hack Technologies")
#   await channel.send(embed=embed)


"""***creating to do list card***"""    
@client.command(aliases=['td'])
async def todolist(ctx, users: Greedy[User], *, message):
    #channel=ctx.channel
    embed = discord.Embed(title = "To-Do List" , description = f"Here's is your today's task \n\n {message} \n\n\n React to the msg with 👍 after the task is done" , colour=discord.Colour.red())
    #embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url , text= f"Alloted by {ctx.author.name}")
    
    for user in users:
       #await user.send(embed=embed) 
        message_m= await user.send(embed=embed)
        await message_m.add_reaction("👍")

client.run("API KEY")