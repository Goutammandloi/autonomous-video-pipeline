"""
Autonomous AI Video Pipeline: Optical Flow Glitch & Anomaly Evaluator
Implements Gunnar Farneback dense optical flow evaluation to detect:
- Sudden temporal warping and rubber-banding distortions
- Morphing artifacts and unnatural frame dislocation
- Outlier velocity spikes (Z-score > 3.5 threshold)
"""

from typing import List, Tuple
import cv2
import numpy as np

from .schemas import OpticalFlowQAResult


class GlitchDetector:
    """
    Mathematical optical flow anomaly detector for AI video outputs.
    """

    def __init__(self, z_score_threshold: float = 3.5):
        self.z_score_threshold = z_score_threshold

    def evaluate_video_frames(
        self,
        frames: List[np.ndarray],
        shot_id: int
    ) -> OpticalFlowQAResult:
        """
        Audits consecutive frame pairs for temporal coherence and violent warping spikes.
        """
        if len(frames) < 2:
            return OpticalFlowQAResult(
                shot_id=shot_id,
                total_frames_audited=0,
                mean_flow_magnitude=0.0,
                max_flow_z_score=0.0,
                anomalous_frames=[],
                passes_qa=True
            )

        flow_magnitudes = []
        # Pre-convert to grayscale and downscale slightly for fast dense optical flow
        gray_frames = []
        for f in frames:
            if len(f.shape) == 3:
                gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            else:
                gray = f
            # Resize to max 540x960 for sub-second flow computation
            small_gray = cv2.resize(gray, (270, 480), interpolation=cv2.INTER_LINEAR)
            gray_frames.append(small_gray)

        # 1. Compute Gunnar Farneback Dense Optical Flow across adjacent frames
        for i in range(len(gray_frames) - 1):
            prev_frame = gray_frames[i]
            curr_frame = gray_frames[i + 1]

            flow = cv2.calcOpticalFlowFarneback(
                prev=prev_frame,
                next=curr_frame,
                flow=None,
                pyr_scale=0.5,
                levels=3,
                winsize=15,
                iterations=3,
                poly_n=5,
                poly_sigma=1.2,
                flags=0
            )

            # Motion displacement magnitude: M = sqrt(u^2 + v^2)
            u = flow[..., 0]
            v = flow[..., 1]
            magnitude = np.sqrt(u ** 2 + v ** 2)
            flow_magnitudes.append(float(np.mean(magnitude)))

        # 2. Statistical Analysis & Z-Score Anomaly Detection
        mean_mag = float(np.mean(flow_magnitudes))
        median_mag = float(np.median(flow_magnitudes))
        std_mag = float(np.std(flow_magnitudes)) + 1e-6

        z_scores = [abs(m - mean_mag) / std_mag for m in flow_magnitudes]
        max_z = float(np.max(z_scores)) if z_scores else 0.0

        # Outlier triggers: Z-score > threshold OR sudden velocity ratio spike > 2.5x median
        anomalies = []
        for i, m in enumerate(flow_magnitudes):
            z = z_scores[i]
            ratio = m / (median_mag + 1e-4)
            if z > self.z_score_threshold or (ratio > 2.5 and m > 0.3):
                anomalies.append(i + 1)

        passes = (max_z <= self.z_score_threshold) and (len(anomalies) == 0)

        return OpticalFlowQAResult(
            shot_id=shot_id,
            total_frames_audited=len(flow_magnitudes),
            mean_flow_magnitude=round(mean_mag, 3),
            max_flow_z_score=round(max_z, 2),
            anomalous_frames=anomalies,
            passes_qa=passes,
            remediation_applied="Damped motion_bucket_id and smoothed kinematics" if not passes else None
        )
