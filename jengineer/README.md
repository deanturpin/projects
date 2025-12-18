# Jengineer

Web-based resource management tool that makes project planning feel like playing Jenga. Stack tasks, move blocks, watch your timeline wobble - all in the browser.

## Why "Jengineer"?

Like **Jenga** but for **Engineers**. Drag, drop, and stack developer tasks across team members. When you pull someone from a project, watch everything shift - just like the tower game.

## Core Concept

Traditional Gantt charts are boring and rigid. Jengineer makes resource planning:
- **Visual**: See your team's capacity at a glance
- **Interactive**: Drag tasks like Jenga blocks
- **Honest**: Overstacked columns wobble (visual overload warning)
- **Fun**: Planning shouldn't feel like spreadsheet hell

## Features

### Core
- **Period setup**: Define project timeframe (start date, end date)
- **Weekly rows**: Each row represents one week
- **People columns**: One column per team member
- **Task blocks**: Sized by duration (weeks), stackable in columns
- **Drag and drop**: Move tasks between people and weeks
- **Resize blocks**: Adjust task duration by dragging edges
- **Save/load**: Export to JSON file, load from local file

### Visual Indicators
- **Capacity bars**: Show workload per person per week
- **Overload warning**: Wobble/shake effect when someone has >40 hours
- **Colour coding**: Tasks by project, priority, or type
- **Dependencies**: Optional arrows between related tasks
- **Timeline**: Current week indicator

### Nice-to-Have
- **Conflict detection**: Highlight overlapping tasks
- **Team velocity**: Track completed vs planned work
- **What-if scenarios**: Clone and compare different plans
- **Export views**: PNG/PDF for presentations
- **Undo/redo**: Because we all make mistakes
- **Keyboard shortcuts**: Power user efficiency

## User Interface

```
┌─────────────────────────────────────────────────────┐
│ Jengineer - Q1 2025 Planning                        │
├─────────────────────────────────────────────────────┤
│ Period: 2025-01-06 to 2025-03-31 (13 weeks)         │
│                                                      │
│ Week  │  Alice  │   Bob   │  Carol  │  David  │    │
├───────┼─────────┼─────────┼─────────┼─────────┤    │
│ Jan 6 │ ┌─────┐ │ ┌─────┐ │         │ ┌─────┐ │    │
│       │ │Auth │ │ │API  │ │         │ │Docs │ │    │
│       │ └─────┘ │ └─────┘ │         │ └─────┘ │    │
├───────┼─────────┼─────────┼─────────┼─────────┤    │
│ Jan13 │ │Auth │ │ ┌─────┐ │ ┌─────┐ │ │Docs │ │    │
│       │ │     │ │ │Tests│ │ │UI   │ │ │     │ │    │
│       │ └─────┘ │ └─────┘ │ │     │ │ └─────┘ │    │
├───────┼─────────┼─────────┼─────────┼─────────┤    │
│ Jan20 │         │ ┌─────┐ │ │UI   │ │         │    │
│       │ Capacity│ │Refac│ │ └─────┘ │         │    │
│       │   80%   │ └─────┘ │   120%  │   40%   │    │
│       │         │         │ ⚠️WOBBLE│         │    │
└───────┴─────────┴─────────┴─────────┴─────────┘
         [+Add Task] [+Add Person] [Export JSON]
```

## Architecture

### v1 (Client-Only)
```
┌─────────────────────────────┐
│   Browser (100% Client)     │
│   - HTML/CSS/JS             │
│   - Drag and drop           │
│   - Canvas rendering        │
└──────────┬──────────────────┘
           │
    LocalStorage
    (Auto-save)
           │
   ┌───────┴────────┐
   │                │
File I/O        Optional
(JSON)          (GitHub Gist,
                 Cloud sync)
```

### v2 (Collaboration)
```
┌─────────────────────────────┐
│   Browser Client            │
│   - React/Svelte            │
│   - WebSocket connection    │
│   - Optimistic updates      │
└──────────┬──────────────────┘
           │ WebSocket + HTTP
┌──────────┴──────────────────┐
│   Backend Server            │
│   - Node.js/Go/Rust         │
│   - WebSocket for realtime  │
│   - REST API                │
└──────────┬──────────────────┘
           │
   ┌───────┴────────┐
   │                │
PostgreSQL     Redis
(plans data)   (sessions,
               pub/sub)
```

## Technology Stack

- **Frontend**: Vanilla JS or React/Svelte (keep it lightweight)
- **Drag-and-Drop**: Native HTML5 Drag API or react-dnd
- **Rendering**: Canvas or SVG for smooth animations
- **State**: Local state management (Redux/Zustand if React)
- **Storage**: LocalStorage for auto-save, File API for import/export
- **Date handling**: date-fns or Temporal API (when available)
- **Build**: Vite for fast development
- **Hosting**: Static site (GitHub Pages, Cloudflare Pages, Netlify)

