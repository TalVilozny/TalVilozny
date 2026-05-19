"""Generate the retro terminal GitHub stats GIF for the profile README."""

import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

GITHUB_USER = "TalVilozny"
OUTPUT_GIF = "assets/github-stats.gif"
ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "gifos"
TERMINAL_IMAGE_CONFIG = ROOT / "config" / "terminal_image.toml"
TERMINAL_ASSETS_DIR = ROOT / "assets" / "terminal"
FONTS_DIR = ROOT / "fonts"
PROFILE_PHOTO_NAMES = (
    "profile-photo.jpg",
    "profile-photo.jpeg",
    "profile-photo.png",
    "profile-photo.webp",
)


def install_gifos_config() -> None:
    """Install repo TOML into ~/.config/gifos/ before gifos loads config."""
    dest = Path.home() / ".config" / "gifos"
    dest.mkdir(parents=True, exist_ok=True)
    if not CONFIG_DIR.is_dir():
        print("INFO: No config/gifos/ directory; using package defaults.", file=sys.stderr)
        return
    for toml_file in sorted(CONFIG_DIR.glob("*.toml")):
        shutil.copy2(toml_file, dest / toml_file.name)
        print(f"INFO: Installed gifos config: {toml_file.name}", file=sys.stderr)


install_gifos_config()

import gifos  # noqa: E402  # must load after config is installed

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


def load_terminal_image_settings() -> dict:
    defaults = {
        "filename": "profile-photo.jpg",
        "row": 3,
        "col": 5,
        "size_multiplier": 0.45,
    }
    if not TERMINAL_IMAGE_CONFIG.is_file():
        return defaults
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]
    with TERMINAL_IMAGE_CONFIG.open("rb") as fp:
        data = tomllib.load(fp)
    image = data.get("image", {})
    return {
        "filename": image.get("filename", defaults["filename"]),
        "row": int(image.get("row", defaults["row"])),
        "col": int(image.get("col", defaults["col"])),
        "size_multiplier": float(
            image.get("size_multiplier", defaults["size_multiplier"])
        ),
    }


def resolve_profile_photo(preferred_name: str | None = None) -> Path | None:
    names: list[str] = []
    if preferred_name:
        names.append(preferred_name)
    names.extend(PROFILE_PHOTO_NAMES)
    seen: set[str] = set()
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        path = TERMINAL_ASSETS_DIR / name
        if path.is_file() and path.stat().st_size > 1000:
            return path
    return None


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


def build_stats_text(
    user_rating: str,
    total_stars: int,
    commits_last_year: int,
    last_year: int,
    top_languages: str,
) -> str:
    """GitHub Stats section only (no PRs, merge %, or contributions)."""
    return f"""
        \x1b[30;101m{GITHUB_USER}@GitHub\x1b[0m
        --------------
        \x1b[96mOS: \x1b[93mWindows\x1b[0m
        \x1b[96mHost: \x1b[93mFrontend Developer / UX/UI Designer\x1b[0m
        \x1b[96mKernel: \x1b[93mReact + TypeScript + JavaScript\x1b[0m
        \x1b[96mIDE: \x1b[93mVS Code, Cursor\x1b[0m

        \x1b[30;101mContact:\x1b[0m
        --------------
        \x1b[96mEmail: \x1b[93mTalVilozny@gmail.com\x1b[0m
        \x1b[96mLinkedIn: \x1b[93mtal-vilozny-frontend\x1b[0m

        \x1b[30;101mGitHub Stats:\x1b[0m
        --------------
        \x1b[96mUser Rating: \x1b[93m{user_rating}\x1b[0m
        \x1b[96mTotal Stars Earned: \x1b[93m{total_stars}\x1b[0m
        \x1b[96mTotal Commits ({last_year}): \x1b[93m{commits_last_year}\x1b[0m
        \x1b[96mTop Languages: \x1b[93m{top_languages}\x1b[0m
        """


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
    # Remove stale GIF so a failed partial run cannot be committed.
    stale_gif = ROOT / OUTPUT_GIF
    if stale_gif.is_file():
        stale_gif.unlink()

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
    user_details_lines = build_stats_text(
        user_rating,
        stats.total_stargazers,
        stats.total_commits_last_year,
        last_year,
        top_languages,
    )

    image_cfg = load_terminal_image_settings()
    profile_photo = resolve_profile_photo(image_cfg["filename"])

    bitmap_font = get_bitmap_font()
    t = gifos.Terminal(750, 500, 15, 15, bitmap_font, 15)

    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(f" -u {GITHUB_USER.lower()}", 1, contin=True)

    t.toggle_show_cursor(False)
    if profile_photo:
        print(f"INFO: Using profile photo: {profile_photo}", file=sys.stderr)
        t.paste_image(
            str(profile_photo),
            row_num=image_cfg["row"],
            col_num=image_cfg["col"],
            size_multiplier=image_cfg["size_multiplier"],
        )
    else:
        print("INFO: No profile photo; using Mona ASCII art fallback.", file=sys.stderr)
        mona_font = get_mona_font()
        t.set_font(mona_font, 16, 0)
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
