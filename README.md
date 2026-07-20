# Martian AI - Complete Documentation Index

Welcome! Everything you need to know about the Martian AI application is documented below. Choose what you need:

---

## I Want to Get Started Quickly!

**Start here:** [GETTING_STARTED.md](GETTING_STARTED.md)

Quick summary:
```bash
docker-compose up --build
# Open http://localhost:3000
```

---

## Documentation by Topic

### Understanding the Project

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [README_SLIDES.md](README_SLIDES.md) | Complete implementation summary, features, architecture | 15 min |
| [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) | What was built, technical details, performance metrics | 10 min |
| [This File](README.md) | Navigation guide for all documentation | 5 min |

### Docker & Deployment

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Step-by-step setup guide with visual walkthrough | 10 min |
| [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) | Quick command reference (bookmark this!) | 5 min |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Comprehensive Docker operations manual | 20 min |
| [DOCKER_README.md](DOCKER_README.md) | Architecture, troubleshooting, cloud deployment | 25 min |

### Feature Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [README_SLIDES.md](README_SLIDES.md) | Slide generator features and capabilities | 15 min |

### Developer Resources

| Document | Purpose | Location |
|----------|---------|----------|
| Slide Generation Engine | Advanced content analysis system | `backend/utils/slidegen_advanced.py` |
| Backend Routes | API endpoint implementations | `backend/routes/slides.py` |
| Frontend API | TypeScript API functions | `frontend/lib/services/api.ts` |
| Test Suite | Comprehensive test cases | `backend/test_slides.py` |

---

## ⚡ Quick Command Reference

### Start Application
```bash
# Windows PowerShell
.\docker-start.ps1 -Build

# macOS/Linux
./docker-start.sh --build

# Any OS
docker-compose up --build
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Essential Commands
```bash
# View status
docker-compose ps

# View logs
docker-compose logs -f

# Stop application  
docker-compose down

# Access container
docker exec -it martian-ai-backend bash
```

**Full reference:** [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md)

---

## What Was Implemented

### Core Features
**Intelligent Slide Generator**
- Analyzes content (type, density, structure)
- Auto-selects professional templates
- Intelligently chunks 1MB documents into 3-50 slides
- Generates PPTX and PDF presentations
- Processes in 2-8 seconds

**Backend Enhancements**
- Two new API endpoints for slide generation
- Support for text, documents (PDF/DOCX/TXT)
- Template override from user prompts
- Comprehensive error handling

**Docker Infrastructure**
- Multi-container application
- Automated health checks
- Persistent data storage
- Easy local deployment

**Documentation & Tools**
- 5 comprehensive guides
- 2 startup scripts (PowerShell & Bash)
- Command cheatsheet
- Test suite

---

## Architecture

### Technology Stack
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11, SQLAlchemy
- **Containers**: Docker, Docker Compose
- **Libraries**: python-pptx, reportlab, transformers, torch
- **System**: LibreOffice (for PDF conversion)

### Services
```
┌─────────────────────────┐
│   Frontend (Port 3000)  │
│   Node.js 18 + Next.js  │
└───────────┬─────────────┘
            │
    ┌───────┴────────┐
    │   Bridge       │
    │   Network      │
    └───────┬────────┘
            │
