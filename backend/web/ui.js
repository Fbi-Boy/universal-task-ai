const task = document.querySelector("#task");
const counter = document.querySelector("#counter");
const apiKey = document.querySelector("#api-key");
const approvalActor = document.querySelector("#approval-actor");
const tool = document.querySelector("#tool");
const args = document.querySelector("#arguments");
const approvalRequired = document.querySelector("#approval-required");
const resultBox = document.querySelector("#result");
const statusBox = document.querySelector("#run-status");

apiKey.value = sessionStorage.getItem("uta_api_key") || "";
approvalActor.value = sessionStorage.getItem("uta_approval_actor") || "web-session";

function authHeaders(extra = {}) {
  const key = sessionStorage.getItem("uta_api_key") || "";
  return key ? {...extra, Authorization: "Bearer " + key} : extra;
}

async function json(url, options = {}) {
  const headers = authHeaders(options.headers || {});
  const response = await fetch(url, {...options, headers});
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

const healthDot = document.querySelector("#health-dot");
const workspaceSearch = document.querySelector(".search input");
const navLinks = Array.from(document.querySelectorAll(".primary-nav .nav"));

function setHealthStatus(status, online) {
  const health = document.querySelector("#health");
  health.textContent = status;
  healthDot.classList.toggle("is-online", Boolean(online));
  healthDot.classList.toggle("is-offline", !online);
  healthDot.setAttribute("aria-label", online ? "Service available" : "Service unavailable");
}

function setCounter() {
  counter.textContent = task.value.length.toLocaleString() + " / 20,000";
}

task.oninput = setCounter;

document.querySelectorAll(".quick button").forEach(button => {
  button.onclick = () => {
    task.value = button.dataset.template;
    task.focus();
    setCounter();
  };
});

document.querySelector("#save-key").onclick = () => {
  const value = apiKey.value.trim();
  if (value) sessionStorage.setItem("uta_api_key", value);
  else sessionStorage.removeItem("uta_api_key");
  refresh();
};

document.querySelector("#focus-task").onclick = () => task.focus();

workspaceSearch.oninput = () => {
  const query = workspaceSearch.value.trim().toLocaleLowerCase();
  navLinks.forEach(link => {
    link.hidden = Boolean(query) && !link.textContent.toLocaleLowerCase().includes(query);
  });
};
workspaceSearch.onkeydown = event => {
  if (event.key === "Enter") {
    const firstVisible = navLinks.find(link => !link.hidden);
    if (firstVisible) firstVisible.click();
  }
  if (event.key === "Escape") {
    workspaceSearch.value = "";
    workspaceSearch.dispatchEvent(new Event("input"));
    workspaceSearch.blur();
  }
};
document.addEventListener("keydown", event => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    workspaceSearch.focus();
  }
});

navLinks.forEach(link => {
  link.addEventListener("click", () => {
    navLinks.forEach(item => item.classList.toggle("active", item === link));
  });
});

document.querySelector("#clear-key").onclick = () => {
  sessionStorage.removeItem("uta_api_key");
  apiKey.value = "";
  refresh();
};

approvalActor.onchange = () => {
  const value = approvalActor.value.trim();
  if (value) sessionStorage.setItem("uta_approval_actor", value);
  else sessionStorage.removeItem("uta_approval_actor");
};

function approvalDecisionBody() {
  const actor = approvalActor.value.trim();
  if (!actor || actor.length > 128) throw new Error("Approval actor ID must be 1-128 characters.");
  sessionStorage.setItem("uta_approval_actor", actor);
  return JSON.stringify({actor_id: actor});
}

async function loadTools() {
  const items = await json("/v1/tools");
  tool.replaceChildren(new Option("Auto — safe intents only", ""));
  for (const item of items) {
    const label = item.name + (item.requires_approval ? " • approval" : "");
    tool.appendChild(new Option(label, item.name));
  }
}

