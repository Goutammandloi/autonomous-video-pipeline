"""
Autonomous AI Video Pipeline: Stage 6 Test Suite
Tests multi-platform social distribution, viral metadata generation,
optimal release slot calculation, and scheduled campaign dispatch.
"""

import json
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.distribution import (
    PlatformType,
    PrivacyStatus,
    SocialMetadataGenerator,
    SocialDispatcher,
    SocialScheduler
)


def run_test():
    print("=== Testing Feature 6: Multi-Platform Dispatch & Social Media Scheduler ===")

    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    assert deck_path.exists(), f"Shot deck file not found: {deck_path}"

    with open(deck_path, "r", encoding="utf-8") as f:
        deck_data = json.load(f)
    shot_deck = ProductionShotDeck.model_validate(deck_data)

    master_video = root_dir / "data" / "final" / "project_origin_ep01_master_9x16.mp4"
    assert master_video.exists(), f"Master video not found: {master_video}"

    # 1. Test Social Metadata Generator
    generator = SocialMetadataGenerator()
    all_meta = generator.generate_all_platform_metadata(shot_deck)

    print("\n[Result] Synthesized Multi-Platform Viral Metadata:")
    for platform, meta in all_meta.items():
        print(f"\n  📱 Platform: {platform.value.upper()}")
        print(f"     Title: {meta.title}")
        print(f"     Hashtags ({len(meta.hashtags)}): {' '.join(meta.hashtags[:4])}...")
        print(f"     CTA Link: {meta.cta_link}")
        if meta.pinned_comment:
            print(f"     Pinned Comment: \"{meta.pinned_comment[:50]}...\"")

    # Assertions on metadata quality
    yt_meta = all_meta[PlatformType.YOUTUBE_SHORTS]
    assert len(yt_meta.title) <= 100, "YouTube title exceeds 100 character limit"
    assert len(yt_meta.hashtags) >= 3, "Missing YouTube hashtags"
    assert "https://" in yt_meta.cta_link, "Invalid CTA link"

    ig_meta = all_meta[PlatformType.INSTAGRAM_REELS]
    assert len(ig_meta.hashtags) >= 8, "Instagram should have robust hashtag clusters"
    assert "LINK IN BIO" in ig_meta.caption_or_description, "Instagram missing Link in Bio CTA"

    # 2. Test Social Scheduler & Multi-Platform Campaign Dispatch
    schedules_dir = root_dir / "data" / "schedules"
    dispatcher = SocialDispatcher(dry_run=True)
    scheduler = SocialScheduler(schedules_dir=str(schedules_dir), dispatcher=dispatcher)

    campaign_report = scheduler.schedule_campaign(
        video_path=str(master_video),
        shot_deck=shot_deck,
        target_platforms=[
            PlatformType.YOUTUBE_SHORTS,
            PlatformType.INSTAGRAM_REELS,
            PlatformType.LINKEDIN
        ]
    )

    print("\n[Result] Social Media Campaign Dispatch Report:")
    print(f"  Batch ID: {campaign_report.batch_id}")
    print(f"  Project Title: {campaign_report.project_title}")
    print(f"  Total Scheduled Jobs: {campaign_report.scheduled_jobs}/{campaign_report.total_jobs}")
    print(f"  Failed Jobs: {campaign_report.failed_jobs}")

    for job in campaign_report.jobs:
        print(f"\n  • [{job.platform.value.upper()}] Status: {job.status}")
        print(f"    Job ID: {job.job_id}")
        print(f"    Scheduled Release (UTC): {job.scheduled_time_iso}")
        print(f"    Remote URL: {job.remote_url}")
        print(f"    Trace Logs: {job.log_history}")

        assert job.status in ("SCHEDULED", "PUBLISHED"), f"Job failed: {job.error_message}"
        assert job.remote_url is not None, "Remote URL was not generated"

    # 3. Verify JSON Persistence
    schedule_json = schedules_dir / "scheduled_dispatches.json"
    assert schedule_json.exists(), f"Schedule file was not written: {schedule_json}"
    with open(schedule_json, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert len(saved_data) > 0, "Schedule json is empty"
    print(f"\n✅ Verified Persistent Storage: {schedule_json.name} ({schedule_json.stat().st_size} bytes)")

    print("\n🎯 STAGE 6 VERIFICATION COMPLETE: Multi-platform social dispatch & scheduler fully operational.")


if __name__ == "__main__":
    run_test()
