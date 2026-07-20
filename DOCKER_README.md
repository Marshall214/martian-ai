# Martian AI - Docker Setup & Deployment

A complete Docker containerized setup for the Martian AI full-stack application with intelligent slide generation, AI humanization, and academic tools.

## Quick Start

### Windows (PowerShell)
```powershell
# Navigate to project root
cd "c:\Users\HP\work projects\martian ai"

# Run startup script (requires Docker installed)
.\docker-start.ps1 -Build
```

### macOS / Linux (Bash)
```bash
cd ~/work\ projects/martian\ ai
chmod +x docker-start.sh
./docker-start.sh --build
```

### Manual Docker Compose
```bash
docker-compose up --build
```

## Access Points

Once running, access:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Web application UI |
| **Backend API** | http://localhost:8000 | REST API endpoints |
| **API Docs** | http://localhost:8000/docs | Swagger interactive documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |

## Architecture

### Services

```
┌─────────────────────────────────────────┐
│          Docker Network: martian        │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────┐ ┌──────────────┐ │
│  │  Frontend (3000) │ │Backend (8000)│ │
│  │  Node.js 18      │ │ Python 3.11  │ │
│  │  Next.js         │ │ FastAPI      │ │
│  │  Multi-stage     │ │ + LibreOffice│ │
│  └──────────────────┘ └──────────────┘ │
│           │                    │        │
│           └────────────────────┘        │
│                    │                    │
│           Shared Network (bridge)       │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Persistent Storage             │   │
│  │  • SQLite Database              │   │
│  │  • Uploads & Generated Files    │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

### Key Features

#### Backend Container
- **Image**: Python 3.11 slim + FastAPI
- **Port**: 8000
- **Key Dependencies**:
  - `python-pptx` - PPTX generation
  - `reportlab` - PDF creation
  - `transformers` + `torch` - AI models
  - `openai-whisper` - Audio transcription
  - `LibreOffice` - PDF conversion
- **Features**:
  - Intelligent slide generation from text/documents
  - Adaptive content chunking
  - Smart template selection
  - PPTX + PDF export
  - Audio transcription
  - Text summarization
  - AI humanization
  - JWT authentication
  - SQLite persistence

#### Frontend Container
- **Image**: Node.js 18 alpine + Next.js
- **Port**: 3000
- **Build Strategy**: Multi-stage (optimized for production)
- **Features**:
  - Responsive React UI
  - Tailwind CSS styling
  - Four main tool dashboards
  - File upload handling
  - User authentication
  - Real-time status updates

## Available Commands

### Startup Variations

```bash
# Start in foreground (logs visible, Ctrl+C to stop)
docker-compose up

# Start with rebuild
docker-compose up --build

# Start in background
docker-compose up -d

# With script (Windows)
.\docker-start.ps1 -Build -Detach

# With script (Unix)
./docker-start.sh --build --detach
```

### Container Management

```bash
# View running containers
docker-compose ps

# View all containers (including stopped)
docker-compose ps -a

# View logs
docker-compose logs          # All services
docker-compose logs -f       # Follow (real-time)
docker-compose logs backend  # Specific service
docker-compose logs -f frontend --tail=50

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove volumes too (WARNING: data loss)
docker-compose down -v

# Restart services
docker-compose restart
docker-compose restart backend
```

### Container Access

```bash
# Interactive shell in backend
docker exec -it martian-ai-backend bash

# Run commands in container
docker exec martian-ai-backend python test_slides.py
docker exec martian-ai-backend pip list

# Frontend shell
docker exec -it martian-ai-frontend sh
docker exec martian-ai-frontend npm list

# View container info
docker inspect martian-ai-backend
```

### Debugging

```bash
# Check service health
docker-compose ps

# View detailed service status
docker ps --no-trunc

# Check network connectivity
docker network inspect martian_network

# View resource usage
docker stats

# Prune unused resources
docker system prune -a

# View disk usage
docker system df
```

## Configuration

### Environment Variables

Edit `docker-compose.yml` or create `.env` file:

```env
# Backend
DATABASE_URL=sqlite:///./martian_ai.db
SECRET_KEY=your-secret-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=production
```

### File Modifications

**Backend changes**: Edit `backend/` files directly (volume-mounted, auto-reloads)
**Frontend changes**: Requires rebuild (`docker-compose up --build`)

```bash
# Edit backend file and restart
docker-compose restart backend

