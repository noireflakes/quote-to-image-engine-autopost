# 🎨 Quote to Image Engine (Echo of Thought)

An automated Python bot that fetches inspirational quotes, pairs them with minimalist nature backgrounds, and posts high-quality portrait designs to Facebook 3 times a day.

## ✨ Features

- **Portrait Mode:** Automatically crops images to 1080x1920 (9:16) for social media
- **Smart Typography:** Adds text shadows and decorative accents to ensure quotes are readable on any background
- **Fully Automated:** Runs via GitHub Actions on a schedule (6 AM, 1 PM, 6 PM PHT)
- **Randomized Content:** Pulls fresh quotes from ZenQuotes and beautiful backgrounds from Unsplash
- **High-Quality Design:** Professional-looking quote graphics with elegant formatting

## 🚀 Setup & Installation

### 1. Prerequisites

- Python 3.9+
- A Meta Developer App (for Facebook Page API)
- An Unsplash Developer Account
- GitHub account (for automated scheduling)

### 2. Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/noireflakes/quote-to-image-engine-autopost.git
   cd quote-to-image-engine-autopost
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (create a `.env` file):
   ```
   UNSPLASH_ACCESS_KEY=your_unsplash_access_key
   FB_PAGE_ACCESS_TOKEN=your_facebook_page_access_token
   FB_PAGE_ID=your_facebook_page_id
   ```

### 3. API Setup

#### Unsplash API
1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Create a new application
3. Copy your Access Key and add it to your `.env` file

#### Facebook Page API
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app or use an existing one
3. Add the Facebook Page API product
4. Generate a Page Access Token with `pages_manage_posts` and `pages_read_engagement` permissions
5. Get your Page ID from your Facebook Page settings
6. Add both to your `.env` file

### 4. GitHub Actions Setup (for automation)

1. Go to your repository's Settings > Secrets and variables > Actions
2. Add the following repository secrets:
   - `UNSPLASH_ACCESS_KEY`
   - `FB_PAGE_ACCESS_TOKEN`
   - `FB_PAGE_ID`

3. The workflow will automatically run at:
   - 6:00 AM PHT (22:00 UTC previous day)
   - 1:00 PM PHT (05:00 UTC)
   - 6:00 PM PHT (10:00 UTC)

## 📝 Usage

### Run Manually
```bash
python main.py
```

### Automated Posting
Once GitHub Actions is configured, the bot will automatically:
1. Fetch a random inspirational quote
2. Download a beautiful nature background from Unsplash
3. Create a portrait-oriented (1080x1920) image with the quote
4. Post the image to your Facebook Page

## 🎨 Customization

You can customize various aspects of the design by modifying `main.py`:

- **Image dimensions:** Change the `portrait_width` and `portrait_height` variables
- **Font styling:** Modify font sizes, colors, and shadows
- **Background categories:** Adjust Unsplash search queries (e.g., "nature", "minimal", "sky")
- **Posting schedule:** Edit the cron schedule in `.github/workflows/autopost.yml`
- **Text positioning:** Adjust vertical centering and padding values

## 🛠️ Tech Stack

- **Python 3.9+**
- **Pillow (PIL):** Image processing and text rendering
- **Requests:** API calls to ZenQuotes and Unsplash
- **Facebook Graph API:** Posting to Facebook Pages
- **GitHub Actions:** Automated scheduling

## 📂 Project Structure

```
quote-to-image-engine-autopost/
│
├── .github/
│   └── workflows/
│       └── autopost.yml          # GitHub Actions workflow
│
├── main.py                       # Main bot script
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
├── .env                         # Environment variables (not committed)
└── README.md                    # This file
```

## 🔒 Security Notes

- Never commit your `.env` file or expose your API keys
- Use GitHub Secrets for all sensitive credentials
- Regularly rotate your Facebook Page Access Token
- Keep your dependencies updated for security patches

## 🐛 Troubleshooting

### Common Issues

**Issue:** Images not posting to Facebook
- Check that your Page Access Token has the correct permissions
- Verify your Page ID is correct
- Ensure the token hasn't expired

**Issue:** Unsplash API errors
- Verify your Access Key is valid
- Check you haven't exceeded Unsplash's rate limits (50 requests/hour for free tier)

**Issue:** GitHub Actions not running
- Verify your secrets are correctly set in repository settings
- Check the Actions tab for error logs
- Ensure the workflow file syntax is correct

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/noireflakes/quote-to-image-engine-autopost/issues).

## 👤 Author

**noireflakes**
- GitHub: [@noireflakes](https://github.com/noireflakes)

## 🌟 Acknowledgments

- [ZenQuotes API](https://zenquotes.io/) for inspirational quotes
- [Unsplash](https://unsplash.com/) for beautiful background images
- [Meta for Developers](https://developers.facebook.com/) for Facebook API

---

Made with ❤️ for spreading daily inspiration
