# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .forms import GameImageForm, GameForm
from .models import Game, Review, ReviewComment, ReviewVote, CommentVote
from .models import Report
from django.shortcuts import redirect
from Shoppingcart.models import ShoppingCart
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
import io
from django.contrib.auth.decorators import login_required
from Useradmin.forms import UserForm


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
    if not request.user.is_authenticated:
        return redirect("login")
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
                already_reviewed = Review.objects.filter(
                    game=that_one_game,
                    user=request.user
                ).exists()

                if not already_reviewed:
                    Review.objects.create(
                        game=that_one_game,
                        user=request.user,
                        text=text
                    )
            return redirect("game_detail", pk=pk)
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            game=that_one_game,
            user=request.user
        ).first()

    return render(request, "gamepage.html", {
        "that_one_game": that_one_game,
        "user_review": user_review,
    })

@login_required
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

@login_required
def add_review_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.method == "POST" and request.user.is_authenticated:
        ReviewComment.objects.create(
            review=review, user=request.user, text=request.POST.get("text")
        )

    return redirect("game_detail", pk=review.game.id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(ReviewComment, pk=comment_id)

    if comment.user != request.user:
        return redirect("game_detail", pk=comment.review.game.id)

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            comment.text = text
            comment.save()

    return redirect("game_detail", pk=comment.review.game.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(ReviewComment, pk=comment_id)

    if comment.user == request.user:
        game_id = comment.review.game.id
        comment.delete()
        return redirect("game_detail", pk=game_id)

    return redirect("game_detail", pk=comment.review.game.id)


@login_required
def delete_comment_cs(request, comment_id):
    comment = get_object_or_404(ReviewComment, pk=comment_id)
    if request.user.user_type == "CS" :
        game_id = comment.review.game.id
        comment.delete()
        return redirect("game_detail", pk=game_id)
    return redirect("game_detail", pk=comment.review.game.id)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # only owner can edit
    if review.user != request.user:
        return redirect("game_detail", pk=review.game.id)

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            review.text = text
            review.save()

    return redirect("game_detail", pk=review.game.id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if review.user == request.user:
        game_id = review.game.id
        review.delete()
        return redirect("game_detail", pk=game_id)

    return redirect("game_detail", pk=review.game.id)

@login_required
def delete_review_cs(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user.user_type == "CS" :
        game_id = review.game.id
        review.delete()
        return redirect("game_detail", pk=game_id)
    return redirect("game_detail", pk=review.game.id)

@login_required
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



@login_required
def create_game(request):
    if request.user.user_type != "CS":
        return redirect("home")
    if request.method == "POST":
        form = GameForm(request.POST)
        image_form = GameImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            game = form.save()
            image = image_form.save(commit=False)
            image.game = game
            image.save()
            return redirect("game_detail", pk=game.pk)
    else:
        form = GameForm()
        image_form = GameImageForm()
    return render(request, "new_game.html", {
        "form": form,
        "image_form": image_form,
    })


@login_required
def cs(request):
    if request.user.user_type != "CS":
        return redirect("home")
    User = get_user_model()
    users = User.objects.filter(user_type="CU")
    all_the_games = Game.objects.all()
    alle_the_reports = Report.objects.all()
    return render(request, "cs_details.html", {
        "all_the_users": users,
        "all_the_games": all_the_games,
        "alle_the_reports": alle_the_reports,
    })


@login_required
def cs_user_detail(request, pk):
    if request.user.user_type != "CS":
        return redirect("home")
    User = get_user_model()
    user_detail = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user_detail)
        if form.is_valid():
            form.save()
            return redirect("cs_page")
    else:
        form = UserForm(instance=user_detail)
    return render(request, "cs_user_detail.html", {
        "form": form,
        "user_detail": user_detail,
    })

@login_required
def cs_game_detail(request, pk):
    if request.user.user_type != "CS":
        return redirect("home")
    game = get_object_or_404(Game, pk=pk)
    image = game.images.first()
    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        image_form = GameImageForm(
            request.POST,
            request.FILES,
            instance=image
        )
        if form.is_valid() and image_form.is_valid():
            game = form.save()
            game_image = image_form.save(commit=False)
            game_image.game = game
            game_image.save()
            return redirect("game_detail", pk=game.pk)
    else:
        form = GameForm(instance=game)
        image_form = GameImageForm(instance=image)
    return render(request, "cs_game_detail.html", {
        "form": form,
        "image_form": image_form,
        "game": game,
    })




@login_required
def report_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    Report.objects.get_or_create(
        review=review,
        user=request.user,
    )
    return redirect("game_detail", pk=review.game.id)


