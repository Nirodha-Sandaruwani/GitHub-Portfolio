import json
import os
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta

USERNAME = "Nirodha-Sandaruwani"
TOKEN = os.environ["GITHUB_TOKEN"]

OUT_FILE = os.path.join(os.path.dirname(__file__), "github-stats.svg")

BG = "#0D1117"
BORDER = "#30363D"
TEXT = "#F0F6FC"
MUTED = "#8B949E"
PURPLE = "#8B5CF6"
PURPLE_LIGHT = "#C4B5FD"

LANG_COLORS = [
    "#DA5B0B",
    "#F1E05A",
    "#3572A5",
    "#C6538C",
    "#663399",
    "#3178C6",
    "#89E051",
    "#E34C26",
]


def request_json(url, data=None, token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-stats",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = None
    if data is not None:
        payload = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=payload, headers=headers)

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def graphql(query, variables):
    result = request_json(
        "https://api.github.com/graphql",
        {"query": query, "variables": variables},
        TOKEN,
    )

    if result.get("errors"):
        raise RuntimeError(result["errors"])

    return result["data"]


def get_contribution_data():
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          commitContributionsByRepository(maxRepositories: 100) {
            repository {
              nameWithOwner
            }
          }
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    data = graphql(query, {"login": USERNAME})
    return data["user"]["contributionsCollection"]


def get_public_repositories():
    repos = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/users/{USERNAME}/repos"
            f"?type=owner&per_page=100&page={page}"
        )

        batch = request_json(url)

        if not batch:
            break

        repos.extend(repo for repo in batch if not repo.get("fork"))

        if len(batch) < 100:
            break

        page += 1

    return repos


def get_languages(repositories):
    totals = defaultdict(int)

    for repo in repositories:
        language_data = request_json(repo["languages_url"])

        for language, byte_count in language_data.items():
            totals[language] += int(byte_count)

    return dict(totals)


def flatten_contribution_days(collection):
    result = []

    for week in collection["contributionCalendar"]["weeks"]:
        for day in week["contributionDays"]:
            result.append(
                (
                    datetime.strptime(day["date"], "%Y-%m-%d").date(),
                    int(day["contributionCount"]),
                )
            )

    return sorted(result)


def calculate_streaks(days):
    if not days:
        return 0, 0

    active = {day: count > 0 for day, count in days}

    cursor = days[-1][0]

    if not active.get(cursor, False):
        cursor -= timedelta(days=1)

    current_streak = 0

    while active.get(cursor, False):
        current_streak += 1
        cursor -= timedelta(days=1)

    longest_streak = 0
    running = 0

    for _, count in days:
        if count > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    return current_streak, longest_streak


def monthly_activity(days):
    totals = defaultdict(int)

    for day, count in days:
        totals[(day.year, day.month)] += count

    if not days:
        return []

    year = days[-1][0].year
    month = days[-1][0].month
    months = []

    for _ in range(12):
        months.append((year, month))
        month -= 1

        if month == 0:
            month = 12
            year -= 1

    months.reverse()

    return [
        (
            datetime(year, month, 1).strftime("%b"),
            totals.get((year, month), 0),
        )
        for year, month in months
    ]


def text(x, y, value, size=14, color=TEXT, weight=400, anchor="start"):
    safe = (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="Segoe UI,Arial,sans-serif" '
        f'font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" text-anchor="{anchor}">'
        f'{safe}</text>'
    )


def card(x, y, width, height):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="6" fill="{BG}" stroke="{BORDER}" />'
    )


def line(x1, y1, x2, y2, color=BORDER, width=1):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}" />'
    )


