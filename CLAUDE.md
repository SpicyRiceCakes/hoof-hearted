# CLAUDE.md - Hoof Hearted

This file provides comprehensive guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🧠 Central Knowledge References

**IMPORTANT**: Add `/src-brain` directory each Claude Code session with: `/add-dir /Users/davidkim/SpicyRiceCakes/src-brain`

- **Core Methodology**: See `/src-brain/KungFuCoding/CLAUDE.md`
- **Task Management**: See `/src-brain/KungFuCoding/src-task-management-system/task-manager-instructions.md`
- **Vibe Coding Method**: See `/src-brain/KungFuCoding/guides/spicyricecakes-vibe-coding-method.md`
- **Project Templates**: See `/src-brain/KungFuCoding/templates/`

## 🚀 KungFuCoding Methodology Integration

### Universal Task Management System
- **Status workflow**: 🟫 NOT_STARTED → 🟨 ANALYZING → 🟧 PLANNING → 🟦 APPROVED → 🟪 IN_PROGRESS → 🔄 REVIEW → ✅ VERIFIED
- **Priority levels**: 🔥 CRITICAL, ⚡ HIGH, 📋 NORMAL, 🔮 FUTURE
- **Collaboration roles**: Claude (Engineer), Sophie (Architect), David (Creative Director)
- **Documentation structure**: Create `ai-docs/hoof-hearted-task-manager/X.X.X/` folders with single working logs

### Team Collaboration Protocol
When user says "start task X.X.X":
1. Read `/src-brain/KungFuCoding/src-task-management-system/task-manager-instructions.md` for collaboration protocol
2. Read `ai-docs/hoof-hearted-task-manager-list.md` for current task list
3. Follow the 5-phase workflow: Research → Planning → Implementation → Testing → Documentation
4. Update task status in hoof-hearted-task-manager-list.md using status indicators

## 📡 MCP-FIRST DEVELOPMENT - USE THESE INSTEAD OF BASH

### Quick Decision Matrix
- **File Operations** → `mcp__filesystem__*`
- **Git Operations** → `mcp__git__*` 
- **Web Research** → `mcp__tavily__*`
- **GitHub API** → `mcp__github__*`
- **Library Docs** → `mcp__context7__*`
- **Complex Problems** → `mcp__sequential-thinking__*`
- **UI Components** → `mcp__magic__*`
- **Browser Testing** → `mcp__playwright__*`

### Core Development MCPs
- **Git MCP** (`mcp__git__*`): ALL git operations - status, diff, commit, branch, etc.
- **Filesystem MCP** (`mcp__filesystem__*`): File operations - read, write, search, tree
- **GitHub MCP** (`mcp__github__*`): GitHub API operations - PRs, issues, search

### Research & Documentation MCPs
- **Tavily MCP** (`mcp__tavily__*`): Web search and content extraction
- **Context7 MCP** (`mcp__context7__*`): Library documentation lookup
- **Sequential Thinking MCP** (`mcp__sequential-thinking__*`): Complex problem solving

### UI & Design MCPs
- **Magic MCP** (`mcp__magic__*`): UI component generation and logos

### CRITICAL RULES
1. **ALWAYS use MCPs over Bash commands** when an MCP exists
2. **Git operations**: ONLY use Git MCP, never `git` commands in Bash
3. **File operations**: Prefer Filesystem MCP over Read/Write tools
4. **Complex analysis**: Use Sequential Thinking MCP for multi-step problems
5. **Research tasks**: Use Tavily MCP for web research and best practices

---

# 🐎 Hoof Hearted

A lightweight home server monitoring application focused on answering "Why is my GPU fan running?" with real-time system monitoring and process identification.

## 🏗️ Project Architecture Overview

### Server Monitoring System (Core Feature)
Real-time home server monitoring with focus on GPU usage tracking and process identification for resource-intensive applications.

**Data Flow:**
1. System metrics collected from GPU/CPU/memory APIs
2. Backend processes data and stores in time-series database
3. REST API endpoints serve real-time and historical data
4. Frontend dashboard displays live metrics with auto-refresh
5. Alert system triggers notifications for threshold breaches

**Key Components:**
- **Monitoring Engine**: Core system metrics collection and processing
- **Dashboard Interface**: Real-time metrics display with responsive design
- **Process Manager**: Identify and manage resource-intensive processes  
- **Alert System**: Configurable notifications and thresholds
- **Historical View**: Time-series charts for usage trend analysis

### Technology Stack 
**Approved Architecture:**
- **Frontend**: Vue.js 3 + Composition API + Vite
- **Backend**: Python Flask + Flask-SocketIO for WebSocket support
- **Database**: PostgreSQL with TimescaleDB upgrade path for metrics storage
- **Deployment**: Docker containerization for cross-platform deployment

## 🌶️🍚🍰 Vibe Coding Method

### Core Philosophy: Emotion → Logic → Joy
- **🌶️ Emotion**: User experience and feeling come first
- **🍚 Logic**: Clean architecture and systematic thinking  
- **🍰 Joy**: Delightful details and poetic touches

