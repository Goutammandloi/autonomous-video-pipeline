"""
Project Origin: The Shattered Crown
Episode 01: "The Gilded Throne" - Master Production Shot Deck Generator
Strict 60.0s CFR 30 FPS vertical 9:16 specification with adversarial QA evaluation.
"""

import json
import sys
from pathlib import Path

# Set up project path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import (
    ProductionShotDeck,
    ProductionShot,
    VisualCue,
    DialogueCue,
    AudioCue,
    AspectRatio,
    CameraAngle,
    CameraMovement,
)
from src.scripting.generator import ScriptingEngine

def create_ep01_shot_deck() -> ProductionShotDeck:
    character_bible = {
        "Ash Ketchum": "16-year-old anime hero Ash Ketchum, athletic teenager, messy jet-black spiky hair, red-and-white trainer cap, royal-blue vest with white collar and gold trim, dark charcoal compression undershirt, Alolan Z-Ring on right wrist, Mega Keystone on left wrist, double zig-zag cheek marks, resolute brown eyes.",
        "Pikachu": "Yellow electric mouse Pokémon Pikachu, black-tipped ears, red circular electric cheek sacs sparking with golden electricity, lightning-bolt shaped tail, intense loyal battle expression.",
        "Vance Stirling": "48-year-old corporate oligarch CEO Vance Stirling, slicked-back silver-gray hair, sharp aristocratic cheekbones, cold ice-blue eyes behind titanium spectacles, tailored three-piece charcoal pinstripe suit, burgundy silk tie, gold DNA double-helix lapel pin, holding encrypted violet holographic datapad.",
        "Consortium Enforcers": "Cybernetic security enforcers in matte-black hydraulic exoskeleton combat armor, non-reflective tactical Kevlar mesh, amber-glowing tactical visors, carrying electromagnetic stun rifles.",
        "Cyber Houndoom": "Quadrupedal dark-type canine Pokémon Houndoom with mechanized skull plates, pulsing violet Helix Neural Chip embedded between curved ram horns, hydraulic leg braces, fangs dripping with violet electrical sparks."
    }

    shots = [
        # Shot 1: 0.0 - 3.0s (3.0s) [Hook]
        ProductionShot(
            shot_id=1,
            start_time_sec=0.0,
            end_time_sec=3.0,
            duration_sec=3.0,
            narrative_beat="Hook / Conflict",
            visual=VisualCue(
                camera_angle=CameraAngle.EXTREME_CLOSE_UP,
                camera_movement=CameraMovement.SLOW_PUSH_IN,
                characters_present=["Vance Stirling"],
                scene_environment="Silph-Macro Executive Spire Floor 40, polished obsidian boardroom table, rainy night city lights outside",
                foreground_action="A gold-embossed black contract dossier labeled 'LEAGUE OVERSIGHT COVENANT' slides across the glossy obsidian surface directly toward camera",
                background_details="Rain cascades down panoramic glass window, reflecting neon cyan and crimson lights of Saffron City skyline",
                image_prompt="cinematic anime 9:16 vertical extreme close-up. Polished reflective black obsidian conference table. A luxurious gold-embossed leather covenant contract labeled 'LEAGUE OVERSIGHT COVENANT' slides toward the viewer. In the dark background, towering rain-streaked glass window overlooking Saffron City cyberpunk skyline at night. Dramatic high-contrast corporate lighting.",
                negative_prompt="blurry, low resolution, warped text, bad lighting, cheerful, cartoonish, 3d render",
                motion_prompt="Camera slowly pushes in as the gold-embossed folder glides across the dark polished table surface, leaving a subtle reflection."
            ),
            dialogue=DialogueCue(
                speaker="Vance Stirling",
                line="Sign the covenant, World Monarch. Or your reign ends tonight.",
                emotion="chillingly polite, authoritative, cold",
                audio_ducking=True,
                estimated_duration_sec=2.6
            ),
            audio=AudioCue(
                bgm_mood="tense minimalist corporate drone with ominous bass pulse",
                bgm_intensity=0.4,
                sfx=["contract_slide_smooth", "distant_thunder_rumble", "rain_on_glass"]
            ),
            character_anchor_tokens=[character_bible["Vance Stirling"]]
        ),

        # Shot 2: 3.0 - 7.5s (4.5s) [The Threat / Helix Reveal]
        ProductionShot(
            shot_id=2,
            start_time_sec=3.0,
            end_time_sec=7.5,
            duration_sec=4.5,
            narrative_beat="Stakes / Threat Exposition",
            visual=VisualCue(
                camera_angle=CameraAngle.MEDIUM_SHOT,
                camera_movement=CameraMovement.SLOW_PUSH_IN,
                characters_present=["Vance Stirling"],
                scene_environment="Silph-Macro Executive Spire penthouse, floor-to-ceiling panoramic glass, stormy night",
                foreground_action="CEO Vance Stirling holds up a pulsing violet micro-device: the Helix Neural Chip, between gloved fingers",
                background_details="Thunder flash outside casts jagged shadows across the lavish chrome and glass boardroom",
                image_prompt="cinematic anime 9:16 vertical medium shot. 48-year-old CEO Vance Stirling, slicked-back silver-gray hair, sharp aristocratic face, cold blue eyes behind titanium glasses. Tailored charcoal three-piece suit with burgundy tie and gold helix pin. Standing before panoramic rain-streaked window at night. In his right hand, he holds a miniature pulsing violet cybernetic Helix Chip emitting faint purple circuitry light. High-end anime cell shading, ominous lighting.",
                negative_prompt="chibi, childish, deformed hands, extra fingers, cartoonish, low resolution",
                motion_prompt="Camera pushes in smoothly. Stirling slightly rotates the glowing violet chip between his thumb and forefinger, violet light casting highlights on his glasses."
            ),
            dialogue=DialogueCue(
                speaker="Vance Stirling",
                line="One hundred percent obedience. Zero hesitation.",
                emotion="calculated, sociopathic certainty",
                audio_ducking=True,
                estimated_duration_sec=2.8
            ),
            audio=AudioCue(
                bgm_mood="cold cybernetic pulsating synth riser",
                bgm_intensity=0.5,
                sfx=["helix_chip_hum", "rain_patter"]
            ),
            character_anchor_tokens=[character_bible["Vance Stirling"]]
        ),

        # Shot 3: 7.5 - 12.0s (4.5s) [Consortium Monopolization]
        ProductionShot(
            shot_id=3,
            start_time_sec=7.5,
            end_time_sec=12.0,
            duration_sec=4.5,
            narrative_beat="Stakes / Monopolization",
            visual=VisualCue(
                camera_angle=CameraAngle.CLOSE_UP,
                camera_movement=CameraMovement.STATIC,
                characters_present=["Vance Stirling"],
                scene_environment="Silph-Macro Penthouse boardroom, dark ambient lighting",
                foreground_action="Close-up of Vance Stirling smiling with cold contempt, violet data streams scrolling across his glasses",
                background_details="Blurred rain streaks and thunder silhouettes through the panoramic window",
                image_prompt="cinematic anime 9:16 vertical close-up. Vance Stirling's sharp face, cold smirk, titanium spectacles reflecting scrolling violet digital telemetry code. Silver hair neatly combed. Dramatic underlighting with purple and charcoal shadows, high-contrast shonen anime aesthetic.",
                negative_prompt="blurry, distorted face, asymmetrical eyes, low resolution",
                motion_prompt="Subtle camera stability. Stirling's cold smirk widens slightly as purple digital code scrolls across his glasses lenses."
            ),
            dialogue=DialogueCue(
                speaker="Vance Stirling",
                line="The League belongs to the Consortium now.",
                emotion="arrogant, calm, menacing",
                audio_ducking=True,
                estimated_duration_sec=2.7
            ),
            audio=AudioCue(
                bgm_mood="tense low-frequency drone with dark orchestral swell",
                bgm_intensity=0.55,
                sfx=["digital_telemetry_chirp", "soft_thunder"]
            ),
            character_anchor_tokens=[character_bible["Vance Stirling"]]
        ),

        # Shot 4: 12.0 - 16.5s (4.5s) [Ash's Defiance]
        ProductionShot(
            shot_id=4,
            start_time_sec=12.0,
            end_time_sec=16.5,
            duration_sec=4.5,
            narrative_beat="Agitation / Moral Outrage",
            visual=VisualCue(
                camera_angle=CameraAngle.MEDIUM_CLOSE_UP,
                camera_movement=CameraMovement.DUTCH_TILT,
                characters_present=["Ash Ketchum", "Pikachu"],
                scene_environment="Opposite side of obsidian boardroom table, Saffron Spire Floor 40",
                foreground_action="16-year-old Ash Ketchum slams both clenched fists onto the table, leaning forward in furious defiance. Pikachu on his shoulder bares fangs with sparking red cheeks",
                background_details="Dark executive office interior, reflections of sparks bouncing off the polished black tabletop",
                image_prompt="cinematic anime 9:16 vertical medium close-up, Dutch angle. 16-year-old hero Ash Ketchum slamming both fists down on obsidian boardroom table. Athletic build, messy jet-black spiky hair under red-and-white trainer cap, royal-blue vest with white collar and gold trim over charcoal compression shirt. Double zig-zag cheek marks, fiery brown eyes filled with moral outrage. Yellow Pikachu on his shoulder in battle stance, red cheeks crackling with golden electric arcs. Dynamic anime lighting.",
                negative_prompt="10-year-old child, chibi, blurry, extra fingers, soft cartoon",
                motion_prompt="Dutch tilt camera shakes violently on the fist slam impact. Ash leans forward aggressively as electric sparks jump from Pikachu's cheeks."
            ),
            dialogue=DialogueCue(
                speaker="Ash Ketchum",
                line="My Pokémon aren't your machines!",
                emotion="furious, unyielding, heroic roar",
                audio_ducking=True,
                estimated_duration_sec=2.5
            ),
            audio=AudioCue(
                bgm_mood="percussive battle urgency, rising anime strings",
                bgm_intensity=0.6,
                sfx=["heavy_fist_table_slam", "electric_spark_arc", "pikachu_snarl"]
            ),
            character_anchor_tokens=[character_bible["Ash Ketchum"], character_bible["Pikachu"]]
        ),

        # Shot 5: 16.5 - 21.0s (4.5s) [Enforcer Stun Rifles]
        ProductionShot(
            shot_id=5,
            start_time_sec=16.5,
            end_time_sec=21.0,
            duration_sec=4.5,
            narrative_beat="Conflict Escalation / Standoff",
            visual=VisualCue(
                camera_angle=CameraAngle.MEDIUM_SHOT,
                camera_movement=CameraMovement.WHIP_PAN,
                characters_present=["Consortium Enforcers"],
                scene_environment="Silph-Macro Boardroom perimeter doors, high-tech security interior",
                foreground_action="Four Consortium Enforcers in matte-black hydraulic exoskeleton armor snap into formation, aiming electromagnetic stun rifles",
                background_details="Security doors slid open, red warning klaxons pulsing in ceiling conduits",
                image_prompt="cinematic anime 9:16 vertical medium shot. Four futuristic Consortium tactical enforcers in matte-black hydraulic exoskeleton combat armor. Glowing amber tactical HUD visors, holding heavy electromagnetic stun carbines. Amber laser sight lines cutting through the dark boardroom air. Red emergency warning light glowing above steel doors.",
                negative_prompt="blurry, distorted armor, low resolution, bad proportions",
                motion_prompt="Fast whip-pan snap to the enforcers raising stun rifles in unison, amber laser dots locking forward as hydraulic armor joints hiss."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="high-tempo electronic combat pulse",
                bgm_intensity=0.65,
                sfx=["whip_pan_whoosh", "rifle_cocking_metallic", "capacitor_charge_whine", "klaxon_alarm"]
            ),
            character_anchor_tokens=[character_bible["Consortium Enforcers"]]
        ),

        # Shot 6: 21.0 - 25.5s (4.5s) [Battle Command: Thunderbolt]
        ProductionShot(
            shot_id=6,
            start_time_sec=21.0,
            end_time_sec=25.5,
            duration_sec=4.5,
            narrative_beat="Action / Battle Climax Command",
            visual=VisualCue(
                camera_angle=CameraAngle.CLOSE_UP,
                camera_movement=CameraMovement.SLOW_PUSH_IN,
                characters_present=["Ash Ketchum", "Pikachu"],
                scene_environment="Silph-Macro Boardroom center stage, backlit by golden electric charge",
                foreground_action="Ash thrusts his right arm forward decisively, Alolan Z-Ring glowing with cyan aura. Pikachu launches into the air with eyes blazing gold",
                background_details="Table papers and folders flying into air from violent electromagnetic updraft",
                image_prompt="cinematic anime 9:16 vertical close-up hero shot. Ash Ketchum thrusts his gloved arm forward in a dynamic battle command. Alolan Z-Ring on his wrist blazes with cyan aura, Mega Keystone bracelet catching the light. Cap bill angled upward, double cheek zig-zag marks glowing with golden voltage. Pikachu leaping off his shoulder surrounded by a sphere of crackling 10-million-volt golden lightning. Masterpiece anime keyframe.",
                negative_prompt="childish, blurry, low resolution, extra arms, weak posture",
                motion_prompt="Camera pushes in rapidly as Ash shouts command, golden lightning trails flare from Pikachu leaping into foreground."
            ),
            dialogue=DialogueCue(
                speaker="Ash Ketchum",
                line="Pikachu, full output—Thunderbolt!",
                emotion="passionate battle roar, peak intensity",
                audio_ducking=True,
                estimated_duration_sec=2.8
            ),
            audio=AudioCue(
                bgm_mood="epic triumphant orchestral battle choir with heavy synth drums",
                bgm_intensity=0.8,
                sfx=["z_ring_chime", "lightning_charge_buildup", "pika_battle_cry"]
            ),
            character_anchor_tokens=[character_bible["Ash Ketchum"], character_bible["Pikachu"]]
        ),

        # Shot 7: 25.5 - 30.5s (5.0s) [Glass Shattering Explosion]
        ProductionShot(
            shot_id=7,
            start_time_sec=25.5,
            end_time_sec=30.5,
            duration_sec=5.0,
            narrative_beat="Action / Window Breach",
            visual=VisualCue(
                camera_angle=CameraAngle.WIDE_SHOT,
                camera_movement=CameraMovement.HANDHELD_ORGANIC,
                characters_present=["Pikachu", "Consortium Enforcers"],
                scene_environment="Silph-Macro Boardroom Floor 40 exterior wall shattering outward",
                foreground_action="Massive apocalyptic golden electrical blast obliterates the 40th-floor tempered panoramic window into millions of glittering crystalline shards. Enforcers thrown backward by the shockwave",
                background_details="Torrents of midnight rain and howling storm winds rush inward through the gaping hole into the high-tech office",
                image_prompt="cinematic anime 9:16 vertical wide shot. Catastrophic golden electrical explosion completely shattering a giant 40th-floor glass skyscraper window into millions of glittering shards. Lightning bolts arc across ceiling and floor. Armored enforcers blown off their feet by kinetic shockwave. Outside the shattered window: stormy night rainstorm and lightning over Saffron City skyline. Ultra-detailed anime action spectacle.",
                negative_prompt="blurry, flat lighting, 3d CGI render, low resolution",
                motion_prompt="Handheld camera violently recoils from the blast impact. Slow-motion glass fragments shower outward into the rainy night void."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="colossal explosion impact followed by rushing hurricane storm wind",
                bgm_intensity=0.85,
                sfx=["thunderbolt_detonation_blast", "massive_glass_shatter", "enforcer_shockwave_impact", "howling_wind_storm"]
            ),
            character_anchor_tokens=[character_bible["Pikachu"], character_bible["Consortium Enforcers"]]
        ),

        # Shot 8: 30.5 - 35.5s (5.0s) [The Void Leap]
        ProductionShot(
            shot_id=8,
            start_time_sec=30.5,
            end_time_sec=35.5,
            duration_sec=5.0,
            narrative_beat="Twist / Daring Escape Leap",
            visual=VisualCue(
                camera_angle=CameraAngle.WIDE_SHOT,
                camera_movement=CameraMovement.TRACKING_FOLLOW,
                characters_present=["Ash Ketchum", "Pikachu"],
                scene_environment="Mid-air exterior of Silph-Macro Spire, 40 floors above ground, rainstorm",
                foreground_action="Ash and Pikachu dive headfirst out of the gaping window hole into the open rainy abyss, silhouetted against skyscraper lights",
                background_details="Exterior architectural steel beams, vertical neon signs, sheets of torrential rain and lightning strikes",
                image_prompt="cinematic anime 9:16 vertical wide dynamic dive. Ash Ketchum and Pikachu freefalling through the midnight rainstorm outside a massive glass skyscraper. Ash in athletic dive posture, cap held onto head with one gloved hand, coat whipping in the storm winds. Lightning illuminates rain droplets frozen mid-air around them. Below: dizzying vertical perspective of neon Saffron City streets 40 floors down. Masterful anime cinematography.",
                negative_prompt="awkward limbs, stiff pose, cartoonish, low resolution",
                motion_prompt="Camera tracks vertically downward at matching freefall speed, neon lights streaking past as rain whips across lens."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="breathless soaring strings with rhythmic rapid percussion",
                bgm_intensity=0.75,
                sfx=["rushing_air_freefall", "storm_thunder_crack", "rain_whoosh"]
            ),
            character_anchor_tokens=[character_bible["Ash Ketchum"], character_bible["Pikachu"]]
        ),

        # Shot 9: 35.5 - 40.5s (5.0s) [Iron Tail Kinetic Brake]
        ProductionShot(
            shot_id=9,
            start_time_sec=35.5,
            end_time_sec=40.5,
            duration_sec=5.0,
            narrative_beat="Action / Kinetic Brake",
            visual=VisualCue(
                camera_angle=CameraAngle.MEDIUM_SHOT,
                camera_movement=CameraMovement.TRACKING_FOLLOW,
                characters_present=["Ash Ketchum", "Pikachu"],
                scene_environment="Construction scaffolding attached to Silph-Macro building facade at floor 32",
                foreground_action="Pikachu somersaults in mid-air, tail morphing into blazing hardened metallic silver Iron Tail, slamming against a heavy steel I-beam. Ash grabs Pikachu's back to arrest momentum",
                background_details="Torrential rain showers, spray of intense orange friction sparks shooting 10 meters into the night air",
                image_prompt="cinematic anime 9:16 vertical action medium shot. Pikachu executes an acrobatic mid-fall flip, tail transforming into glowing metallic silver Iron Tail, striking a vertical steel construction girder. Massive spray of brilliant golden-orange friction sparks illuminates the scene. Ash Ketchum clutching structural cables with gloved hand, utilizing the momentum brake. Torrential rain splashing off steel. Dynamic anime motion blur.",
                negative_prompt="blurry face, missing tail, distorted body, 3d CGI",
                motion_prompt="Pikachu flips and slams tail against steel girder, heavy friction sparks erupting outward in a blinding arc as descent abruptly decelerates."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="high-adrenaline industrial metal percussion with anime strings",
                bgm_intensity=0.8,
                sfx=["steel_screech_friction", "sparks_burst", "scaffolding_creak"]
            ),
            character_anchor_tokens=[character_bible["Ash Ketchum"], character_bible["Pikachu"]]
        ),

        # Shot 10: 40.5 - 45.5s (5.0s) [Rooftop Impact Landing]
        ProductionShot(
            shot_id=10,
            start_time_sec=40.5,
            end_time_sec=45.5,
            duration_sec=5.0,
            narrative_beat="Twist / Recovery & Grounding",
            visual=VisualCue(
                camera_angle=CameraAngle.MEDIUM_SHOT,
                camera_movement=CameraMovement.SLOW_PUSH_IN,
                characters_present=["Ash Ketchum", "Pikachu"],
                scene_environment="Industrial lower rooftop of Saffron Spire annex, wet dark gravel, AC units and exhaust vents",
                foreground_action="Ash completes a three-point tuck-and-roll landing in a low athletic crouch, rainwater splashing from gravel. Pikachu lands right beside him, tail raised, cheeks sparking",
                background_details="Heavy rain pouring over rooftop structures, distant Saffron Spire tower disappearing into storm clouds above",
                image_prompt="cinematic anime 9:16 vertical medium shot. 16-year-old Ash Ketchum landed in a soaked three-point athletic crouch on a dark gravel rooftop at night. Rainwater dripping from his cap brim and dark messy hair. His royal-blue vest soaked with rain sheen. Pikachu in battle crouch beside him on wet asphalt, steam rising from Pikachu's electric cheeks. Atmospheric anime rain reflections, cool teal and dark charcoal tones.",
                negative_prompt="childish, dry clothes, cheerful, low resolution, warped limbs",
                motion_prompt="Ash rolls through landing into low crouch, water droplets flying off his cap and vest, looking up sharply into the darkness."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="tense brooding atmospheric synth with deep heartbeat thrum",
                bgm_intensity=0.6,
                sfx=["heavy_boot_gravel_splash", "roll_impact", "heavy_panting_breaths", "rooftop_rain_drumming"]
            ),
            character_anchor_tokens=[character_bible["Ash Ketchum"], character_bible["Pikachu"]]
        ),

        # Shot 11: 45.5 - 50.5s (5.0s) [Laser Ambush]
        ProductionShot(
            shot_id=11,
            start_time_sec=45.5,
            end_time_sec=50.5,
            duration_sec=5.0,
            narrative_beat="Cliffhanger / Laser Ambush",
            visual=VisualCue(
                camera_angle=CameraAngle.CLOSE_UP,
                camera_movement=CameraMovement.STATIC,
                characters_present=["Ash Ketchum"],
                scene_environment="Dark wet rooftop, shadowed industrial background",
                foreground_action="Four sharp crimson laser targeting dots converge onto Ash's chest and cap emblem. Ash's eyes widen as he freezes",
                background_details="Rain droplets caught in the crimson laser beams, steam rising from wet gravel",
                image_prompt="cinematic anime 9:16 vertical close-up. Ash Ketchum's chest and intense face in shadow. Four distinct razor-sharp crimson laser dots converge directly over the World Monarch insignia on his chest. Raindrops cut through the bright red laser lines. Ash's brown eyes widen in sudden shock and tactical awareness. Cinematic anime suspense lighting.",
                negative_prompt="blurry, distorted face, smiling, sunny, cartoonish",
                motion_prompt="Camera remains dead still. Four laser beams dart across his jacket before snapping together into an overlapping red crosshair on his chest."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="dead silence under ambient rain with high-tension digital drone",
                bgm_intensity=0.5,
                sfx=["laser_lock_high_frequency_beep", "heartbeat_thud", "rain_patters"]
            ),
            character_anchor_tokens=[character_bible["Ash Ketchum"]]
        ),

        # Shot 12: 50.5 - 55.5s (5.0s) [Cyber Houndoom Emergence]
        ProductionShot(
            shot_id=12,
            start_time_sec=50.5,
            end_time_sec=55.5,
            duration_sec=5.0,
            narrative_beat="Cliffhanger / Apex Predators",
            visual=VisualCue(
                camera_angle=CameraAngle.WIDE_SHOT,
                camera_movement=CameraMovement.SLOW_PUSH_IN,
                characters_present=["Cyber Houndoom"],
                scene_environment="Rooftop perimeter edge, steam vents billowing white mist into rain",
                foreground_action="Four cybernetic Houndoom stalk forward through steam, mechanical skull implants pulsing radioactive violet. Violet electric sparks drip from their razor fangs",
                background_details="Industrial exhaust fans spinning slowly, rain illuminated by violet and amber cybernetic optics",
                image_prompt="cinematic anime 9:16 vertical wide shot. Four cybernetic Houndoom stalking forward through billowing steam on a dark wet rooftop. Curved horns with titanium reinforcement, glowing violet Helix Neural Chips embedded between their brows. Hydraulic leg braces, glowing amber cyber-eyes, fangs crackling with dark violet electric fire. Menacing predatory anime composition.",
                negative_prompt="friendly dogs, blurry, cute, cartoonish, low resolution",
                motion_prompt="The four cyber-hounds prowl slowly out of steam plumes toward the camera, fangs dripping violet sparks as hydraulic joints hiss."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="terrifying cyber-hellhound snarling with distorted industrial bass",
                bgm_intensity=0.75,
                sfx=["houndoom_cyber_growl", "hydraulic_footstep_clicks", "violet_plasma_arc"]
            ),
            character_anchor_tokens=[character_bible["Cyber Houndoom"]]
        ),

        # Shot 13: 55.5 - 60.0s (4.5s) [Dragon Roar & Cut to Black]
        ProductionShot(
            shot_id=13,
            start_time_sec=55.5,
            end_time_sec=60.0,
            duration_sec=4.5,
            narrative_beat="Cliffhanger / Baton Pass Hook",
            visual=VisualCue(
                camera_angle=CameraAngle.MEDIUM_TWO_SHOT,
                camera_movement=CameraMovement.DUTCH_TILT,
                characters_present=["Ash Ketchum", "Pikachu", "Cyber Houndoom"],
                scene_environment="Rooftop standoff, storm clouds suddenly parting in sky above",
                foreground_action="Ash and Pikachu stand back-to-back surrounded by Houndoom flames. Suddenly, the sky above ignites in blinding crimson fire. A colossal winged dragon shadow blots out the moon. Hard cut to black with glowing typography: 'EPISODE 2 NEXT'",
                background_details="Raging orange-red thermal heat vaporizing falling raindrops into clouds of white steam",
                image_prompt="cinematic anime 9:16 vertical dramatic standoff. Ash Ketchum and Pikachu surrounded on rooftop by dark cyber-hounds. Suddenly, the storm sky directly above them ignites in blinding crimson-orange thermal fire. A colossal winged dragon silhouette (Charizard) swoops through storm clouds, vaporizing rain into steam. Bold glowing kinetic anime text in lower third: 'EPISODE 2 NEXT'. Peak cliffhanger shonen anime visual.",
                negative_prompt="blurry, low resolution, distorted text, cartoonish",
                motion_prompt="The sky above violently explodes in crimson dragon fire, vaporizing the rain into steam as the winged shadow descends. Sudden hard cut to black."
            ),
            dialogue=None,
            audio=AudioCue(
                bgm_mood="apocalyptic brass crescendo abruptly cut to silence",
                bgm_intensity=0.9,
                sfx=["sky_fire_eruption", "colossal_charizard_dragon_roar", "steam_hiss", "slam_cut_to_silence"]
            ),
            character_anchor_tokens=[character_bible["Ash Ketchum"], character_bible["Pikachu"], character_bible["Cyber Houndoom"]]
        )
    ]

    deck = ProductionShotDeck(
        title="Project Origin: The Shattered Crown - Episode 01: The Gilded Throne",
        target_platform="YouTube Shorts / Instagram Reels / TikTok",
        aspect_ratio=AspectRatio.VERTICAL_9_16,
        target_total_duration_sec=60.0,
        hook_thesis="Silph-Macro Consortium issues an ultimatum to World Monarch Ash Ketchum to surrender his Pokémon to cybernetic Helix Chips, triggering a skyscraper window blast and rooftop ambush.",
        call_to_action="Follow for Episode 2: Black-Ops Protocol dropping tomorrow!",
        character_bible=character_bible,
        shots=shots
    )
    return deck

