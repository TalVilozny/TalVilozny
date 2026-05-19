"""Generate the retro terminal GitHub stats GIF for the profile README."""

import os
import shutil
from datetime import datetime, timezone

import gifos

GITHUB_USER = "TalVilozny"
OUTPUT_GIF = "assets/github-stats.gif"


def main() -> None:
    os.makedirs("assets", exist_ok=True)

    year_now = datetime.now(timezone.utc).strftime("%Y")
    stats = gifos.utils.fetch_github_stats(GITHUB_USER)
    top_languages = ", ".join(lang[0] for lang in stats.languages_sorted[:5])

    t = gifos.Terminal(width=640, height=420, xpad=10, ypad=10)

    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mGIF OS v1.0 — profile terminal\x1b[0m", 1, count=4)
    t.gen_text("login: ", 3, count=3)
    t.toggle_show_cursor(True)
    t.gen_typing_text(GITHUB_USER.lower(), 3, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=2)
    t.toggle_show_cursor(True)
    t.gen_typing_text("********", 4, contin=True)
    t.toggle_show_cursor(False)

    t.gen_prompt(6, count=3)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mneofet", 6, contin=True)
    t.delete_row(6, prompt_col)
    t.gen_text("\x1b[92mneofetch\x1b[0m", 6, count=2, contin=True)

    stats_block = f"""
\x1b[30;101m{GITHUB_USER}@GitHub\x1b[0m
--------------
\x1b[96mOS: \x1b[93mWindows / Linux\x1b[0m
\x1b[96mHost: \x1b[93mFrontend Developer\x1b[0m
\x1b[96mShell: \x1b[93mReact + TypeScript\x1b[0m
\x1b[96mEmail: \x1b[93mTalVilozny@gmail.com\x1b[0m

\x1b[30;101mGitHub Stats:\x1b[0m
--------------
\x1b[96mAccount: \x1b[93m{stats.account_name}\x1b[0m
\x1b[96mUser Rating: \x1b[93m{stats.user_rank.level}\x1b[0m
\x1b[96mTotal Stars: \x1b[93m{stats.total_stargazers}\x1b[0m
\x1b[96mCommits ({int(year_now) - 1}): \x1b[93m{stats.total_commits_last_year}\x1b[0m
\x1b[96mTotal PRs: \x1b[93m{stats.total_pull_requests_made}\x1b[0m
\x1b[96mMerged PR %: \x1b[93m{stats.pull_requests_merge_percentage}\x1b[0m
\x1b[96mContributions: \x1b[93m{stats.total_repo_contributions}\x1b[0m
\x1b[96mTop Languages: \x1b[93m{top_languages}\x1b[0m
"""

    t.clear_frame()
    t.gen_text(stats_block.strip(), 1, count=8, contin=True)
    t.gen_prompt(t.curr_row)
    t.toggle_show_cursor(True)
    t.gen_typing_text(
        "\x1b[92m# Thanks for visiting my profile!",
        t.curr_row,
        contin=True,
    )
    t.gen_text("", t.curr_row, count=60, contin=True)

    t.gen_gif()
    shutil.move("output.gif", OUTPUT_GIF)
    print(f"Wrote {OUTPUT_GIF}")


if __name__ == "__main__":
    main()
