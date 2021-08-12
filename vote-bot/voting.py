"""Manage the user voting flow."""
import discord
import peewee
from discord.ui import Button, View

from .models import Artwork, Vote


def render_artwork(artwork: Artwork) -> discord.Embed:
    """Display an artwork in a Discord embed."""
    options = {}
    if artwork.title:
        options["title"] = artwork.title
    if artwork.link:
        options["url"] = artwork.link
    if artwork.text:
        options["description"] = artwork.text
    embed = discord.Embed(**options, color=0xDD2244)
    if artwork.image:
        embed.set_image(url=artwork.image)
    return embed


class VotingView(View):
    """View that allows the user to vote on an artwork."""

    def __init__(self, interaction: discord.Interaction, artwork: Artwork):
        """Create a new voting view."""
        super().__init__(timeout=None)
        self.vote_buttons = [VoteButton(score) for score in range(1, 6)]
        for button in self.vote_buttons:
            self.add_item(button)
        self.artwork = artwork
        self.user = interaction.user
        self.interaction = interaction

    async def setup(self):
        """Send a message with the artwork and view."""
        await self.interaction.response.send_message(
            embed=render_artwork(self.artwork), view=self,
        )

    @discord.ui.button(
        label="Skip",
        style=discord.ButtonStyle.red,
        emoji="\N{BLACK RIGHTWARDS ARROW}",
        row=2,
    )
    async def skip(self, button: Button, interaction: discord.Interaction):
        """Skip this artwork."""
        if interaction.user.id != self.user.id:
            return
        await start_voting(interaction)

    @discord.ui.button(
        label="Stop Voting",
        style=discord.ButtonStyle.red,
        emoji="\N{OCTAGONAL SIGN}",
        row=2,
    )
    async def stop(self, button: Button, interaction: discord.Interaction):
        """End the voting flow."""
        # This doesn't actually do anything - the user can still use other
        # buttons to continue voting. Mainly here to avoid "how do I stop voting"
        # questions - though you can just *stop*.


class VoteButton(Button):
    """Button that allows the user to vote on an artwork."""

    view: VotingView

    def __init__(self, score: int):
        """Create a new vote button."""
        super().__init__(label=str(score), style=discord.ButtonStyle.secondary)
        self.score = score

    async def callback(self, interaction: discord.Interaction):
        """Handle the button being pressed."""
        if interaction.user.id != self.view.user.id:
            return
        self.view.artwork.vote(self.view.interaction.user.id, self.score)
        await start_voting(interaction)


async def start_voting(interaction: discord.Interaction):
    """Start the voting flow."""
    query = (
        Artwork.select()
        .join(
            Vote,
            peewee.JOIN.LEFT_OUTER,
            ((Artwork.artist == Vote.artwork_id) & (Vote.user == interaction.user.id)),
        )
        .where(Vote.id.is_null())
        .order_by(peewee.fn.Random())
    )
    try:
        artwork = query.get()
    except peewee.DoesNotExist:
        await interaction.response.send_message(
            "You've voted on all the artwork!", ephemeral=True
        )
        return
    view = VotingView(interaction, artwork)
    await view.setup()
