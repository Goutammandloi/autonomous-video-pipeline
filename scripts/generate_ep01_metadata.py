"""
Project Origin: The Shattered Crown
Episode 01: "The Gilded Throne" - Viral Social Metadata & Distribution Generator
Generates high-CTR titles, curiosity hooks, algorithmic hashtags, and pinned comments.
"""

import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

def generate_social_metadata():
    metadata = {
        "episode_id": "EP01",
        "title": "Project Origin: The Shattered Crown — Episode 01: The Gilded Throne",
        "aspect_ratio": "9:16 Vertical (1080x1920)",
        "duration_sec": 60.0,
        "platforms": {
            "youtube_shorts": {
                "title": "Ash REFUSES the Corporate Crown?! 😱 Pikachu Shatters Floor 40!",
                "caption": (
                    "World Monarch Ash Ketchum is summoned to the 40th floor of the Silph-Macro Spire...\n"
                    "CEO Vance Stirling reveals the Helix Neural Chip—100% obedience, uncapped power.\n"
                    "Ash's answer? 'My Pokémon aren't your machines!' 🔥⚡\n\n"
                    "Wait till you see Pikachu's 10-Million-Volt Thunderbolt escape!\n\n"
                    "📺 Project Origin: Episode 02 drops tomorrow! Subscribe for the full 60-episode anime serial.\n\n"
                    "#Pokemon #AshKetchum #PokemonJourneys #AnimeShorts #Pikachu #ProjectOrigin #RedPokemon #Anime"
                ),
                "hashtags": ["#Pokemon", "#AshKetchum", "#PokemonJourneys", "#AnimeShorts", "#Pikachu", "#ProjectOrigin", "#RedPokemon", "#Anime"],
                "pinned_comment": "⚡ What would YOU do if they tried to chip your partner Pokémon? Drop your starter below! Episode 2 drops tomorrow at 18:30 IST / 13:00 UTC."
            },
            "instagram_reels": {
                "title": "POV: Ash Ketchum tells the Silph CEO to go to hell ⚡🏢",
                "caption": (
                    "They thought winning the Masters Eight meant Ash could be bought.\n"
                    "They were dead wrong. 💀⚡\n\n"
                    "100% obedience? Zero hesitation? Not on Ash's watch.\n\n"
                    "Episode 1 of PROJECT ORIGIN: THE SHATTERED CROWN 👑\n"
                    "A new gritty post-Journeys anime universe teaming up Ash & Red.\n\n"
                    "#PokemonAnime #AshKetchum #Pikachu #RedPokemon #AnimeReels #PokemonCommunity #Animation #Otaku #PokemonMaster"
                ),
                "hashtags": ["#PokemonAnime", "#AshKetchum", "#Pikachu", "#RedPokemon", "#AnimeReels", "#PokemonCommunity", "#Animation", "#Otaku"],
                "pinned_comment": "Episode 2: 'Black-Ops Protocol' drops tomorrow! Turn on notifications 🔔"
            },
            "tiktok": {
                "title": "When the CEO tries to chip Pikachu 💀⚡ #pokemon #ashketchum #animetiktok",
                "caption": (
                    "World Monarch Ash did NOT hold back on floor 40 🔥\n"
                    "Full anime serial: Project Origin: The Shattered Crown (Ep 1/60)\n"
                    "#pokemon #ashketchum #pikachu #animetiktok #animefight #fyp #foryoupage #viral"
                ),
                "hashtags": ["#pokemon", "#ashketchum", "#pikachu", "#animetiktok", "#animefight", "#fyp", "#foryoupage", "#viral"],
                "pinned_comment": "Episode 2 drops tomorrow! Follow so you don't miss Red's arrival 👀🔥"
            }
        }
    }

    output_path = root_dir / "data" / "schedules" / "ep01_social_metadata.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Generated and saved Episode 01 social metadata to:\n   {output_path}")

if __name__ == "__main__":
    generate_social_metadata()
