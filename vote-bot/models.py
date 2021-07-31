"""Peewee ORM models for the bot."""
from typing import Optional

import peewee

from .config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

db = peewee.PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    autorollback=True,
)


class BaseModel(peewee.Model):
    """Base model to set default Peewee settings."""

    class Meta:
        """Configure Peewee."""

        database = db
        use_legacy_table_names = False


class Artwork(BaseModel):
    """A piece of artwork from a user."""

    # Author's Discord ID.
    artist = peewee.BigIntegerField(primary_key=True)
    title = peewee.CharField(max_length=255, null=True)
    # Description or textual content.
    text = peewee.CharField(max_length=2047, null=True)
    # URL to the image.
    image = peewee.CharField(max_length=255, null=True)
    link = peewee.CharField(max_length=255, null=True)

    @classmethod
    def upsert_artwork(
        cls,
        artist: int,
        title: Optional[str],
        text: Optional[str],
        image: Optional[str],
        link: Optional[str],
    ) -> tuple["Artwork", bool]:
        """Create or update a user's artwork.

        Returns the artwork and whether or not it was overwritten.
        """
        if not (image or text or link):
            raise ValueError("At least one of artwork, text or link is required.")
        if link and not title:
            raise ValueError("A title is required if link is set.")
        existing = cls.get_or_none(cls.artist == artist)
        if existing:
            existing.title = title
            existing.text = text
            existing.image = image
            existing.link = link
            existing.save()
            return existing, True
        else:
            return (
                cls.create(
                    artist=artist, title=title, text=text, image=image, link=link
                ),
                False,
            )

    def vote(self, user: int, rating: int):
        """Set a user's rating for this artwork."""
        vote = Vote.get_or_none(Vote.artwork == self, user=user)
        if vote:
            vote.rating = rating
            vote.save()
        else:
            Vote.create(artwork=self, user=user, rating=rating)


class Vote(BaseModel):
    """A rating for a piece of art, from a user."""

    artwork = peewee.ForeignKeyField(Artwork)
    # Voter's Discord ID.
    user = peewee.BigIntegerField()
    # Rating, 1 to 5.
    rating = peewee.SmallIntegerField()


db.create_tables([Artwork, Vote])
