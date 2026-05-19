"""Generate the retro terminal GitHub stats GIF for the profile README."""

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import gifos

GITHUB_USER = "TalVilozny"
OUTPUT_GIF = "assets/github-stats.gif"
ROOT = Path(__file__).resolve().parents[1]
FONTS_DIR = ROOT / "fonts"
GIFOS_FONTS_DIR = Path(gifos.__file__).resolve().parent / "fonts"

FONT_FILE_BITMAP = "gohufont-uni-14.pil"
FONT_FILE_MONA = "Inversionz.otf"

MONA_LINES = r"""
        \x1b[49m    \x1b[90;100m}}\x1b[49m      \x1b[90;100m}}\x1b[0m
        \x1b[49m   \x1b[90;100m}}}}\x1b[49m     \x1b[90;100m}}}}\x1b[0m
        \x1b[49m  \x1b[90;100m}}}}}\x1b[49m    \x1b[90;100m}}}}}\x1b[0m
        \x1b[49m  \x1b[90;100m}}}}}}}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}}}}}}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}\x1b[37;47m}}}}}}}\x1b[90;100m}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}\x1b[37;47m}}}}}}}}}}\x1b[90;100m}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}\x1b[37;47m}\x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}\x1b[37;47m}}\x1b[90;100m}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}\x1b[37;47m}}\x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}\x1b[37;47m}}}\x1b[90;100m}}}\x1b[0m
        \x1b[90;100m}}}\x1b[37;47m}}}}\x1b[90;100m}}}\x1b[37;47m}}}}}\x1b[90;100m}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}\x1b[37;47m}}}}}\x1b[90;100m}}\x1b[37;47m}}}}}\x1b[90;100m}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}\x1b[37;47m}}}}}}}}}}}}\x1b[90;100m}}}\x1b[0m
        \x1b[90;100m}\x1b[49m \x1b[90;100m}}\x1b[37;47m}}}}}}}}\x1b[90;100m}}}\x1b[49m \x1b[90;100m}\x1b[0m
        \x1b[49m  \x1b[90;100m}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}}}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}}}}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}\x1b[49m  \x1b[90;100m}}}}}}\x1b[49m \x1b[90;100m}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}}}}}\x1b[0m
        \x1b[49m \x1b[90;100m}}}\x1b[49m  \x1b[90;100m}}\x1b[0m
"""


def latin1_safe(text: str | None) -> str:
    """Bitmap font only supports latin-1; strip/replace other characters."""
    if not text:
        return ""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def get_bitmap_font() -> str:
    """Always use the font shipped inside the gifos package."""
    path = GIFOS_FONTS_DIR / FONT_FILE_BITMAP
    if not path.is_file():
        raise FileNotFoundError(f"Bundled bitmap font missing: {path}")
    return str(path)


def get_mona_font() -> str:
    """Mona art needs Inversionz.otf (downloaded in CI or placed in fonts/)."""
    path = FONTS_DIR / FONT_FILE_MONA
    if path.is_file() and path.stat().st_size > 10_000:
        return str(path)
    raise FileNotFoundError(
        f"Missing {FONT_FILE_MONA} in fonts/. "
        "Re-run the GitHub Action or download it from x0rzavi/x0rzavi."
    )


def main() -> None:
    os.makedirs("assets", exist_ok=True)

    year_now = datetime.now(timezone.utc).strftime("%Y")
    last_year = int(year_now) - 1
    stats = gifos.utils.fetch_github_stats(GITHUB_USER)
    if stats is None:
        raise RuntimeError(f"Could not fetch GitHub stats for {GITHUB_USER}")

    top_languages = latin1_safe(
        ", ".join(lang[0] for lang in stats.languages_sorted[:5])
        if stats.languages_sorted
        else "N/A"
    )
    user_rating = latin1_safe(stats.user_rank.level)

    user_details_lines = f"""
        \x1b[30;101m{GITHUB_USER}@GitHub\x1b[0m
        --------------
        \x1b[96mOS: \x1b[93mWindows / Linux\x1b[0m
        \x1b[96mHost: \x1b[93mFrontend Developer\x1b[0m
        \x1b[96mKernel: \x1b[93mReact + TypeScript\x1b[0m
        \x1b[96mIDE: \x1b[93mVS Code, Cursor\x1b[0m

        \x1b[30;101mContact:\x1b[0m
        --------------
        \x1b[96mEmail: \x1b[93mTalVilozny@gmail.com\x1b[0m
        \x1b[96mLinkedIn: \x1b[93mtal-vilozny-frontend\x1b[0m

        \x1b[30;101mGitHub Stats:\x1b[0m
        --------------
        \x1b[96mUser Rating: \x1b[93m{user_rating}\x1b[0m
        \x1b[96mTotal Stars Earned: \x1b[93m{stats.total_stargazers}\x1b[0m
        \x1b[96mTotal Commits ({last_year}): \x1b[93m{stats.total_commits_last_year}\x1b[0m
        \x1b[96mTop Languages: \x1b[93m{top_languages}\x1b[0m
        """

    bitmap_font = get_bitmap_font()
    mona_font = get_mona_font()

    t = gifos.Terminal(750, 500, 15, 15, bitmap_font, 15)

    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(f" -u {GITHUB_USER.lower()}", 1, contin=True)

    t.set_font(mona_font, 16, 0)
    t.toggle_show_cursor(False)
    t.gen_text(MONA_LINES, 10)

    t.set_font(bitmap_font)
    t.toggle_show_cursor(True)
    t.gen_text(user_details_lines, 2, 35, count=5, contin=True)
    t.gen_prompt(t.curr_row)
    t.gen_typing_text(
        "\x1b[92m# Thanks for visiting my profile!",
        t.curr_row,
        contin=True,
    )
    t.gen_text("", t.curr_row, count=120, contin=True)

    t.gen_gif()
    shutil.move("output.gif", OUTPUT_GIF)
    print(f"Wrote {OUTPUT_GIF}")


if __name__ == "__main__":
    main()
