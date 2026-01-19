# Quick Start - Deploy to Netlify

## 🚀 Fastest Way to Deploy

### 1. Push to Git
```bash
git init
git add .
git commit -m "Ready for Netlify deployment"
git remote add origin <your-git-repo-url>
git push -u origin main
```

### 2. Deploy on Netlify

**Option A: Via Netlify Dashboard (Easiest)**
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Connect your Git provider (GitHub/GitLab/Bitbucket)
4. Select your repository
5. Configure:
   - **Build command:** (leave empty)
   - **Publish directory:** `public`
   - **Functions directory:** `netlify/functions`
6. Click "Deploy site"

**Option B: Via Netlify CLI**
```bash
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --prod
```

### 3. Test Your Deployment

Once deployed, visit your Netlify URL and test the itinerary optimizer!

## 📁 Project Structure for Netlify

```
.
├── public/                    # Static files served by Netlify
│   └── index.html            # Main web interface
├── netlify/
│   └── functions/
│       ├── optimize.py       # Serverless function
│       ├── requirements.txt  # Python dependencies
│       ├── scraper.py        # Copied modules
│       ├── optimizer.py      # Copied modules
│       └── config.py         # Copied modules
├── netlify.toml              # Netlify configuration
└── _redirects                # SPA routing rules
```

## ⚠️ Important Notes

1. **Function Timeout**: Netlify Functions have a 10-second timeout on free tier. The current mock data implementation should work fine, but real scraping might need optimization.

2. **Selenium Limitation**: Selenium won't work in Netlify Functions. The app currently uses mock data which is perfect for demonstration.

3. **Dependencies**: All Python dependencies must be in `netlify/functions/requirements.txt`

4. **CORS**: Already configured in `netlify.toml` and the function handler

## 🔧 Testing Locally

Test the Netlify setup locally:
```bash
npm install -g netlify-cli
netlify dev
```

This will:
- Serve static files from `public/`
- Run functions locally
- Simulate the Netlify environment

## 📝 Next Steps

After deployment:
- Add a custom domain in Netlify settings
- Set up environment variables if needed
- Monitor function logs in Netlify dashboard
- Enable continuous deployment from your Git repo

## 🐛 Troubleshooting

**Function not found?**
- Check that `netlify/functions/optimize.py` exists
- Verify `netlify.toml` has correct functions directory

**Import errors?**
- Ensure `scraper.py`, `optimizer.py`, and `config.py` are in `netlify/functions/`
- Check `requirements.txt` has all dependencies

**Timeout errors?**
- Reduce number of websites being scraped
- Add caching for repeated requests
- Optimize the scraping logic