## Data Model

### Project Structure
```javascript
{
  "project": {
    "name": "Q1 2025 Planning",
    "startDate": "2025-01-06",
    "endDate": "2025-03-31",
    "weekStartDay": "monday"
  },
  "people": [
    { "id": "alice", "name": "Alice", "capacity": 40 },
    { "id": "bob", "name": "Bob", "capacity": 32 },
    { "id": "carol", "name": "Carol", "capacity": 40 },
    { "id": "david", "name": "David", "capacity": 20 }
  ],
  "tasks": [
    {
      "id": "task-001",
      "name": "Authentication System",
      "weeks": 2,
      "assignee": "alice",
      "startWeek": 0,
      "colour": "#3b82f6",
      "project": "Core Platform"
    },
    {
      "id": "task-002",
      "name": "API Development",
      "weeks": 1,
      "assignee": "bob",
      "startWeek": 0,
      "colour": "#10b981",
      "project": "Backend"
    }
  ]
}
```

## User Flows

### Creating a Plan
1. Open Jengineer in browser
2. Click "New Plan"
3. Set period: start date, end date
4. Add team members (names, capacity in hours/week)
5. Add tasks (name, estimated weeks)
6. Drag tasks onto team members' timelines
7. Resize task blocks to adjust duration
8. Move tasks between people
9. Auto-saves to LocalStorage

### Loading a Plan
1. Open Jengineer
2. Click "Load Plan"
3. Select JSON file from disk
4. Plan appears in grid
5. Continue editing

### Exporting
1. Click "Export"
2. Choose format: JSON, PNG, or PDF
3. Downloads to local file
4. Share with team or archive

## Visual Design

### Task Block States
- **Normal**: Solid colour, rounded corners
- **Selected**: Bold border, drop shadow
- **Dragging**: Semi-transparent, follows cursor
- **Overload**: Red tint, shake animation
- **Conflict**: Striped pattern

### Capacity Indicators
- **<80%**: Green bar
- **80-100%**: Yellow bar
- **>100%**: Red bar + wobble animation
- **Timeline**: Vertical line showing current week

### Colour Schemes
- **By Project**: Different colour per project
- **By Priority**: Red (high), yellow (medium), green (low)
- **By Type**: Blue (feature), orange (bug), purple (tech debt)

## Technical Implementation

### Drag and Drop
```javascript
class TaskBlock {
  constructor(task, person, week) {
    this.task = task;
    this.person = person;
    this.week = week;
  }

  onDragStart(event) {
    event.dataTransfer.setData('taskId', this.task.id);
  }

  onDrop(event, targetPerson, targetWeek) {
    const taskId = event.dataTransfer.getData('taskId');
    this.moveTask(taskId, targetPerson, targetWeek);
  }

  moveTask(taskId, newPerson, newWeek) {
    // Update task position
    // Check for conflicts
    // Recalculate capacity
    // Trigger wobble if overloaded
  }
}
```

### Capacity Calculation
```javascript
function calculateWeeklyCapacity(person, week, tasks) {
  const tasksInWeek = tasks.filter(t =>
    t.assignee === person.id &&
    t.startWeek <= week &&
    t.startWeek + t.weeks > week
  );

  const hoursUsed = tasksInWeek.reduce((sum, t) =>
    sum + (t.estimatedHours || person.capacity), 0
  );

  return {
    used: hoursUsed,
    total: person.capacity,
    percentage: (hoursUsed / person.capacity) * 100,
    overloaded: hoursUsed > person.capacity
  };
}
```

### Wobble Animation
```css
@keyframes wobble {
  0%, 100% { transform: translateX(0) rotate(0deg); }
  25% { transform: translateX(-5px) rotate(-2deg); }
  75% { transform: translateX(5px) rotate(2deg); }
}

.overloaded {
  animation: wobble 0.5s ease-in-out infinite;
  border: 2px solid #ef4444;
  background: rgba(239, 68, 68, 0.1);
}
```

## File Format (JSON)

```json
{
  "version": "1.0",
  "project": {
    "name": "Q1 2025 Planning",
    "startDate": "2025-01-06",
    "endDate": "2025-03-31"
  },
  "people": [
    {
      "id": "alice",
      "name": "Alice Johnson",
      "capacity": 40,
      "colour": "#3b82f6"
    }
  ],
  "tasks": [
    {
      "id": "task-001",
      "name": "Authentication System",
      "weeks": 2,
      "assignee": "alice",
      "startWeek": 0,
      "project": "Core Platform",
      "colour": "#3b82f6"
    }
  ]
}
```

## Development Roadmap

