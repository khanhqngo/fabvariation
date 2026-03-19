# FabVariation Deployment Guide

Complete guide for deploying FabVariation to production environments.

## Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - Free & Easy)

**Best for**: Public demos, portfolio projects, team collaboration

**Steps**:

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - FabVariation SPC tool"
   git branch -M main
   ```

2. **Push to GitHub**
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/fabvariation.git
   git push -u origin main
   ```

3. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/fabvariation`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

4. **Your App is Live!**
   - URL: `https://YOUR_APP_NAME.streamlit.app`
   - Auto-deploys on every git push
   - Free SSL certificate included
   - Automatic dependency installation

**Deployment Time**: 2-3 minutes

**Cost**: FREE (Community Cloud tier)

---

### Option 2: Local Server / Production Server

**Best for**: Internal fab deployment, on-premises requirements

#### Linux/Ubuntu Server

1. **Install Python 3.11+**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/fabvariation.git
   cd fabvariation
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run as Service** (systemd)

   Create `/etc/systemd/system/fabvariation.service`:

   ```ini
   [Unit]
   Description=FabVariation Streamlit App
   After=network.target

   [Service]
   Type=simple
   User=YOUR_USER
   WorkingDirectory=/path/to/fabvariation
   Environment="PATH=/path/to/fabvariation/venv/bin"
   ExecStart=/path/to/fabvariation/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable fabvariation
   sudo systemctl start fabvariation
   ```

6. **Configure Nginx (Optional)**

   `/etc/nginx/sites-available/fabvariation`:

   ```nginx
   server {
       listen 80;
       server_name fabvariation.yourcompany.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/fabvariation /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

### Option 3: Docker Container

**Best for**: Containerized environments, Kubernetes, cloud platforms

#### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run

```bash
# Build image
docker build -t fabvariation:latest .

# Run container
docker run -d -p 8501:8501 --name fabvariation fabvariation:latest

# Check logs
docker logs fabvariation

# Stop container
docker stop fabvariation
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  fabvariation:
    build: .
    ports:
      - "8501:8501"
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
    volumes:
      - ./exports:/app/exports
```

Run:
```bash
docker-compose up -d
```

---

### Option 4: Cloud Platforms

#### AWS EC2

1. Launch Ubuntu 22.04 instance (t2.medium recommended)
2. Follow "Local Server" instructions above
3. Configure security group: Allow inbound on port 8501
4. Access via: `http://EC2_PUBLIC_IP:8501`

#### Google Cloud Run

1. Create `Dockerfile` (see Docker section)
2. Build and push:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/fabvariation
   ```
3. Deploy:
   ```bash
   gcloud run deploy fabvariation \
     --image gcr.io/PROJECT_ID/fabvariation \
     --platform managed \
     --port 8501
   ```

#### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name fabvariation \
  --image fabvariation:latest \
  --dns-name-label fabvariation-demo \
  --ports 8501
```

---

## Pre-Deployment Checklist

### Code Review
- [ ] All Python files pass syntax check
- [ ] No sensitive data (API keys, passwords) in code
- [ ] Comments are professional and helpful
- [ ] No debug print statements or test code

### Configuration
- [ ] `.gitignore` includes `.env` and secrets
- [ ] `.streamlit/config.toml` has correct theme settings
- [ ] `requirements.txt` lists all dependencies with versions
- [ ] No local file paths in code

### Testing
- [ ] Run `python test_imports.py` - all packages installed
- [ ] Test locally: `streamlit run app.py` works
- [ ] Test all 5 process presets load correctly
- [ ] Test all 4 drift scenarios generate data
- [ ] Test all 4 chart types display properly
- [ ] Test "Inject Defect" button works
- [ ] Test "Export PDF" generates valid PDF
- [ ] Test "Save Log" downloads CSV
- [ ] Test violation detection with sudden spike scenario
- [ ] Test email alert appears when violations detected

### Documentation
- [ ] README.md is complete and accurate
- [ ] QUICKSTART.md has clear 5-minute guide
- [ ] All code files have header comments
- [ ] FILE_STRUCTURE.md describes all files

### Performance
- [ ] Test with 100 batches (maximum)
- [ ] PDF export completes in <5 seconds
- [ ] Chart rendering is smooth
- [ ] No memory leaks after extended use

---

## Post-Deployment Verification

### Smoke Tests

1. **Access Test**
   - Navigate to deployed URL
   - App loads within 5 seconds
   - Dark theme applied correctly

2. **Functionality Test**
   - Generate simulation (Plasma Etch Rate, 30 batches, stable)
   - Verify control chart displays
   - Check metrics show: mean, std, violations, cost

3. **Interaction Test**
   - Change to "Gradual Shift" drift scenario
   - Click "Refresh Chart"
   - Verify violations detected after batch 15