async function refreshApprovals() {
  try {
    const approvals = await json("/v1/approvals");
    const target = document.querySelector("#approvals");
    target.replaceChildren();
    for (const approval of approvals) {
      const card = document.createElement("div");
      card.className = "card";
      card.textContent = approval.action + " — " + approval.state;
      if (approval.state === "pending") {
        const approve = document.createElement("button");
        approve.textContent = "Approve + resume";
        approve.onclick = async () => {
          try {
            await json("/v1/approvals/" + approval.approval_id + "/approve", {method: "POST", headers: {"content-type": "application/json"}, body: approvalDecisionBody()});
            const info = await json("/v1/approvals/" + approval.approval_id + "/execution");
            const resumed = await json("/v1/approvals/" + approval.approval_id + "/resume", {
              method: "POST",
              headers: {"content-type": "application/json"},
              body: JSON.stringify({
                run_id: info.run_id,
                approval_id: approval.approval_id,
                actor_id: approvalActor.value.trim()
              })
            });
            resultBox.textContent = resumed.output || "";
            statusBox.textContent = resumed.status;
            document.querySelector("#run-id").value = resumed.run_id;
            await refresh();
          } catch (error) {
            resultBox.textContent = String(error);
          }
        };
        card.appendChild(approve);

        const reject = document.createElement("button");
        reject.textContent = "Reject";
        reject.onclick = async () => {
          try {
            await json("/v1/approvals/" + approval.approval_id + "/reject", {method: "POST", headers: {"content-type": "application/json"}, body: approvalDecisionBody()});
            await refresh();
          } catch (error) {
            resultBox.textContent = String(error);
          }
        };
        card.appendChild(reject);
      }
      target.appendChild(card);
    }
  } catch (error) {
    document.querySelector("#approvals").textContent = "Authentication required or unavailable.";
  }
}

async function refreshRuns() {
  try {
    const runs = await json("/v1/runs?limit=20");
    const target = document.querySelector("#runs");
    target.replaceChildren();
    for (const run of runs) {
      const card = document.createElement("div");
      card.className = "card";
      card.textContent = run.run_id + " — " + run.status;
      target.appendChild(card);
    }
  } catch {
    document.querySelector("#runs").textContent = "Authentication required or unavailable.";
  }
}

async function refresh() {
  try {
    const health = await json("/health");
    setHealthStatus(health.status, health.status === "ok" || health.status === "ready");
  } catch {
    setHealthStatus("offline", false);
  }
  try {
    await loadTools();
  } catch {
    tool.replaceChildren(new Option("Set a valid API key to load tools", ""));
  }
  await refreshApprovals();
  await refreshRuns();
}

document.querySelector("#analyze").onclick = async () => {
  try {
    document.querySelector("#analysis").textContent = JSON.stringify(
      await json("/v1/tasks/analyze", {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify({task: task.value})
      }),
      null,
      2
    );
  } catch (error) {
    document.querySelector("#analysis").textContent = String(error);
  }
};

document.querySelector("#run").onclick = async () => {
  const taskText = task.value.trim();
  if (!taskText) {
    resultBox.textContent = "Task is required.";
    return;
  }

  let parsedArgs = {};
  try {
    parsedArgs = JSON.parse(args.value || "{}");
  } catch {
    resultBox.textContent = "Arguments JSON is invalid.";
    return;
  }

  const invocations = tool.value
    ? [{tool_name: tool.value, arguments: parsedArgs}]
    : [];

  statusBox.textContent = "running…";
  try {
    const response = await json("/v1/tasks", {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        task: taskText,
        tool_invocations: invocations,
        approval_required: approvalRequired.checked,
        auto_route_tools: !tool.value
      })
    });
    statusBox.textContent = response.status + " · route: " + response.routing_mode;
    const routedTools = Array.isArray(response.routed_tools) ? response.routed_tools : [];
    const routingSummary = routedTools.length ? "Tools: " + routedTools.join(", ") + "\n\n" : "No tools invoked.\n\n";
    resultBox.textContent = routingSummary + (response.output || "");
    document.querySelector("#run-id").value = response.run_id;
    await refresh();
  } catch (error) {
    statusBox.textContent = "failed";
    resultBox.textContent = String(error);
  }
};

let timer;
document.querySelector("#watch").onclick = () => {
  clearInterval(timer);
  const id = document.querySelector("#run-id").value.trim();
  let after = 0;
  const poll = async () => {
    if (!id) return;
    try {
      const events = await json("/v1/runs/" + encodeURIComponent(id) + "/events?after=" + after);
      if (events.length) {
        document.querySelector("#events").textContent += events
          .map(event => event.sequence + " " + event.kind + " " + event.detail)
          .join("\n") + "\n";
        after = events[events.length - 1].sequence;
      }
    } catch (error) {
      document.querySelector("#events").textContent = String(error);
    }
  };
  poll();
  timer = setInterval(poll, 1000);
};

setCounter();
refresh();
