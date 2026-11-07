"""
Autonomous AI Video Pipeline: OpenCV 4-Point Perspective Screen Warper
Enables programmatic screen replacements inside keyframes and video sequences:
- 4-point homography transform (cv2.getPerspectiveTransform + cv2.warpPerspective)
- Subpixel boundary antialiasing and seamless alpha blending
- Automated corner calibration for laptop / mobile device screens
"""

from pathlib import Path
from typing import Tuple, List, Union
import cv2
import numpy as np
from pydantic import BaseModel, Field


class CornerPoints(BaseModel):
    top_left: Tuple[float, float] = Field(..., description="[x, y] coordinates of top-left corner")
    top_right: Tuple[float, float] = Field(..., description="[x, y] coordinates of top-right corner")
    bottom_right: Tuple[float, float] = Field(..., description="[x, y] coordinates of bottom-right corner")
    bottom_left: Tuple[float, float] = Field(..., description="[x, y] coordinates of bottom-left corner")


class ScreenWarper:
    """
    Precision OpenCV homography perspective transformation engine.
    """

    @staticmethod
    def warp_screen_onto_image(
        base_image: Union[np.ndarray, str],
        screen_content: Union[np.ndarray, str],
        corners: CornerPoints,
        feather_border_px: int = 2
    ) -> np.ndarray:
        """
        Warps screen_content onto base_image inside the quadrilateral defined by corners.
        """
        # Load images if filepaths provided
        if isinstance(base_image, (str, Path)):
            base = cv2.imread(str(base_image))
        else:
            base = base_image.copy()

        if isinstance(screen_content, (str, Path)):
            screen = cv2.imread(str(screen_content))
        else:
            screen = screen_content.copy()

        h_base, w_base = base.shape[:2]
        h_screen, w_screen = screen.shape[:2]

        # 1. Source coordinates (entire screen_content rectangle)
        src_pts = np.float32([
            [0, 0],
            [w_screen - 1, 0],
            [w_screen - 1, h_screen - 1],
            [0, h_screen - 1]
        ])

        # 2. Destination coordinates (target quadrilateral in base image)
        dst_pts = np.float32([
            [corners.top_left[0], corners.top_left[1]],
            [corners.top_right[0], corners.top_right[1]],
            [corners.bottom_right[0], corners.bottom_right[1]],
            [corners.bottom_left[0], corners.bottom_left[1]]
        ])

        # 3. Compute 3x3 Homography Matrix
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # 4. Warp Screen Content into Base Dimension
        warped_screen = cv2.warpPerspective(
            screen,
            matrix,
            (w_base, h_base),
            flags=cv2.INTER_LANCZOS4,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0)
        )

        # 5. Create Antialiased Alpha Polygon Mask
        mask = np.zeros((h_base, w_base), dtype=np.uint8)
        pts_poly = np.int32([dst_pts])
        cv2.fillPoly(mask, pts_poly, 255)

        # Soft edge antialiasing
        if feather_border_px > 0:
            ksize = feather_border_px * 2 + 1
            mask = cv2.GaussianBlur(mask, (ksize, ksize), 0)

        alpha = (mask.astype(np.float32) / 255.0)[:, :, np.newaxis]

        # 6. Alpha Blend
        blended = (warped_screen.astype(np.float32) * alpha +
                   base.astype(np.float32) * (1.0 - alpha))

        return np.clip(blended, 0, 255).astype(np.uint8)

    @classmethod
    def create_mock_terminal_screen(
        cls,
        width: int = 1280,
        height: int = 800,
        title: str = "APPIN CYBER SECURITY LAB - LIVE SCANNER",
        theme: str = "matrix_dark"
    ) -> np.ndarray:
        """
        Synthesizes a high-contrast terminal / dashboard screen for screen insets.
        """
        img = np.zeros((height, width, 3), dtype=np.uint8)
        # Dark navy background
        img[:] = (18, 12, 8)  # BGR

        # Window titlebar
        cv2.rectangle(img, (0, 0), (width, 50), (35, 25, 20), -1)
        # Window buttons (red, yellow, green)
        cv2.circle(img, (25, 25), 8, (70, 70, 240), -1)
        cv2.circle(img, (50, 25), 8, (60, 215, 250), -1)
        cv2.circle(img, (75, 25), 8, (80, 200, 50), -1)

        # Title
        cv2.putText(img, title, (110, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (230, 230, 230), 2, cv2.LINE_AA)

        # Terminal lines
        lines = [
            ("[root@appin-cyber-node-01 ~]# nmap -sV -T4 -p- 192.168.1.105", (100, 230, 100)),
            ("Starting Nmap 7.94 ( https://nmap.org ) at 2026-11-07 16:30 IST", (180, 180, 180)),
            ("Nmap scan report for target-internal.appin.local (192.168.1.105)", (180, 180, 180)),
            ("Host is up (0.00042s latency).", (180, 180, 180)),
            ("PORT     STATE SERVICE       VERSION", (255, 200, 80)),
            ("22/tcp   open  ssh           OpenSSH 9.2p1 (Protocol 2.0)", (120, 255, 120)),
            ("80/tcp   open  http          nginx/1.24.0 (Live Demo Lab)", (120, 255, 120)),
            ("443/tcp  open  ssl/http      nginx/1.24.0 (Enterprise Gateway)", (120, 255, 120)),
            ("8080/tcp open  http-proxy    Appin Practical Sandbox Daemon v2.4", (255, 120, 200)),
            ("[+] VULNERABILITY AUDIT: 0 Critical / 3 Patched / Production Ready", (50, 230, 255)),
            ("[+] CAREER STATUS: 100% Practical Industry Placement Track Active", (80, 255, 80)),
        ]

        y_offset = 110
        for text, color in lines:
            cv2.putText(img, text, (40, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 1, cv2.LINE_AA)
            y_offset += 45

        # Progress bar
        cv2.rectangle(img, (40, height - 70), (width - 40, height - 40), (45, 35, 30), 2)
        cv2.rectangle(img, (42, height - 68), (int(width * 0.88), height - 42), (50, 200, 80), -1)
        cv2.putText(img, "TRAINING MODULE PROGRESS: 88% COMPLETED", (50, height - 48), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        return img
