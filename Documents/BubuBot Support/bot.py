import discord, sqlite3
import bot
from discord.ext import commands
from discord import app_commands

db = sqlite3.connect(database="database.db")


client = commands.Bot(command_prefix="q", intents=discord.Intents.all())

@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print("Conectado como:\n{}#{}".format(client.user.name, client.user.discriminator))
        print("Sincronizados {} comandos".format(len(synced)))

    except discord.RateLimited:
        pass




reportes = 1
cursor = db.cursor()



@client.event
async def on_message(message:discord.Message):
    guild = message.guild

    cursor.execute("""SELECT mensaje FROM bugs WHERE servidor = 1038484670326779945""")

    res = cursor.fetchall()

    msg = res[0][0]

    if not guild:

        cursor.execute("""SELECT activo FROM bugs WHERE servidor = 1038484670326779945""")
        active = cursor.fetchone()

        inti = active

        if inti == 0:
            return await message.author.send("""Los reportes por MD están desactivados""")

        elif inti == 1:
            pass

        report = discord.Embed(title="Bug Reportado", description=msg, color=discord.Color.random())

        await message.author.send(embeds=[report])

        canal = await client.fetch_channel(1043498666033430538)
    


        num_reps = bot.reportes

        bot.reportes = num_reps+1
        



        bug = discord.Embed(title="Reporte de bugs Nº {}".format(num_reps), description="```\n{}```".format(message.content), color=discord.Color.random())
        bug.set_footer(text="Reporte realizado por: | {}#{}".format(message.author.name, message.author.discriminator), icon_url=str(message.author.display_avatar.url))

        await canal.send(embeds=[bug])


@client.tree.command(name="settings")
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def _l_view(ctx:discord.Interaction):

    cursor.execute("SELECT * FROM bugs WHERE servidor = {}".format(ctx.guild.id))

    results = cursor.fetchall()

    if IndexError in results:
        
        return await ctx.response.send_message("Se han creado tus ajustes, vuelve a usar el comando para verlos.", ephemeral=True)

    if(len(results) == 0):
            
        cursor.execute("""INSERT INTO bugs VALUES({}, 0, '¡Gracias por reportar el error, se ha enviado al canal de errores para que sea solucionado!')""".format(ctx.guild.id))

        results = cursor.fetchall()

    
    activo = results[0][1]
    msg = results[0][2]

    valor_a = "..."

    if activo == 1:
        valor_a = "Sí"

    elif activo == 0:
        valor_a = "No"


    embed = discord.Embed(title="Configuración", color=discord.Color.random())
    embed.add_field(name="Reportes Activos:", value=valor_a)
    embed.add_field(name="Mensaje:", value=str(msg))

    await ctx.response.send_message(embeds=[embed], ephemeral=True)


@_l_view.error
async def setting_error(ctx:discord.Interaction, error):
    await ctx.response.send_message("Se han creado tus ajustes, vuelve a usar el comando para verlos", ephemeral=True)

@client.tree.command(name="set-bug-message")
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def _set_msg(ctx:discord.Interaction):

    class Modal(discord.ui.Modal, title="Establecer mensaje"):

        msg = discord.ui.TextInput(label="Nuevo mensaje", required=True, style=discord.TextStyle.long)

        async def on_submit(self, interaction: discord.Interaction):
            cursor.execute("""UPDATE bugs SET mensaje = '{}' WHERE servidor = {}""".format(self.msg, interaction.guild.id))
            await interaction.response.send_message("¡Mensaje nuevo establecido!\n```\n{}```".format(self.msg), ephemeral=True)


    class Buttons(discord.ui.View):
        @discord.ui.button(label="Ver mensaje actual", style=discord.ButtonStyle.blurple, row=0)
        async def first_button_callback(self, interaction:discord.Interaction, button:discord.Button):
            try:
                cursor.execute("""SELECT mensaje FROM bugs WHERE servidor = {}""".format(interaction.guild.id))
                res = cursor.fetchall()

                msg = res[0][0]

            except: return await interaction.response.send_message("```\n¡Gracias por reportar el error, se ha enviado al canal de errores para que sea solucionado!```", ephemeral=True)

            await interaction.response.send_message(content="```\n{}```".format(msg), ephemeral=True)

        @discord.ui.button(label="Establecer mensaje", style=discord.ButtonStyle.blurple, row=0)
        async def second_button_callback(self, interaction:discord.Interaction, button:discord.Button):
            await interaction.response.send_modal(Modal())

    await ctx.response.send_message("Elige que quieres hacer con el mensaje de reportes de bugs:", view=Buttons(), ephemeral=True)