┌───────────┴─────────────┐
│  Backend (Port 8000)    │
│  Python 3.11 + FastAPI  │
│  + LibreOffice System   │
└─────────────────────────┘
```

---

## Learning Resources

### For Understanding the System
1. Read [README_SLIDES.md](README_SLIDES.md) - Overview of features
2. Read [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) - Technical details
3. Explore code in `backend/utils/slidegen_advanced.py`

### For Using Docker
1. Read [GETTING_STARTED.md](GETTING_STARTED.md) - Step-by-step
2. Keep [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) bookmarked
3. Reference [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for advanced topics

### For Development
1. Clone and explore the code
2. Read inline comments in `slidegen_advanced.py`
3. Check API endpoints in `routes/slides.py`
4. Run test suite: `backend/test_slides.py`

---

## Common Questions

### Q: How do I start the app?
**A:** See [GETTING_STARTED.md](GETTING_STARTED.md)
```bash
docker-compose up --build
```

### Q: Where's the slide generator?
**A:** 
- **Web UI**: http://localhost:3000 → Click "Slide Generator"
- **API**: POST /generate-slides-from-text
- **Docs**: [README_SLIDES.md](README_SLIDES.md)

### Q: What files were created?
**A:** See [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) section "Files Created/Modified"

### Q: How do I troubleshoot?
**A:** Check [DOCKER_README.md](DOCKER_README.md) section "Troubleshooting"

### Q: Can I deploy this?
**A:** Yes! See [DOCKER_README.md](DOCKER_README.md) section "Production Deployment"

### Q: How do I make changes?
**A:** Backend changes auto-reload. Frontend needs rebuild:
```bash
docker-compose up --build frontend
```

---

## File Structure

### Documentation Files (In Root)
```
GETTING_STARTED.md          ← Start here for setup
README_SLIDES.md            ← Feature details
DOCKER_CHEATSHEET.md        ← Command quick reference
DOCKER_GUIDE.md             ← Detailed Docker guide
DOCKER_README.md            ← Architecture & troubleshooting
IMPLEMENTATION_REPORT.md    ← What was built
README.md                   ← This file
.env.example                ← Configuration template
```

### Application Files (Modified/Created)
```
backend/
├── Dockerfile              ← Container definition
├── .dockerignore           ← Build exclusions
├── requirements.txt        ← Updated dependencies
├── routes/
│   └── slides.py          ← NEW: API endpoints
├── utils/
│   └── slidegen_advanced.py  ← NEW: Slide engine (450+ lines)
└── test_slides.py         ← NEW: Test suite

frontend/
├── Dockerfile             ← Multi-stage build
├── .dockerignore          ← Build exclusions
└── lib/services/
    └── api.ts            ← Updated API functions

Docker/
├── docker-compose.yml     ← Orchestration
├── docker-start.ps1       ← Windows script
└── docker-start.sh        ← Unix script
```

---

## Verification Checklist

After setup, verify everything works:

- [ ] `docker-compose ps` shows 2 healthy containers
- [ ] Can open http://localhost:3000
- [ ] Can open http://localhost:8000
- [ ] API docs available at http://localhost:8000/docs
- [ ] "Slide Generator" option visible in dashboard
- [ ] Can generate PPTX file
- [ ] Can download generated file

---

## Next Steps

1. **Get Started** → Read [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Run Application** → `docker-compose up --build`
3. **Test Features** → Generate some slides
4. **Explore API** → Visit http://localhost:8000/docs
5. **Read Details** → Check [README_SLIDES.md](README_SLIDES.md)
6. **Deploy** → Follow [DOCKER_README.md](DOCKER_README.md) deployment section

---

## Support & Help

### Documentation by Difficulty Level

**Beginner:**
1. [GETTING_STARTED.md](GETTING_STARTED.md) - Visual step-by-step
2. [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) - Basic commands

**Intermediate:**
1. [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Operations guide
2. [README_SLIDES.md](README_SLIDES.md) - Feature documentation

**Advanced:**
1. [DOCKER_README.md](DOCKER_README.md) - Architecture details
2. Source code in `backend/utils/slidegen_advanced.py`
3. [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) - Technical deep dive

### Quick Help

| Problem | Solution |
|---------|----------|
| App won't start | → [DOCKER_README.md](DOCKER_README.md#troubleshooting) |
| Port in use | → [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) |
| API not working | → [DOCKER_GUIDE.md](DOCKER_GUIDE.md#health-checks) |
| Can't generate slides | → Check logs: `docker-compose logs -f` |
| Need a command | → [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) |

---

## Key Features Summary

| Feature | Status | Doc |
|---------|--------|-----|
| Slide generation from text | Complete | [README_SLIDES.md](README_SLIDES.md) |
| Document upload (PDF/DOCX) | Complete | [README_SLIDES.md](README_SLIDES.md) |
| Smart template selection | Complete | [README_SLIDES.md](README_SLIDES.md) |
| PPTX export | Complete | [README_SLIDES.md](README_SLIDES.md) |
| PDF export | Complete | [README_SLIDES.md](README_SLIDES.md) |
| Docker containerization | Complete | [DOCKER_README.md](DOCKER_README.md) |
| Health checks | Complete | [DOCKER_GUIDE.md](DOCKER_GUIDE.md) |
| Error handling | Complete | [README_SLIDES.md](README_SLIDES.md) |

---

## You're All Set!

Everything is documented, tested, and ready to use. 

**Start with:** [GETTING_STARTED.md](GETTING_STARTED.md)

**Questions?** Check the relevant documentation file from the list above.

---

Last Updated: January 4, 2026
