"""Registers the Discord slash commands."""
import peewee
from discord import Interaction, Member
from dslash import allow_roles, option
from polympics import ClientError

from .bot import client, polympics
from .config import ADMIN_ROLE_ID
from .models import Artwork, Vote
from .voting import render_artwork, start_voting

ARTIST_OPTION = option("The author of the artwork.", required=True)
ADMIN_PERMS = allow_roles(ADMIN_ROLE_ID)


@ADMIN_PERMS
@client.command(default_permission=False)
async def upload(
    interaction: Interaction,
    artist: Member = ARTIST_OPTION,
    title: str = option("The artwork title."),
    image: str = option("A link to an image of the artwork."),
    text: str = option("Artwork description or textual content."),
    link: str = option("A link to (or associated with) the artwork."),
):
    """Register an artwork to be voted on."""
    artwork, overwritten = Artwork.upsert_artwork(
        artist=artist.id,
        title=title,
        image=image,
        text=text,
        link=link,
    )
    if overwritten:
        message = f"Warning: overwriting existing artwork for {artist}."
    else:
        message = f"Artwork saved for {artist}:"
    await interaction.response.send_message(
        message, embed=render_artwork(artwork), ephemeral=True
    )


@ADMIN_PERMS
@client.command(default_permission=False)
async def delete(interaction: Interaction, artist: Member = ARTIST_OPTION):
    """Delete a user's artwork from the database."""
    if not (artwork := Artwork.get_or_none(Artwork.artist == artist.id)):
        raise ValueError(f"No artwork found for {artist}.")
    artwork.delete_instance()
    await interaction.response.send_message(
        f"Artwork deleted for {artist}.", ephemeral=True
    )


@ADMIN_PERMS
@client.command(default_permission=False)
async def artwork(interaction: Interaction, artist: Member = ARTIST_OPTION):
    """View a user's artwork."""
    if not (artwork := Artwork.get_or_none(Artwork.artist == artist.id)):
        raise ValueError(f"No artwork found for {artist}.")
    await interaction.response.send_message(
        embed=render_artwork(artwork), ephemeral=True
    )


@client.command()
async def vote(interaction: Interaction):
    """Get an artwork to vote on."""
    try:
        await polympics.get_account(interaction.user.id)
    except ClientError as e:
        raise ValueError("You must be registered to vote.") from e
    await start_voting(interaction)


@client.command()
async def tickets(interaction: Interaction):
    """Check how many raffle tickets you have."""
    tickets = Vote.select().where(Vote.user == interaction.user.id).count()
    plural = "" if tickets == 1 else "s"
    await interaction.response.send_message(
        f"You have {tickets} ticket{plural}. You can get more by voting."
    )


@ADMIN_PERMS
@client.command(default_permission=False)
async def raffle(interaction: Interaction):
    """Get a raffle winner."""
    winner = Vote.select().order_by(peewee.fn.Random()).get()
    user = await interaction.guild.fetch_member(winner.user)
    await interaction.response.send_message(
        f"The winner is **{user}** ({user.mention})!!! :tada:"
    )


@ADMIN_PERMS
@client.command(default_permission=False)
async def winner(interaction: Interaction):
    """Get the winning artwork, and runners up."""
    rating = peewee.fn.Avg(Vote.rating).alias("rating")
    votes = peewee.fn.Count(Vote.id).alias("votes")
    leaderboard = list(
        Artwork.select(Artwork, rating, votes)
        .join(Vote, peewee.JOIN.LEFT_OUTER)
        .group_by(Artwork.artist)
        .order_by(-rating)
        .limit(5)
    )
    lines = [f"**The winner is <@{leaderboard[0].artist}>!!! :tada:**\n", "__Top 5:__"]
    for n, artwork in enumerate(leaderboard):
        lines.append(
            f"{n + 1}. <@{artwork.artist}> (average rating of **{artwork.rating:.2f}** "
            f"from **{artwork.votes}** votes)"
        )
    lines.append("\nHere's the winning artwork:")
    await interaction.response.send_message(
        "\n".join(lines),
        embed=render_artwork(leaderboard[0]),
    )
