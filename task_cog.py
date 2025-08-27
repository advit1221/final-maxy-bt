import discord
from discord.ext import commands
from discord import app_commands
import db

class TaskCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    task_group = app_commands.Group(name="task", description="Commands for managing volunteer tasks.")

    @task_group.command(name="add", description="Adds a new task for volunteers.")
    @app_commands.describe(details="Describe the task that needs to be done.")
    async def add(self, interaction: discord.Interaction, details: str):
        try:
            task_id = db.create_task(details)
            embed = discord.Embed(
                title="Task Added",
                description=f"New task `{task_id}` created: {details}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @task_group.command(name="claim", description="Claim an active task.")
    @app_commands.describe(task_id="The ID of the task you want to claim.")
    async def claim(self, interaction: discord.Interaction, task_id: int):
        task = db.fetch_task_by_id(task_id)
        if not task:
            await interaction.response.send_message(f"Task with ID `{task_id}` not found.", ephemeral=True)
            return
        
        if task['status'] != 'active':
            await interaction.response.send_message(f"Task `{task_id}` is not available for claiming.", ephemeral=True)
            return

        if db.update_task_claim(task_id, interaction.user.id, interaction.user.name):
            embed = discord.Embed(
                title="Task Claimed",
                description=f"{interaction.user.mention} has claimed task `{task_id}`:\n> {task['description']}",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Failed to claim task. It may have been claimed by another user.", ephemeral=True)

    @task_group.command(name="done", description="Mark a task you claimed as completed.")
    @app_commands.describe(task_id="The ID of the task you completed.")
    async def done(self, interaction: discord.Interaction, task_id: int):
        task = db.fetch_task_by_id(task_id)
        if not task:
            await interaction.response.send_message(f"Task with ID `{task_id}` not found.", ephemeral=True)
            return

        if task['claimed_by'] != interaction.user.id:
            await interaction.response.send_message(f"You cannot mark this task as done; you did not claim it.", ephemeral=True)
            return
            
        if task['status'] == 'completed':
            await interaction.response.send_message(f"This task has already been completed.", ephemeral=True)
            return

        if db.update_task_completion(task_id, interaction.user.id):
            embed = discord.Embed(
                title="Task Completed",
                description=f"Kudos to {interaction.user.mention}! Task `{task_id}` is complete:\n> {task['description']}",
                color=discord.Color.gold()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("An error occurred while completing the task.", ephemeral=True)

    @task_group.command(name="unclaim", description="Release a task you previously claimed.")
    @app_commands.describe(task_id="The ID of the task to release.")
    async def unclaim(self, interaction: discord.Interaction, task_id: int):
        task = db.fetch_task_by_id(task_id)
        if not task:
            await interaction.response.send_message(f"Task with ID `{task_id}` not found.", ephemeral=True)
            return

        if task['claimed_by'] != interaction.user.id:
            await interaction.response.send_message(f"You cannot unclaim this task as you did not claim it.", ephemeral=True)
            return
            
        if task['status'] != 'claimed':
            await interaction.response.send_message(f"This task is not currently claimed.", ephemeral=True)
            return

        if db.update_task_unclaim(task_id, interaction.user.id):
            embed = discord.Embed(
                title="Task Unclaimed",
                description=f"{interaction.user.mention} released task `{task_id}`. It is now active.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("An error occurred while trying to unclaim the task.", ephemeral=True)

    @app_commands.command(name="tasks", description="Displays all current tasks.")
    async def tasks(self, interaction: discord.Interaction):
        all_tasks = db.fetch_all_tasks()
        
        embed = discord.Embed(
            title="Volunteer Task Board",
            color=0x5865F2 # Discord Blurple
        )

        active_tasks = [t for t in all_tasks if t['status'] == 'active']
        claimed_tasks = [t for t in all_tasks if t['status'] == 'claimed']
        completed_tasks = [t for t in all_tasks if t['status'] == 'completed']

        active_str = "\n".join([f"`{t['id']}`: {t['description']}" for t in active_tasks]) or "None"
        claimed_str = "\n".join([f"`{t['id']}`: {t['description']} (Claimed by **{t['claimed_by_username']}**)" for t in claimed_tasks]) or "None"
        completed_str = "\n".join([f"`{t['id']}`: {t['description']} (Completed by **{t['claimed_by_username']}**)" for t in completed_tasks[:10]]) or "None" # Limit completed to 10

        embed.add_field(name="🟢 Active", value=active_str, inline=False)
        embed.add_field(name="🔵 Claimed", value=claimed_str, inline=False)
        embed.add_field(name="✅ Completed", value=completed_str, inline=False)
        
        embed.set_footer(text="Use /task claim <id> to get started.")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(TaskCog(bot))
