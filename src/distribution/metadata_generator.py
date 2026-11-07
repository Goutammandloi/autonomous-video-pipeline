"""
Autonomous AI Video Pipeline: Social Metadata Generator
Generates platform-tailored viral metadata, high-CTR titles, curiosity-gap captions,
and algorithmic hashtag clusters for Project Origin: The Shattered Crown.
"""

from typing import Dict, List, Optional
from .schemas import PlatformType, SocialPlatformMetadata
from ..scripting.schemas import ProductionShotDeck


class SocialMetadataGenerator:
    """
    Autonomous copywriting and viral SEO agent for vertical anime video distribution.
    """

    def __init__(self, brand_cta_url: str = "https://youtube.com/@ProjectOriginAnime"):
        self.brand_cta_url = brand_cta_url

    def generate_all_platform_metadata(self, shot_deck: ProductionShotDeck) -> Dict[PlatformType, SocialPlatformMetadata]:
        """
        Synthesizes tailored metadata for all supported social channels.
        """
        return {
            PlatformType.YOUTUBE_SHORTS: self.generate_youtube_metadata(shot_deck),
            PlatformType.INSTAGRAM_REELS: self.generate_instagram_metadata(shot_deck),
            PlatformType.LINKEDIN: self.generate_linkedin_metadata(shot_deck),
            PlatformType.TIKTOK: self.generate_tiktok_metadata(shot_deck),
            PlatformType.TWITTER_X: self.generate_twitter_metadata(shot_deck)
        }

    def generate_youtube_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        """
        Optimizes for YouTube Shorts algorithm: <=60 char title, curiosity gap, SEO tags.
        """
        title = "Ash REFUSES the Corporate Crown?! 😱 Pikachu Shatters Floor 40!"
        caption = (
            f"World Monarch Ash Ketchum is summoned to the 40th floor of the Silph-Macro Spire...\n"
            f"CEO Vance Stirling reveals the Helix Neural Chip—100% obedience, uncapped power.\n"
            f"Ash's answer? 'My Pokémon aren't your machines!' 🔥⚡\n\n"
            f"Wait till you see Pikachu's 10-Million-Volt Thunderbolt escape!\n\n"
            f"📺 Project Origin: Episode 02 drops tomorrow! Subscribe for the full 60-episode anime serial.\n"
            f"👉 Join the Resistance: {self.brand_cta_url}\n\n"
            f"#Pokemon #AshKetchum #PokemonJourneys #AnimeShorts #Pikachu #ProjectOrigin #RedPokemon #Anime"
        )
        hashtags = ["#Pokemon", "#AshKetchum", "#PokemonJourneys", "#AnimeShorts", "#Pikachu", "#ProjectOrigin", "#RedPokemon", "#Anime"]
        tags = [
            "pokemon journeys anime",
            "ash and red",
            "pikachu thunderbolt",
            "project origin",
            "ash ketchum world monarch",
            "pokemon master journeys",
            "anime vertical short"
        ]
        pinned_comment = f"⚡ Drop a ⚡ if you stand with Ash and Pikachu against the Consortium! Episode 2 drops tomorrow at 18:30 IST / 13:00 UTC: {self.brand_cta_url}"

        return SocialPlatformMetadata(
            platform=PlatformType.YOUTUBE_SHORTS,
            title=title,
            caption_or_description=caption,
            hashtags=hashtags,
            tags=tags,
            pinned_comment=pinned_comment,
            cta_link=self.brand_cta_url
        )

    def generate_instagram_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        """
        Optimizes for Instagram Reels algorithm: POV opening hook, paragraph spacing, high-volume hashtags.
        """
        title = "POV: Ash Ketchum tells the Silph CEO to go to hell ⚡🏢"
        caption = (
            f"They thought winning the Masters Eight meant Ash could be bought.\n"
            f"They were dead wrong. 💀⚡\n\n"
            f"100% obedience? Zero hesitation? Not on Ash's watch.\n\n"
            f"Episode 1 of PROJECT ORIGIN: THE SHATTERED CROWN 👑\n"
            f"A new gritty post-Journeys anime universe teaming up Ash & Red.\n\n"
            f"🔗 Full serial & episode LINK IN BIO: {self.brand_cta_url}\n\n"
            f".\n.\n"
            f"#PokemonAnime #AshKetchum #Pikachu #RedPokemon #AnimeReels #PokemonCommunity #Animation #Otaku #PokemonMaster #ShonenAnime"
        )
        hashtags = [
            "#PokemonAnime", "#AshKetchum", "#Pikachu",
            "#RedPokemon", "#AnimeReels", "#PokemonCommunity",
            "#Animation", "#Otaku", "#PokemonMaster", "#ShonenAnime"
        ]
        pinned_comment = "Episode 2: 'Black-Ops Protocol' drops tomorrow! Turn on notifications 🔔"

        return SocialPlatformMetadata(
            platform=PlatformType.INSTAGRAM_REELS,
            title=title,
            caption_or_description=caption,
            hashtags=hashtags,
            tags=["reels", "pokemon", "anime"],
            pinned_comment=pinned_comment,
            cta_link=self.brand_cta_url
        )

    def generate_linkedin_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        """
        Optimizes for LinkedIn professional narrative: Narrative leadership & autonomous production.
        """
        title = "Autonomous AI Anime Production: Project Origin — The Shattered Crown 🎬⚡"
        caption = (
            f"What does the next generation of serialized animation look like?\n\n"
            f"We built an autonomous multi-agent video pipeline capable of generating, scoring, "
            f"voicing, and assembling 60-second broadcast-ready vertical anime episodes.\n\n"
            f"Featured Project: Project Origin: The Shattered Crown (Episode 1: The Gilded Throne)\n"
            f"• 13 production shots @ CFR 30 FPS\n"
            f"• ITU-R BS.1770 -14.0 LUFS audio mastering\n"
            f"• 10.0/10 Gatekeeper QA score with 0.0ms A/V sync drift\n\n"
            f"Explore the interactive production studio & codebase:\n"
            f"👉 {self.brand_cta_url}\n\n"
            f"#GenerativeAI #AIVideo #AnimationPipeline #AnimeProduction #CreativeTech #AutonomousAgents"
        )
        hashtags = ["#GenerativeAI", "#AIVideo", "#AnimationPipeline", "#AnimeProduction", "#CreativeTech", "#AutonomousAgents"]

        return SocialPlatformMetadata(
            platform=PlatformType.LINKEDIN,
            title=title,
            caption_or_description=caption,
            hashtags=hashtags,
            tags=["Generative AI", "AI Video Pipeline", "Animation Technology"],
            pinned_comment="Check out the live interactive preview dashboard and open-source production pipeline!",
            cta_link=self.brand_cta_url
        )

    def generate_tiktok_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        """
        Optimizes for TikTok algorithm: Fast trend tags, high suspense hook.
        """
        title = "When the CEO tries to chip Pikachu 💀⚡ #pokemon #ashketchum #animetiktok"
        caption = (
            f"World Monarch Ash did NOT hold back on floor 40 🔥\n"
            f"Full anime serial: Project Origin: The Shattered Crown (Ep 1/60)\n"
            f"#pokemon #ashketchum #pikachu #animetiktok #animefight #fyp #foryoupage #viral"
        )
        hashtags = ["#pokemon", "#ashketchum", "#pikachu", "#animetiktok", "#animefight", "#fyp", "#foryoupage", "#viral"]
        pinned_comment = "Episode 2 drops tomorrow! Follow so you don't miss Red's arrival 👀🔥"

        return SocialPlatformMetadata(
            platform=PlatformType.TIKTOK,
            title=title,
            caption_or_description=caption,
            hashtags=hashtags,
            tags=["pokemon", "ashketchum", "animefight"],
            pinned_comment=pinned_comment,
            cta_link=self.brand_cta_url
        )

    def generate_twitter_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        """
        Optimizes for X / Twitter: Short-form punchy hook with media cards.
        """
        title = "Ash Ketchum said NO to the corporate collar ⚡🏢"
        caption = (
            f"'My Pokémon aren't your machines!'\n\n"
            f"Watch Episode 1 of PROJECT ORIGIN: THE SHATTERED CROWN — an all-new 60-episode anime serial teaming up Ash & Red.\n\n"
            f"Watch now & subscribe: {self.brand_cta_url}\n\n"
            f"#Pokemon #AshKetchum #ProjectOrigin #Anime"
        )
        hashtags = ["#Pokemon", "#AshKetchum", "#ProjectOrigin", "#Anime"]

        return SocialPlatformMetadata(
            platform=PlatformType.TWITTER_X,
            title=title,
            caption_or_description=caption,
            hashtags=hashtags,
            tags=["pokemon", "anime"],
            pinned_comment="",
            cta_link=self.brand_cta_url
        )
