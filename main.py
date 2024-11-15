from instabot import Bot
from datetime import datetime
from itertools import dropwhile, takewhile
import instaloader

username = input("Enter your username: ")
password = input("Enter your password: ")
search_user = input("Enter username you want: ")

# Initialize Instabot and log in
my_bot = Bot()
my_bot.login(username=username, password=password)

# Initialize Instaloader and log in
L = instaloader.Instaloader()
L.login(username, password)

# Get posts from the specified user
posts = instaloader.Profile.from_username(L.context, search_user).get_posts()

SINCE = datetime(2023, 8, 24)
UNTIL = datetime(2023, 7, 23)

# Directory to save the downloaded posts
download_directory = r"C:\Users\default.LAPTOP-GNE1HV1K\Videos\fola"  # Replace with your desired folder path

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    L.download_post(post, target=download_directory)

    # Get the post details
    post_details = instaloader.Post.from_shortcode(L.context, post.shortcode)

    # Create an empty list to store the usernames
    likers_list = []

    # Collect likers' usernames in the list
    for liker in post_details.get_likes():
        likers_list.append(liker.username)

    # Print the list of likers' usernames
    print("Likers of the post:")
    print(likers_list)

    # Interact with likers using Instabot
    for i in range(len(likers_list)):
        try:
            my_bot.like_user(likers_list[i], amount=3, filtration=False)
        except Exception as e:
            print("Exception occurred while liking:", e)

        try:
            user_id = my_bot.get_user_id_from_username(likers_list[i])
            media_id = my_bot.get_last_user_medias(user_id)
            my_bot.comment(media_id, "cool")

        except Exception as e:
            print("Exception occurred while commenting:", e)

