"""
Autonomous AI Video Pipeline: Social Metadata Generator
Generates platform-tailored viral metadata, high-CTR titles, curiosity-gap captions,
and algorithmic hashtag clusters from the production screenplay and master video specs.
"""

from typing import Dict, List, Optional
from .schemas import PlatformType, SocialPlatformMetadata
from ..scripting.schemas import ProductionShotDeck


class SocialMetadataGenerator:
    """
    Autonomous copywriting and viral SEO agent for vertical video distribution.
    """

    def __init__(self, brand_cta_url: str = "https://appintechnology.com/cybersecurity-demo"):
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
        title = "Rajat Caught Hacking Live?! 😱 Placement Secret Revealed"
        caption = (
            f"Didi caught Rajat 'watching Netflix' during placement season... but wait till you see his screen! 💻🔥\n\n"
            f"Instead of boring theory, he's hacking live in Appin Technology's real-world cybersecurity lab!\n\n"
            f"⚡ Want 100% placement support and hands-on ethical hacking training?\n"
            f"👉 Book your FREE Demo Session now: {self.brand_cta_url}\n\n"
            f"#Shorts #CyberSecurity #EthicalHacking #PlacementSeason #AppinTechnology #TechCareer #BTech"
        )
        hashtags = ["#Shorts", "#CyberSecurity", "#EthicalHacking", "#PlacementSeason", "#AppinTechnology", "#TechCareer"]
        tags = [
            "cyber security course",
            "ethical hacking tutorial",
            "placement preparation btech",
            "appin technology",
            "cyber lab training",
            "college placement hacks",
            "hindi tech shorts"
        ]
        pinned_comment = f"Drop a 🔥 if your college lab looks nothing like this! Book your Free Demo via the link in description/bio: {self.brand_cta_url}"

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
        title = "POV: Didi catches you 'chilling' during placement season 👀💻"
        caption = (
            f"Didi thought Rajat was wasting his future on Netflix 🍿👀\n\n"
            f"Plot twist: He was executing real-time penetration testing in Appin's cyber lab! 🛡️⚡\n\n"
            f"Why mug up outdated textbooks when you can get:\n"
            f"✅ Real-world cyber lab simulations\n"
            f"✅ Industry recognized certification\n"
            f"✅ 100% placement assistance for top tech roles\n\n"
            f"🚀 Upgrade your career today!\n"
            f"🔗 Tap the LINK IN BIO to reserve your 1-on-1 Free Demo Session.\n\n"
            f".\n.\n"
            f"#BTechLife #PlacementSeason #CyberSecurityIndia #EthicalHacking #EngineeringMemes #AppinTechnology #CollegePlacements #StudentHacks #TechCareers #LearnHacking #CyberSecurityTraining #CodingMemes"
        )
        hashtags = [
            "#BTechLife", "#PlacementSeason", "#CyberSecurityIndia",
            "#EthicalHacking", "#EngineeringMemes", "#AppinTechnology",
            "#CollegePlacements", "#StudentHacks", "#TechCareers",
            "#LearnHacking", "#CyberSecurityTraining"
        ]
        pinned_comment = "Link in bio to book your free cyber lab demo session! 🎯 Don't miss out."

        return SocialPlatformMetadata(
            platform=PlatformType.INSTAGRAM_REELS,
            title=title,
            caption_or_description=caption,
            hashtags=hashtags,
            tags=["reels", "instagram video", "cybersecurity"],
            pinned_comment=pinned_comment,
            cta_link=self.brand_cta_url
        )

    def generate_linkedin_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        """
        Optimizes for LinkedIn professional narrative: Skill gap transformation & career readiness.
        """
        title = "Why Hands-On Cyber Labs Beat Theoretical Degrees for Campus Placements 🛡️"
        caption = (
            f"During placement season, engineering students often face a harsh reality:\n"
            f"Textbook knowledge alone rarely clears technical security interviews.\n\n"
            f"In this scenario, Rajat demonstrates the difference between passive studying and active hands-on defense in Appin Technology's live cyber labs.\n\n"
            f"Key takeaways for aspiring engineers:\n"
            f"1. Real vulnerability environments teach what slides cannot.\n"
            f"2. Practical lab portfolios stand out directly to hiring recruiters.\n"
            f"3. 100% placement mentorship bridges the gap between campus and corporate.\n\n"
            f"Learn more and explore practical cybersecurity training:\n"
            f"👉 {self.brand_cta_url}\n\n"
            f"#CyberSecurity #EngineeringEducation #CampusPlacements #AppinTechnology #CareerReadiness #TechTalent"
        )
        hashtags = ["#CyberSecurity", "#CampusPlacements", "#AppinTechnology", "#CareerReadiness", "#TechTalent"]

        return SocialPlatformMetadata(
            platform=PlatformType.LINKEDIN,
            title=title,
            caption_or_description=caption,
            hashtags=hashtags,
            tags=["cybersecurity", "placements", "education"],
            pinned_comment=None,
            cta_link=self.brand_cta_url
        )

    def generate_tiktok_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        title = "When your sister catches you 'watching Netflix' 😂 #cybersecurity #hacktok"
        caption = (
            f"She thought it was Netflix... it was live ethical hacking! 💻🔥 "
            f"Free demo link in bio! #CyberSecurity #EthicalHacking #TechHacks #Student #Placement #Hacking"
        )
        return SocialPlatformMetadata(
            platform=PlatformType.TIKTOK,
            title=title,
            caption_or_description=caption,
            hashtags=["#CyberSecurity", "#EthicalHacking", "#TechHacks", "#Hacking"],
            tags=["tech", "hacking", "shorts"],
            pinned_comment=None,
            cta_link=self.brand_cta_url
        )

    def generate_twitter_metadata(self, shot_deck: ProductionShotDeck) -> SocialPlatformMetadata:
        title = "Rajat got caught... but not doing what Didi thought! 🍿💻"
        caption = (
            f"Didi thought Rajat was bingeing Netflix during placements.\n"
            f"Plot twist: He's mastering penetration testing in live labs @AppinTech! 🛡️⚡\n\n"
            f"Book your free cyber demo: {self.brand_cta_url}\n\n"
            f"#CyberSecurity #EthicalHacking #BTech"
        )
        return SocialPlatformMetadata(
            platform=PlatformType.TWITTER_X,
            title=title,
            caption_or_description=caption,
            hashtags=["#CyberSecurity", "#EthicalHacking", "#BTech"],
            tags=["infosec", "tech"],
            pinned_comment=None,
            cta_link=self.brand_cta_url
        )
