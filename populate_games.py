import os
import django
import urllib.request
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from datetime import date

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 2. Import your Game model
from store.models import Game

def populate():
    print("--------------------------------------")
    print("STEP 1: Cleaning database...")
    deleted_count, _ = Game.objects.all().delete()
    print(f"Deleted {deleted_count} old game entries.")
    print("--------------------------------------")

    # List of high-quality games with reliable Wiki/Steam/Console URLs
    games_data = [
        {
            "title": "Elden Ring",
            "description": "Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring and become an Elden Lord in the Lands Between.",
            "price": 59.99, "discount_price": 39.99, "genre": "rpg", "release_date": date(2022, 2, 25), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_Art.jpg"
        },
        {
            "title": "God of War Ragnarök",
            "description": "Kratos and Atreus must journey to each of the Nine Realms in search of answers as Asgardian forces prepare for a prophesied battle.",
            "price": 69.99, "discount_price": 49.99, "genre": "action", "release_date": date(2022, 11, 9), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/e/ee/God_of_War_Ragnar%C3%B6k_cover.jpg"
        },
        {
            "title": "The Last of Us Part I",
            "description": "Experience the emotional storytelling and unforgettable characters in Joel and Ellie, in a game that won over 200 Game of the Year awards.",
            "price": 69.99, "discount_price": None, "genre": "action", "release_date": date(2022, 9, 2), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/4/46/Video_Game_Cover_-_The_Last_of_Us.jpg"
        },
        {
            "title": "Cyberpunk 2077",
            "description": "An open-world, action-adventure story set in Night City, a megalopolis obsessed with power, glamour and body modification.",
            "price": 59.99, "discount_price": 29.99, "genre": "rpg", "release_date": date(2020, 12, 10), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Cyberpunk_2077_box_art.jpg"
        },
        {
            "title": "Grand Theft Auto V",
            "description": "Experience the interwoven stories of three criminals as they wreak havoc on the streets of Los Santos.",
            "price": 29.99, "discount_price": 14.99, "genre": "action", "release_date": date(2013, 9, 17), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png"
        },
        {
            "title": "Red Dead Redemption 2",
            "description": "Arthur Morgan and the Van der Linde gang are outlaws on the run. The wild west era is ending.",
            "price": 59.99, "discount_price": 19.80, "genre": "action", "release_date": date(2018, 10, 26), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg"
        },
        {
            "title": "The Witcher 3: Wild Hunt",
            "description": "You are Geralt of Rivia, mercenary monster slayer. Before you stands a war-torn, monster-infested continent.",
            "price": 39.99, "discount_price": 9.99, "genre": "rpg", "release_date": date(2015, 5, 19), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg"
        },
        {
            "title": "Marvel's Spider-Man 2",
            "description": "Spider-Men, Peter Parker and Miles Morales, return for an exciting new adventure in the critically acclaimed Marvel’s Spider-Man franchise.",
            "price": 69.99, "discount_price": None, "genre": "action", "release_date": date(2023, 10, 20), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0f/Marvel%27s_Spider-Man_2_cover_art.jpg"
        },
        {
            "title": "Hades",
            "description": "Defy the god of the dead as you hack and slash out of the Underworld in this rogue-like dungeon crawler.",
            "price": 24.99, "discount_price": 12.49, "genre": "indie", "release_date": date(2020, 9, 17), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/c/cc/Hades_cover_art.jpg"
        },
        {
            "title": "Hollow Knight",
            "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.",
            "price": 14.99, "discount_price": 7.49, "genre": "indie", "release_date": date(2017, 2, 24), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/04/Hollow_Knight_first_cover_art.webp"
        },
        {
            "title": "Call of Duty: Modern Warfare III",
            "description": "Captain Price and Task Force 141 face off against the ultimate threat in this direct sequel.",
            "price": 69.99, "discount_price": 48.99, "genre": "action", "release_date": date(2023, 11, 10), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/1f/Call_of_Duty_Modern_Warfare_III_%282023%29_cover_art.jpg"
        },
        {
            "title": "Baldur's Gate 3",
            "description": "Gather your party and return to the Forgotten Realms in a tale of fellowship and betrayal.",
            "price": 59.99, "discount_price": None, "genre": "rpg", "release_date": date(2023, 8, 3), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/12/Baldur%27s_Gate_3_cover_art.jpg"
        },
        {
            "title": "Stardew Valley",
            "description": "You've inherited your grandfather's old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins.",
            "price": 14.99, "discount_price": None, "genre": "indie", "release_date": date(2016, 2, 26), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/f/fd/Stardew_Valley_Box_Art.jpg"
        },
        {
            "title": "Overwatch 2",
            "description": "Overwatch 2 is a free-to-play, team-based action game set in the optimistic future.",
            "price": 0.00, "discount_price": None, "genre": "action", "release_date": date(2022, 10, 4), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/5/51/Overwatch_2_cover_art.jpg"
        },
        {
            "title": "Valorant",
            "description": "Blend your style and experience on a global, competitive stage. You have 13 rounds to attack and defend.",
            "price": 0.00, "discount_price": None, "genre": "action", "release_date": date(2020, 6, 2), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/f/fb/Valorant_cover_art.jpg"
        },
        {
            "title": "Terraria",
            "description": "The very world is at your fingertips as you fight for survival, fortune, and glory.",
            "price": 9.99, "discount_price": 4.99, "genre": "indie", "release_date": date(2011, 5, 16), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/3/30/Terraria_Box_Art.jpg"
        },
        {
            "title": "Resident Evil 4 Remake",
            "description": "Survival is just the beginning. Six years have passed since the biological disaster in Raccoon City.",
            "price": 59.99, "discount_price": 39.99, "genre": "action", "release_date": date(2023, 3, 24), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/d/df/Resident_Evil_4_remake_cover_art.jpg"
        },
        {
            "title": "League of Legends",
            "description": "A team-based strategy game where two teams of five powerful champions face off to destroy the other’s base.",
            "price": 0.00, "discount_price": None, "genre": "strategy", "release_date": date(2009, 10, 27), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/7/77/League_of_Legends_cover.jpg"
        },
        {
            "title": "Horizon Forbidden West",
            "description": "Join Aloy as she braves the Forbidden West – a majestic but dangerous frontier that conceals mysterious new threats.",
            "price": 59.99, "discount_price": 39.99, "genre": "action", "release_date": date(2022, 2, 18), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/6/69/Horizon_Forbidden_West_cover_art.jpg"
        },
        {
            "title": "Ghost of Tsushima",
            "description": "Uncover the hidden wonders of Tsushima in this open-world action adventure.",
            "price": 59.99, "discount_price": 29.39, "genre": "action", "release_date": date(2020, 7, 17), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b6/Ghost_of_Tsushima.jpg"
        }
    ]

    print("STEP 2: Downloading new images and creating games...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for game_data in games_data:
        image_url = game_data.pop('image_url', None)
        
        # Only proceed if we have an image URL
        if image_url:
            try:
                # 1. Verify URL is reachable first
                req = urllib.request.Request(image_url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        # 2. Only Create Game AFTER successful image check
                        game = Game.objects.create(**game_data)
                        
                        # 3. Save Image
                        parsed_url = urlparse(image_url)
                        ext = os.path.splitext(parsed_url.path)[1]
                        if not ext: ext = ".jpg"
                        file_name = f"{game.title.replace(' ', '_').replace(':', '').replace('\'', '').lower()}{ext}"
                        
                        game.image.save(file_name, ContentFile(response.read()), save=True)
                        print(f"Created & Verified: {game.title}")
                    else:
                        print(f"Skipped {game_data['title']}: URL returned status {response.status}")
            except Exception as e:
                print(f"Skipped {game_data['title']}: Image download failed - {e}")
        else:
            print(f"Skipped {game_data['title']}: No image URL provided")

    print("\nSUCCESS! Database refreshed.")

if __name__ == '__main__':
    populate()