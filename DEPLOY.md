# Deploying to Netlify

This guide will help you deploy the Travel Itinerary Optimizer to Netlify.

## Prerequisites

1. A Netlify account (sign up at https://www.netlify.com)
2. Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### Option 1: Deploy via Netlify UI (Recommended)

1. **Push your code to Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Connect to Netlify**
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Connect your Git provider and select your repository

3. **Configure Build Settings**
   - Build command: (leave empty or use `echo "No build needed"`)
   - Publish directory: `public`
   - Functions directory: `netlify/functions`

4. **Set Environment Variables** (if needed)
   - Go to Site settings → Environment variables
   - Add any required variables

5. **Deploy**
   - Click "Deploy site"
   - Netlify will automatically build and deploy your site

### Option 2: Deploy via Netlify CLI

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Initialize and Deploy**
   ```bash
   netlify init
   netlify deploy --prod
   ```

## Important Notes

### Python Runtime
- Netlify Functions support Python 3.9
- Dependencies are installed from `netlify/functions/requirements.txt`
- The function handler must be named `handler` and accept `(event, context)` parameters

### Function Timeout
- Netlify Functions have a maximum execution time of 10 seconds (free tier) or 26 seconds (paid)
- If your scraping takes longer, consider:
  - Using background jobs
  - Caching results
  - Optimizing the scraping process

### Selenium Limitation
- Selenium/ChromeDriver may not work in Netlify Functions environment
- The current implementation uses mock data, which works fine
- For real scraping, consider:
  - Using APIs instead of scraping
  - Using headless browser services (e.g., Puppeteer on a separate service)
  - Moving scraping to a separate backend service

### File Structure
```
.
├── public/              # Static files (HTML, CSS, JS)
│   └── index.html
├── netlify/
│   └── functions/
│       ├── optimize.py  # Serverless function
│       └── requirements.txt
├── scraper.py
├── optimizer.py
├── config.py
└── netlify.toml         # Netlify configuration
```

## Testing Locally

You can test the Netlify function locally using Netlify Dev:

```bash
npm install -g netlify-cli
netlify dev
```

This will:
- Start a local server
- Serve static files from `public/`
- Run functions locally
- Simulate the Netlify environment

## Troubleshooting

### Function Timeout
If you see timeout errors:
- Reduce the number of websites being scraped
- Add caching for repeated requests
- Optimize the scraping logic

### Import Errors
If you see import errors:
- Ensure all dependencies are in `netlify/functions/requirements.txt`
- Check that file paths are correct (functions run from their own directory)

### CORS Issues
- CORS headers are configured in `netlify.toml`
- The function also sets CORS headers in the response

## Custom Domain

After deployment:
1. Go to Site settings → Domain management
2. Add your custom domain
3. Follow Netlify's DNS configuration instructions

## Continuous Deployment

Netlify automatically deploys when you push to your connected branch:
- Push to `main` → Production deployment
- Create a pull request → Preview deployment