def main():
    print("=" * 70)
    print("PROJECT ORIGIN: EPISODE 01 SCREENPLAY PRODUCTION COMPILATION")
    print("=" * 70)

    deck = create_ep01_shot_deck()
    engine = ScriptingEngine(output_dir=str(root_dir / "data" / "shot_decks"))

    # Adversarial QA Evaluation
    critique = engine.evaluate_shot_deck(deck)

    print(f"\n[Project Title] {deck.title}")
    print(f"[Aspect Ratio]  {deck.aspect_ratio.value} (Target: 1080x1920 Vertical)")
    print(f"[Total Shots]   {len(deck.shots)} shots")
    print(f"[Total Time]    {sum(s.duration_sec for s in deck.shots):.1f}s / {deck.target_total_duration_sec:.1f}s")
    print(f"[QA Score]      {critique.overall_score}/10.0")
    print(f"[Hook Score]    {critique.hook_score}/10.0")
    print(f"[Pacing Score]  {critique.pacing_score}/10.0")
    print(f"[Visual Score]  {critique.visual_continuity_feasibility}/10.0")
    print(f"[Passes Gate]   {critique.passes_quality_gate}")

    if critique.flaws_and_bottlenecks:
        print("\n[Identified Bottlenecks]:")
        for flaw in critique.flaws_and_bottlenecks:
            print(f"  - {flaw}")

    assert critique.passes_quality_gate, f"QA Quality Gate failed with score {critique.overall_score}"
    assert sum(s.duration_sec for s in deck.shots) == 60.0, "Total duration must equal 60.0s exactly!"

    # Save to JSON
    output_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deck.model_dump(), f, indent=2)

    print(f"\n✅ Production shot deck successfully compiled and saved to:\n   {output_path}")

if __name__ == "__main__":
    main()
