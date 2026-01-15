# 🎯 Getting Started - Visual Guide

## Step 1: Prerequisites ✓

### Windows
- [ ] Install Docker Desktop from https://www.docker.com/products/docker-desktop
- [ ] Docker will include Docker Compose automatically

### macOS  
- [ ] Install Docker Desktop from https://www.docker.com/products/docker-desktop
- [ ] Or use Homebrew: `brew install docker`

### Linux
- [ ] Install Docker: `sudo apt-get install docker.io docker-compose`
- [ ] Start service: `sudo systemctl start docker`

**Verify Installation:**
```bash
docker --version
docker-compose --version
```

---

## Step 2: Navigate to Project

### Windows (PowerShell)
```powershell
cd "c:\Users\HP\work projects\martian ai"
```

### macOS/Linux
```bash
cd ~/path/to/martian\ ai
# Or however you navigated to the project
```

---

## Step 3: Start Application

### Option A: PowerShell Script (Windows) 🟦
```powershell
.\docker-start.ps1 -Build
```

### Option B: Bash Script (macOS/Linux) 🟧
```bash
chmod +x docker-start.sh
./docker-start.sh --build
```

### Option C: Manual Docker Compose (Any OS)
```bash
docker-compose up --build
```

---

## Step 4: Wait for Startup

You'll see output like this:

```
[10:30:15] ✓ Docker found
[10:30:16] ✓ Docker Compose found  
[10:30:17] Building Docker images...
Step 1/15 : FROM python:3.11-slim...
...
[10:32:45] ✓ Build successful
[10:32:46] Starting Martian AI...
[10:33:10] martian-ai-backend    | Application startup complete
[10:33:15] martian-ai-frontend   | ▲ Next.js 18.2.0
[10:33:15] martian-ai-frontend   | - Local: http://0.0.0.0:3000
```

**Wait until you see "Listening on 0.0.0.0:3000"** (typically 2-5 minutes on first run)

---

## Step 5: Access Application

### Frontend
Open in your browser:
```
http://localhost:3000
```

You should see the Martian AI dashboard with:
- 🧠 Proof AI
- 📄 Summarizer  
- 🎤 Smart Notes
- 🎯 **Slide Generator** ← NEW!

### Backend API
```
http://localhost:8000
```

### API Documentation (Interactive)
```
http://localhost:8000/docs
```

---

## Step 6: Test Slide Generation

### Option 1: Web Interface
1. Go to http://localhost:3000
2. Click on "Slide Generator" 
3. Enter text or upload a document
4. Click "Generate"
5. Download PPTX or PDF

### Option 2: API Test (Terminal)
```bash
curl -X POST http://localhost:8000/generate-slides-from-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is transforming education. Machine learning enables personalized learning. Deep learning powers advanced language models.",
    "title": "AI in Education",
    "export_format": "pptx"
  }' \
  --output presentation.pptx
```

Then open `presentation.pptx` in PowerPoint or Google Slides.

---

## Step 7: Monitor & Debug

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 50 lines
docker-compose logs --tail=50
```

### Check Status
```bash
docker-compose ps
```

You should see:
```
NAME                    STATUS
martian-ai-backend      Up 2 minutes (healthy)
martian-ai-frontend     Up 2 minutes (healthy)
```

### Access Container
```bash
# Backend
docker exec -it martian-ai-backend bash

# Frontend  
docker exec -it martian-ai-frontend sh
```

---

## Step 8: Stop Application

### When Done
```bash
# Press Ctrl+C in terminal (if running in foreground)

# Or in new terminal
docker-compose down
```

### Full Cleanup
```bash
docker-compose down -v
```

---

## 🎯 Testing Different Inputs

### Test 1: Short Text (Academic)
```json
{
  "text": "Research methodology involves systematic investigation. Primary data collection uses surveys and interviews. Secondary data comes from existing sources. Analysis requires statistical methods.",
  "title": "Research Methods",
  "template": "academic",
  "export_format": "pptx"
}
```

### Test 2: Business Content
```json
{
  "text": "Q3 revenue increased 25% year-over-year. Market expansion reached three new regions. Customer acquisition cost decreased 15%. Quarterly profit margin improved by 2%.",
  "title": "Quarterly Report",
  "template": "business",
  "export_format": "pptx"
}
```

### Test 3: Large Document
- Use a PDF or Word document
- Upload via the web interface
- Select template
- Generate with one click

### Test 4: PDF Export
```bash
curl -X POST http://localhost:8000/generate-slides-from-text \
  -H "Content-Type: application/json" \
  -d '{"text":"Your content here","title":"Title","export_format":"pdf"}' \
  --output slides.pdf
