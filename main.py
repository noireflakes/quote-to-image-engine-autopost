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
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
UNSPLASH_KEY = os.getenv("UNSPLASH_API_KEY")


def get_content():

    try:
        z_url = "https://zenquotes.io/api/random"
        z_res = requests.get(z_url)
        z_data = z_res.json()[0]
        quote = z_data["q"]
        author = z_data["a"]

    except Exception as e:

        return None, None, None

    try:
        u_url = f"https://api.unsplash.com/photos/random?query=nature,minimalist&orientation=portrait&client_id={UNSPLASH_KEY}"
        u_res = requests.get(u_url)
        img_url = u_res.json()["urls"]["regular"]

    except Exception as e:

        return None, None, None

    return quote, author, img_url


def get_multiple_contents(count=3):

    contents = []

    for i in range(count):
        print(f"\n  Content {i+1}/{count}:")
        quote, author, img_url = get_content()
        if quote and img_url:
            contents.append((quote, author, img_url))
        else:
            print(f"    ✗ Failed to get content {i+1}")

    return contents


def create_image(quote, author, img_url, filename="final_post.jpg"):

    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

    target_width = 1080
    target_height = 1920
    img = ImageOps.fit(img, (target_width, target_height), centering=(0.5, 0.5))

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 180))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    width, height = img.size

    quote_font = None
    author_font = None

    font_paths = [
        # Windows fonts
        ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"),
        ("C:/Windows/Fonts/calibrib.ttf", "C:/Windows/Fonts/calibri.ttf"),
        # Linux fonts
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ),
        (
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ),
        # Mac fonts
        ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Helvetica.ttc"),
    ]

    for bold_path, regular_path in font_paths:
        try:
            quote_font = ImageFont.truetype(bold_path, 65)
            author_font = ImageFont.truetype(regular_path, 38)
            break
        except:
            continue

    if quote_font is None:
        try:
            quote_font = ImageFont.truetype("arial.ttf", 65)
            author_font = ImageFont.truetype("arial.ttf", 38)
        except:
            quote_font = ImageFont.load_default()
            author_font = ImageFont.load_default()

    lines = textwrap.wrap(quote, width=20)

    line_height = 85
    total_text_height = len(lines) * line_height
    current_h = (height - total_text_height) / 2 - 50

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        w = bbox[2] - bbox[0]

        draw.text(
            ((width - w) / 2 + 4, current_h + 4),
            line,
            font=quote_font,
            fill=(0, 0, 0, 200),
        )

        draw.text(((width - w) / 2, current_h), line, font=quote_font, fill="white")
        current_h += line_height

    current_h += 30

    line_length = 60
    draw.line(
        [(width / 2 - line_length, current_h), (width / 2 + line_length, current_h)],
        fill="white",
        width=3,
    )

    current_h += 20
    author_text = f"— {author.upper()} —"
    abox = draw.textbbox((0, 0), author_text, font=author_font)
    aw = abox[2] - abox[0]

    draw.text(
        ((width - aw) / 2 + 2, current_h + 2),
        author_text,
        font=author_font,
        fill=(0, 0, 0, 180),
    )

    draw.text(
        ((width - aw) / 2, current_h),
        author_text,
        font=author_font,
        fill=(220, 220, 220, 255),
    )

    img.convert("RGB").save(filename, quality=95)

    return filename


def post_to_facebook(image_path, author):

    url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/photos"

    with open(image_path, "rb") as f:
        files = {"source": f}
        payload = {
            "caption": f"Today's Inspiration By {author} #EchoOfThought #Quotes #Mindset",
            "access_token": FB_TOKEN,
        }
        r = requests.post(url, data=payload, files=files)

    result = r.json()
    if "id" in result:
        print(f"✓ Facebook Success! Post ID: {result['id']}")
        return True
    else:
        print(f"✗ Facebook Failed: {result}")
        return False