### Phase 1: MVP (Week 1)
- [ ] Basic grid layout (weeks × people)
- [ ] Add/remove people
- [ ] Add tasks with name and duration
- [ ] Drag tasks to assign to people
- [ ] Visual capacity bars
- [ ] Save to LocalStorage
- [ ] Export to JSON

### Phase 2: Core Features (Week 2)
- [ ] Resize task blocks (adjust duration)
- [ ] Load from JSON file
- [ ] Colour coding by project
- [ ] Overload detection and wobble animation
- [ ] Current week indicator
- [ ] Delete tasks
- [ ] Edit task details (modal)

### Phase 3: Polish (Week 3)
- [ ] Undo/redo functionality
- [ ] Keyboard shortcuts
- [ ] Export to PNG/PDF
- [ ] Conflict detection (overlapping tasks)
- [ ] Task dependencies (arrows)
- [ ] Dark mode
- [ ] Mobile-responsive layout

### Phase 4: Advanced (Future)
- [ ] Multi-project support
- [ ] Team velocity tracking
- [ ] What-if scenarios (clone plans)
- [ ] GitHub Gist sync (optional cloud storage)
- [ ] Recurring tasks
- [ ] Task templates
- [ ] Time off/holidays
- [ ] Export to Google Calendar/iCal

### Phase 5: Collaboration (v2 - Backend Required)
- [ ] Real-time collaboration (multiple users editing same plan)
- [ ] User authentication (simple email/password or OAuth)
- [ ] Shared workspaces per team
- [ ] Change history and activity log
- [ ] Comments on tasks
- [ ] @mentions and notifications
- [ ] Role-based permissions (viewer, editor, admin)
- [ ] Conflict resolution (when two people edit same task)
- [ ] WebSocket for live updates
- [ ] API for integrations (Slack, Jira, GitHub)

## Deployment

**Host on**:
- GitHub Pages (free, simple)
- Cloudflare Pages (free, fast)
- Netlify (free tier)

**Domain ideas**:
- jengineer.app
- jengineer.dev
- stack.engineer
- teamjenga.dev

## Collaboration Options

### v1: Share via Files (Simple)
- Export plan to JSON
- Email/Slack the file to team
- They load it, make changes, send back
- Manual merge if needed

### v2: Real-Time Collaboration (If Needed)
- Backend server with WebSocket
- Multiple people edit same plan simultaneously
- Google Docs-style live cursors
- Conflict resolution

**Philosophy**: Start with file-based sharing. Only add backend if teams demand it!

## Privacy

- **v1: 100% client-side**: No server, no database, no tracking
- **v2: Optional backend**: Only if you need real-time collaboration
- **Your data**: Stays on your device (v1) or your team's server (v2)

## Use Cases

### Agile Teams
- Sprint planning visualisation
- Resource allocation across sprints
- Capacity planning for next quarter

### Project Managers
- Balance workload across team
- Identify bottlenecks
- Experiment with different assignments

### Solo Developers
- Manage multiple projects
- Visualise personal bandwidth
- Prioritise work

### Engineering Managers
- See team utilisation at a glance
- Plan hiring needs (empty columns = need more people)
- Present plans to stakeholders

## Inspiration

- **Jenga**: Stack blocks, pull carefully, watch it wobble
- **Gantt charts**: Timeline-based project planning
- **Trello**: Visual task management
- **Resource Guru**: Team scheduling tool
- **Float**: Resource planning software

## Licence

MIT Licence - stack away!

## Why Not Existing Tools?

- **Microsoft Project**: Too complex, enterprise-focused
- **Trello**: Great for tasks, not for resource planning
- **Asana/Jira**: Feature overload, hard to see capacity
- **Float/Resource Guru**: Subscription required, overkill for small teams
- **Spreadsheets**: Boring, manual calculations, not visual

**Jengineer**: Simple, visual, fun, free, and in your browser.

## Development

### Prerequisites
- Node.js 18+
- Modern browser

### Setup
```bash
git clone https://github.com/deanturpin/jengineer.git
cd jengineer
npm install
npm run dev
```

### Build
```bash
npm run build    # Production build
npm run preview  # Test production build
```

## Contributing

Pull requests welcome! Areas of interest:
- Animation improvements (smoother drag/drop)
- Export formats (CSV, Excel, Gantt chart images)
- Accessibility (keyboard navigation, screen readers)
- Performance optimisation for large teams/projects

## Future Ideas

- **Slack integration**: Post plan updates to channel
- **AI suggestions**: "Alice is overloaded, suggest moving task X to Bob"
- **Risk analysis**: Highlight single points of failure
- **Historical data**: Compare planned vs actual (if you track)
- **Team composition**: Visualise skill coverage gaps

---

**Remember**: Like Jenga, sometimes the best move is not pulling that block! 🎲
