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

    # EXPANDED LIST OF GAMES
    games_data = [
        # --- FEATURED / TRENDING (Top 10) ---
        {
            "title": "Elden Ring",
            "description": "Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring.",
            "price": 59.99, "discount_price": 39.99, "genre": "rpg", "release_date": date(2022, 2, 25), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_Art.jpg"
        },
        {
            "title": "God of War Ragnarök",
            "description": "Kratos and Atreus must journey to each of the Nine Realms in search of answers.",
            "price": 69.99, "discount_price": 49.99, "genre": "action", "release_date": date(2022, 11, 9), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/e/ee/God_of_War_Ragnar%C3%B6k_cover.jpg"
        },
        {
            "title": "Cyberpunk 2077",
            "description": "An open-world, action-adventure story set in Night City.",
            "price": 59.99, "discount_price": 29.99, "genre": "rpg", "release_date": date(2020, 12, 10), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Cyberpunk_2077_box_art.jpg"
        },
        {
            "title": "Red Dead Redemption 2",
            "description": "Arthur Morgan and the Van der Linde gang are outlaws on the run.",
            "price": 59.99, "discount_price": 19.80, "genre": "action", "release_date": date(2018, 10, 26), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg"
        },
        {
            "title": "Baldur's Gate 3",
            "description": "Gather your party and return to the Forgotten Realms in a tale of fellowship and betrayal.",
            "price": 59.99, "discount_price": None, "genre": "rpg", "release_date": date(2023, 8, 3), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/12/Baldur%27s_Gate_3_cover_art.jpg"
        },
        {
            "title": "Call of Duty: Modern Warfare III",
            "description": "Captain Price and Task Force 141 face off against the ultimate threat.",
            "price": 69.99, "discount_price": 48.99, "genre": "action", "release_date": date(2023, 11, 10), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/1f/Call_of_Duty_Modern_Warfare_III_%282023%29_cover_art.jpg"
        },
        {
            "title": "Marvel's Spider-Man 2",
            "description": "Spider-Men, Peter Parker and Miles Morales, return for an exciting new adventure.",
            "price": 69.99, "discount_price": None, "genre": "action", "release_date": date(2023, 10, 20), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0f/Marvel%27s_Spider-Man_2_cover_art.jpg"
        },
        {
            "title": "Resident Evil 4 Remake",
            "description": "Survival is just the beginning. Six years have passed since the biological disaster.",
            "price": 59.99, "discount_price": 39.99, "genre": "action", "release_date": date(2023, 3, 24), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/d/df/Resident_Evil_4_remake_cover_art.jpg"
        },
        {
            "title": "Starfield",
            "description": "In this next generation role-playing game set amongst the stars, create any character you want.",
            "price": 69.99, "discount_price": 55.99, "genre": "rpg", "release_date": date(2023, 9, 6), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/6/6d/Starfield_cover_art.jpg"
        },
        {
            "title": "Final Fantasy XVI",
            "description": "An epic dark fantasy where the fates of the land are decided by the mighty Eikons.",
            "price": 69.99, "discount_price": 49.99, "genre": "rpg", "release_date": date(2023, 6, 22), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/02/Final_Fantasy_XVI_cover_art.jpg"
        },

        # --- STANDARD CATALOG (Browse Page) ---
        {
            "title": "Grand Theft Auto V",
            "description": "Experience the interwoven stories of three criminals in Los Santos.",
            "price": 29.99, "discount_price": 14.99, "genre": "action", "release_date": date(2013, 9, 17), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png"
        },
        {
            "title": "The Witcher 3: Wild Hunt",
            "description": "You are Geralt of Rivia, mercenary monster slayer.",
            "price": 39.99, "discount_price": 9.99, "genre": "rpg", "release_date": date(2015, 5, 19), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg"
        },
        {
            "title": "Minecraft",
            "description": "Prepare for an adventure of limitless possibilities.",
            "price": 29.99, "discount_price": None, "genre": "strategy", "release_date": date(2011, 11, 18), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/5/51/Minecraft_cover.png"
        },
        {
            "title": "Hades",
            "description": "Defy the god of the dead as you hack and slash out of the Underworld.",
            "price": 24.99, "discount_price": 12.49, "genre": "indie", "release_date": date(2020, 9, 17), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/c/cc/Hades_cover_art.jpg"
        },
        {
            "title": "Hollow Knight",
            "description": "Forge your own path in Hollow Knight! An epic action adventure.",
            "price": 14.99, "discount_price": 7.49, "genre": "indie", "release_date": date(2017, 2, 24), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/04/Hollow_Knight_first_cover_art.webp"
        },
        {
            "title": "Stardew Valley",
            "description": "You've inherited your grandfather's old farm plot in Stardew Valley.",
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
            "description": "A 5v5 character-based tactical shooter.",
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
            "title": "League of Legends",
            "description": "A team-based strategy game where two teams of five powerful champions face off.",
            "price": 0.00, "discount_price": None, "genre": "strategy", "release_date": date(2009, 10, 27), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/7/77/League_of_Legends_cover.jpg"
        },
        {
            "title": "Horizon Forbidden West",
            "description": "Join Aloy as she braves the Forbidden West.",
            "price": 59.99, "discount_price": 39.99, "genre": "action", "release_date": date(2022, 2, 18), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/6/69/Horizon_Forbidden_West_cover_art.jpg"
        },
        {
            "title": "Ghost of Tsushima",
            "description": "Uncover the hidden wonders of Tsushima in this open-world action adventure.",
            "price": 59.99, "discount_price": 29.39, "genre": "action", "release_date": date(2020, 7, 17), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b6/Ghost_of_Tsushima.jpg"
        },
        {
            "title": "Doom Eternal",
            "description": "Hell’s armies have invaded Earth. Become the Slayer in an epic single-player campaign.",
            "price": 39.99, "discount_price": 9.99, "genre": "action", "release_date": date(2020, 3, 20), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9d/Cover_Art_of_Doom_Eternal.png"
        },
        {
            "title": "Control",
            "description": "After a secretive agency in New York is invaded by an otherworldly threat, you become the new Director.",
            "price": 29.99, "discount_price": 7.49, "genre": "action", "release_date": date(2019, 8, 27), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/5/5c/Control_game_cover_art.jpg"
        },
        {
            "title": "Sekiro: Shadows Die Twice",
            "description": "Carve your own clever path to vengeance in this award-winning adventure.",
            "price": 59.99, "discount_price": 29.99, "genre": "action", "release_date": date(2019, 3, 22), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/6/6e/Sekiro_art.jpg"
        }
    ]

    print("STEP 2: Downloading new images and creating games...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for game_data in games_data:
        image_url = game_data.pop('image_url', None)
        
        # Only proceed if we have an image URL
        if image_url:
            try:
                req = urllib.request.Request(image_url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        game = Game.objects.create(**game_data)
                        
                        parsed_url = urlparse(image_url)
                        ext = os.path.splitext(parsed_url.path)[1]
                        if not ext: ext = ".jpg"
                        file_name = f"{game.title.replace(' ', '_').replace(':', '').replace('\'', '').lower()}{ext}"
                        
                        game.image.save(file_name, ContentFile(response.read()), save=True)
                        print(f"Created: {game.title}")
                    else:
                        print(f"Skipped {game_data['title']}: URL returned status {response.status}")
            except Exception as e:
                print(f"Skipped {game_data['title']}: Image download failed - {e}")

    print("\nSUCCESS! Database refreshed.")

if __name__ == '__main__':
    populate()