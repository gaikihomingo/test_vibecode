# 🚀 Deploy to Netlify - Step by Step

Your code is committed and ready! Follow these steps:

## Step 1: Push to GitHub

### Option A: Create New GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (name it `travel-itinerary-optimizer` or any name you like)
3. **DO NOT** initialize with README, .gitignore, or license
4. Copy the repository URL (e.g., `https://github.com/yourusername/travel-itinerary-optimizer.git`)

### Option B: Use Existing Repository

If you already have a GitHub repo, use its URL.

### Step 2: Push Your Code

Run these commands (replace with your actual repo URL):

```bash
cd /Users/amitgaiki/flam/code/test_transcriber
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Netlify

### Via Netlify Dashboard (Easiest - No CLI needed!)

1. **Go to Netlify**: https://app.netlify.com
   - Sign up or log in (free account works)

2. **Import Your Site**:
   - Click "Add new site" → "Import an existing project"
   - Click "Deploy with GitHub" (or GitLab/Bitbucket)
   - Authorize Netlify to access your GitHub account
   - Select your repository: `travel-itinerary-optimizer`

3. **Configure Build Settings**:
   - **Build command**: (leave empty or use: `echo "No build needed"`)
   - **Publish directory**: `public`
   - **Functions directory**: `netlify/functions`
   
   Click "Show advanced" if you don't see these options.

4. **Deploy**:
   - Click "Deploy site"
   - Wait 2-3 minutes for deployment
   - Your site will be live at: `https://random-name-123.netlify.app`

## Step 4: Test Your Site

Once deployed, visit your Netlify URL and test the itinerary optimizer!

## ✅ What's Already Configured

- ✅ Git repository initialized
- ✅ All files committed
- ✅ Netlify configuration (`netlify.toml`)
- ✅ Serverless function (`netlify/functions/optimize.py`)
- ✅ Static files in `public/`
- ✅ CORS headers configured
- ✅ SPA routing configured

## 🎉 You're Done!

Your Travel Itinerary Optimizer is now live on Netlify!

## 📝 Next Steps (Optional)

- Add a custom domain in Netlify settings
- Set up environment variables if needed
- Enable continuous deployment (automatic on every git push)

## 🐛 Troubleshooting

**Build fails?**
- Check that `publish directory` is set to `public`
- Check that `functions directory` is set to `netlify/functions`

**Function not working?**
- Check function logs in Netlify dashboard
- Verify all Python files are in `netlify/functions/`
- Check `netlify/functions/requirements.txt` has all dependencies

**Need help?**
- Check Netlify logs: Site settings → Functions → View logs
- Check build logs: Deploys → Click on a deploy → View build log