def post_to_instagram_carousel(image_paths, authors):

    if not INSTAGRAM_ACCOUNT_ID:
        print("✗ Instagram Account ID not found in .env file")
        return False

    # Caption with all authors
    authors_text = ", ".join(set(authors))  # Remove duplicates
    caption = f"Today's Inspiration ✨\n\nBy: {authors_text}\n\n#EchoOfThought #Quotes #Mindset #Motivation #Inspiration #DailyQuotes"

    try:
        # Step 1: Upload all images and create item containers
        print(f"  → Step 1: Uploading {len(image_paths)} images...")
        item_ids = []

        for idx, image_path in enumerate(image_paths):
            print(f"    Image {idx+1}/{len(image_paths)}:")

            # Upload image to Facebook
            upload_url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/photos"
            with open(image_path, "rb") as f:
                files = {"source": f}
                upload_payload = {
                    "published": "false",
                    "access_token": FB_TOKEN,
                }
                upload_response = requests.post(
                    upload_url, data=upload_payload, files=files
                )

            upload_result = upload_response.json()

            if "id" not in upload_result:
                print(f" ✗ Failed to upload image {idx+1}: {upload_result}")
                return False

            photo_id = upload_result["id"]

            # Get image URL
            photo_url = f"https://graph.facebook.com/v21.0/{photo_id}?fields=images&access_token={FB_TOKEN}"
            photo_response = requests.get(photo_url)
            photo_data = photo_response.json()

            if "images" not in photo_data or len(photo_data["images"]) == 0:
                print(f"      ✗ Failed to get image URL for image {idx+1}")
                return False

            image_url = photo_data["images"][0]["source"]

            # Create carousel item container
            item_url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media"
            item_payload = {
                "image_url": image_url,
                "is_carousel_item": "true",
                "access_token": FB_TOKEN,
            }

            item_response = requests.post(item_url, data=item_payload)
            item_result = item_response.json()

            if "id" not in item_result:
                print(f"      ✗ Failed to create carousel item {idx+1}: {item_result}")
                return False

            item_ids.append(item_result["id"])
            print(f"      ✓ Item {idx+1} created: {item_result['id']}")

        # Step 2: Create carousel container with all items
        print(f"  → Step 2: Creating carousel container...")
        carousel_url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media"
        carousel_payload = {
            "media_type": "CAROUSEL",
            "children": ",".join(item_ids),
            "caption": caption,
            "access_token": FB_TOKEN,
        }

        carousel_response = requests.post(carousel_url, data=carousel_payload)
        carousel_result = carousel_response.json()

        if "id" not in carousel_result:

            return False

        creation_id = carousel_result["id"]

        time.sleep(3)

        status_url = f"https://graph.facebook.com/v21.0/{creation_id}?fields=status_code&access_token={FB_TOKEN}"
        max_retries = 15

        for i in range(max_retries):
            status_response = requests.get(status_url)
            status_result = status_response.json()
            status_code = status_result.get("status_code")

            if status_code == "FINISHED":
                print(f"    ✓ Carousel ready!")
                break
            elif status_code == "ERROR":

                return False
            else:

                time.sleep(2)

        # Step 4: Publish carousel
        print(f"  → Step 4: Publishing carousel to Instagram...")
        publish_url = (
            f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        )
        publish_payload = {
            "creation_id": creation_id,
            "access_token": FB_TOKEN,
        }

        publish_response = requests.post(publish_url, data=publish_payload)
        publish_result = publish_response.json()

        if "id" in publish_result:
            print(f"✓ Instagram Carousel Success! Post ID: {publish_result['id']}")
            return True
        else:
            print(f"✗ Instagram Publish Failed: {publish_result}")
            return False

    except Exception as e:
        print(f"✗ Error creating carousel: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Social Media Quote Poster")
    print("=" * 60)

    # Get 3 different quotes for Instagram carousel
    contents = get_multiple_contents(count=3)

    if len(contents) < 3:
        print(f"\n✗ Only got {len(contents)}/3 quotes. Need at least 3 for carousel.")
        print("  Trying to continue anyway...")
        if len(contents) == 0:
            print("✗ Script stopped: No content fetched.")
            exit(1)

    carousel_images = []
    all_authors = []

    for idx, (quote, author, img_url) in enumerate(contents):
        filename = f"carousel_{idx+1}.jpg"
        path = create_image(quote, author, img_url, filename)
        carousel_images.append(path)
        all_authors.append(author)

    # Use first image for Facebook single post
    first_quote, first_author, first_img_url = contents[0]
    fb_image = create_image(
        first_quote, first_author, first_img_url, "facebook_post.jpg"
    )

    # Post to Facebook (single image)
    fb_success = post_to_facebook(fb_image, first_author)

    # Post to Instagram (carousel)
    ig_success = post_to_instagram_carousel(carousel_images, all_authors)
