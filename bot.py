import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

REQUIRED_ROLE = "AboMkr"  # Only members with this role can use the bot

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def has_required_role():
    async def predicate(interaction: discord.Interaction) -> bool:
        role = discord.utils.get(interaction.user.roles, name=REQUIRED_ROLE)
        if role is None:
            await interaction.response.send_message(
                f"❌ You need the **{REQUIRED_ROLE}** role to use this bot.", ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

# ─────────────────────────────────────────
#  ON READY
# ─────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Sync failed: {e}")


# ─────────────────────────────────────────
#  ROLE COMMANDS
# ─────────────────────────────────────────

@bot.tree.command(name="createrole", description="Create a new role")
@app_commands.describe(
    name="Role name",
    color="Hex color (e.g. ff5733) — optional",
    hoist="Show role separately in member list? (True/False)",
    mentionable="Make role mentionable? (True/False)"
)
@has_required_role()
@app_commands.checks.has_permissions(manage_roles=True)
async def createrole(
    interaction: discord.Interaction,
    name: str,
    color: str = "ffffff",
    hoist: bool = False,
    mentionable: bool = False
):
    await interaction.response.defer(ephemeral=True)
    try:
        hex_color = int(color.lstrip("#"), 16)
        role = await interaction.guild.create_role(
            name=name,
            colour=discord.Colour(hex_color),
            hoist=hoist,
            mentionable=mentionable
        )
        await interaction.followup.send(f"✅ Role **{role.name}** created!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


@bot.tree.command(name="deleterole", description="Delete a role by name")
@app_commands.describe(role="The role to delete")
@has_required_role()
@app_commands.checks.has_permissions(manage_roles=True)
async def deleterole(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer(ephemeral=True)
    try:
        name = role.name
        await role.delete()
        await interaction.followup.send(f"🗑️ Role **{name}** deleted.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


@bot.tree.command(name="assignrole", description="Assign a role to a member")
@app_commands.describe(member="The member to assign the role to", role="The role to assign")
@has_required_role()
@app_commands.checks.has_permissions(manage_roles=True)
async def assignrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await interaction.response.defer(ephemeral=True)
    try:
        await member.add_roles(role)
        await interaction.followup.send(f"✅ Gave **{role.name}** to **{member.display_name}**.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


@bot.tree.command(name="removerole", description="Remove a role from a member")
@app_commands.describe(member="The member to remove the role from", role="The role to remove")
@has_required_role()
@app_commands.checks.has_permissions(manage_roles=True)
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await interaction.response.defer(ephemeral=True)
    try:
        await member.remove_roles(role)
        await interaction.followup.send(f"✅ Removed **{role.name}** from **{member.display_name}**.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


@bot.tree.command(name="listroles", description="List all roles in the server")
@has_required_role()
async def listroles(interaction: discord.Interaction):
    roles = [r for r in interaction.guild.roles if r.name != "@everyone"]
    if not roles:
        await interaction.response.send_message("No roles found.", ephemeral=True)
        return
    embed = discord.Embed(title="📋 Server Roles", color=0x5865F2)
    embed.description = "\n".join([f"• {r.mention} — `{r.id}`" for r in reversed(roles)])
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ─────────────────────────────────────────
#  CHANNEL COMMANDS
# ─────────────────────────────────────────

@bot.tree.command(name="createchannel", description="Create a text or voice channel")
@app_commands.describe(
    name="Channel name",
    type="text or voice",
    category="Category name to put it in (optional)",
    topic="Channel topic/description (text channels only)"
)
@has_required_role()
@app_commands.checks.has_permissions(manage_channels=True)
async def createchannel(
    interaction: discord.Interaction,
    name: str,
    type: str = "text",
    category: str = None,
    topic: str = None
):
    await interaction.response.defer(ephemeral=True)
    try:
        cat = None
        if category:
            cat = discord.utils.get(interaction.guild.categories, name=category)
            if not cat:
                cat = await interaction.guild.create_category(category)

        if type.lower() == "voice":
            ch = await interaction.guild.create_voice_channel(name=name, category=cat)
        else:
            ch = await interaction.guild.create_text_channel(name=name, category=cat, topic=topic)

        await interaction.followup.send(f"✅ Channel {ch.mention} created!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


@bot.tree.command(name="deletechannel", description="Delete a channel")
@app_commands.describe(channel="The channel to delete")
@has_required_role()
@app_commands.checks.has_permissions(manage_channels=True)
async def deletechannel(interaction: discord.Interaction, channel: discord.abc.GuildChannel):
    await interaction.response.defer(ephemeral=True)
    try:
        name = channel.name
        await channel.delete()
        await interaction.followup.send(f"🗑️ Channel **#{name}** deleted.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


@bot.tree.command(name="createcategory", description="Create a new category")
@app_commands.describe(name="Category name")
@has_required_role()
@app_commands.checks.has_permissions(manage_channels=True)
async def createcategory(interaction: discord.Interaction, name: str):
    await interaction.response.defer(ephemeral=True)
    try:
        cat = await interaction.guild.create_category(name)
        await interaction.followup.send(f"✅ Category **{cat.name}** created!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


@bot.tree.command(name="setchannelperm", description="Set a role's permission for a channel")
@app_commands.describe(
    channel="Target channel",
    role="Target role",
    permission="e.g. send_messages, view_channel, connect",
    allow="True to allow, False to deny"
)
@has_required_role()
@app_commands.checks.has_permissions(manage_channels=True)
async def setchannelperm(
    interaction: discord.Interaction,
    channel: discord.abc.GuildChannel,
    role: discord.Role,
    permission: str,
    allow: bool
):
    await interaction.response.defer(ephemeral=True)
    try:
        overwrite = channel.overwrites_for(role)
        setattr(overwrite, permission, allow)
        await channel.set_permissions(role, overwrite=overwrite)
        status = "✅ Allowed" if allow else "❌ Denied"
        await interaction.followup.send(
            f"{status} `{permission}` for **{role.name}** in **#{channel.name}**.", ephemeral=True
        )
    except AttributeError:
        await interaction.followup.send(f"❌ Unknown permission: `{permission}`", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


# ─────────────────────────────────────────
#  SERVER SETUP COMMAND (template-based)
# ─────────────────────────────────────────

@bot.tree.command(name="setupserver", description="Set up server from a JSON template file")
@app_commands.describe(template="Template name: gaming | community | study | custom")
@has_required_role()
@app_commands.checks.has_permissions(administrator=True)
async def setupserver(interaction: discord.Interaction, template: str = "gaming"):
    await interaction.response.defer(ephemeral=True)

    templates = {
        "gaming": {
            "roles": [
                {"name": "Admin",      "color": "e74c3c", "hoist": True, "mentionable": False},
                {"name": "Moderator",  "color": "e67e22", "hoist": True, "mentionable": True},
                {"name": "VIP",        "color": "f1c40f", "hoist": True, "mentionable": True},
                {"name": "Member",     "color": "2ecc71", "hoist": False, "mentionable": True},
            ],
            "categories": [
                {
                    "name": "📢 INFO",
                    "channels": [
                        {"name": "rules",         "type": "text", "topic": "Read the server rules"},
                        {"name": "announcements",  "type": "text", "topic": "Server announcements"},
                        {"name": "welcome",        "type": "text", "topic": "Welcome new members"},
                    ]
                },
                {
                    "name": "💬 GENERAL",
                    "channels": [
                        {"name": "general",        "type": "text", "topic": "General chat"},
                        {"name": "memes",          "type": "text", "topic": "Post memes here"},
                        {"name": "introductions",  "type": "text", "topic": "Introduce yourself"},
                    ]
                },
                {
                    "name": "🎮 GAMING",
                    "channels": [
                        {"name": "game-chat",      "type": "text", "topic": "Discuss games"},
                        {"name": "lfg",            "type": "text", "topic": "Looking for group"},
                        {"name": "gaming-vc",      "type": "voice"},
                        {"name": "chill-vc",       "type": "voice"},
                    ]
                },
                {
                    "name": "🔒 STAFF",
                    "channels": [
                        {"name": "staff-chat",     "type": "text", "topic": "Staff only"},
                        {"name": "mod-log",        "type": "text", "topic": "Moderation log"},
                    ]
                }
            ]
        },
        "community": {
            "roles": [
                {"name": "Admin",       "color": "9b59b6", "hoist": True, "mentionable": False},
                {"name": "Moderator",   "color": "3498db", "hoist": True, "mentionable": True},
                {"name": "Member",      "color": "1abc9c", "hoist": False, "mentionable": True},
                {"name": "New Member",  "color": "95a5a6", "hoist": False, "mentionable": False},
            ],
            "categories": [
                {
                    "name": "📌 INFO",
                    "channels": [
                        {"name": "rules",         "type": "text"},
                        {"name": "announcements", "type": "text"},
                        {"name": "roles",         "type": "text"},
                    ]
                },
                {
                    "name": "💬 COMMUNITY",
                    "channels": [
                        {"name": "general",       "type": "text"},
                        {"name": "off-topic",     "type": "text"},
                        {"name": "media",         "type": "text"},
                        {"name": "lounge",        "type": "voice"},
                    ]
                },
                {
                    "name": "🎤 VOICE",
                    "channels": [
                        {"name": "general-vc",    "type": "voice"},
                        {"name": "music",         "type": "voice"},
                    ]
                }
            ]
        },
        "study": {
            "roles": [
                {"name": "Admin",       "color": "e74c3c", "hoist": True,  "mentionable": False},
                {"name": "Tutor",       "color": "3498db", "hoist": True,  "mentionable": True},
                {"name": "Student",     "color": "2ecc71", "hoist": False, "mentionable": True},
            ],
            "categories": [
                {
                    "name": "📚 INFO",
                    "channels": [
                        {"name": "rules",         "type": "text"},
                        {"name": "announcements", "type": "text"},
                        {"name": "resources",     "type": "text", "topic": "Share study resources"},
                    ]
                },
                {
                    "name": "📖 STUDY",
                    "channels": [
                        {"name": "general-study", "type": "text"},
                        {"name": "math",          "type": "text"},
                        {"name": "science",       "type": "text"},
                        {"name": "programming",   "type": "text"},
                        {"name": "help-desk",     "type": "text", "topic": "Ask questions here"},
                    ]
                },
                {
                    "name": "🎤 STUDY ROOMS",
                    "channels": [
                        {"name": "study-room-1",  "type": "voice"},
                        {"name": "study-room-2",  "type": "voice"},
                        {"name": "tutoring",      "type": "voice"},
                    ]
                }
            ]
        }
    }

    tmpl = templates.get(template.lower())
    if not tmpl:
        await interaction.followup.send(
            f"❌ Unknown template `{template}`. Available: `gaming`, `community`, `study`", ephemeral=True
        )
        return

    guild = interaction.guild
    created_roles = {}
    created_counts = {"roles": 0, "categories": 0, "channels": 0}

    # Create roles
    for role_data in tmpl["roles"]:
        try:
            hex_color = int(role_data["color"].lstrip("#"), 16)
            role = await guild.create_role(
                name=role_data["name"],
                colour=discord.Colour(hex_color),
                hoist=role_data.get("hoist", False),
                mentionable=role_data.get("mentionable", False)
            )
            created_roles[role_data["name"]] = role
            created_counts["roles"] += 1
        except Exception:
            pass

    # Create categories and channels
    for cat_data in tmpl["categories"]:
        try:
            cat = await guild.create_category(cat_data["name"])
            created_counts["categories"] += 1

            for ch_data in cat_data.get("channels", []):
                try:
                    if ch_data["type"] == "voice":
                        await guild.create_voice_channel(name=ch_data["name"], category=cat)
                    else:
                        await guild.create_text_channel(
                            name=ch_data["name"],
                            category=cat,
                            topic=ch_data.get("topic", "")
                        )
                    created_counts["channels"] += 1
                except Exception:
                    pass
        except Exception:
            pass

    embed = discord.Embed(
        title=f"🚀 Server Setup Complete — `{template}` template",
        color=0x5865F2
    )
    embed.add_field(name="Roles Created",      value=str(created_counts["roles"]),      inline=True)
    embed.add_field(name="Categories Created", value=str(created_counts["categories"]), inline=True)
    embed.add_field(name="Channels Created",   value=str(created_counts["channels"]),   inline=True)
    embed.set_footer(text="Use /createrole and /createchannel to customize further!")
    await interaction.followup.send(embed=embed, ephemeral=False)


# ─────────────────────────────────────────
#  SERVER INFO
# ─────────────────────────────────────────

@bot.tree.command(name="serverinfo", description="Show server info summary")
@has_required_role()
async def serverinfo(interaction: discord.Interaction):
    g = interaction.guild
    embed = discord.Embed(title=f"🏠 {g.name}", color=0x5865F2)
    embed.add_field(name="Members",    value=str(g.member_count),              inline=True)
    embed.add_field(name="Roles",      value=str(len(g.roles) - 1),            inline=True)
    embed.add_field(name="Channels",   value=str(len(g.channels)),             inline=True)
    embed.add_field(name="Categories", value=str(len(g.categories)),           inline=True)
    embed.add_field(name="Owner",      value=g.owner.mention if g.owner else "Unknown", inline=True)
    embed.add_field(name="Created",    value=g.created_at.strftime("%b %d, %Y"), inline=True)
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await interaction.response.send_message(embed=embed)


# ─────────────────────────────────────────
#  ERROR HANDLER
# ─────────────────────────────────────────

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You don't have permission to use this.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)


bot.run(TOKEN)
