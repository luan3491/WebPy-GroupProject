from django.contrib import admin
from .models import Game, ReviewComment, CommentVote, Review, ReviewVote, GameImage

admin.site.register(Game)
admin.site.register(ReviewComment)
admin.site.register(CommentVote)
admin.site.register(Review)
admin.site.register(ReviewVote)
admin.site.register(GameImage)