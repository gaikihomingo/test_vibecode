# Troubleshooting Guide

## Error: "JSON.parse: unexpected character at line 1 column 1"

This error means the server returned HTML (like an error page) instead of JSON.

### Common Causes & Solutions:

#### 1. **Function Not Found (404 Error)**
**Symptom**: Getting HTML 404 page instead of JSON

**Solution**:
- Verify the function is deployed: Check Netlify dashboard → Functions
- Ensure function file is at: `netlify/functions/optimize.py`
- Check `netlify.toml` has: `functions = "netlify/functions"`
- Redeploy your site

#### 2. **Function Import Error**
**Symptom**: Function fails to import modules

**Solution**:
- Ensure all files are in `netlify/functions/`:
  - `optimize.py`
  - `scraper.py`
  - `optimizer.py`
  - `config.py`
  - `requirements.txt`
- Check function logs in Netlify dashboard

#### 3. **Function Timeout**
**Symptom**: Function takes too long (>10 seconds on free tier)

**Solution**:
- The mock data should be fast, but if timing out:
  - Check Netlify function logs
  - Reduce number of websites in `config.py`
  - Optimize the scraping logic

#### 4. **Testing Locally**
**Symptom**: Error when testing on localhost

**Solution**:
- Use Flask app for local testing: `python app.py`
- Or use Netlify Dev: `netlify dev` (requires Node.js 18+)

#### 5. **CORS Issues**
**Symptom**: CORS errors in browser console

**Solution**:
- Already configured in `netlify.toml` and function
- Check browser console for specific CORS error

### Debugging Steps:

1. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Check Network tab for the API call
   - Look at the Response tab to see what was actually returned

2. **Check Netlify Function Logs**:
   - Go to Netlify dashboard
   - Site settings → Functions → View logs
   - Look for error messages

3. **Test Function Directly**:
   ```bash
   curl -X POST https://your-site.netlify.app/.netlify/functions/optimize \
     -H "Content-Type: application/json" \
     -d '{"origin":"New York","destination":"Paris","departure_date":"2024-02-20","return_date":"2024-02-27","travelers":2}'
   ```

4. **Check Function Response**:
   - The improved error handling will show the actual error
   - Check browser console for detailed error messages

### Quick Fixes:

**If function returns HTML instead of JSON:**
1. Check Netlify dashboard → Functions → Is the function listed?
2. Check function logs for import errors
3. Verify all Python files are in `netlify/functions/`
4. Redeploy the site

**If testing locally:**
- Use `python app.py` and visit `http://localhost:5000`
- The Flask app handles local development better

**If on Netlify:**
- Check function logs in Netlify dashboard
- Verify function is deployed (should see it in Functions list)
- Try redeploying
