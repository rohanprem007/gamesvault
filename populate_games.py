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

    # EXPANDED LIST OF GAMES (30+ Titles)
    games_data = [
        # --- TRENDING / FEATURED (Top 10) ---
        {
            "title": "Elden Ring",
            "description": "Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring.",
            "price": 59.99, "discount_price": 39.99, "genre": "rpg", "release_date": date(2022, 2, 25), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_Art.jpg",
            "min_os": "Windows 10", "min_cpu": "Intel Core i5-8400", "min_ram": "12 GB RAM", "min_gpu": "GTX 1060 3GB",
            "rec_os": "Windows 11", "rec_cpu": "Intel Core i7-8700K", "rec_ram": "16 GB RAM", "rec_gpu": "GTX 1070 8GB"
        },
        {
            "title": "God of War Ragnarök",
            "description": "Kratos and Atreus must journey to each of the Nine Realms in search of answers.",
            "price": 69.99, "discount_price": 49.99, "genre": "action", "release_date": date(2022, 11, 9), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/e/ee/God_of_War_Ragnar%C3%B6k_cover.jpg",
            "min_os": "Windows 10", "min_cpu": "Intel i5-2500k", "min_ram": "8 GB RAM", "min_gpu": "GTX 960",
            "rec_os": "Windows 10", "rec_cpu": "Intel i5-6600k", "rec_ram": "16 GB RAM", "rec_gpu": "GTX 1060"
        },
        {
            "title": "Cyberpunk 2077",
            "description": "An open-world, action-adventure story set in Night City.",
            "price": 59.99, "discount_price": 29.99, "genre": "rpg", "release_date": date(2020, 12, 10), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Cyberpunk_2077_box_art.jpg",
            "min_os": "Windows 10", "min_cpu": "Core i7-6700", "min_ram": "12 GB RAM", "min_gpu": "GTX 1060",
            "rec_os": "Windows 10", "rec_cpu": "Core i7-12700", "rec_ram": "16 GB RAM", "rec_gpu": "RTX 2060"
        },
        {
            "title": "Red Dead Redemption 2",
            "description": "Arthur Morgan and the Van der Linde gang are outlaws on the run.",
            "price": 59.99, "discount_price": 19.80, "genre": "action", "release_date": date(2018, 10, 26), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg",
            "min_os": "Windows 7", "min_cpu": "i5-2500K", "min_ram": "8 GB RAM", "min_gpu": "GTX 770",
            "rec_os": "Windows 10", "rec_cpu": "i7-4770K", "rec_ram": "12 GB RAM", "rec_gpu": "GTX 1060"
        },
        {
            "title": "Baldur's Gate 3",
            "description": "Gather your party and return to the Forgotten Realms.",
            "price": 59.99, "discount_price": None, "genre": "rpg", "release_date": date(2023, 8, 3), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/12/Baldur%27s_Gate_3_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "i5 4690", "min_ram": "8 GB RAM", "min_gpu": "GTX 970",
            "rec_os": "Windows 10", "rec_cpu": "i7 8700K", "rec_ram": "16 GB RAM", "rec_gpu": "RTX 2060 Super"
        },
        {
            "title": "Call of Duty: MW III",
            "description": "Captain Price and Task Force 141 face off against the ultimate threat.",
            "price": 69.99, "discount_price": 48.99, "genre": "action", "release_date": date(2023, 11, 10), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/1f/Call_of_Duty_Modern_Warfare_III_%282023%29_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "i5-6600", "min_ram": "8 GB RAM", "min_gpu": "GTX 960",
            "rec_os": "Windows 11", "rec_cpu": "i7-6700K", "rec_ram": "16 GB RAM", "rec_gpu": "GTX 1080Ti"
        },
        {
            "title": "Marvel's Spider-Man 2",
            "description": "Spider-Men, Peter Parker and Miles Morales, return for an exciting new adventure.",
            "price": 69.99, "discount_price": None, "genre": "action", "release_date": date(2023, 10, 20), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0f/Marvel%27s_Spider-Man_2_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "i3-8100", "min_ram": "8 GB RAM", "min_gpu": "GTX 1060",
            "rec_os": "Windows 10", "rec_cpu": "i5-10400", "rec_ram": "16 GB RAM", "rec_gpu": "RTX 3070"
        },
        {
            "title": "Starfield",
            "description": "In this next generation role-playing game set amongst the stars, create any character you want.",
            "price": 69.99, "discount_price": 55.99, "genre": "rpg", "release_date": date(2023, 9, 6), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/6/6d/Starfield_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "AMD Ryzen 5 2600X", "min_ram": "16 GB RAM", "min_gpu": "AMD Radeon RX 5700",
            "rec_os": "Windows 11", "rec_cpu": "AMD Ryzen 5 3600X", "rec_ram": "16 GB RAM", "rec_gpu": "AMD Radeon RX 6800 XT"
        },
        {
            "title": "Resident Evil 4",
            "description": "Survival is just the beginning. Six years have passed since the biological disaster.",
            "price": 59.99, "discount_price": 39.99, "genre": "action", "release_date": date(2023, 3, 24), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/d/df/Resident_Evil_4_remake_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "Ryzen 3 1200", "min_ram": "8 GB RAM", "min_gpu": "RX 560",
            "rec_os": "Windows 10", "rec_cpu": "Ryzen 5 3600", "rec_ram": "16 GB RAM", "rec_gpu": "RX 5700"
        },
        {
            "title": "Final Fantasy XVI",
            "description": "An epic dark fantasy where the fates of the land are decided by the mighty Eikons.",
            "price": 69.99, "discount_price": 49.99, "genre": "rpg", "release_date": date(2023, 6, 22), "is_featured": True,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/02/Final_Fantasy_XVI_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "i5-8400", "min_ram": "16 GB RAM", "min_gpu": "GTX 1070",
            "rec_os": "Windows 10", "rec_cpu": "i7-10700", "rec_ram": "16 GB RAM", "rec_gpu": "RTX 2080"
        },

        # --- CATALOG GAMES (Browse Page) ---
        {
            "title": "Grand Theft Auto V",
            "description": "Experience the interwoven stories of three criminals in Los Santos.",
            "price": 29.99, "discount_price": 14.99, "genre": "action", "release_date": date(2013, 9, 17), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png",
            "min_os": "Windows 8.1", "min_cpu": "Q6600", "min_ram": "4 GB RAM", "min_gpu": "9800 GT",
            "rec_os": "Windows 10", "rec_cpu": "i5 3470", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 660"
        },
        {
            "title": "The Witcher 3",
            "description": "You are Geralt of Rivia, mercenary monster slayer.",
            "price": 39.99, "discount_price": 9.99, "genre": "rpg", "release_date": date(2015, 5, 19), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg",
            "min_os": "Windows 7", "min_cpu": "i5-2500K", "min_ram": "6 GB RAM", "min_gpu": "GTX 660",
            "rec_os": "Windows 10", "rec_cpu": "i7 3770", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 770"
        },
        {
            "title": "Minecraft",
            "description": "Prepare for an adventure of limitless possibilities.",
            "price": 29.99, "discount_price": None, "genre": "strategy", "release_date": date(2011, 11, 18), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/5/51/Minecraft_cover.png",
            "min_os": "Windows 7", "min_cpu": "Core i3", "min_ram": "4 GB RAM", "min_gpu": "Intel HD",
            "rec_os": "Windows 10", "rec_cpu": "Core i5", "rec_ram": "8 GB RAM", "rec_gpu": "GeForce 700"
        },
        {
            "title": "Hades",
            "description": "Defy the god of the dead as you hack and slash out of the Underworld.",
            "price": 24.99, "discount_price": 12.49, "genre": "indie", "release_date": date(2020, 9, 17), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/c/cc/Hades_cover_art.jpg",
            "min_os": "Windows 7", "min_cpu": "Dual Core 2.4", "min_ram": "4 GB RAM", "min_gpu": "1GB VRAM",
            "rec_os": "Windows 10", "rec_cpu": "Dual Core 3.0", "rec_ram": "8 GB RAM", "rec_gpu": "2GB VRAM"
        },
        {
            "title": "Hollow Knight",
            "description": "Forge your own path in Hollow Knight! An epic action adventure.",
            "price": 14.99, "discount_price": 7.49, "genre": "indie", "release_date": date(2017, 2, 24), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/04/Hollow_Knight_first_cover_art.webp",
            "min_os": "Windows 7", "min_cpu": "Intel Core 2 Duo", "min_ram": "4 GB RAM", "min_gpu": "GeForce 9800GT",
            "rec_os": "Windows 10", "rec_cpu": "Intel Core i5", "rec_ram": "8 GB RAM", "rec_gpu": "GeForce GTX 560"
        },
        {
            "title": "Stardew Valley",
            "description": "You've inherited your grandfather's old farm plot in Stardew Valley.",
            "price": 14.99, "discount_price": None, "genre": "indie", "release_date": date(2016, 2, 26), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/f/fd/Stardew_Valley_Box_Art.jpg",
            "min_os": "Windows Vista", "min_cpu": "2 Ghz", "min_ram": "2 GB RAM", "min_gpu": "256 mb video memory",
            "rec_os": "Windows 10", "rec_cpu": "2 Ghz", "rec_ram": "4 GB RAM", "rec_gpu": "512 mb video memory"
        },
        {
            "title": "Overwatch 2",
            "description": "Overwatch 2 is a free-to-play, team-based action game.",
            "price": 0.00, "discount_price": None, "genre": "action", "release_date": date(2022, 10, 4), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/5/51/Overwatch_2_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "i3-6100", "min_ram": "6 GB RAM", "min_gpu": "GTX 600",
            "rec_os": "Windows 10", "rec_cpu": "i7-4790", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 1060"
        },
        {
            "title": "Valorant",
            "description": "A 5v5 character-based tactical shooter.",
            "price": 0.00, "discount_price": None, "genre": "action", "release_date": date(2020, 6, 2), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/f/fb/Valorant_cover_art.jpg",
            "min_os": "Windows 7", "min_cpu": "Core 2 Duo", "min_ram": "4 GB RAM", "min_gpu": "Intel HD 4000",
            "rec_os": "Windows 10", "rec_cpu": "i5-4460", "rec_ram": "4 GB RAM", "rec_gpu": "GTX 1050 Ti"
        },
        {
            "title": "Terraria",
            "description": "Dig, fight, explore, build! Nothing is impossible.",
            "price": 9.99, "discount_price": 4.99, "genre": "indie", "release_date": date(2011, 5, 16), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/3/30/Terraria_Box_Art.jpg",
            "min_os": "Windows XP", "min_cpu": "1.6 Ghz", "min_ram": "512 MB RAM", "min_gpu": "128mb Video Memory",
            "rec_os": "Windows 7", "rec_cpu": "Dual Core 3.0 Ghz", "rec_ram": "4 GB RAM", "rec_gpu": "256mb Video Memory"
        },
        {
            "title": "Apex Legends",
            "description": "Master an ever-growing roster of legendary characters with powerful abilities.",
            "price": 0.00, "discount_price": None, "genre": "action", "release_date": date(2019, 2, 4), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/d/db/Apex_legends_cover.jpg",
            "min_os": "Windows 7", "min_cpu": "i3-6300", "min_ram": "6 GB RAM", "min_gpu": "GT 640",
            "rec_os": "Windows 10", "rec_cpu": "i5-3570K", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 970"
        },
        {
            "title": "Among Us",
            "description": "An online and local party game of teamwork and betrayal in space!",
            "price": 4.99, "discount_price": 3.99, "genre": "indie", "release_date": date(2018, 6, 15), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9a/Among_Us_cover_art.jpg",
            "min_os": "Windows 7", "min_cpu": "SSE2 instruction set support", "min_ram": "1 GB RAM", "min_gpu": "Any",
            "rec_os": "Windows 10", "rec_cpu": "Intel i3", "rec_ram": "2 GB RAM", "rec_gpu": "Nvidia GT 610"
        },
        {
            "title": "Rocket League",
            "description": "Soccer meets driving once again in the long-awaited, physics-based sequel.",
            "price": 0.00, "discount_price": None, "genre": "sports", "release_date": date(2015, 7, 7), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/e/e8/Rocket_League_coverart.jpg",
            "min_os": "Windows 7", "min_cpu": "2.4 GHz Dual core", "min_ram": "2 GB RAM", "min_gpu": "GTX 260",
            "rec_os": "Windows 10", "rec_cpu": "Quad Core 3.0+ GHz", "rec_ram": "4 GB RAM", "rec_gpu": "GTX 660"
        },
        {
            "title": "Dota 2",
            "description": "Every day, millions of players worldwide enter battle as one of over a hundred Dota heroes.",
            "price": 0.00, "discount_price": None, "genre": "strategy", "release_date": date(2013, 7, 9), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/0/08/Dota_2_official_art.jpg",
            "min_os": "Windows 7", "min_cpu": "Dual core from Intel or AMD", "min_ram": "4 GB RAM", "min_gpu": "GeForce 8600/9600GT",
            "rec_os": "Windows 10", "rec_cpu": "Dual core from Intel or AMD", "rec_ram": "8 GB RAM", "rec_gpu": "Nvidia GeForce GTX 650"
        },
        {
            "title": "Civilization VI",
            "description": "Civilization VI offers new ways to interact with your world, expand your empire across the map.",
            "price": 59.99, "discount_price": 5.99, "genre": "strategy", "release_date": date(2016, 10, 21), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/3/3b/Civilization_VI_cover_art.jpg",
            "min_os": "Windows 7", "min_cpu": "i3 2.5 Ghz", "min_ram": "4 GB RAM", "min_gpu": "AMD 5570",
            "rec_os": "Windows 10", "rec_cpu": "i5 2.5 Ghz", "rec_ram": "8 GB RAM", "rec_gpu": "AMD 7970"
        },
        {
            "title": "Street Fighter 6",
            "description": "Here comes a new challenger! The latest evolution of the renowned fighting game franchise.",
            "price": 59.99, "discount_price": 39.59, "genre": "action", "release_date": date(2023, 6, 2), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/14/Street_Fighter_6_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "i5-7500", "min_ram": "8 GB RAM", "min_gpu": "GTX 1060",
            "rec_os": "Windows 10", "rec_cpu": "i7-8700", "rec_ram": "16 GB RAM", "rec_gpu": "RTX 2070"
        },
        {
            "title": "Mortal Kombat 11",
            "description": "Mortal Kombat is back and better than ever in the next evolution of the iconic franchise.",
            "price": 49.99, "discount_price": 9.99, "genre": "action", "release_date": date(2019, 4, 23), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/7/7e/Mortal_Kombat_11_cover_art.png",
            "min_os": "Windows 7", "min_cpu": "i5-750", "min_ram": "8 GB RAM", "min_gpu": "GTX 670",
            "rec_os": "Windows 10", "rec_cpu": "i3-2100", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 780"
        },
        {
            "title": "The Elder Scrolls V: Skyrim",
            "description": "The next chapter in the highly anticipated Elder Scrolls saga.",
            "price": 39.99, "discount_price": 9.99, "genre": "rpg", "release_date": date(2011, 11, 11), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/1/15/The_Elder_Scrolls_V_Skyrim_cover.png",
            "min_os": "Windows 7", "min_cpu": "i5-750", "min_ram": "8 GB RAM", "min_gpu": "GTX 470",
            "rec_os": "Windows 10", "rec_cpu": "i5-2400", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 780"
        },
        {
            "title": "Horizon Forbidden West",
            "description": "Join Aloy as she braves the Forbidden West – a majestic but dangerous frontier.",
            "price": 59.99, "discount_price": 39.99, "genre": "action", "release_date": date(2022, 2, 18), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/6/69/Horizon_Forbidden_West_cover_art.jpg",
            "min_os": "Windows 10", "min_cpu": "i3-8100", "min_ram": "16 GB RAM", "min_gpu": "GTX 1650",
            "rec_os": "Windows 10", "rec_cpu": "i5-8600", "rec_ram": "16 GB RAM", "rec_gpu": "RTX 3060"
        },
        {
            "title": "Ghost of Tsushima",
            "description": "Uncover the hidden wonders of Tsushima in this open-world action adventure.",
            "price": 59.99, "discount_price": 29.39, "genre": "action", "release_date": date(2020, 7, 17), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b6/Ghost_of_Tsushima.jpg",
            "min_os": "Windows 10", "min_cpu": "i3-7100", "min_ram": "8 GB RAM", "min_gpu": "GTX 960",
            "rec_os": "Windows 10", "rec_cpu": "i5-8600", "rec_ram": "16 GB RAM", "rec_gpu": "RTX 2060"
        },
        {
            "title": "Sekiro: Shadows Die Twice",
            "description": "Carve your own clever path to vengeance in this award-winning adventure.",
            "price": 59.99, "discount_price": 29.99, "genre": "action", "release_date": date(2019, 3, 22), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/6/6e/Sekiro_art.jpg",
            "min_os": "Windows 7", "min_cpu": "i3-2100", "min_ram": "4 GB RAM", "min_gpu": "GTX 760",
            "rec_os": "Windows 10", "rec_cpu": "i5-2500K", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 970"
        },
        {
            "title": "Control",
            "description": "After a secretive agency in New York is invaded by an otherworldly threat, you become the new Director.",
            "price": 29.99, "discount_price": 7.49, "genre": "action", "release_date": date(2019, 8, 27), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/5/5c/Control_game_cover_art.jpg",
            "min_os": "Windows 7", "min_cpu": "i5-4690", "min_ram": "8 GB RAM", "min_gpu": "GTX 780",
            "rec_os": "Windows 10", "rec_cpu": "i5-7600K", "rec_ram": "16 GB RAM", "rec_gpu": "GTX 1060"
        },
        {
            "title": "Doom Eternal",
            "description": "Hell’s armies have invaded Earth. Become the Slayer in an epic single-player campaign.",
            "price": 39.99, "discount_price": 9.99, "genre": "action", "release_date": date(2020, 3, 20), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9d/Cover_Art_of_Doom_Eternal.png",
            "min_os": "Windows 7", "min_cpu": "i5 @ 3.3 GHz", "min_ram": "8 GB RAM", "min_gpu": "GTX 1050Ti",
            "rec_os": "Windows 10", "rec_cpu": "i7-6700K", "rec_ram": "8 GB RAM", "rec_gpu": "GTX 1080"
        },
        {
            "title": "EA SPORTS FC 24",
            "description": "The World’s Game: the most true-to-football experience ever.",
            "price": 69.99, "discount_price": 20.99, "genre": "sports", "release_date": date(2023, 9, 29), "is_featured": False,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b7/EA_Sports_FC_24_cover.jpg",
            "min_os": "Windows 10", "min_cpu": "i5-6600K", "min_ram": "8 GB RAM", "min_gpu": "GTX 1050 Ti",
            "rec_os": "Windows 10", "rec_cpu": "i7-6700", "rec_ram": "12 GB RAM", "rec_gpu": "GTX 1660"
        }
    ]

    print("STEP 2: Downloading new images and creating games...")
    
    # User-Agent to avoid 403 Forbidden errors
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

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