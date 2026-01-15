# 🎯 Docker Quick Reference Cheat Sheet

## 🚀 Start Application

```bash
# Windows PowerShell
.\docker-start.ps1 -Build

# macOS/Linux
./docker-start.sh --build

# Manual (any OS)
docker-compose up --build
```

## 📍 Access Points
- Frontend: http://localhost:3000
- Backend: http://localhost:8000  
- API Docs: http://localhost:8000/docs

## 🛑 Stop Application

```bash
# Ctrl+C (if running in foreground)

# Or in another terminal
docker-compose down
```

## 📊 Check Status

```bash
# View running containers
docker-compose ps

# View logs (all)
docker-compose logs

# View logs (follow/live)
docker-compose logs -f

# View logs (specific service)
docker-compose logs backend
docker-compose logs frontend

# View last 50 lines
docker-compose logs --tail=50
```

## 🐚 Access Container Shell

```bash
# Backend Python shell
docker exec -it martian-ai-backend bash

# Frontend Node shell
docker exec -it martian-ai-frontend sh
```

## 🧪 Run Tests

```bash
# Test slide generation
docker exec martian-ai-backend python test_slides.py

# Check Python packages
docker exec martian-ai-backend pip list

# Check Node packages
docker exec martian-ai-frontend npm list
```

## 🔧 Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific
docker-compose restart backend
docker-compose restart frontend
```

## 🧹 Clean Up

```bash
# Remove containers (data persists)
docker-compose down

# Remove everything including volumes (WARNING: data loss)
docker-compose down -v

# Remove unused images
docker image prune -a

# Full system cleanup
docker system prune -a
```

## 🔍 Debugging

```bash
# Check container details
docker inspect martian-ai-backend

# Check network
docker network inspect martian_network

# View resource usage
docker stats

# Check disk usage
docker system df
```

## 🌐 Test API Endpoints

```bash
# Test backend is running
curl http://localhost:8000/

# Generate slides from text
curl -X POST http://localhost:8000/generate-slides-from-text \
  -H "Content-Type: application/json" \
  -d '{"text":"Test","title":"Test"}'

# Test frontend
curl http://localhost:3000/
```

## 🔄 Useful Patterns

### Development Workflow
```bash
# 1. Start with build
docker-compose up --build

# 2. Edit backend files (auto-reloads via volume)

# 3. Rebuild frontend if needed
docker-compose up --build frontend

# 4. Check logs
docker-compose logs -f

# 5. Stop when done
docker-compose down
```

### Troubleshooting Workflow
```bash
# 1. Check status
docker-compose ps

# 2. View logs
docker-compose logs -f

# 3. Restart problematic service
docker-compose restart backend

# 4. Check system resources
docker stats

# 5. Nuclear option: full rebuild
docker-compose down -v
docker-compose up --build
```

### Production Deployment
```bash
# 1. Build images
docker-compose build

# 2. Start in background
docker-compose up -d

# 3. Verify health
docker-compose ps

# 4. Monitor logs
docker-compose logs -f

# 5. Update containers on changes
docker-compose down
docker-compose up -d
```

## 📋 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Port 3000 in use | `docker-compose down` or change port in docker-compose.yml |
| Port 8000 in use | `docker-compose down` or change port in docker-compose.yml |
| Out of memory | Increase Docker memory in Desktop settings |
| Build fails | `docker-compose down -v` then `docker-compose up --build` |
| Can't connect APIs | Check `docker-compose ps` all healthy |
| PDF not generating | Check `docker-compose logs backend` for LibreOffice errors |
| Frontend blank screen | Check `docker-compose logs frontend` and http://localhost:3000 |

## 💡 Pro Tips

1. **Use `-d` flag to run in background**
   ```bash
   docker-compose up -d
   ```

2. **Follow logs in real-time**
   ```bash
   docker-compose logs -f --tail=20
   ```

3. **Only rebuild what changed**
   ```bash
   docker-compose up --build frontend  # Only frontend
   ```

4. **Save terminal output to file**
   ```bash
   docker-compose logs > output.log
   ```

5. **Check specific service**
   ```bash
   docker-compose ps backend
   ```

6. **Run command without shell**
   ```bash
   docker exec martian-ai-backend python -c "print('hello')"
   ```

7. **Monitor in real-time**
   ```bash
   watch docker-compose ps
   ```

## 📚 Full Documentation

- `DOCKER_GUIDE.md` - Comprehensive guide
- `DOCKER_README.md` - Architecture & troubleshooting
- `README_SLIDES.md` - Implementation details

## ⚡ One-Liners

```bash
# Start fresh
docker-compose down -v && docker-compose up --build

# Restart everything
docker-compose restart

# Full cleanup
docker-compose down -v && docker system prune -a

# Check everything is running
docker-compose ps && docker stats

# Monitor in background, start fresh
docker-compose up -d --build && docker-compose logs -f

# Development: quick rebuild frontend
docker-compose down && docker-compose up --build
```

---

**Bookmark this page! 📌**