def build_svg(collection, repositories, languages):
    days = flatten_contribution_days(collection)
    current_streak, longest_streak = calculate_streaks(days)

    total_contributions = collection["contributionCalendar"]["totalContributions"]
    total_commits = collection["totalCommitContributions"]
    total_prs = collection["totalPullRequestContributions"]
    total_issues = collection["totalIssueContributions"]
    contributed_repos = len(collection["commitContributionsByRepository"])
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repositories)

    width = 900
    height = 440

    left_x = 20
    right_x = 460
    top_y = 20
    bottom_y = 230
    card_width = 420
    card_height = 190

    svg = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
        ),
        f'<rect width="{width}" height="{height}" fill="{BG}" />',
    ]

    # Top-left: contribution / streak card
    svg.append(card(left_x, top_y, card_width, card_height))
    svg.append(line(left_x + 140, top_y + 45, left_x + 140, top_y + 150))
    svg.append(line(left_x + 280, top_y + 45, left_x + 280, top_y + 150))

    centers = [left_x + 70, left_x + 210, left_x + 350]

    svg.extend([
        text(centers[0], top_y + 88, total_contributions, 26, TEXT, 700, "middle"),
        text(centers[0], top_y + 116, "Total Contributions", 11, TEXT, 400, "middle"),
        text(centers[0], top_y + 139, "last year", 9, MUTED, 400, "middle"),

        (
            f'<circle cx="{centers[1]}" cy="{top_y + 85}" r="34" '
            f'fill="none" stroke="{PURPLE}" stroke-width="5" />'
        ),
        text(centers[1], top_y + 94, current_streak, 25, TEXT, 700, "middle"),
        text(centers[1], top_y + 130, "Current Streak", 11, PURPLE_LIGHT, 700, "middle"),

        text(centers[2], top_y + 88, longest_streak, 26, TEXT, 700, "middle"),
        text(centers[2], top_y + 116, "Longest Streak", 11, TEXT, 400, "middle"),
    ])

    # Top-right: GitHub stats
    svg.append(card(right_x, top_y, card_width, card_height))
    svg.append(text(right_x + 24, top_y + 38, "Stats", 26, PURPLE_LIGHT, 600))

    rows = [
        ("Total Stars", total_stars),
        ("Total Commits", total_commits),
        ("Total PRs", total_prs),
        ("Total Issues", total_issues),
        ("Contributed to", contributed_repos),
    ]

    row_y = top_y + 72

    for label, value in rows:
        svg.append(
            f'<circle cx="{right_x + 30}" cy="{row_y - 5}" r="5" '
            f'fill="none" stroke="{PURPLE}" stroke-width="2" />'
        )
        svg.append(text(right_x + 45, row_y, f"{label}:", 14))
        svg.append(text(right_x + 250, row_y, value, 15, TEXT, 500))
        row_y += 27

    # Bottom-left: languages
    svg.append(card(left_x, bottom_y, card_width, card_height))
    svg.append(
        text(left_x + 24, bottom_y + 36, "Programming Languages", 20, PURPLE_LIGHT, 600)
    )

    language_total = sum(languages.values())
    ranked = sorted(languages.items(), key=lambda item: item[1], reverse=True)[:6]

    bar_x = left_x + 24
    bar_y = bottom_y + 58
    bar_width = card_width - 48
    cursor = bar_x

    for index, (_, byte_count) in enumerate(ranked):
        width_value = (byte_count / language_total * bar_width) if language_total else 0

        svg.append(
            f'<rect x="{cursor:.2f}" y="{bar_y}" '
            f'width="{max(width_value, 1):.2f}" height="9" '
            f'fill="{LANG_COLORS[index]}" />'
        )

        cursor += width_value

    for index, (language, byte_count) in enumerate(ranked):
        column = index % 2
        row = index // 2

        x = left_x + 28 + column * 190
        y = bottom_y + 94 + row * 27

        percentage = (
            byte_count / language_total * 100 if language_total else 0
        )

        svg.append(
            f'<circle cx="{x}" cy="{y - 4}" r="5" '
            f'fill="{LANG_COLORS[index]}" />'
        )

        svg.append(
            text(x + 12, y, f"{language} {percentage:.2f}%", 11)
        )

    # Bottom-right: contribution graph
    svg.append(card(right_x, bottom_y, card_width, card_height))
    svg.append(
        text(right_x + 24, bottom_y + 34, "Contribution Activity", 18, PURPLE_LIGHT, 600)
    )

    months = monthly_activity(days)

    chart_x = right_x + 34
    chart_y = bottom_y + 62
    chart_width = card_width - 58
    chart_height = 88

    for fraction in (0, 0.5, 1):
        y = chart_y + chart_height * fraction
        svg.append(line(chart_x, y, chart_x + chart_width, y, "#21262D"))

    values = [value for _, value in months]
    maximum = max(values) if values else 1
    maximum = max(maximum, 1)

    points = []

    for index, (_, value) in enumerate(months):
        x = chart_x + chart_width * index / max(len(months) - 1, 1)
        y = chart_y + chart_height - (value / maximum) * chart_height
        points.append((x, y))

    if points:
        line_points = " ".join(
            f"{x:.1f},{y:.1f}" for x, y in points
        )

        area_points = (
            [(points[0][0], chart_y + chart_height)]
            + points
            + [(points[-1][0], chart_y + chart_height)]
        )

        area = " ".join(
            f"{x:.1f},{y:.1f}" for x, y in area_points
        )

        svg.append(
            f'<polygon points="{area}" fill="{PURPLE}" opacity="0.18" />'
        )

        svg.append(
            f'<polyline points="{line_points}" fill="none" '
            f'stroke="{PURPLE}" stroke-width="3" '
            f'stroke-linecap="round" stroke-linejoin="round" />'
        )

    for index, (label, _) in enumerate(months):
        if index % 2 == 0 or index == len(months) - 1:
            x = chart_x + chart_width * index / max(len(months) - 1, 1)

            svg.append(
                text(
                    x,
                    chart_y + chart_height + 20,
                    label,
                    9,
                    MUTED,
                    400,
                    "middle",
                )
            )

    svg.append(
        text(
            right_x + 24,
            bottom_y + 174,
            f"{total_contributions} contributions · {len(repositories)} public repos",
            10,
            MUTED,
        )
    )

    svg.append("</svg>")

    return "\n".join(svg)


collection = get_contribution_data()
repositories = get_public_repositories()
languages = get_languages(repositories)

svg = build_svg(collection, repositories, languages)

with open(OUT_FILE, "w", encoding="utf-8") as file:
    file.write(svg)

print(f"Updated {OUT_FILE}")
