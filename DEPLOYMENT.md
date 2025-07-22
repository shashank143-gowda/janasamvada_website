# 🚀 JanSamvaad Deployment Guide

This guide will help you deploy JanSamvaad with GitHub Pages serving the landing page and a separate backend service.

## 📋 Prerequisites

- GitHub account
- Git installed on your local machine
- Python 3.8+ (for local development)
- Heroku CLI or Railway CLI (for backend deployment)

## 🌐 GitHub Pages Setup (Frontend)

### Step 1: Fork or Upload Repository

1. **Fork this repository** or create a new repository
2. **Upload all files** to your GitHub repository
3. **Ensure the following files are in the root directory**:
   - `index.html` (main landing page)
   - `manifest.json` (PWA manifest)
   - `sw.js` (service worker)
   - `_config.yml` (Jekyll configuration)
   - `README.md`
   - `CNAME` (if using custom domain)

### Step 2: Configure Repository Settings

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions** or **Deploy from a branch**
4. If using branch deployment, select **main/master branch**
5. Click **Save**

### Step 3: Update Configuration

Update the following files with your information:

#### `index.html`
Replace all instances of:
- `https://jansamvaad-backend.herokuapp.com` → Your backend URL
- `yourusername` → Your GitHub username

#### `_config.yml`
```yaml
url: "https://yourusername.github.io"
baseurl: "/your-repo-name"
```

#### `README.md`
- Update all GitHub URLs
- Replace demo links with your actual URLs

### Step 4: Custom Domain (Optional)

If you have a custom domain:

1. **Update `CNAME` file**:
   ```
   yourdomain.com
   ```

2. **Configure DNS** with your domain provider:
   ```
   Type: CNAME
   Name: @
   Value: yourusername.github.io
   ```

## 🖥️ Backend Deployment Options

### Option 1: Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   cd c:/srushack
   heroku login
   heroku create jansamvaad-backend
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DATABASE_URL=postgres://...
   heroku config:set DHVANI_API_KEY=your-dhvani-api-key
   ```

4. **Create Procfile**
   ```bash
   echo "web: python run.py" > Procfile
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 2: Railway Deployment

1. **Sign up at Railway.app**
2. **Connect GitHub repository**
3. **Deploy with one click**
4. **Set environment variables** in Railway dashboard

### Option 3: PythonAnywhere

1. **Upload files** to PythonAnywhere
2. **Create web app** with Flask
3. **Configure WSGI file**
4. **Set environment variables**

## 🔧 Environment Variables

Set these environment variables in your backend deployment:

```bash
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://... # Or sqlite:///app.db for development
DHVANI_API_KEY=your-dhvani-api-key
FLASK_ENV=production
```

## 📱 PWA Configuration

The app is configured as a Progressive Web App (PWA):

1. **Manifest file** (`manifest.json`) defines app metadata
2. **Service worker** (`sw.js`) enables offline functionality
3. **Users can install** the app on mobile devices

## 🔗 URL Structure After Deployment

### GitHub Pages (Frontend)
- **Landing Page**: `https://yourusername.github.io/jansamvaad/`
- **Static Assets**: Served by GitHub Pages CDN

### Backend Service
- **API Base**: `https://jansamvaad-backend.herokuapp.com/`
- **Main App**: `https://jansamvaad-backend.herokuapp.com/app/`
- **Services**: `https://jansamvaad-backend.herokuapp.com/services/`
- **API Endpoints**: `https://jansamvaad-backend.herokuapp.com/api/`

## 🧪 Testing Your Deployment

### Frontend Testing
1. Visit your GitHub Pages URL
2. Check responsive design on mobile
3. Test PWA installation
4. Verify service worker caching

### Backend Testing
```bash
# Health check
curl https://your-backend-url.herokuapp.com/app/

# API test
curl https://your-backend-url.herokuapp.com/api/stats
```

### Integration Testing
1. Click all buttons in the landing page
2. Verify they redirect to correct backend URLs
3. Test form submissions
4. Check mobile responsiveness

## 🔒 Security Considerations

### Production Settings
1. **Use HTTPS** for all connections
2. **Set secure headers** in Flask app
3. **Configure CORS** properly
4. **Use environment variables** for secrets
5. **Enable rate limiting**

### Flask Security Headers
Add to your Flask app:
```python
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=True)
```

## 📊 Monitoring & Analytics

### Setup Google Analytics
1. **Get tracking ID** from Google Analytics
2. **Update `index.html`**:
   ```javascript
   gtag('config', 'GA_TRACKING_ID');
   ```

### Performance Monitoring
- Use **Heroku metrics** for backend monitoring
- Use **GitHub Pages insights** for traffic
- Set up **error tracking** (e.g., Sentry)

## 🚨 Troubleshooting

### Common Issues

#### GitHub Pages not updating
- Check **Actions** tab for deployment status
- Clear browser cache and try incognito mode
- Verify file names and paths

#### Backend connection errors
- Check environment variables
- Verify database connection
- Check Heroku logs: `heroku logs --tail`

#### CORS issues
```python
from flask_cors import CORS
CORS(app, origins=['https://yourusername.github.io'])
```

#### SSL/HTTPS issues
- Ensure both frontend and backend use HTTPS
- Update all URLs to use HTTPS
- Check mixed content warnings

### Debug Commands

```bash
# Check Heroku logs
heroku logs --tail --app jansamvaad-backend

# Check GitHub Actions
# Go to Actions tab in your repository

# Test local deployment
python run.py
# Visit http://localhost:5000
```

## 🔄 Continuous Deployment

### GitHub Actions (Automated)
The included `.github/workflows/deploy.yml` automatically:
1. **Builds** the frontend on every push
2. **Optimizes** files for production
3. **Deploys** to GitHub Pages

### Manual Deployment
```bash
# Update frontend
git add .
git commit -m "Update frontend"
git push origin main

# Update backend (if using Heroku)
git push heroku main
```

## 📈 Scaling Considerations

### Frontend Scaling
- GitHub Pages handles **high traffic** automatically
- Use **CDN** for additional performance
- Implement **progressive loading**

### Backend Scaling
- Use **Heroku dynos** for scaling
- Implement **database connection pooling**
- Add **Redis caching**
- Consider **microservices architecture**

## 🎯 Go-Live Checklist

- [ ] Frontend deployed to GitHub Pages
- [ ] Backend deployed to cloud service
- [ ] All URLs updated and working
- [ ] SSL certificates configured
- [ ] Environment variables set
- [ ] Database initialized
- [ ] Analytics configured
- [ ] Error monitoring set up
- [ ] Performance testing completed
- [ ] Mobile testing done
- [ ] SEO optimization checked
- [ ] Accessibility audit passed

## 📞 Support

If you need help with deployment:

1. **Check Issues**: Look at existing GitHub issues
2. **Create Issue**: Open a new issue with details
3. **Community**: Join our Discord/Telegram group
4. **Email**: contact@jansamvaad.gov.in

---

**🎉 Congratulations! Your JanSamvaad platform is now live and ready to empower rural communities!**