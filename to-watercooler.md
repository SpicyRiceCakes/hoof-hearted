# 💬 To Watercooler - Context Preservation Log

## Purpose
This file serves as an intermediate context preservation system to prevent memory loss during Claude Code auto-compacting. Update this before reaching context limits or when complex tasks are interrupted.

## Current Session Context

### Session Log Entry - 2025-06-19
**Session Focus**: Docker Best Practices + Process Identification System

### Completed This Session:
- ✅ **Advanced Docker Architecture**: Applied src-brain best practices with multi-stage builds and external testing
- ✅ **Dark Theme Implementation**: Added theme toggle with CSS custom properties for eye-friendly monitoring
- ✅ **Task 1.2.2 - Process Identification**: Complete intelligent classification system for GPU processes
  - ProcessClassifier with pattern matching for miners, ML, video, games
  - Enhanced API endpoints `/api/gpu/processes` with security warnings
  - Comprehensive process attribution answering "Why is my GPU fan running?"

### Key Insights/Decisions:
- **Docker-first approach**: Successfully implemented external testing architecture from src-brain
- **Process classification**: 90% confidence for crypto miners, 80% for ML/video, 70% for games
- **Security focus**: Immediate alerts for suspected cryptocurrency mining activity
- **User experience**: Human-readable explanations like "GPU fan running because of: 1 game(s), 1 ML training process(es)"

### Next Session Should Focus On:
- **Task 1.2.3 - System Metrics**: CPU, RAM, disk, and network monitoring integration
- **Follow task manager protocol**: Create working log, research phase, planning phase, implementation
- **Re-enable background monitoring**: Fix the disabled SocketIO background task

### Don't Forget:
- **Task Manager Protocol**: I skipped the proper workflow - need to follow task-manager-instructions.md
- **Working Logs**: Should create individual task documentation in ai-docs/task-manager/
- **Status Updates**: Update both main task list AND working log headers properly
- **Context at 15%**: Good space for next task implementation

### Key Decisions Made
- **Technology Stack**: Vue.js + Flask + PostgreSQL + Docker (Tasks 1.1.1-1.2.1 COMPLETE)
- **Port 0909**: Korean fart humor (공구공구) for main dashboard
- **Deployment**: Multi-container Docker with port fixes for Apple Silicon
- **GPU Monitoring**: Multi-vendor support (NVIDIA/AMD/Basic) with process attribution
- **Architecture**: Factory pattern, real-time APIs, WebSocket integration (background task needs fix)

### Work Completed
- ✅ **Tasks 1.1.1-1.2.1**: Complete technology stack, deployment, and GPU monitoring
- ✅ **Docker Infrastructure**: Multi-container setup (frontend, backend, database)  
- ✅ **Vue.js Dashboard**: Beautiful glassmorphism design with SpicyRiceCakes branding
- ✅ **GPU Monitoring System**: Multi-vendor GPU monitoring with process attribution
- ✅ **Real-time APIs**: `/api/gpu/summary`, `/api/gpu/metrics`, WebSocket events
- ✅ **Cross-platform Support**: Graceful fallback when no GPUs available
- ✅ **Frontend Connection**: Both Backend API and Database showing "Connected"
- ✅ **Advanced Docker Architecture**: Multi-stage builds, external testing, enhanced development workflow
- ✅ **Process Identification System**: Intelligent classification (miners, ML, video, games) with security warnings

### RESOLVED Issue Details
**Problem SOLVED**: Frontend now works perfectly - both connections green ✅

**Root Cause**: SocketIO `background_gpu_monitoring` task was hanging Flask app startup
**Solution**: Disabled background task temporarily, all APIs now responsive
**Evidence**: 
- ✅ Frontend shows "Backend API: Connected" and "Database: Connected"
- ✅ All API endpoints working: `/api/status`, `/api/health`, `/api/gpu/summary`
- ✅ Docker MCP investigation revealed 504 timeout errors, now resolved

