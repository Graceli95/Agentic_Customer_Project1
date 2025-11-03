# Development Workflow Guide

**Project**: Advanced Customer Service AI  
**Last Updated**: After Phase 1 Completion  
**Status**: Ready for Phase 2

---

## 🎯 Current Status

### ✅ Completed Phases
- **Phase 1: Project Skeleton** - All setup, infrastructure, and validation complete
  - PRD: `tasks/0001-prd-project-setup.md`
  - Tasks: `tasks/tasks-0001-prd-project-setup.md`
  - Status: ✅ 100% Complete

### 🚀 Next Phase
- **Phase 2: Simple Agent Foundation**
  - Integrate LangChain/LangGraph
  - Add real LLM responses (OpenAI)
  - Implement conversation memory

---

## 📋 Standard Workflow for Each Phase

### Step 1: Create PRD
Use `@create-prd.mdc` to generate a Product Requirements Document

### Step 2: Generate Task List
Use `@generate-tasks.mdc` to break down PRD into actionable tasks

### Step 3: Execute Tasks
Use `@process-task-list.mdc` to implement one subtask at a time

---

## 🔄 Complete Development Cycle

```
Phase N
  ↓
1. Create PRD (create-prd.mdc)
  ↓
2. Generate Tasks (generate-tasks.mdc)
  ↓
3. Execute Tasks (process-task-list.mdc)
  ↓
✅ Phase N Complete!
  ↓
Phase N+1
  ↓
Repeat steps 1-3...
```

---

## 📝 Exact Prompts to Use

### Prompt 1: Create the PRD

**When to use**: Starting a new phase  
**Mode required**: Agent mode

```
Using @create-prd.mdc, create a PRD for Phase [N] of @PHASED_DEVELOPMENT_GUIDE.md 
([Phase Name]). This phase includes:
- [Key deliverable 1]
- [Key deliverable 2]
- [Key deliverable 3]

Please ask clarifying questions before generating the PRD.
```

**Example for Phase 2:**
```
Using @create-prd.mdc, create a PRD for Phase 2 of @PHASED_DEVELOPMENT_GUIDE.md 
(Simple Agent Foundation). This phase includes:
- Integrating LangChain/LangGraph
- Adding real LLM responses (OpenAI)
- Implementing conversation memory
- Replace echo response with actual agent

Please ask clarifying questions before generating the PRD.
```

**What happens:**
1. AI asks clarifying questions
2. You answer (options provided for easy selection)
3. AI generates `[nnnn]-prd-[feature-name].md` in `/tasks/`

---

### Prompt 2: Generate Task List

**When to use**: After PRD is created and reviewed  
**Mode required**: Agent mode

```
Using @generate-tasks.mdc, create a task list for @[nnnn]-prd-[feature-name].md
```

**Example for Phase 2:**
```
Using @generate-tasks.mdc, create a task list for @0002-prd-simple-agent-foundation.md
```

**What happens:**
1. AI analyzes PRD and current codebase
2. AI generates high-level parent tasks
3. AI asks for confirmation ("Go")
4. AI breaks down each parent task into sub-tasks
5. AI creates `tasks-[nnnn]-prd-[feature-name].md` in `/tasks/`

---

### Prompt 3: Execute Tasks

**When to use**: After task list is created and reviewed  
**Mode required**: Agent mode

```
Let's start executing @tasks-[nnnn]-prd-[feature-name].md following @process-task-list.mdc
```

**Example for Phase 2:**
```
Let's start executing @tasks-0002-prd-simple-agent-foundation.md following @process-task-list.mdc
```

**What happens:**
1. AI works through each subtask one at a time
2. Each subtask gets its own feature branch
3. AI asks for your approval between subtasks
4. Test → Commit → Push → Merge → Repeat

---

## 📚 Phase-to-File Mapping

| Phase | PRD File | Task File | Status |
|-------|----------|-----------|--------|
| Phase 1: Project Skeleton | `0001-prd-project-setup.md` | `tasks-0001-prd-project-setup.md` | ✅ Complete |
| Phase 2: Simple Agent Foundation | `0002-prd-simple-agent-foundation.md` | `tasks-0002-prd-simple-agent-foundation.md` | ⏳ Next |
| Phase 3: Supervisor + First Worker | `0003-prd-supervisor-first-worker.md` | `tasks-0003-prd-supervisor-first-worker.md` | 📋 Planned |
| Phase 4: Remaining Workers | `0004-prd-remaining-workers.md` | `tasks-0004-prd-remaining-workers.md` | 📋 Planned |
| Phase 5: RAG/CAG Implementation | `0005-prd-rag-cag-implementation.md` | `tasks-0005-prd-rag-cag-implementation.md` | 📋 Planned |
| Phase 6: Multi-Provider & Polish | `0006-prd-polish-multi-provider.md` | `tasks-0006-prd-polish-multi-provider.md` | 📋 Planned |

---

## 🛠️ Task Execution Rules

### From `@process-task-list.mdc`:

1. **ONE SUB-TASK AT A TIME**
   - Complete subtask
   - Create feature branch: `feat/<task-number>-<subtask-name>`
   - Commit with conventional commits
   - Push feature branch
   - Merge to main with `--no-ff`
   - Push main
   - PAUSE for approval

2. **Branch Naming**
   - Format: `feat/<task-number>-<subtask-name>`
   - Example: `feat/2.1-integrate-langchain`

3. **Commit Messages**
   ```bash
   git commit -m "feat: <short summary>" \
   -m "- Key change 1" \
   -m "- Key change 2" \
   -m "Related to Task X.Y in PRD-NNNN"
   ```

4. **Completion Protocol**
   - Mark subtask `[x]` in task list
   - Run tests (if applicable)
   - Clean up temporary files
   - Commit changes
   - Push feature branch
   - Merge to main
   - Push main
   - Wait for approval before next subtask

---

## 🎬 Quick Start: Begin Phase 2

Ready to start Phase 2? Copy this prompt:

```
Using @create-prd.mdc, create a PRD for Phase 2 of @PHASED_DEVELOPMENT_GUIDE.md 
(Simple Agent Foundation). This phase includes:
- Integrating LangChain/LangGraph
- Adding real LLM responses (OpenAI)
- Implementing conversation memory
- Replace echo response with actual agent

Please ask clarifying questions before generating the PRD.
```

**Remember**: Switch to **agent mode** first! 🚀

---

## 📖 Reference Documents

- `@PHASED_DEVELOPMENT_GUIDE.md` - Overall project phases and objectives
- `@create-prd.mdc` - PRD generation rules
- `@generate-tasks.mdc` - Task list generation rules
- `@process-task-list.mdc` - Task execution workflow

---

## 💡 Tips

1. **Always review PRDs before generating tasks**
   - Make sure requirements are clear
   - Ask questions if anything is ambiguous

2. **Review task lists before execution**
   - Check parent tasks make sense
   - Verify sub-tasks are properly scoped

3. **Test between subtasks**
   - Don't wait until the end to test
   - Catch issues early

4. **Use Git strategically**
   - Each feature branch is a safety net
   - Can rollback if needed

5. **Reference existing code**
   - Look at Phase 1 implementation patterns
   - Maintain consistency

---

## 🎯 Success Metrics

After each phase:
- [ ] All deliverables completed
- [ ] Success criteria met
- [ ] Manual testing passed
- [ ] Code committed to Git
- [ ] README updated
- [ ] Known issues documented

---

**Happy Coding! 🚀**

