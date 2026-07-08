from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    GAMETYPES = [
        ("PH", _("Physical")),
        ("DI", _("Digital")),
    ]

    GENRES = [
        ("FP", _("First-person shooter")),
        ("RP", _("Role Playing")),
        ("PU", _("Puzzle")),
        ("SP", _("Sport")),
        ("TA", _("Tactics")),
        ("AD", _("Adventure")),
        ("SI", _("Simulation")),
        ("TT", _("Tabletop")),
    ]

    FSK = [
        (0, _("0 and above")),
        (6, _("6 and above")),
        (12, _("12 and above")),
        (16, _("16 and above")),
        (18, _("18 and above")),
    ]

    OPERATIONSYSTEMS = [
        ("W", _("Windows")),
        ("L", _("Linux")),
        ("M", _("MacOS")),
        ("X", _("Xbox")),
        ("P", _("PlayStation")),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()

    game_type = models.CharField(
        max_length=2,
        choices=GAMETYPES,
    )

    genre = models.CharField(
        max_length=2,
        choices=GENRES,
    )

    fsk = models.IntegerField(
        choices=FSK,
    )

    price = models.DecimalField(max_digits=8, decimal_places=2)

    operation_system = models.CharField(
        choices=OPERATIONSYSTEMS,
    )

    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="owned_games", blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + " / " + self.get_genre_display() + " / FSK " + str(self.fsk)


class GameImage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="images")

    image = models.ImageField(upload_to="game_images/")
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return _("Image for %(game_name)s") % {"game_name": self.game.name}


class Review(models.Model):
    STARS = [
        (1, _("1 Star")),
        (2, _("2 Stars")),
        (3, _("3 Stars")),
        (4, _("4 Stars")),
        (5, _("5 Stars")),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField(
        choices=STARS,
        default=3,
    )
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.game}"

    def get_yes_count(self):
        return ReviewVote.objects.filter(review=self, vote_type="Y").count()

    def get_no_count(self):
        return ReviewVote.objects.filter(review=self, vote_type="N").count()

    def get_funny_count(self):
        return ReviewVote.objects.filter(review=self, vote_type="F").count()


class ReviewComment(models.Model):

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    text = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return self.text

    def get_upvotes_count(self):
        return CommentVote.objects.filter(comment=self, up_or_down="U").count()

    def get_downvotes_count(self):
        return CommentVote.objects.filter(comment=self, up_or_down="D").count()


class ReviewVote(models.Model):
    VOTE_TYPES = [("Y", "Yes"), ("N", "No"), ("F", "Funny")]
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=1, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("review", "user")

    def __str__(self):
        return f"{self.vote_type} by {self.user}"


class CommentVote(models.Model):
    VOTE_TYPES = [
        ("U", "up"),
        ("D", "down"),
    ]

    up_or_down = models.CharField(
        max_length=1,
        choices=VOTE_TYPES,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(ReviewComment, on_delete=models.CASCADE)

    def __str__(self):
        return self.up_or_down + " by " + self.user.username



class Report(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("review", "user")

    def __str__(self):
        return f"{self.user} reported {self.review}"