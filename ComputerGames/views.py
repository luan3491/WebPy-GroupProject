# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Game, Review, ReviewComment, ReviewVote, CommentVote
from django.shortcuts import redirect
from Shoppingcart.models import ShoppingCart
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
import io


# Class-based Views
class GameListView(ListView):
    model = Game
    context_object_name = "all_the_games"
    template_name = "library.html"


class GameDetailView(DetailView):
    model = Game
    context_object_name = "that_one_game"
    template_name = "gamepage.html"

    def post(self, request, *args, **kwargs):
        game = self.get_object()

        Review.objects.create(
            game=game, user=request.user, text=request.POST.get("text")
        )

        return redirect("game_detail", pk=game.pk)





def game_pdf(request,pk):
    game = Game.objects.get(pk=pk)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, game.name)

    # Erstes Bild des Spiels
    first_image = game.images.first()

    if first_image:
        image = ImageReader(first_image.image.path)
        pdf.drawImage(image, 50, 600, width=250, height=180, preserveAspectRatio=True)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(300, 760, f"Genre: {game.get_genre_display()}")
    pdf.drawString(300, 740, f"Preis: {game.price} €")
    pdf.drawString(300, 720, f"FSK: {game.get_fsk_display()}")
    pdf.drawString(300, 700, f"Spieltyp: {game.get_game_type_display()}")
    pdf.drawString(300, 680, f"OS: {game.get_operation_system_display()}")
    text = pdf.beginText(300, 660)
    text.setFont("Helvetica", 12)
    text.textLine("Beschreibung:")
    text.textLines(game.description)
    pdf.drawText(text)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{game.name}.pdf")


# Function-based Views
def game_list(request):
    all_the_games = request.user.owned_games.all()
    return render(request, "library.html", {"all_the_games": all_the_games})


def game_detail(request, pk):
    that_one_game = get_object_or_404(Game, pk=pk)

    if request.method == "POST" and request.user.is_authenticated:

        if "add_to_cart" in request.POST:
            ShoppingCart.add_item(request.user, that_one_game)
            return redirect("cart")

        elif "save_review" in request.POST:
            text = request.POST.get("text")

            if text:
                Review.objects.create(
                    game=that_one_game,
                    user=request.user,
                    text=text
                )

            return redirect("game_detail", pk=pk)

    return render(request, "gamepage.html", {"that_one_game": that_one_game})


def comment_vote(request, comment_id, up_or_down):
    comment = get_object_or_404(ReviewComment, pk=comment_id)
    vote = CommentVote.objects.filter(user=request.user, comment=comment).first()

    new_vote = "U" if up_or_down == "up" else "D"

    if vote is None:
        CommentVote.objects.create(
            user=request.user, comment=comment, up_or_down=new_vote
        )

    elif vote.up_or_down == new_vote:
        vote.delete()

    else:
        vote.up_or_down = new_vote
        vote.save()

    return redirect("game_detail", pk=comment.review.game.id)


def add_review_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.method == "POST" and request.user.is_authenticated:
        ReviewComment.objects.create(
            review=review, user=request.user, text=request.POST.get("text")
        )

    return redirect("game_detail", pk=review.game.id)


def review_vote(request, review_id, vote_type):
    review = get_object_or_404(Review, pk=review_id)

    vote = ReviewVote.objects.filter(review=review, user=request.user).first()

    if vote is None:
        ReviewVote.objects.create(review=review, user=request.user, vote_type=vote_type)
    elif vote.vote_type == vote_type:
        vote.delete()
    else:
        vote.vote_type = vote_type
        vote.save()

    return redirect("game_detail", pk=review.game.id)


def home(request):
    all_the_games = Game.objects.all()

    return render(request, "homepage.html", {"all_the_games": all_the_games})
