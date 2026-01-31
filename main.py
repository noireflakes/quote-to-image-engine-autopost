import os
import requests
import textwrap
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from dotenv import load_dotenv


load_dotenv()

FB_TOKEN = os.getenv("FACEBOOK_BOT_API_KEY")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
UNSPLASH_KEY = os.getenv("UPSPLASH_API_KEY")


def get_content():
    print("Fetching quote and vertical background...")

    try:
        z_url = "https://zenquotes.io/api/random"
        z_res = requests.get(z_url)
        z_data = z_res.json()[0]
        quote = z_data["q"]
        author = z_data["a"]
    except Exception as e:
        print(f"Failed to get quote: {e}")
        return None, None, None

    try:
        u_url = f"https://api.unsplash.com/photos/random?query=nature,minimalist&orientation=portrait&client_id={UNSPLASH_KEY}"
        u_res = requests.get(u_url)
        img_url = u_res.json()["urls"]["regular"]
    except Exception as e:
        print(f"Failed to get background: {e}")
        return None, None, None

    return quote, author, img_url


def create_image(quote, author, img_url):
    print("Designing your portrait post...")
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

    target_width = 1080
    target_height = 1920
    img = ImageOps.fit(img, (target_width, target_height), centering=(0.5, 0.5))

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 130))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    width, height = img.size

    try:

        quote_font = ImageFont.truetype("arialbd.ttf", 70)
        author_font = ImageFont.truetype("arial.ttf", 40)
    except:
        quote_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    lines = textwrap.wrap(quote, width=22)

    line_height = 90
    total_text_height = len(lines) * line_height
    current_h = (height - total_text_height) / 2 - 100

    for line in lines:

        bbox = draw.textbbox((0, 0), line, font=quote_font)
        w = bbox[2] - bbox[0]

        draw.text(
            ((width - w) / 2 + 3, current_h + 3),
            line,
            font=quote_font,
            fill=(0, 0, 0, 180),
        )

        draw.text(((width - w) / 2, current_h), line, font=quote_font, fill="white")
        current_h += line_height

    author_text = f"— {author.upper()} —"
    abox = draw.textbbox((0, 0), author_text, font=author_font)
    aw = abox[2] - abox[0]

    draw.line(
        [(width / 2 - 40, current_h + 50), (width / 2 + 40, current_h + 50)],
        fill="white",
        width=2,
    )

    draw.text(
        ((width - aw) / 2, current_h + 80),
        author_text,
        font=author_font,
        fill=(200, 200, 200, 255),
    )

    final_path = "final_post.jpg"
    img.convert("RGB").save(final_path, quality=98)
    return final_path


def post_to_facebook(image_path):
    print("Uploading to Facebook...")

    url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/photos"

    with open(image_path, "rb") as f:
        files = {"source": f}
        payload = {
            "caption": "Today's Inspiration ✨ #EchoOfThought #Quotes #Mindset",
            "access_token": FB_TOKEN,
        }
        r = requests.post(url, data=payload, files=files)

    result = r.json()
    if "id" in result:
        print(f" Success! Post ID: {result['id']}")
    else:
        print(" Failed:", result)


if __name__ == "__main__":
    quote, author, img_url = get_content()

    if quote and img_url:
        path = create_image(quote, author, img_url)
        post_to_facebook(path)
    else:
        print(" Script stopped: Error fetching content.")
