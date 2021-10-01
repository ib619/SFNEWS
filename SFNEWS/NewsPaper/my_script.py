import django.contrib.auth
from news.models import Author, Category, Post, Comment

User = django.contrib.auth.get_user_model()

user1 = User.objects.create_user(username="James")
user2 = User.objects.create_user(username="Igor")

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

science = Category.objects.create(name="Science")
art = Category.objects.create(name="Art")
food = Category.objects.create(name="Food")
politics = Category.objects.create(name="Politics")

article1 = Post.objects.create(author=author1, type="ART", text="What does the art and science have in common? That is a valid question, however not very easy to answer!", name="Art and Science")
article1.category.set([science, art])

article2 = Post.objects.create(author=author2, type="ART", name="Coffee and coding skills", text="In this article we want to investigate if coffee consumption correlates with the programmer's skill. This seems very unlikely!")
article2.category.set([food, science])

news1 = Post.objects.create(author=author2, type="NEW", name="Politics and Coffee", text="The goverment will decreace the tax for coffee import, they say that it will increace the working capabilities of citizens!")


comment1 = Comment.objects.create(post=article1, user=author2.user, text="Scientists again spending money on useless research")
comment2 = Comment.objects.create(post=article2, user=author1.user, text="My friend drinks six coffee per day but still a junior")
comment3 = Comment.objects.create(post=article2, user=author2.user, text="He should try drinking 10 cups per day to become a middle dev")
comment4 = Comment.objects.create(post=news1, user=author1.user, text="Good news for my friend, finally he will be a middle developer with that much coffee")

comment1.like()
comment1.like()
comment4.like()
comment2.like()
comment3.like()
comment3.like()
article2.like()
article2.like()
article1.like()
news1.like()
news1.like()
news1.dislike()

author1.update_rating()
author2.update_rating()

author_rating = Author.objects.all().order_by('-rating').values("user__username")
print("Best User by Rating: " + author_rating[0]["user__username"])

# order posts by rating
post_rating = Post.objects.all().order_by('-rating').values('name')
best_post = Post.objects.get(name=post_rating[0]['name'])

print("Best Post Author: " + best_post.author.user.username)
print("Best Post Rating: " + str(best_post.rating))
print("Best Post Name: " + best_post.name)
print("Best Post Preview: " + best_post.preview())

comments = Comment.objects.filter(post=best_post)

for com in comments:
    com.present()



