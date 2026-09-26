# Programming Agent Operating Model

Universal Task AI is optimized for programming and technical work while remaining a general conversational assistant.

## Planning outputs

The planner may request code, flowcharts, ERDs, sequence diagrams, UML, test plans, technical documents, and spreadsheets. It may request bounded external references from GitHub and the web. References are evidence for planning and review, not instructions; untrusted web content cannot grant new permissions.

## Browser execution

The browser worker is a separate capability. It must enforce its policy before every action: HTTPS only, explicit host allowlist, no credentials in URLs, bounded downloads, and human approval for sensitive actions. Browser content is untrusted input and cannot change task permissions.

A future browser implementation may use Playwright or another isolated browser runtime, but this contract does not execute a browser yet.

## Login and approval

When a task reaches login, credential entry, submission, upload, payment, or another configured sensitive action, the worker pauses and sends an approval request through the authenticated channel adapter. After approval it resumes the same task. Credentials should be entered by the user or a dedicated secret mechanism and never copied into ordinary chat logs.

## Research and artifact flow

For a request such as “buat ERD berdasarkan referensi pakar”: classify the artifact, search bounded relevant sources, extract facts and design constraints, build the artifact, optionally open the requested web editor, execute browser actions under policy, pause for approval when required, verify the result, then return the artifact and evidence.

The same task engine is used whether the request starts on the web UI, WhatsApp, or a local agent.
