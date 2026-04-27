from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .config import load_settings
from .notifier import build_daily_message, push_message
from .scraper import fetch_internship_jobs
from .storage import connect, jobs_deadline_on, upsert_jobs


def run_once(push: bool = True) -> None:
    settings = load_settings()
    timezone = ZoneInfo(settings.timezone)
    now = datetime.now(timezone)

    jobs = fetch_internship_jobs(settings.search_url, headless=settings.playwright_headless)
    today_jobs = [job for job in jobs if job.posted_date == now.date()]
    with connect(settings.database_path) as connection:
        upsert_jobs(connection, jobs, now)
        deadline_date = (now + timedelta(days=settings.lookahead_days)).date()
        deadline_jobs = jobs_deadline_on(connection, deadline_date)

    title, body = build_daily_message(today_jobs, deadline_jobs)
    if push:
        push_message(
            settings.push_channel,
            title,
            body,
            serverchan_sendkey=settings.serverchan_sendkey,
            wecom_webhook_url=settings.wecom_webhook_url,
        )
    else:
        print(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor UN Careers internship openings.")
    parser.add_argument("--no-push", action="store_true", help="只抓取并输出摘要，不发送微信推送")
    args = parser.parse_args()
    run_once(push=not args.no_push)


if __name__ == "__main__":
    main()
