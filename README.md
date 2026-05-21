# 🤖 Discord Server Manager Bot

A fully customizable Discord bot to manage roles, channels, categories, and run full server setups from templates.

---

## ⚙️ Setup

### 1. Install Python 3.10+
Make sure you have Python installed: https://python.org

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your Discord Bot
1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it
3. Go to **Bot** tab → click **Add Bot**
4. Under **Privileged Gateway Intents**, enable:
   - **Server Members Intent**
   - **Message Content Intent**
5. Copy the **Token** and paste it in `.env`:
   ```
   DISCORD_TOKEN=your_token_here
   ```

### 4. Invite the bot to your server
1. In the Developer Portal → **OAuth2 → URL Generator**
2. Check **bot** and **applications.commands**
3. Under Bot Permissions, check:
   - Manage Roles
   - Manage Channels
   - Send Messages
   - Embed Links
4. Copy the generated URL → open in browser → invite to server

### 5. Run the bot
```bash
python bot.py
```

---

## 🎮 Commands

### Role Management
| Command | Description |
|---|---|
| `/createrole name color hoist mentionable` | Create a new role |
| `/deleterole role` | Delete a role |
| `/assignrole member role` | Give a role to a member |
| `/removerole member role` | Remove a role from a member |
| `/listroles` | List all server roles |

### Channel Management
| Command | Description |
|---|---|
| `/createchannel name type category topic` | Create text or voice channel |
| `/deletechannel channel` | Delete a channel |
| `/createcategory name` | Create a new category |
| `/setchannelperm channel role permission allow` | Set role permission for channel |

### Server Setup
| Command | Description |
|---|---|
| `/setupserver template` | Build entire server from template |
| `/serverinfo` | Show server stats |

### Templates available for `/setupserver`:
- `gaming` — Info, General, Gaming, Staff categories with matching roles
- `community` — Info, Community, Voice with community roles
- `study` — Info, Study, Study Rooms with Tutor/Student roles

---

## 🔧 Adding Custom Templates

In `bot.py`, find the `templates` dictionary inside the `setupserver` command. Copy an existing template and modify the roles and channels to match your needs.

---

## 📝 Permission names for `/setchannelperm`
Common ones: `view_channel`, `send_messages`, `read_message_history`, `connect`, `speak`, `manage_messages`, `attach_files`, `embed_links`
