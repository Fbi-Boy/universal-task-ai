"use client";

import { useState } from "react";
import {
  Activity, ArrowDownRight, ArrowRight, ArrowUpRight, Bell, Blocks, Bot, Check,
  ChevronDown, ChevronRight, CircleHelp, Clock3, Command, Cpu, Database, FileText,
  GitBranch, Globe2, LayoutDashboard, LockKeyhole, MessageSquare, MoreHorizontal,
  Play, Plus, Search, Settings2, ShieldCheck, Sparkles, Workflow, Zap, Menu, X,
  RotateCcw, SlidersHorizontal, CircleDot, CheckCircle2, Timer, Webhook,
  type LucideIcon,
} from "lucide-react";

type PageKey = "Overview" | "AI Workspace" | "Workflows" | "Agents" | "Runs" | "Approvals" | "Integrations" | "Settings";

const navigation: { label: PageKey; icon: typeof LayoutDashboard; group: string }[] = [
  { label: "Overview", icon: LayoutDashboard, group: "WORKSPACE" },
  { label: "AI Workspace", icon: MessageSquare, group: "WORKSPACE" },
  { label: "Workflows", icon: Workflow, group: "WORKSPACE" },
  { label: "Agents", icon: Bot, group: "WORKSPACE" },
  { label: "Runs", icon: Activity, group: "MONITOR" },
  { label: "Approvals", icon: ShieldCheck, group: "MONITOR" },
  { label: "Integrations", icon: Blocks, group: "BUILD" },
  { label: "Settings", icon: Settings2, group: "BUILD" },
];

type WorkflowNode = {
  id: number;
  type: string;
  label: string;
  detail: string;
  icon: LucideIcon;
  color: string;
};

type LibraryCategory = "TRIGGERS" | "AI & LOGIC" | "ACTIONS";

type LibraryNodeDefinition = {
  category: LibraryCategory;
  nodeType: string;
  title: string;
  detail: string;
  icon: LucideIcon;
  tone: string;
};

const libraryCategories: LibraryCategory[] = ["TRIGGERS", "AI & LOGIC", "ACTIONS"];

const nodeCatalog: LibraryNodeDefinition[] = [
  { category: "TRIGGERS", nodeType: "trigger", title: "Webhook", detail: "Incoming HTTP event", icon: Webhook, tone: "violet" },
  { category: "TRIGGERS", nodeType: "trigger", title: "Schedule", detail: "Run at a set time", icon: Clock3, tone: "orange" },
  { category: "TRIGGERS", nodeType: "trigger", title: "Chat message", detail: "User starts a task", icon: MessageSquare, tone: "blue" },
  { category: "AI & LOGIC", nodeType: "agent", title: "AI Agent", detail: "Reason and plan", icon: Sparkles, tone: "violet" },
  { category: "AI & LOGIC", nodeType: "condition", title: "Condition", detail: "Branch by a rule", icon: GitBranch, tone: "teal" },
  { category: "AI & LOGIC", nodeType: "action", title: "Code step", detail: "Sandboxed execution", icon: Cpu, tone: "blue" },
  { category: "ACTIONS", nodeType: "action", title: "HTTP request", detail: "Allowlisted endpoints", icon: Globe2, tone: "teal" },
  { category: "ACTIONS", nodeType: "output", title: "Create artifact", detail: "Code, ERD, document", icon: FileText, tone: "green" },
  { category: "ACTIONS", nodeType: "approval", title: "Human approval", detail: "Pause for review", icon: ShieldCheck, tone: "orange" },
];

const initialNodes: WorkflowNode[] = [
  { id: 1, type: "trigger", label: "When a task arrives", detail: "Chat / webhook trigger", icon: Zap, color: "violet" },
  { id: 2, type: "agent", label: "Understand the goal", detail: "Task Analyzer", icon: Sparkles, color: "blue" },
  { id: 3, type: "agent", label: "Plan & route", detail: "Orchestrator", icon: GitBranch, color: "teal" },
  { id: 4, type: "action", label: "Execute approved tools", detail: "Permission boundary", icon: ShieldCheck, color: "orange" },
  { id: 5, type: "output", label: "Review & deliver", detail: "Reviewer agent", icon: CheckCircle2, color: "green" },
];