4. **Export Test**
   - Click "Export PDF"
   - Download completes successfully
   - PDF opens and displays charts correctly

5. **Mobile Test** (if public)
   - Access from mobile browser
   - UI is responsive
   - Buttons are clickable
   - Charts zoom/pan properly

---

## Monitoring & Maintenance

### Health Checks

**Streamlit Health Endpoint**:
```bash
curl http://YOUR_URL/_stcore/health
```

Expected response: `{"status": "ok"}`

### Log Monitoring

**Local deployment**:
```bash
tail -f /var/log/fabvariation/app.log
```

**Docker**:
```bash
docker logs -f fabvariation
```

**Streamlit Cloud**:
- View logs in Streamlit Cloud dashboard
- Set up email alerts for errors

### Performance Metrics

Monitor:
- **Response time**: Should be <2s for chart generation
- **Memory usage**: ~200-500 MB typical
- **CPU usage**: <50% average
- **Disk usage**: <100 MB for app code

### Backup Strategy

**What to backup**:
- Source code (git repository)
- Configuration files (`.streamlit/config.toml`)
- Exported reports (if storing on server)
- User simulation logs (if persisting)

**Not needed**:
- Python cache (`__pycache__`)
- Virtual environments (`venv/`)
- Temporary files

---

## Security Considerations

### Production Hardening

1. **Network Security**
   - Use HTTPS (SSL/TLS)
   - Configure firewall rules
   - Restrict access by IP if internal only

2. **Application Security**
   - No sensitive data in session state
   - Validate all user inputs
   - Sanitize file uploads (if added)
   - Keep dependencies updated

3. **Access Control** (if needed)
   - Add authentication (Streamlit supports)
   - Implement user roles
   - Audit logs for compliance

### Updates

**Regular maintenance**:
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip install safety
safety check

# Update Streamlit
pip install --upgrade streamlit
```

---

## Troubleshooting Deployment Issues

### Issue: App won't start on Streamlit Cloud

**Symptom**: Deployment fails with "ModuleNotFoundError"

**Solution**:
1. Check `requirements.txt` has all dependencies
2. Verify file names are correct (case-sensitive)
3. Check Python version compatibility (3.11+)
4. Look at Streamlit Cloud logs for specific error

---

### Issue: Charts not rendering after deployment

**Symptom**: Blank chart areas or "Kaleido not found" error

**Solution**:
```bash
# Add to requirements.txt
kaleido>=0.2.1

# If still failing, try:
pip install plotly --upgrade
```

---

### Issue: PDF export fails on server

**Symptom**: Error when clicking "Export PDF"

**Solution**:
1. Ensure reportlab installed: `pip install reportlab`
2. Check write permissions for `/tmp/` directory
3. Verify Pillow is installed: `pip install Pillow`
4. Test manually:
   ```python
   from reportlab.pdfgen import canvas
   c = canvas.Canvas("/tmp/test.pdf")
   c.save()
   ```

---

### Issue: Slow performance in production

**Symptom**: Chart generation takes >5 seconds

**Solutions**:
1. Reduce default batch count to 30
2. Optimize DataFrame operations
3. Add caching with `@st.cache_data`
4. Increase server resources (RAM, CPU)
5. Use `plotly.graph_objects` optimization

---

## Scaling Considerations

### For Large Organizations

**Multi-User Support**:
- Deploy on cloud platform with auto-scaling
- Use load balancer for multiple instances
- Implement session persistence
- Consider Streamlit for Teams ($250/mo)

**Data Persistence**:
- Add database backend (PostgreSQL, MongoDB)
- Store simulation history
- Enable multi-user analysis
- Track usage metrics

**Integration**:
- Connect to MES/LIMS systems
- Real-time data feeds from equipment
- Automated report generation
- Email/Slack notifications

---

## Cost Estimates

| Deployment Option | Monthly Cost | Best For |
|-------------------|--------------|----------|
| Streamlit Community Cloud | FREE | Demos, portfolios |
| AWS EC2 t2.medium | $30-40 | Small teams |
| Google Cloud Run | $10-30 | Variable traffic |
| Azure Container | $25-50 | Enterprise integration |
| Streamlit for Teams | $250+ | Professional teams |
| On-premises server | $0 (hardware cost) | Sensitive data |

---

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Deployment Guide**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io
- **GitHub Issues**: [Your repository]/issues

---

## Update Policy

**Recommended update schedule**:
- **Security patches**: Immediately
- **Dependency updates**: Monthly
- **Feature updates**: Quarterly
- **Python version**: Every 6-12 months

---

**Ready to deploy?** Start with Streamlit Community Cloud for the easiest 2-minute deployment!
