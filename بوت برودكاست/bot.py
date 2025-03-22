import discord
from discord.ext import commands
from discord.ui import Button, View

# إعدادات البوت
intents = discord.Intents.default()
intents.members = True  # تأكد من أن البوت يستطيع قراءة الأعضاء
bot = commands.Bot(command_prefix="!", intents=intents)

# دالة لإرسال برودكاست (رسالة خاصة لكل الأعضاء)
async def send_broadcast(message):
    for member in bot.get_all_members():
        if not member.bot:  # تأكد من أنك لا ترسل للبوتات
            try:
                await member.send(message)
            except discord.Forbidden:
                pass  # إذا كان العضو قد أغلق الرسائل الخاصة من البوتات

# لوحة تحكم للبوت
class ControlPanel(View):
    def __init__(self, message):
        super().__init__()
        self.message = message

    @discord.ui.button(label="إرسال برودكاست", style=discord.ButtonStyle.green)
    async def send_broadcast_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await send_broadcast(self.message)
            await interaction.response.send_message("تم إرسال البرودكاست إلى جميع الأعضاء!", ephemeral=True)
        else:
            await interaction.response.send_message("ليس لديك صلاحيات كافية!", ephemeral=True)

# الحدث عند جاهزية البوت
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# أمر لإنشاء البرودكاست
@bot.command()
async def setup(ctx, *, message: str):
    if ctx.author.guild_permissions.administrator:
        panel = ControlPanel(message)
        await ctx.send("تم إعداد لوحة التحكم لإرسال البرودكاست:", view=panel)
    else:
        await ctx.send("ليس لديك صلاحيات كافية!")

# بدء تشغيل البوت
bot.run('MTM1MzEzODYxNzY0Nzg5NDY1Mg.G_Oe2N.Q13h-p5JGKPPXMavsT9-pppdnxtHzVMSDILFqobot.py')
