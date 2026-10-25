import os, csv, time, requests, praw
from dotenv import load_dotenv

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

SUBREDDITS = ["memes", "dankmemes"]
LIMIT = 20  # test sghir, nkabbrouha ba3d
IMG_DIR = "data/raw/images"
CSV_PATH = "data/raw/reddit_raw.csv"
FIELDS = ["post_id", "image_path", "text", "subreddit", "score", "created_utc"]

os.makedirs(IMG_DIR, exist_ok=True)

# nest7fedhou bel post_id elli déjà jebnehom (anti-doublons)
seen = set()
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, encoding="utf-8") as f:
        seen = {row["post_id"] for row in csv.DictReader(f)}

new_file = not os.path.exists(CSV_PATH)
with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    if new_file:
        writer.writeheader()

    for sub in SUBREDDITS:
        count = 0
        for post in reddit.subreddit(sub).hot(limit=LIMIT):
            ext = os.path.splitext(post.url)[1].lower()
            if post.id in seen or ext not in (".jpg", ".jpeg", ".png"):
                continue

            text = f"{post.title} {post.selftext}".strip()
            if not text:
                continue

            path = f"{IMG_DIR}/{post.id}{ext}"
            try:
                r = requests.get(post.url, timeout=10)
                r.raise_for_status()
            except requests.RequestException:
                continue
            with open(path, "wb") as img:
                img.write(r.content)

            writer.writerow({
                "post_id": post.id, "image_path": path, "text": text,
                "subreddit": sub, "score": post.score,
                "created_utc": int(post.created_utc),
            })
            seen.add(post.id)
            count += 1
            time.sleep(1)  # rate limit

        print(f"r/{sub}: {count} posts jdod")