const activities = [
  { title: "Weekly research brief", detail: "Research Agent · completed 2 min ago", status: "Completed", color: "green", icon: Globe2 },
  { title: "Review database schema", detail: "Coding Agent · awaiting approval", status: "Needs review", color: "amber", icon: Database },
  { title: "Summarize project notes", detail: "Document Agent · completed 18 min ago", status: "Completed", color: "green", icon: FileText },
  { title: "Campus portal watcher", detail: "Scheduled workflow · next run in 42 min", status: "Scheduled", color: "blue", icon: Clock3 },
];

export default function Home() {
  const [activePage, setActivePage] = useState<PageKey>("Overview");
  const [nodes, setNodes] = useState<WorkflowNode[]>(initialNodes);
  const [selectedNodeId, setSelectedNodeId] = useState<number | null>(null);
  const [canvasZoom, setCanvasZoom] = useState(100);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [workflowName, setWorkflowName] = useState("Universal task pipeline");
  const [toast, setToast] = useState("");
  const [taskPrompt, setTaskPrompt] = useState("");
  const [requireApproval, setRequireApproval] = useState(true);
  const [auditEveryStep, setAuditEveryStep] = useState(true);
  const [nodeSearch, setNodeSearch] = useState("");

  function notify(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(""), 2600);
  }

  function addNode() {
    const id = Math.max(0, ...nodes.map((node) => node.id)) + 1;
    setNodes([...nodes, { id, type: "action", label: "New workflow step", detail: "Configure this step", icon: Blocks, color: "blue" }]);
    setSelectedNodeId(id);
    notify("Step added to the visual draft. Save/run integration is not connected yet.");
  }

  function addLibraryNode(node: Omit<WorkflowNode, "id">) {
    const id = Math.max(0, ...nodes.map((item) => item.id)) + 1;
    setNodes([...nodes, { ...node, id }]);
    setSelectedNodeId(id);
    notify(`${node.label} added to the visual draft. Save/run integration is not connected yet.`);
  }

  const normalizedNodeSearch = nodeSearch.trim().toLowerCase();
  const filteredLibraryNodes = nodeCatalog.filter((node) =>
    `${node.category} ${node.title} ${node.detail}`.toLowerCase().includes(normalizedNodeSearch),
  );

  const selectedNode = nodes.find((node) => node.id === selectedNodeId) ?? null;
  const SelectedNodeIcon = selectedNode?.icon;
  const isWorkflow = activePage === "Workflows";
  const pageHeading = activePage === "Overview" ? "Good evening, builder." : activePage;
  const pageSubheading = activePage === "Overview"
    ? "Your AI operations, workflows, and agents — all in one command center."
    : activePage === "Workflows"
      ? "Design automation visually, connect steps, and inspect every execution."
      : "Manage your workspace with clear visibility and secure control.";

  return (
    <main className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <div className="brand-row">
          <div className="brand-mark"><Sparkles size={19} strokeWidth={2.2} /></div>
          <div className="brand-name">universal<span>TASK AI</span></div>
          <button className="icon-btn mobile-close" onClick={() => setSidebarOpen(false)} aria-label="Close navigation"><X size={17} /></button>
        </div>
        <button className="workspace-select" onClick={() => notify("Personal workspace selected")}>
          <span className="workspace-avatar">F</span><span className="workspace-copy"><b>Personal workspace</b><small>Free plan · Local mode</small></span><ChevronDown size={15} />
        </button>
        <button className="search-control" onClick={() => notify("Search is coming with the workspace data API")}><Search size={16} /><span>Search anything...</span><kbd>⌘ K</kbd></button>
        {(["WORKSPACE", "MONITOR", "BUILD"] as const).map((group) => (
          <div className="nav-group" key={group}>
            <div className="nav-caption">{group}</div>
            {navigation.filter((item) => item.group === group).map(({ label, icon: Icon }) => (
              <button key={label} className={`nav-item ${activePage === label ? "nav-active" : ""}`} onClick={() => { setActivePage(label); setSidebarOpen(false); }}>
                <Icon size={17} strokeWidth={1.8} /><span>{label}</span>
                {label === "Approvals" && <span className="nav-badge">2</span>}
                {activePage === label && <span className="nav-active-mark" />}
              </button>
            ))}
          </div>
        ))}
        <div className="sidebar-bottom">
          <div className="plan-card"><div className="plan-card-top"><span className="plan-icon"><Zap size={15} /></span><span className="plan-label">WORKSPACE HEALTH</span><span className="health-dot" /></div><b>Security-first runtime</b><p>Capabilities stay permissioned by default.</p><div className="health-bar"><span /></div><div className="health-foot"><span>Policy controls</span><b>Active</b></div></div>
          <button className="user-profile" onClick={() => setActivePage("Settings")}><span className="user-avatar">F</span><span><b>Local user</b><small>Personal workspace</small></span><MoreHorizontal size={17} /></button>
        </div>
      </aside>

      {sidebarOpen && <button className="mobile-backdrop" aria-label="Close navigation" onClick={() => setSidebarOpen(false)} />}
      <section className="main-area">
        <header className="topbar">
          <div className="crumbs"><button className="icon-btn mobile-menu" onClick={() => setSidebarOpen(true)} aria-label="Open navigation"><Menu size={18} /></button><span>Workspace</span><ChevronRight size={14} /><b>{activePage}</b></div>
          <div className="topbar-right"><span className="environment-pill"><span className="health-dot" /> Local environment</span><button className="icon-btn" aria-label="Notifications" onClick={() => setActivePage("Approvals")}><Bell size={17} /><i /></button><button className="help-btn" onClick={() => notify("Help center will be connected in a later milestone")}><CircleHelp size={16} /> Help</button><span className="top-avatar">F</span></div>
        </header>

        <div className="content">
          <div className="page-head">
            <div><div className="overline"><span className="overline-line" /> COMMAND CENTER <span className="overline-dot">·</span> OCTOBER 15, 2026</div><h1>{pageHeading}</h1><p>{pageSubheading}</p></div>
            <div className="page-head-actions"><button className="btn btn-secondary" onClick={() => setActivePage("Workflows")}><Workflow size={16} /> Explore workflows</button><button className="btn btn-primary" onClick={() => setActivePage("AI Workspace")}><Plus size={17} /> New task</button></div>
          </div>

          {activePage === "Overview" && <>
            <section className="welcome-banner">
              <div className="banner-glow" /><div className="banner-content"><div className="banner-kicker"><Sparkles size={14} /> YOUR AI OPERATIONS, CONNECTED</div><h2>Make busywork<br /><em>disappear.</em></h2><p>Bring your tasks, tools, and automations into one thoughtful workspace. You stay in control at every step.</p><div className="banner-actions"><button className="btn btn-white" onClick={() => setActivePage("AI Workspace")}>Open AI workspace <ArrowUpRight size={16} /></button><button className="text-btn" onClick={() => setActivePage("Workflows")}>Explore automation <ArrowRight size={15} /></button></div></div><div className="banner-art" aria-hidden="true"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="orbit orbit-three" /><div className="core-glow"><Sparkles size={35} /></div><div className="float-chip chip-a"><Bot size={16} /><span>AI agents</span></div><div className="float-chip chip-b"><Workflow size={16} /><span>Workflows</span></div><div className="float-chip chip-c"><ShieldCheck size={16} /><span>Guardrails</span></div><div className="float-chip chip-d"><Zap size={16} /><span>Automation</span></div></div>
            </section>

            <div className="section-title-row"><div><h2>Workspace overview</h2><p>Preview data only — metrics and activity are illustrative, not live workspace data.</p></div><button className="date-filter" onClick={() => notify("Metrics will be populated from live run analytics")}><SlidersHorizontal size={15} /> Last 7 days <ChevronDown size={14} /></button></div>
            <section className="metric-grid">
              <Metric icon={Activity} label="Total executions" value="1,284" change="+12.8%" tone="violet" note="vs previous 7 days" />
              <Metric icon={CheckCircle2} label="Successful runs" value="1,196" change="93.1%" tone="green" note="success rate" />
              <Metric icon={Timer} label="Time saved" value="42.6h" change="+8.4h" tone="blue" note="estimated this week" />
              <Metric icon={Bot} label="Active agents" value="08" change="06 ready" tone="orange" note="2 need configuration" />
            </section>
            <div className="dashboard-grid">
              <section className="surface activity-surface"><div className="surface-head"><div><h3>Recent activity</h3><p>Latest updates from your workspace</p></div><button className="subtle-link" onClick={() => setActivePage("Runs")}>View all <ArrowUpRight size={14} /></button></div><div className="activity-list">{activities.map((item) => { const Icon = item.icon; return <div className="activity-row" key={item.title}><span className={`activity-icon ${item.color}`}><Icon size={17} /></span><span className="activity-copy"><b>{item.title}</b><small>{item.detail}</small></span><span className={`status-label ${item.color}`}>{item.status}</span><button className="icon-btn row-more" aria-label={`More about ${item.title}`} onClick={() => notify("Run details will open when connected to live run data")}><MoreHorizontal size={17} /></button></div>; })}</div></section>
              <section className="surface automation-surface"><div className="surface-head"><div><h3>Automation pulse</h3><p>Execution volume · illustrative preview</p></div><span className="tiny-live"><span className="health-dot" /> LIVE UI</span></div><div className="chart-wrap"><div className="chart-y"><span>200</span><span>150</span><span>100</span><span>50</span><span>0</span></div><svg className="chart" viewBox="0 0 440 160" preserveAspectRatio="none" role="img" aria-label="Illustrative automation activity chart"><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="#7667f6" stopOpacity=".22" /><stop offset="100%" stopColor="#7667f6" stopOpacity="0" /></linearGradient></defs>{[20,55,90,125].map(y => <line key={y} x1="0" x2="440" y1={y} y2={y} stroke="#ececf4" strokeDasharray="4 5" />)}<path d="M0 119 C25 110 28 81 54 91 S83 111 110 75 S149 88 171 63 S205 78 231 48 S268 73 291 59 S328 39 348 51 S385 18 410 28 L440 15 L440 145 L0 145 Z" fill="url(#area)" /><path d="M0 119 C25 110 28 81 54 91 S83 111 110 75 S149 88 171 63 S205 78 231 48 S268 73 291 59 S328 39 348 51 S385 18 410 28 L440 15" fill="none" stroke="#7767ed" strokeWidth="2.5" strokeLinecap="round" /></svg></div><div className="chart-x"><span>MON</span><span>TUE</span><span>WED</span><span>THU</span><span>FRI</span><span>SAT</span><span>SUN</span></div><div className="chart-footer"><span><i className="legend-dot" /> Executions</span><b>Preview only <ArrowUpRight size={13} /></b></div></section>
            </div>
            <section className="surface workflow-preview"><div className="surface-head"><div><h3>Featured workflow</h3><p>Your reusable task pipeline</p></div><button className="btn btn-secondary btn-small" onClick={() => setActivePage("Workflows")}>Open editor <ArrowUpRight size={14} /></button></div><div className="workflow-mini"><div className="mini-flow-node"><span className="mini-node-icon violet"><Webhook size={17} /></span><b>Task trigger</b><small>On new request</small></div><span className="mini-connector" /><div className="mini-flow-node"><span className="mini-node-icon blue"><Sparkles size={17} /></span><b>Analyze intent</b><small>Task Analyzer</small></div><span className="mini-connector" /><div className="mini-flow-node"><span className="mini-node-icon teal"><GitBranch size={17} /></span><b>Plan & route</b><small>Orchestrator</small></div><span className="mini-connector" /><div className="mini-flow-node"><span className="mini-node-icon orange"><ShieldCheck size={17} /></span><b>Execute safely</b><small>Policy boundary</small></div><span className="mini-connector" /><div className="mini-flow-node"><span className="mini-node-icon green"><Check size={17} /></span><b>Review</b><small>Quality gate</small></div></div></section>
          </>}

          {activePage === "AI Workspace" && <section className="surface workspace-chat"><div className="chat-welcome"><div className="chat-spark"><Sparkles size={25} /></div><span className="overline">UNIVERSAL TASK ASSISTANT</span><h2>What can I help you build?</h2><p>Describe the outcome. The task engine will plan the work and apply configured permissions.</p></div><textarea value={taskPrompt} onChange={(e) => setTaskPrompt(e.target.value)} placeholder="Ask anything… e.g. Research these APIs and create a secure integration plan."/><div className="chat-bottom"><span><LockKeyhole size={14}/> Sensitive actions require approval</span><button className="btn btn-primary" onClick={() => notify(taskPrompt.trim() ? "Task API integration is the next step; this screen is currently a UI prototype." : "Enter a task first.")}><ArrowUpRight size={16}/> Submit task</button></div><div className="prompt-chips">{["Create an ERD for my app","Research a programming topic","Build a workflow","Review a codebase"].map((item) => <button key={item} onClick={() => setTaskPrompt(item)}>{item}<ArrowUpRight size={13}/></button>)}</div></section>}

          {isWorkflow && <section className="workflow-editor">
            <div className="editor-toolbar surface"><div className="workflow-name"><span className="workflow-name-icon"><Workflow size={17}/></span><input aria-label="Workflow name" value={workflowName} onChange={(e) => setWorkflowName(e.target.value)}/><span className="draft-pill">DRAFT</span></div><div className="editor-actions"><button className="btn btn-secondary" onClick={addNode}><Plus size={15}/> Add step</button><button className="btn btn-primary" onClick={() => notify("Workflow execution is not connected yet. This canvas is a visual draft.")}><Play size={15} fill="currentColor"/> Test workflow</button><button className="icon-btn" onClick={() => notify("Workflow save API is not connected yet")} aria-label="More workflow actions"><MoreHorizontal size={18}/></button></div></div>
            <div className="workflow-layout"><aside className="node-library surface"><div className="library-heading"><div><h3>Node library</h3><p>Drag-and-drop coming next</p></div><Search size={16}/></div><label className="node-search"><Search size={15} aria-hidden="true"/><input type="search" aria-label="Find a node" placeholder="Find a node..." value={nodeSearch} onChange={(event) => setNodeSearch(event.target.value)}/></label>{libraryCategories.map((category) => { const entries = filteredLibraryNodes.filter((node) => node.category === category); if (entries.length === 0) return null; return <div className="library-category" key={category}><p className="library-label">{category}</p>{entries.map((node) => <LibraryNode key={node.title} icon={node.icon} title={node.title} detail={node.detail} tone={node.tone} nodeType={node.nodeType} onAdd={addLibraryNode}/>)}</div>; })}{filteredLibraryNodes.length === 0 && <p className="library-empty" role="status">No nodes match “{nodeSearch.trim()}”.</p>}</aside>
              <div className="canvas-shell"><div className="canvas-top"><div><span className="canvas-live-dot"/><b>Workflow canvas</b><span className="canvas-sub">· Visual builder</span></div><div className="canvas-controls"><button className="icon-btn" onClick={() => setCanvasZoom((zoom) => Math.max(60, zoom - 10))} aria-label="Zoom out" disabled={canvasZoom <= 60}>−</button><span aria-live="polite">{canvasZoom}%</span><button className="icon-btn" onClick={() => setCanvasZoom((zoom) => Math.min(140, zoom + 10))} aria-label="Zoom in" disabled={canvasZoom >= 140}>+</button><button className="icon-btn" onClick={() => setCanvasZoom(100)} aria-label="Reset zoom" disabled={canvasZoom === 100}><RotateCcw size={15}/></button></div></div>
                <div className="canvas-grid" style={{ zoom: canvasZoom / 100 }}><div className="flow-column">{nodes.map((node, index) => { const Icon = node.icon; return <div className="node-and-link" key={node.id}><button className={selectedNodeId === node.id ? "flow-node flow-node-selected" : "flow-node"} aria-pressed={selectedNodeId === node.id} onClick={() => setSelectedNodeId(node.id)}><span className={"node-icon " + node.color}><Icon size={18}/></span><span className="node-copy"><b>{node.label}</b><small>{node.detail}</small></span><MoreHorizontal size={16} className="node-more"/></button>{index < nodes.length - 1 && <div className="node-link"><span/><i/></div>}</div>; })}<button className="add-node" onClick={addNode}><Plus size={16}/> Add another step</button></div><div className="canvas-note"><span><LockKeyhole size={14}/></span><b>Policy preview only</b><p>These local settings do not enforce policy. A real runtime must enforce approvals before any live tool action.</p></div></div>
              </div><aside className="properties-panel surface"><div className="properties-heading"><div><h3>Workflow settings</h3><p>Pipeline configuration</p></div><Settings2 size={16}/></div>{selectedNode && SelectedNodeIcon ? <section className="selected-node-summary" aria-live="polite"><div className="selected-node-heading"><span className={"node-icon " + selectedNode.color}><SelectedNodeIcon size={16}/></span><div><span className="selected-node-eyebrow">SELECTED NODE</span><h4>{selectedNode.label}</h4></div></div><p>{selectedNode.detail}</p><span className="selected-node-type">Type: {selectedNode.type}</span><p className="selected-node-note">Selection only — node configuration is not implemented yet.</p></section> : <div className="selected-node-empty" role="status">Select a node on the canvas to inspect its summary.</div>}<label className="setting-label">Workflow name<input value={workflowName} onChange={(e) => setWorkflowName(e.target.value)}/></label><label className="setting-label">Execution mode<select defaultValue="approval"><option value="approval">Approval-first</option><option value="manual">Manual trigger</option><option value="schedule">Scheduled</option></select></label><div className="settings-divider"/><div className="setting-row"><span><b>Require approval</b><small>For sensitive actions</small></span><button type="button" role="switch" aria-label="Require approval" aria-checked={requireApproval} className={`toggle ${requireApproval ? "on" : ""}`} onClick={() => setRequireApproval((current) => !current)}/></div><div className="setting-row"><span><b>Audit every step</b><small>Keep execution history</small></span><button type="button" role="switch" aria-label="Audit every step" aria-checked={auditEveryStep} className={`toggle ${auditEveryStep ? "on" : ""}`} onClick={() => setAuditEveryStep((current) => !current)}/></div><div className="setting-row"><span><b>Allow unrestricted shell</b><small>Disabled by policy</small></span><span className="toggle locked" aria-label="Unrestricted shell disabled"><LockKeyhole size={12}/></span></div><div className="properties-foot"><ShieldCheck size={16}/><span>Local policy preview</span></div></aside></div>
            <div className="editor-disclaimer"><CircleDot size={14}/> Visual editor prototype — nodes, draft name, and approval/audit preview switches are interactive. These switches do not enforce runtime policy or emit audit logs; persistent save, drag-and-drop, and live execution are not connected.</div>
          </section>}

          {!["Overview", "AI Workspace", "Workflows"].includes(activePage) && <section className="surface coming-soon"><div className="coming-icon"><Blocks size={25}/></div><span className="overline">WORKSPACE MODULE</span><h2>{activePage}</h2><p>This module is planned in the product roadmap. The page shell is ready, and live data will be connected as the backend contract is implemented.</p><div className="coming-list"><span><CheckCircle2 size={16}/> Navigation and information architecture</span><span><CheckCircle2 size={16}/> Security-first interaction design</span><span><Timer size={16}/> Backend integration planned</span></div><button className="btn btn-secondary" onClick={() => setActivePage("Overview")}>Back to overview <ArrowRight size={15}/></button></section>}

          <footer className="footer"><span><Sparkles size={14}/> Universal Task AI</span><span>Designed for useful work. Built around trust.</span><a href="https://github.com/Fbi-Boy/universal-task-ai" target="_blank" rel="noreferrer">Repository <ArrowUpRight size={13}/></a></footer>
        </div>
      </section>
      {toast && <div className="toast" role="status"><CheckCircle2 size={17}/>{toast}</div>}
    </main>
  );
}

function Metric({ icon: Icon, label, value, change, tone, note }: { icon: typeof Activity; label: string; value: string; change: string; tone: string; note: string }) {
  return <article className="metric-card"><div className="metric-top"><span className={`metric-icon ${tone}`}><Icon size={18}/></span><button className="icon-btn" aria-label={`More about ${label}`}><MoreHorizontal size={17}/></button></div><span className="metric-label">{label}</span><div className="metric-value-row"><strong>{value}</strong><span className={`metric-change ${tone}`}>{tone === "green" || tone === "violet" ? <ArrowUpRight size={13}/> : <ArrowDownRight size={13}/>} {change}</span></div><small>{note}</small></article>;
}

function LibraryNode({ icon: Icon, title, detail, tone, nodeType, onAdd }: {
  icon: LucideIcon;
  title: string;
  detail: string;
  tone: string;
  nodeType: string;
  onAdd: (node: Omit<WorkflowNode, "id">) => void;
}) {
  return <button className="library-node" onClick={() => onAdd({ type: nodeType, label: title, detail, icon: Icon, color: tone })}><span className={`node-icon ${tone}`}><Icon size={16}/></span><span><b>{title}</b><small>{detail}</small></span><Plus size={14}/></button>;
}
