from django.db import models
from django.conf import settings


class Game(models.Model):
    GAMETYPES = [
        ("PH", "Physical"),
        ("DI", "Digital"),
    ]

    GENRES = [
        ("FP", "First-person shooter"),
        ("RP", "Role Playing"),
        ("PU", "Puzzle"),
        ("SP", "Sport"),
        ("TA", "Tactics"),
        ("AD", "Adventure"),
        ("SI", "Simulation"),
        ("TT", "Tabletop"),
    ]

    FSK = [
        (0, "ab 0"),
        (6, "ab 6"),
        (12, "ab 12"),
        (16, "ab 16"),
        (18, "ab 18"),
    ]

    OPERATIONSYSTEMS = [
        ("W", "Windows"),
        ("L", "Linux"),
        ("M", "Macos"),
        ("X", "Xbox"),
        ("P", "Playstation"),
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
        return f"Bild für {self.game.name}"


class Review(models.Model):
    STARS = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField(
        choices=STARS,
        default= 3
    )
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

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