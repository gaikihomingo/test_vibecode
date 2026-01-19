#!/bin/bash

# Script to push code to GitHub and prepare for Netlify deployment

echo "🚀 Travel Itinerary Optimizer - GitHub Push Script"
echo "=================================================="
echo ""

# Check if remote exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "✅ Git remote 'origin' already exists:"
    git remote -v
    echo ""
    read -p "Do you want to use this remote? (y/n): " use_existing
    if [ "$use_existing" != "y" ]; then
        echo "Please remove the existing remote first:"
        echo "  git remote remove origin"
        exit 1
    fi
else
    echo "📝 No Git remote found. You need to create a GitHub repository first."
    echo ""
    echo "Steps:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository (don't initialize with README)"
    echo "3. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL: " repo_url
    
    if [ -z "$repo_url" ]; then
        echo "❌ No URL provided. Exiting."
        exit 1
    fi
    
    git remote add origin "$repo_url"
    echo "✅ Added remote: $repo_url"
fi

echo ""
echo "📤 Pushing to GitHub..."
echo ""

# Ensure we're on main branch
git branch -M main

# Push to GitHub
if git push -u origin main; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Next Steps:"
    echo "1. Go to https://app.netlify.com"
    echo "2. Click 'Add new site' → 'Import an existing project'"
    echo "3. Connect your GitHub account"
    echo "4. Select your repository"
    echo "5. Configure:"
    echo "   - Publish directory: public"
    echo "   - Functions directory: netlify/functions"
    echo "6. Click 'Deploy site'"
    echo ""
    echo "📖 See DEPLOY_NOW.md for detailed instructions"
else
    echo ""
    echo "❌ Failed to push. Please check:"
    echo "   - Your GitHub repository exists"
    echo "   - You have push access"
    echo "   - Your internet connection"
    exit 1
fi