# Rebuild frontend after changes
docker-compose up --build frontend
```

## Health Checks

Both services have automated health checks:

```bash
# Backend (every 30s)
GET http://localhost:8000/

# Frontend (every 30s)
GET http://localhost:3000/
```

Check status:
```bash
docker-compose ps
```

## Testing Features

### Test Slide Generation

```bash
# Generate PPTX from text
curl -X POST http://localhost:8000/generate-slides-from-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning is powerful. It has many applications.",
    "title": "ML Basics",
    "export_format": "pptx"
  }' \
  --output test.pptx

# Generate from document
curl -X POST http://localhost:8000/generate-slides-from-document \
  -F "file=@document.pdf" \
  -F "title=Generated Slides" \
  --output slides.pptx
```

### Test Other Features

```bash
# Proofread text
curl -X POST http://localhost:8000/proofread \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'

# Summarize text
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text", "mode": "short"}'
```

## Troubleshooting

### Issue: Containers won't start

```bash
# Check logs
docker-compose logs

# Try rebuild
docker-compose down
docker-compose up --build

# Check port availability
netstat -ano | findstr :3000  # Windows
lsof -i :3000                  # macOS/Linux
```

### Issue: Port already in use

Edit `docker-compose.yml`:
```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Change 3000 to 3001
```

### Issue: Out of memory

**Windows (Docker Desktop)**:
- Settings → Resources → Memory: increase slider

**macOS (Docker Desktop)**:
- Preferences → Resources → Memory: increase

### Issue: PDF conversion not working

```bash
# Verify LibreOffice installation
docker exec martian-ai-backend which libreoffice

# Check backend logs
docker-compose logs backend | grep -i "libreoffice\|pdf"
```

### Issue: Frontend can't reach backend API

```bash
# Verify network
docker network inspect martian_network

# Test connectivity from frontend container
docker exec martian-ai-frontend wget -O- http://backend:8000/

# Check docker-compose.yml networks configuration
```

## Performance Tuning

### Build Optimization

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build

# Limit layers
docker image prune
docker system prune -a
```

### Runtime Optimization

```yaml
# In docker-compose.yml
services:
  backend:
    cpus: '2'                    # Limit CPU
    mem_limit: 2G               # Limit memory
    environment:
      - PYTHONUNBUFFERED=1
```

### Database Optimization

For production with large databases:
```bash
# Use named volume
docker volume create martian_db_data

# Point to it in docker-compose.yml
volumes:
  martian_db_data:
    driver: local
```

## Security Considerations

### For Production

1. **Change Secret Key**:
   ```bash
   # Generate new secret
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # Add to .env
   SECRET_KEY=your-generated-secret
   ```

2. **Use PostgreSQL** instead of SQLite:
   ```yaml
   services:
     postgres:
       image: postgres:15-alpine
       environment:
         POSTGRES_PASSWORD: secure-password
   ```

3. **Add reverse proxy** (Nginx):
   ```yaml
   services:
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
   ```

4. **Use .env file**:
   ```bash
   cp .env.example .env
   # Edit .env with sensitive values
   # Add .env to .gitignore
   ```

## Deployment Options

### Local Docker
```bash
docker-compose up -d
# Running locally with persistence
```

### Docker Hub
```bash
docker tag martian-ai-backend username/martian-ai-backend:latest
docker push username/martian-ai-backend:latest
```

### Cloud Platforms

**AWS ECS**:
```bash
docker-compose config > ecs-compose.yml
# Upload to AWS ECS
```

**DigitalOcean App Platform**:
- Deploy from GitHub
- Auto-builds on push

**Render/Railway**:
- Connect repository
- Auto-deploys on commit

**Kubernetes**:
```bash
# Convert to Kubernetes manifests
kompose convert -f docker-compose.yml
# Deploy with kubectl
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Next.js Docker Guide](https://nextjs.org/docs/deployment/docker)

## Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Verify ports: `netstat -an | grep -E "3000|8000"`
3. Check resources: `docker stats`
4. Inspect services: `docker-compose ps`

## License

See LICENSE file in project root.

---

**Happy containerizing! 🚀**
