"""
Automated script to purge all references to the legacy Appin sister/brother story
across schemas, generators, orchestrators, tests, and schedule data.
Replaces with Project Origin: The Shattered Crown (Ash & Red).
"""

import re
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

def clean_file(path: Path, replacements: list):
    if not path.exists():
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = content
    for pattern, repl in replacements:
        modified = re.sub(pattern, repl, modified, flags=re.MULTILINE)

    if modified != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"✅ Cleaned: {path.name}")
    else:
        print(f"ℹ️ No changes needed: {path.name}")

def main():
    print("=" * 70)
    print("PURGING ALL LEGACY APPIN STORY REFERENCES ACROSS CODEBASE")
    print("=" * 70)

    # 1. src/audio/tts_engine.py
    clean_file(
        root_dir / "src" / "audio" / "tts_engine.py",
        [
            (
                r'DEFAULT_PERSONAS = \{[\s\S]*?^\s{4}\}',
                '''DEFAULT_PERSONAS = {
        "Ash Ketchum": VoicePersona(
            persona_name="Ash Ketchum",
            voice_identifier="en-US-GuyNeural",
            gender="male",
            speaking_rate=1.05,
            provider="windows-sapi"
        ),
        "Vance Stirling": VoicePersona(
            persona_name="Vance Stirling",
            voice_identifier="en-GB-RyanNeural",
            gender="male",
            speaking_rate=0.95,
            provider="windows-sapi"
        ),
        "Red": VoicePersona(
            persona_name="Red",
            voice_identifier="en-US-AndrewNeural",
            gender="male",
            speaking_rate=0.90,
            provider="windows-sapi"
        ),
        "Narrator": VoicePersona(
            persona_name="Narrator",
            voice_identifier="en-US-ChristopherNeural",
            gender="male",
            speaking_rate=1.0,
            provider="windows-sapi"
        ),
    }'''
            )
        ]
    )

    # 2. src/distribution/metadata_generator.py
    clean_file(
        root_dir / "src" / "distribution" / "metadata_generator.py",
        [
            (r'https://appintechnology\.com/cybersecurity-demo', 'https://youtube.com/@ProjectOriginAnime'),
            (r'Rajat Caught Hacking Live[\s\S]*?#BTech"', '''Ash REFUSES the Corporate Crown?! 😱 Pikachu Shatters Floor 40!\\n\\nWorld Monarch Ash Ketchum is summoned to the 40th floor of the Silph-Macro Spire...\\nCEO Vance Stirling reveals the Helix Neural Chip.\\nAsh's answer? 'My Pokémon aren't your machines!' 🔥⚡\\n\\n#Pokemon #AshKetchum #PokemonJourneys #AnimeShorts #Pikachu"'''),
            (r'cyber security course', 'pokemon journeys anime'),
            (r'ethical hacking tutorial', 'ash and red'),
            (r'placement preparation btech', 'pikachu thunderbolt'),
            (r'appin technology', 'project origin'),
            (r'Drop a 🔥 if your college lab looks nothing like this! Book your Free Demo via the link in description/bio', 'Drop a ⚡ if you stand with Ash and Pikachu against the Consortium! Episode 2 drops tomorrow at 18:30 IST / 13:00 UTC.')
        ]
    )

    # 3. run_studio.py
    clean_file(
        root_dir / "run_studio.py",
        [
            (r'project_title: str = "Appin Career Ka Asli Netflix"', 'project_title: str = "Project Origin: The Shattered Crown"'),
            (r'target_duration: float = 18\.5', 'target_duration: float = 60.0'),
            (r'appin_master_9x16\.mp4', 'project_origin_ep01_master_9x16.mp4'),
            (r'Elder sister confronts brother for bingeing Netflix during campus placements, only to discover he is hacking in a real-world Appin cybersecurity lab', 'Silph-Macro Consortium issues an ultimatum to World Monarch Ash Ketchum to surrender his Pokémon to cybernetic Helix Chips, triggering a skyscraper window blast and rooftop ambush.')
        ]
    )

    # 4. tests/test_scripting_engine.py
    clean_file(
        root_dir / "tests" / "test_scripting_engine.py",
        [
            (r'premise = "Elder sister confronts brother[\s\S]*?target_duration=18\.5\)', 'premise = "Silph-Macro Consortium issues an ultimatum to World Monarch Ash Ketchum to surrender his Pokémon to cybernetic Helix Chips, triggering a skyscraper window blast and rooftop ambush"\n    deck, critique = engine.generate_shot_deck(premise=premise, target_duration=60.0)')
        ]
    )

    # 5. tests/test_audio_engine.py
    clean_file(
        root_dir / "tests" / "test_audio_engine.py",
        [
            (r'appin_career_ka_asli_netflix_shot_deck\.json', 'project_origin_ep01_shot_deck.json')
        ]
    )

    # 6. tests/test_motion_and_compositor.py
    clean_file(
        root_dir / "tests" / "test_motion_and_compositor.py",
        [
            (r'appin_career_ka_asli_netflix_shot_deck\.json', 'project_origin_ep01_shot_deck.json')
        ]
    )

    # 7. tests/test_timeline_assembly.py
    clean_file(
        root_dir / "tests" / "test_timeline_assembly.py",
        [
            (r'appin_career_ka_asli_netflix_shot_deck\.json', 'project_origin_ep01_shot_deck.json'),
            (r'range\(1, 6\)', 'range(1, 14)'),
            (r'appin_master_9x16\.mp4', 'project_origin_ep01_master_9x16.mp4'),
            (r'master_soundtrack\.wav', 'project_origin_ep01_soundtrack.wav'),
            (r'video_clips_dir = root_dir / "data" / "video_clips"', 'video_clips_dir = root_dir / "data" / "video_clips" / "ep01"'),
            (r'target_duration_sec=18\.5', 'target_duration_sec=60.0')
        ]
    )

    # 8. tests/test_distribution.py
    clean_file(
        root_dir / "tests" / "test_distribution.py",
        [
            (r'appin_career_ka_asli_netflix_shot_deck\.json', 'project_origin_ep01_shot_deck.json'),
            (r'appin_master_9x16\.mp4', 'project_origin_ep01_master_9x16.mp4')
        ]
    )

    # 9. data/schedules/scheduled_dispatches.json
    clean_file(
        root_dir / "data" / "schedules" / "scheduled_dispatches.json",
        [
            (r'Appin Career Ka Asli Netflix', 'Project Origin: The Shattered Crown'),
            (r'appin_master_9x16\.mp4', 'project_origin_ep01_master_9x16.mp4'),
            (r'https://appintechnology\.com/cybersecurity-demo', 'https://youtube.com/@ProjectOriginAnime')
        ]
    )

    print("\n✅ All Appin story references successfully purged from codebase!")

if __name__ == "__main__":
    main()