@client.tree.command(name="set-bug-reports")
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def _set_act(ctx:discord.Interaction):
    class Buttons(discord.ui.View):
        @discord.ui.button(label="Activar", style=discord.ButtonStyle.success, row=0)
        async def first_button_callback(self, interaction:discord.Interaction, button:discord.Button):
            try:
                cursor.execute("""UPDATE bugs SET activo = 1 WHERE servidor = {}""".format(interaction.guild.id))
            except:
                cursor.execute("""INSERT INTO bugs VALUS ({}, 1, '¡Gracias por reportar el error, se ha enviado al canal de errores para que sea solucionado!')""")
                return await interaction.response.edit_message(view=Cambioopinion(), content="Se han actualizado tus ajustes.\nReportes de bugs:\n```\nActivos```")

            await interaction.response.edit_message(view=Cambioopinion(), content="Se han actualizado tus ajustes.\nReportes de bugs:\n```\nActivos```")


        @discord.ui.button(label="Desactivar", style=discord.ButtonStyle.danger, row=0)
        async def second_button_callback(self, interaction:discord.Interaction, button:discord.Button):
            try:
                cursor.execute("""UPDATE bugs SET activo = 0 WHERE servidor = {}""".format(interaction.guild.id))
            except:
                cursor.execute("""INSERT INTO bugs VALUS ({}, 0, '¡Gracias por reportar el error, se ha enviado al canal de errores para que sea solucionado!')""")
                return await interaction.response.edit_message(view=Cambioopinion(), content="Se han actualizado tus ajustes.\nReportes de bugs:\n```\nActivos```")

            await interaction.response.edit_message(view=Cambioopinion(), content="Se han actualizado tus ajustes.\nReportes de bugs:\n```\nInactivos```")


    class Cambioopinion(discord.ui.View):
        @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.success)
        async def first_button_callback(self, interaction:discord.Interaction, button:discord.Button):
            await interaction.response.edit_message(view=None)

        @discord.ui.button(label="Cambiar ajuste", style=discord.ButtonStyle.red)
        async def second_button_callback(self, interaction:discord.Interaction, button:discord.Button):
            await interaction.response.edit_message(content="Elige que quieres hacer con los reportes de bugs:", view=Buttons())

    await ctx.response.send_message("Elige que quieres hacer con los reportes de bugs:", view=Buttons(), ephemeral=True)

            


client.run("MTA0Mzk2NzM1MTcyMjM1Njc2OA.G1YfaT.g78PZwOb-isUSZS11RXDqbERT0PYwcrp_Qz2sM")

from difflib import get_close_matches


# Ahora se define el bot:
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all()) ## command_prefix establece el prefijo, puedes usar commands.when_mentioned_or() para que sea si se le menciona o usa un prefijo

warns = sqlite3.connect(database="warns.db")

import googletrans
from discord.app_commands import describe
#Con eso sirve, ahora, quieres comandos de / o con . ? #no se pueden ambos? # si se puede, y muy facil


class SupremeHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.blurple())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if command_signatures := [
                self.get_command_signature(c) for c in filtered
            ]:
                cog_name = getattr(cog, "qualified_name", "Descategorizados")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command) , color=discord.Color.blurple())
        if command.help:
            embed.description = command.help
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = discord.Embed(title=title, description=description or "Sin descripción...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "Sin descripción...")

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

bot.help_command = SupremeHelpCommand()


#primero hacemos el comando


@bot.hybrid_command(name="warn")
@commands.has_permissions(moderate_members=True)
@describe(usuario = "El usuario a advertir", numero_warns = "El número de warns que agregarás al usuario", razon = "La razón por la que le adviertes")
async def _warn(ctx, usuario:discord.Member, numero_warns:int, *, razon:str = None):
  
  if razon == None:
    razon = "Incumplir las reglas"
  
  
  cursor = warns.cursor()

  cursor.execute("CREATE TABLE IF NOT EXISTS warns (servidor BIGINT NOT NULL PRIMARY KEY, usuario BIGINT NOT NULL UNIQUE, numero INT DEFAULT 0)")

  cursor.execute("SELECT numero FROM warns WHERE servidor = {} AND usuario = {}".format(ctx.guild.id, usuario.id))
  no = cursor.fetchone()

  if no is None:
    cursor.execute("INSERT INTO warns VALUES ({}, {}, {})".format(ctx.guild.id, usuario.id, numero_warns))

    return await ctx.reply("He advertido a {}, ahora tiene {} warn(s)".format(usuario, numero_warns))


  else:
    pass

  nom = no[0]
  nuevas = int(nom+numero_warns)
  
  cursor.execute("""UPDATE warns SET numero = {} WHERE servidor = {} AND usuario = {} """.format(nuevas, ctx.guild.id, usuario.id))

  await ctx.reply("He añadido {} warn(s) a {} por:\n```\n{}```Ahora tiene {} advertencias".format(numero_warns, usuario, razon, nuevas))


@bot.hybrid_command(name="ban")  #tremendo comando lol
@commands.has_permissions(ban_members=True)
@describe(usuario = "El usuario a banear", razon="La razón por la que baneas al usuario")
async def _ban(ctx, usuario:discord.Member, *, razon:str = None): # el None dice que por defecto, la razon será ninguna.

  """
  Banea al usuario indicado
  """

  if razon == None: # si la razon es ninguna...
    razon = "{}#{} ha baneado a {}".format(ctx.author.name, ctx.author.discriminator, usuario) # esto dice que la razon sea "" si no se ha especificado

  else:
    razon = razon



  # ahora hagamos que discord banee el usuario

  try:
    await ctx.guild.ban(usuario, reason=razon) # banea al usuario por la razon dada
    await ctx.reply("He baneado a {}".format(usuario)) # cuando lo usas, responde con "He baneado a Usuario#1111" si es que lo ha podido banear, si no, no.
  except:
    await ctx.reply("No he podido banear a {}".format(usuario)) # este mensaje solo se envía si no se ha podido banear a Usuario#1111

  # y ya estaría el comando .ban y /ban



#por aqui si eso
@bot.hybrid_command(name="unban") # ahora con el comando .unban y /unban
@commands.has_permissions(ban_members=True)
@describe(usuario = "La ID del usuario a desbanear")
async def _unban(ctx, *, usuario:id): # esto dice que hay dos parametros, ctx, que hace que el bot responda y usuario, que una opcion del comando

  """
  Desbanea al usuario especificado
  """

  user = await bot.fetch_user(usuario)
  await ctx.guild.unban(user)
  await ctx.reply("He desbaneado a {}".format(usuario))



# pero, para que los usuario puedan ejecutar el comando necesitan permisos de banear usuarios, ¿no?, pues se añade usando:
# @commands.has_permissions(ban_members=True) #ok # ahora añade tu token abajo



@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):

    cmd = ctx.invoked_with

    cmds = [cmd.name for cmd in bot.commands if not cmd.hidden]

    matches = get_close_matches(cmd, cmds)

    if len(matches) > 0:
      await ctx.reply("Comando `{}` no encontrado, a lo mejor te referías a:\n{}".format(cmd, matches[0]))
    else:
      await ctx.reply("Comando no encontrado")

  else:

    trans = googletrans.Translator()

    texto = trans.translate(text=error, dest="es", src="en")
    
    await ctx.reply(content=f"Error en español:\n{texto.text}\n\nError en inglés:\n{texto.pronunciation}")

@bot.event
async def on_ready():
  await bot.tree.sync()

bot.run("MTA0NDMxODQyNTk0Nzg0MDYwMg.GeEAtM.RsM0u04kFuuYGCbow2pd_8fcxpP2-LpJpYQ7gk") #ok perame #vale, ahora lo ejecuto #ok # fallo mio, ahora si # vale, agrega el bot a un server y si eso me invitas #ok esperame #ahora que haces?? para saber# ahora hago que si se usa un comando que no existe, muestre un error y comandos similares #ya acabaste??