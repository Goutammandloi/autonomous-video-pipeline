"""
Autonomous AI Video Pipeline: Social Scheduler & Queue Engine
Computes peak audience engagement release windows, generates dispatch jobs,
executes scheduling across platforms, and maintains persistent state logs.
"""

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict
from pathlib import Path

from .schemas import (
    PlatformType,
    PrivacyStatus,
    SchedulingSlot,
    DispatchJob,
    DispatchBatchReport
)
from .metadata_generator import SocialMetadataGenerator
from .social_dispatcher import SocialDispatcher
from ..scripting.schemas import ProductionShotDeck


class SocialScheduler:
    """
    Automated queue scheduler and multi-platform distribution coordinator.
    """

    def __init__(
        self,
        schedules_dir: Optional[str] = None,
        dispatcher: Optional[SocialDispatcher] = None
    ):
        self.schedules_dir = Path(schedules_dir or "data/schedules")
        self.schedules_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_generator = SocialMetadataGenerator()
        self.dispatcher = dispatcher or SocialDispatcher(dry_run=True)

    def calculate_optimal_slot(self, platform: PlatformType, target_days_ahead: int = 1) -> SchedulingSlot:
        """
        Calculates optimal audience posting window for Indian engineering / B.Tech demographic.
        Evening prime window: 18:30 IST (13:00 UTC).
        """
        # UTC baseline
        now_utc = datetime.now(timezone.utc)
        target_date = now_utc + timedelta(days=target_days_ahead)

        # Set to 13:00 UTC (which is exactly 18:30 IST)
        scheduled_dt = target_date.replace(hour=13, minute=0, second=0, microsecond=0)
        iso_str = scheduled_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        reasoning = (
            "Peak engagement slot for college & engineering students in India "
            "(18:30 IST / 13:00 UTC): post-college commute and evening social media browsing window."
        )

        return SchedulingSlot(
            platform=platform,
            target_publish_time_iso=iso_str,
            timezone="Asia/Kolkata",
            optimal_reasoning=reasoning
        )

    def schedule_campaign(
        self,
        video_path: str,
        shot_deck: ProductionShotDeck,
        target_platforms: Optional[List[PlatformType]] = None
    ) -> DispatchBatchReport:
        """
        Packages and schedules the master video across all specified platforms.
        """
        platforms = target_platforms or [
            PlatformType.YOUTUBE_SHORTS,
            PlatformType.INSTAGRAM_REELS,
            PlatformType.LINKEDIN
        ]

        batch_id = f"batch_{uuid.uuid4().hex[:8]}"
        created_at_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        all_metadata = self.metadata_generator.generate_all_platform_metadata(shot_deck)

        jobs: List[DispatchJob] = []

        print(f"\n🚀 Launching Multi-Platform Social Scheduling Campaign [Batch: {batch_id}]")
        print(f"  Target Platforms: {[p.value for p in platforms]}")
        print(f"  Master Video Source: {Path(video_path).name}")

        for platform in platforms:
            slot = self.calculate_optimal_slot(platform)
            meta = all_metadata.get(platform)
            if not meta:
                continue

            job = DispatchJob(
                job_id=f"job_{platform.value}_{uuid.uuid4().hex[:6]}",
                platform=platform,
                video_path=video_path,
                metadata=meta,
                scheduled_time_iso=slot.target_publish_time_iso,
                privacy_status=PrivacyStatus.SCHEDULED
            )

            # Dispatch job via dispatcher
            dispatched_job = self.dispatcher.dispatch_job(job)
            jobs.append(dispatched_job)

        scheduled_cnt = sum(1 for j in jobs if j.status in ("SCHEDULED", "PUBLISHED"))
        failed_cnt = sum(1 for j in jobs if j.status == "FAILED")

        batch_report = DispatchBatchReport(
            batch_id=batch_id,
            created_at_iso=created_at_iso,
            project_title=shot_deck.title,
            total_jobs=len(jobs),
            scheduled_jobs=scheduled_cnt,
            published_jobs=sum(1 for j in jobs if j.status == "PUBLISHED"),
            failed_jobs=failed_cnt,
            jobs=jobs
        )

        # Persist schedule to JSON
        save_file = self.schedules_dir / "scheduled_dispatches.json"
        self._persist_schedules(batch_report, save_file)
        print(f"💾 Persistent Schedule Log Saved to: {save_file}")

        return batch_report

    def _persist_schedules(self, batch_report: DispatchBatchReport, output_file: Path):
        """Appends or creates persistent campaign dispatch registry."""
        history = []
        if output_file.exists():
            try:
                history = json.loads(output_file.read_text(encoding="utf-8"))
                if not isinstance(history, list):
                    history = [history]
            except Exception:
                history = []

        history.append(batch_report.model_dump())
        output_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
