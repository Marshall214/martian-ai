# Martian AI - Docker Deployment Guide

## Prerequisites

- Docker installed ([Get Docker](https://www.docker.com/get-started))
- Docker Compose installed (usually included with Docker Desktop)
- At least 2GB free RAM
- Available ports: 3000 (frontend), 8000 (backend)

## Quick Start

### 1. Navigate to project root
```bash
cd "c:\Users\HP\work projects\martian ai"
```

### 2. Build and start containers
```bash
docker-compose up --build
```

This command will:
- Build the backend image (FastAPI + Python dependencies)
- Build the frontend image (Next.js)
- Start both services with proper networking
- Create volumes for persistent data

### 3. Access the application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **API ReDoc**: http://localhost:8000/redoc

### 4. Stop the application
```bash
docker-compose down
```

---

## Commands Reference

### Start services in background
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild containers
```bash
docker-compose up --build
```

### Remove everything (including volumes)
```bash
docker-compose down -v
```

### Access container shell
```bash
# Backend
docker exec -it martian-ai-backend bash

# Frontend
docker exec -it martian-ai-frontend sh
```

### Run one-time commands
```bash
# Backend Python command
docker exec martian-ai-backend python test_slides.py

# Frontend npm command
docker exec martian-ai-frontend npm list
```

---

## Architecture

### Services

1. **Backend (martian-ai-backend)**
   - FastAPI application
   - Python 3.11 slim image
   - Port: 8000
   - Dependencies: python-pptx, reportlab, transformers, torch, etc.
   - Includes LibreOffice for PDF conversion
   - Database: SQLite (persistent volume)

2. **Frontend (martian-ai-frontend)**
   - Next.js 18 application
   - Node.js 18 alpine image
   - Port: 3000
   - Two-stage build: optimized production image
   - Health checks: auto-restarts on failure

### Network
- Custom bridge network: `martian_network`
- Services communicate via service names: `http://backend:8000`
- Frontend connects to backend via `http://localhost:8000` (from host)

### Volumes
- `backend_db`: Persistent storage for SQLite database
- `backend` code: Volume-mounted for development (live reload possible)

---

## Features Included

### Backend Features
- ✅ Slide generation from text/documents (PPTX)
- ✅ PDF conversion with LibreOffice
- ✅ Document processing (PDF, DOCX, TXT)
- ✅ Audio transcription
- ✅ Text summarization
- ✅ AI text humanization
- ✅ Authentication with JWT
- ✅ Database persistence

### Frontend Features
- ✅ Modern UI with Tailwind CSS
- ✅ Responsive design (mobile-friendly)
- ✅ Dashboard with 4 main tools
- ✅ User authentication
- ✅ Real-time status updates
- ✅ File upload support

---

## Health Checks

Both services include health checks that automatically restart them if they become unresponsive:

- **Backend**: Checks every 30 seconds
- **Frontend**: Checks every 30 seconds
- Start period: 10-15 seconds (allows startup time)

---

## Environment Variables

### Backend (Auto-configured)
```
DATABASE_URL=sqlite:///./martian_ai.db
PYTHONUNBUFFERED=1
```

### Frontend (Auto-configured)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=production
```

To customize, edit `docker-compose.yml` and restart:
```bash
docker-compose down
docker-compose up
```

---

## Performance Notes

### First Run
- First build: 2-5 minutes (downloads images, installs dependencies)
- Subsequent runs: <30 seconds

### Optimization Tips
- Use `docker-compose up -d` to run in background
- Use `docker-compose logs -f` to monitor
- Database persists in volumes (no data loss on restart)
- Frontend uses multi-stage build for optimal image size

---

## Troubleshooting

### Containers won't start
```bash
# Check logs
docker-compose logs

# Try rebuilding
docker-compose down
docker-compose up --build
```

### Port already in use
```bash
# Change ports in docker-compose.yml
# Example: 3000:3000 → 3001:3000
# Then: docker-compose up
```

### Out of memory
```bash
# Increase Docker memory limits in settings
# Docker Desktop → Preferences → Resources
```

### PDF conversion not working
```bash
# LibreOffice is installed in backend
# Check backend logs:
docker-compose logs backend
```

### Frontend can't reach backend API
```bash
# Ensure both containers are on the same network
# Check docker-compose.yml has networks configuration
docker network inspect martian_network
```

---

## Production Deployment

For production deployment:

1. **Use `.env` file** instead of hardcoded variables:
   ```bash
   DATABASE_URL=postgresql://user:password@db:5432/martian_ai
   SECRET_KEY=your-secret-key
   ```

2. **Use PostgreSQL** instead of SQLite:
   - Add PostgreSQL service to docker-compose.yml
   - Update DATABASE_URL connection string

3. **Add Nginx reverse proxy** for SSL/TLS

4. **Use separate environment files**:
   - `docker-compose.yml` (base)
   - `docker-compose.prod.yml` (production overrides)

5. **Example command**:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

---

## Testing the Slide Generation

Once running, test the new slide generation feature:

```bash
# Terminal 1: Check backend is running
curl http://localhost:8000/

# Terminal 2: Test slide generation
curl -X POST http://localhost:8000/generate-slides-from-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a test. Machine learning is powerful. It has many applications.",
    "title": "Test Presentation",
    "export_format": "pptx"
  }' \
  --output test.pptx
```

---

## Next Steps

1. ✅ Containers are running and healthy
2. ⬜ Deploy to cloud (AWS, DigitalOcean, Heroku)
3. ⬜ Set up CI/CD pipeline
4. ⬜ Configure custom domain and SSL
5. ⬜ Add monitoring and logging

---

## Support

For issues or questions:
1. Check Docker logs: `docker-compose logs`
2. Verify port availability: `netstat -an | grep 3000`
3. Check Docker disk space: `docker system df`
4. Clean up unused resources: `docker system prune -a`