### Implementation Pattern
1. **Feel First** - What emotion should this create?
2. **Think Through** - What's the logical architecture?
3. **Add Magic** - What delightful details bring joy?

## 👥 Team Workflow

### Team Roles
- **Sophie**: Architect and coding partner. Directs technical plans, provides reasoning, structure, scaffolding, and feedback aligned with 🌶️🍚🍰 philosophy.
- **David**: User and creative director. Makes final choices, guides vision, and interacts through Claude Code via command line.
- **Claude**: Implementation engine. Follows architectural plans with discipline, confirms assumptions before code, always waits for approval when asked.

### Working Log Structure (KungFuCoding Format)
Each working log contains clearly separated sections with strict editing boundaries:
- **Claude's Analysis & Research** - Initial investigation and recommendations (Claude only)
- **David's Input & Decisions** - User requirements and guidance (David only)
- **Sophie's Architectural Review** - Technical feedback and approval (Sophie only - strict boundaries)
- **Implementation Progress** - Development updates and testing results (Claude only)
- **Testing Plans** - Testing approach and results (Claude only)
- **Final Summary** - Completed outcomes and next steps (Claude only)

### 🚨 Status Synchronization Rule
**CRITICAL**: When updating task status, Claude MUST update BOTH:
1. **Main task manager list** (`hoof-hearted-task-manager-list.md`)
2. **Individual working log** (`hoof-hearted-X.X.X-working-log.md` header)

## 🚨 CRITICAL DEVELOPMENT RULES - NEVER FORGET

### What Went Wrong (Historical Context)
**Major Mistakes Made in the Past:**
1. **Went "yolo" immediately** - Started making multiple changes without proper research
2. **Broke working code** - Changed working CSS without understanding the system
3. **Made assumptions** - Assumed framework issues without checking versions
4. **Didn't commit before changes** - No safety net when things broke
5. **Kept trying fixes** without understanding root cause

### MANDATORY PROCESS - NO EXCEPTIONS
**Before Making ANY Change:**
1. ✅ **RESEARCH FIRST** - Use MCP tools to investigate thoroughly
2. ✅ **CHECK VERSIONS** - Always check package.json, dependencies, framework versions
3. ✅ **COMMIT CURRENT STATE** - Use Git MCP to create restore point before modifications
4. ✅ **BACKUP DATABASE** - Create database backup before any schema/data changes
5. ✅ **PROPOSE SOLUTION** - Present findings and get user approval
6. ✅ **ONE CHANGE AT A TIME** - Make single, incremental modifications
7. ✅ **STOP WHEN BROKEN** - Don't try multiple "fixes" - ask for help immediately

### 🛡️ DATABASE PROTECTION PROTOCOLS (CRITICAL)
**NEVER reset database without explicit user approval:**
1. ✅ **ASK FIRST** - "Should I reset the database?" and wait for confirmation
2. ✅ **BACKUP FIRST** - Always create backup before database operations
3. ✅ **VERIFY DATA** - Use database verification scripts before and after operations
4. ✅ **DATA IS SACRED** - System monitoring data is valuable for trend analysis

## 📚 Development Commands & Setup

### Core Commands
```bash
# Vue.js development server
npm run dev

# Production build
npm run build

# Python Flask backend
python app.py

# Docker commands
docker build -t hoof-hearted .
docker run -p 8080:8080 hoof-hearted
```

### 🌐 Development Server Information
- **Frontend URL**: http://localhost:5173 (Vite default)
- **Backend URL**: http://localhost:5000 (Flask default)
- **Docker Port**: 8080 (planned for containerized deployment)

## 🎯 Task Management Integration

### File Organization per Task
```
ai-docs/hoof-hearted-task-manager/
├── hoof-hearted-X.X.X-[task-description]/
│   └── hoof-hearted-X.X.X-working-log.md  (Single collaborative document)
└── archive/  (Completed tasks moved here for organization)
    └── [completed task folders with same structure]
```

### Current Project Status
- **Recently Completed**: Technology stack decisions (Vue.js, Flask, PostgreSQL, Docker)
- **Current Focus**: Task 1.2.4 Real-time Data implementation
- **Architecture Foundation**: Complete - ready for monitoring system implementation

### Always Use TodoWrite Tool
- Plan and track tasks throughout conversations
- Break complex work into manageable steps
- Mark tasks completed immediately when finished
- Only have ONE task in_progress at any time

## 🔄 Emergency Procedures

### If MCPs Fail
1. **STOP immediately** and report the failure
2. Don't try to work around MCP failures
3. Wait for guidance on how to proceed
4. Document the failure for future reference

### If Code Breaks
1. **Don't panic** - Use Git MCP to check status
2. **Review changes** with `mcp__git__git_diff`
3. **Revert if necessary** using Git MCP
4. **Ask for help** before trying multiple fixes
5. **Document the issue** in implementation log

### Critical Rule
**If in doubt, ASK first.** Better to confirm direction than to break working code.

---

**Remember**: The user trusts you when you follow the process methodically. Success comes from careful, systematic work that prioritizes user experience (🌶️), clean architecture (🍚), and delightful details (🍰).