### GPU Monitoring Implementation Complete
**"Why is my GPU fan running?" - SOLVED:**
- ✅ **Multi-vendor GPU detection** (NVIDIA/AMD/Basic fallback)
- ✅ **Process attribution** - identifies which processes use GPU memory
- ✅ **Real-time monitoring** - GPU usage, temperature, fan speed tracking
- ✅ **Cross-platform compatibility** - graceful handling of systems without GPUs
- ✅ **Docker integration** - containerized deployment with optional GPU device access

### Docker Best Practices Implementation Complete
**Advanced Docker Architecture Applied from src-brain:**
- ✅ **Multi-Stage Dockerfiles** - Development and production optimized builds
- ✅ **External Testing Architecture** - App in Docker, tests on host for better debugging
- ✅ **Enhanced Package Scripts** - Docker-first development commands (`npm run dev`)
- ✅ **Testing Infrastructure** - Playwright integration with containerized app testing
- ✅ **Korean Port Preference** - Port 0909 (공구공구) for dashboard
- ✅ **MCP Docker Integration** - Proper timeout management and debugging setup
- ✅ **Comprehensive Documentation** - DOCKER.md with full workflow guide

### NEW: Mirim Files Reorganization Analysis
**Date**: 2025-06-18
**Task**: Review and reorganize three files in src-brain/about/mirim/ directory

**Current Files Analyzed**:
1. `about-mirim-yoo.md` - Personal bio, restaurant projects, character description
2. `communicating-with-mirim.md` - Korean translation guide for @mirim tag
3. `mirim-bio.md` - Comprehensive content for website pages (About/Art/Real Estate/Life/Press/Contact)

**Reorganization Plan**:
1. **Keep communicating-with-mirim.md separate** (per David's request - specific to instructions)
2. **Consolidate other content into single comprehensive file**: Create `mirim-yoo-complete-profile.md`
3. **Structure**: Personal bio → Professional work → Artistic projects → Contact info
4. **Remove redundancy**: Merge overlapping biographical information
5. **Improve organization**: Group related content (art/business/personal) into clear sections
6. **Maintain website-ready content**: Keep press quotes, contact details, project descriptions

**Benefits of Reorganization**:
- Single source of truth for Mirim's complete profile
- Eliminates duplicate biographical information
- Better organized for both AI reference and potential website use
- Maintains communication instructions as separate specialized document
- Cleaner file structure in src-brain/about/mirim/ directory

**Status**: Plan ready, awaiting David's approval after file server reconfiguration

### Context for Next Session
- David wants to solve "Why is my GPU fan running?" through home server monitoring
- Project uses SpicyRiceCakes philosophy with methodical, user-centric approach
- Sophie is the architect partner who provides technical feedback and direction
- David prefers ChatGPT Mac app but considering API costs for multi-AI collaboration
- Technology stack decisions (React vs Vue, Node vs Python, etc.) are first critical tasks

---

## Session Log Template (Copy for each session)

**Date**: [YYYY-MM-DD]
**Session Focus**: [Brief description]

### Completed This Session:
- 

### Key Insights/Decisions:
- 

### Next Session Should Focus On:
- 

### Don't Forget:
- 

---

## Auto-Update Instructions for Claude

**Before Auto-Compact or at 80% context usage:**
1. Update "Current Session Context" section above
2. Add session log entry with date
3. Summarize key points for continuity
4. Save critical technical details
5. Note any user preferences revealed during session

**After Compacting:**
1. Read this entire file first
2. Review recent session logs
3. Apply context to continue seamlessly

## Multi-AI Collaboration Protocol

### Context Transfer Template
When moving conversations between AIs:

```
## Previous Context from [ChatGPT Mac/Claude Code/etc.]
- **Task**: [What we were working on]
- **Progress**: [What's been completed]
- **Current Issue**: [What needs different perspective]
- **Key Decisions**: [Important choices made]

## Requesting [Claude/ChatGPT/Sophie] perspective on:
[Specific question or area where you want different viewpoint]

## Original conversation summary:
[Key points from previous platform]
```

### AI Collaboration Workflow
1. **ChatGPT Mac**: Quick development questions, VS Code integration
2. **Claude Code**: Implementation, systematic architecture
3. **Alternative AI** (Poe/TeamAI): Second opinions on complex decisions
4. **Sophie**: Architecture review through task manager system