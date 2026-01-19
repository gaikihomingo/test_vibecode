# How to Redeploy on Netlify

## 🚀 Quick Redeploy Methods

### Method 1: Automatic Redeploy (Recommended)
If your Netlify site is connected to GitHub/GitLab/Bitbucket, it will **automatically redeploy** when you push changes.

1. **Push your changes to Git:**
   ```bash
   git push origin main
   ```
   (or `git push` if already set up)

2. **Netlify will automatically:**
   - Detect the push
   - Start a new deployment
   - Build and deploy your site
   - Update your live site

3. **Check deployment status:**
   - Go to your Netlify dashboard
   - Click on your site
   - Go to "Deploys" tab
   - You'll see the new deployment in progress

### Method 2: Manual Redeploy via Dashboard

1. **Go to Netlify Dashboard:**
   - Visit https://app.netlify.com
   - Click on your site

2. **Trigger Redeploy:**
   - Go to "Deploys" tab
   - Click "Trigger deploy" button (top right)
   - Select "Clear cache and deploy site"
   - Wait 2-3 minutes

### Method 3: Redeploy via Netlify CLI

If you have Netlify CLI installed:

```bash
# Login (if not already)
netlify login

# Deploy
netlify deploy --prod
```

## 📋 Step-by-Step: Push Changes and Auto-Redeploy

### Step 1: Check Your Changes
```bash
git status
```

### Step 2: Add and Commit (if needed)
```bash
git add .
git commit -m "Your commit message"
```

### Step 3: Push to GitHub
```bash
git push origin main
```

### Step 4: Monitor Deployment
1. Go to https://app.netlify.com
2. Click on your site
3. Watch the "Deploys" tab
4. Wait for "Published" status (green checkmark)

## ✅ Verify Deployment

1. **Check Site URL:**
   - Visit your Netlify site URL
   - Test the functionality

2. **Check Function Logs:**
   - Site settings → Functions → View logs
   - Look for any errors

3. **Check Build Logs:**
   - Deploys tab → Click on latest deploy
   - View build log for any issues

## 🔍 Troubleshooting

### If Auto-Deploy Doesn't Work:

1. **Check Git Connection:**
   - Site settings → Build & deploy
   - Verify "Continuous Deployment" is enabled
   - Check connected repository

2. **Check Build Settings:**
   - Publish directory: `public`
   - Functions directory: `netlify/functions`
   - Build command: (empty or `echo "No build needed"`)

3. **Manual Trigger:**
   - Use Method 2 above to manually trigger

### If Deployment Fails:

1. **Check Build Logs:**
   - Deploys tab → Failed deploy → View build log
   - Look for error messages

2. **Common Issues:**
   - Missing files in `netlify/functions/`
   - Python import errors
   - Missing dependencies in `requirements.txt`

## 🎯 Quick Commands Summary

```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Fix JSON parsing error"

# Push to trigger auto-deploy
git push origin main

# Or if using different branch
git push origin <branch-name>
```

## 📝 Notes

- **Auto-deploy is enabled by default** when you connect a Git repository
- Deployments usually take **2-3 minutes**
- You can see deployment progress in real-time in the dashboard
- Each deployment gets a unique URL for preview
- Production URL updates automatically when deployment succeeds