```

---

## 📊 Understanding Output

### Generated Files

**PPTX File:**
- ✅ Editable in PowerPoint, Google Slides, LibreOffice
- ✅ Professional formatting
- ✅ Ready to present or customize
- ✅ ~200-500 KB typical size

**PDF File:**
- ✅ Print-ready
- ✅ Shareable
- ✅ View-only (or print-to-edit)
- ✅ ~300-800 KB typical size

### Presentation Structure
Every generated presentation includes:
1. **Title Slide** - With presentation title and subtitle
2. **Content Slides** - Main content with bullet points
3. **Summary Slide** - Recap with statistics

---

## 🆘 Troubleshooting

### Issue: "Port 3000 already in use"

**Solution:**
```bash
# Stop other containers
docker-compose down

# Or use different port
# Edit docker-compose.yml:
# ports:
#   - "3001:3000"  ← Change 3000 to 3001
```

### Issue: "Docker is not installed"

**Solution:** Install Docker from https://www.docker.com/get-started

### Issue: Application won't start

**Solution:**
```bash
# Check logs
docker-compose logs

# Try rebuild
docker-compose down -v
docker-compose up --build

# Check Docker status
docker system df
```

### Issue: "Can't reach http://localhost:3000"

**Solution:**
```bash
# Check containers are running
docker-compose ps

# View logs
docker-compose logs

# Restart
docker-compose restart
```

### Issue: Slow performance

**Solution:**
- Increase Docker memory in Desktop settings
- Restart Docker: `docker-compose restart`
- Check system resources: `docker stats`

---

## 💡 Pro Tips

### Tip 1: Live Logs
```bash
# Watch logs in real-time
docker-compose logs -f
```

### Tip 2: Background Startup
```bash
# Run in background
docker-compose up -d

# Check status later
docker-compose ps
```

### Tip 3: Quick Restart
```bash
docker-compose restart backend
# No need to stop/start everything
```

### Tip 4: Database Reset
```bash
# Start fresh
docker-compose down -v
docker-compose up
```

### Tip 5: Terminal Access
```bash
# Run commands in container
docker exec martian-ai-backend python -c "print('Hello')"
```

---

## 🎓 Next Steps

### 1. Explore Features
- [ ] Generate slides from text
- [ ] Upload documents (PDF/DOCX)
- [ ] Try different templates
- [ ] Export as PPTX and PDF
- [ ] Test other tools (Proof AI, Summarizer)

### 2. Customize
- [ ] Edit presentation templates
- [ ] Add custom colors
- [ ] Modify slide layouts
- [ ] Change fonts

### 3. Integrate
- [ ] Connect to your app
- [ ] Add to workflows
- [ ] Automate generation
- [ ] Batch processing

### 4. Deploy
- [ ] Deploy to cloud
- [ ] Setup monitoring
- [ ] Configure backups
- [ ] Add SSL certificate

---

## 📞 Need Help?

### Documentation
- **DOCKER_GUIDE.md** - Complete operations guide
- **DOCKER_README.md** - Architecture & troubleshooting  
- **DOCKER_CHEATSHEET.md** - Quick command reference
- **README_SLIDES.md** - Feature details

### Quick Commands
```bash
# Check everything is running
docker-compose ps

# View real-time logs
docker-compose logs -f

# Access backend shell
docker exec -it martian-ai-backend bash

# Test API
curl http://localhost:8000/

# Reset everything
docker-compose down -v && docker-compose up --build
```

---

## 🚀 You're All Set!

Your Martian AI application is now:
- ✅ Fully containerized
- ✅ Running locally
- ✅ Ready to use
- ✅ Easy to scale
- ✅ Simple to deploy

### Quick Reference
| Task | Command |
|------|---------|
| Start | `docker-compose up --build` |
| Stop | `Ctrl+C` or `docker-compose down` |
| Logs | `docker-compose logs -f` |
| Status | `docker-compose ps` |
| Shell | `docker exec -it martian-ai-backend bash` |

---

**Happy Presenting! 🎉**

Generated presentations are waiting to be created at **http://localhost:3000**
