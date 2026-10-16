## 6. API contract yang perlu distandardisasi

Jangan membuat seluruh endpoint sebelum kontrak domain dan authorization jelas. Contoh grouping target:

```text
/v1/auth/*
/v1/workspaces/*
/v1/projects/*
/v1/tasks/*
/v1/ai/conversations/*
/v1/ai/runs/*
/v1/runs/{run_id}/events
/v1/artifacts/*
/v1/integrations/*
/v1/campus/connections/*
/v1/campus/assignments/*
/v1/automations/workflows/*
/v1/automations/runs/*
/v1/developer/github/*
/v1/developer/diagrams/*
/v1/usage/*
/v1/billing/*
/v1/webhooks/whatsapp/*
/v1/health
/v1/ready
```

Standar responsi run:

```json
{
  "run_id": "uuid",
  "status": "queued | running | needs_input | waiting_approval | ready_for_review | completed | failed | cancelled",
  "created_at": "ISO-8601",
  "progress": {"current_step": 1, "total_steps": 3},
  "artifact_ids": [],
  "error": null
}
```

Contoh ini adalah rancangan kontrak, bukan bentuk response yang sekarang dijamin oleh API. Semua endpoint perlu validasi Pydantic, error mapping konsisten, auth/tenant check, pagination, rate limit, request ID dan test kontrak.

---

## 7. Prioritas pengerjaan per sprint

Sprint berikut adalah urutan dependensi, bukan janji kalender. Setiap sprint baru dimulai setelah acceptance criteria sprint sebelumnya terbukti.

### Sprint 0 — Audit & keputusan arsitektur

**Branch:** `docs/product-architecture`  
**Output:** PRD, architecture decision records (ADR), module map, data model draft, API contracts, security boundaries, backlog terprioritas.

- Review PR #173, perbaiki syntax CSS, jalankan lint/build dan review desktop/mobile.
- Tandai fitur prototype, fitur backend yang nyata, dan fitur yang belum ada.
- Bekukan konvensi status run/task, ownership, error format, IDs, pagination, file storage dan event dedupe.

**Gate:** kontrak disepakati; tidak ada scope yang bergantung pada data palsu; PR #173 tetap terpisah sampai kualitas UI dan strategi integrasi dipastikan.

### Sprint 1 — Multi-user foundation & persistence

**Branch:** `feat/identity-workspace-foundation`

- Rancang akun, session/auth, workspace dan membership.
- Ganti asumsi single global API key untuk mode SaaS dengan per-user auth yang benar. Mode local development dapat tetap menyediakan API key.
- Tambah workspace-scoped authorization dan PostgreSQL migrations; jangan memutuskan bahwa ID dari body otomatis sah.
- Persist settings per user; cek run/approval/history/event isolation antar tenant.

**Gate:** pengujian dua akun/workspace membuktikan akses silang ditolak untuk task, setting, runs, approvals dan artefak.

### Sprint 2 — Frontend shell terhubung ke API nyata

**Branch:** `feat/frontend-api-integration`

- Review PR #173 sebelum merge; tambah typed API client, loading/empty/error states, auth flow dan environment config.
- Connect health/readiness, tool catalog, task analyzer/run, approvals, run history dan events ke kontrak backend.
- Ganti kartu contoh menjadi API data atau label demo; tidak boleh ada metrik palsu seolah data real.
- Tambah keyboard navigation, responsive smoke tests dan pengujian status/error.

**Gate:** satu alur task dapat dijalankan dari dashboard sampai hasil nyata muncul, termasuk unauthorized/error/needs-tool state.

### Sprint 3 — Projects, tasks & backlog

**Branch:** `feat/projects-task-management`

- CRUD project/task, status, priority, assignee, due date, labels, subtasks, checklist, comment dan attachment.
- List/board/kanban dengan filtering dan pagination; backlog/sprint dapat menyusul setelah task CRUD stabil.
- Sinkronkan task yang dibuat manual dan task hasil deteksi kampus tanpa menduplikasi sumber.

**Gate:** data tersimpan di database, authorization dites, board/list punya empty/loading/error state dan setiap aksi memengaruhi backend.

### Sprint 4 — AI Workspace & artifact management

**Branch:** `feat/ai-workspace-artifacts`

- Conversation/message history per workspace; streaming/polling jika kontrak runtime mendukung.
- Tampilkan plan, step events, approval state, provider/model yang aman ditampilkan, output serta run history.
- Artefak dengan metadata, versi, MIME type/size, checksum, download policy, ownership dan signed URL.
- Provider routing: budget, timeout, fallback yang tidak mengulangi side effect, dan output validation.

**Gate:** chat/task dapat membuat artefak nyata yang tetap tersedia setelah restart, terikat pada owner yang benar, dan kegagalan tidak dilaporkan sebagai sukses.

### Sprint 5 — WhatsApp gateway

**Branch:** `feat/whatsapp-command-gateway`

- Implementasi mapping payload inbound yang saat ini belum selesai; normalisasi phone number/message ID/text.
- Implementasikan HTTPS webhook verification/signature, opt-in, sender-account binding, replay/idempotency, rate limits dan safe error handling.
- Pesan notifikasi tugas/deadline/run status, command help/detail/start/retry, dan handoff ketika perlu klarifikasi.
- Outbound provider memakai interface/injected HTTP client serta secret provider; credentials tidak muncul pada UI/log.

**Gate:** signature invalid ditolak; sender tak tertaut tidak dapat memicu task; webhook duplikat tidak membuat job kedua; job tidak menahan request webhook.

### Sprint 6 — Campus Hub / assignment detection

**Branch:** `feat/campus-connectors`

- Buat interface `CampusConnector` dengan `connect`, `sync_changes`, `health`, `revoke` dan capability declarations.
- Implementasikan satu adapter terlebih dahulu dari LMS yang tersedia dan authorized, atau source notifikasi yang paling realistis.
- Simpan courses, assignments, deadline, provider external ID, sync checkpoint dan last sync status.
- Map perubahan jadi My Tasks dan WhatsApp notification; gunakan retry/backoff, source allowlist, dedupe dan rate limit.
- Presensi berfungsi sebagai jadwal/reminder dan membuka sumber resmi, bukan pemalsuan atau auto-attendance.

**Gate:** test fixture untuk new/updated/deleted event, duplicate delivery, token expired, provider timeout, malformed payload dan tenant isolation.

### Sprint 7 — Workflow builder & automation

**Branch:** `feat/automation-workflows`

- Workflow definition/version, trigger, nodes, edges, schema input/output, conditions, variables dan credential references.
- Canvas memungkinkan tambah/hapus/configure/reorder node; simpan dan load dari API; versioning dan validation.
- Runtime menjalankan satu step pada satu waktu melalui worker yang sudah ada/diadaptasi, dengan timeout, retries, logs, cancellation dan approvals.
- Awali dengan beberapa node yang aman: schedule trigger, campus event, WhatsApp command, create task, AI draft, notify, condition dan wait-for-approval.
- Jangan mengeksekusi kode/workflow dari UI tanpa validasi server-side.

**Gate:** workflow yang disimpan bisa dimuat kembali dan dieksekusi pada test environment; setiap run memiliki jejak step dan kegagalan akurat.

### Sprint 8 — Developer Studio

**Branch:** `feat/developer-studio`

- GitHub OAuth/install connection dengan minimal scopes, encrypted credentials, disconnect/revoke, dan workspace-scoped repository access.
- Repository overview, branch/commit/issue/PR read views terlebih dahulu. Write actions seperti membuat issue/PR membutuhkan permission dan konfirmasi eksplisit.
- Diagram documents dengan versioned source: ERD, DFD, flowchart, sequence, UML/class, system architecture, API flow.
- Visual editor berbasis node/edge + typed schema; render/export PNG/SVG/Mermaid/SQL jika format itu didukung dan tervalidasi.
- Validator saat ini hanya pemeriksaan teks sederhana; jangan menganggapnya sebagai structural/database correctness validator.

**Gate:** diagram dapat dibuat, disimpan, diedit dan diekspor; koneksi GitHub tidak membocorkan token; resource cross-workspace ditolak.

### Sprint 9 — Premium & usage metering

**Branch:** `feat/plans-usage-billing`

- Plan, subscription state, quota/entitlement, usage events dan usage summary.
- Terapkan limit di server sebelum job/provider invocation; frontend hanya menampilkan statusnya.
- Pembayaran melalui payment gateway yang dipilih setelah analisis pasar/legal/operasional; abstract adapter agar provider dapat diganti.
- Webhook pembayaran perlu signature verification, idempotency, reconciliation dan audit.
- Free tiers dari model provider tidak boleh dijanjikan selalu tersedia; sediakan BYOK dan opsi model lokal bila masuk akal.

**Gate:** quota enforcement dites pada API/worker, event duplikat tak menggandakan kredit, dan pengguna dapat melihat dasar penggunaan secara transparan.

### Sprint 10 — Quality, security & production readiness

**Branch:** `chore/release-hardening`

- Unit/integration/security tests; tenant access matrix; browser smoke tests; mobile/keyboard/a11y check.
- Load tests untuk webhook/task queue; timeout, retry, queue backlog dan interrupted worker recovery.
- Secrets rotation, backup/restore, database migration rehearsal, monitoring dan rollback.
- Recheck deployment config, immutable images, health/readiness, logs redaction, retention/deletion policy, privacy consent dan terms.

**Gate:** deployment nyata dilakukan di environment yang dikonfigurasi dan diverifikasi. Local smoke test atau production rehearsal bukan bukti bahwa production sudah deployed.

---

## 8. Pembagian tugas untuk beberapa AI engineer

Setiap AI bekerja di branch terpisah, scope/file ownership yang jelas, dan membuka PR kecil. Tidak ada dua agent menulis file yang sama bersamaan kecuali satu agent ditetapkan sebagai integrator. Agent tidak boleh mengubah main langsung atau merge PR tanpa tahap review/gate yang disepakati.

| Agent | Fokus | Dependensi |
|---|---|---|
| A0 — Architect/Integrator | ADR, contract, dependency map, review scope, menyelesaikan konflik | Sprint 0, lalu setiap sprint |
| A1 — Identity/Data | Auth, tenant, migrations, repository layer, isolation tests | Sprint 1; paling awal |
| A2 — Frontend | Next shell, typed API client, real states, responsive UI | PR #173 + contract A0; dimulai setelah kontrak |
| A3 — Work Management | Project/task/backlog/board APIs dan UI | A1 + API contract |
| A4 — AI Workspace | Chat, model routing, run details, artifacts | A1 + current TaskService |
| A5 — WhatsApp | Inbound/outbound adapter, webhook, command router, notification | A1 + run/artifact APIs |
| A6 — Campus | Connector interface, sync/checkpoint, assignment mapping | A1 + A5 notification contract |
| A7 — Automation | Workflow schema/canvas, version, execution worker/logs | A1 + A4 + approval boundary |
| A8 — Developer Studio | GitHub adapter dan diagram editors | A1 + A2 |
| A9 — Premium | Plans, quota, usage, payment provider abstraction | A1 + A4 metering contract |
| A10 — QA/Security | Test plan, tenant matrix, integration/security tests, release gates | Seluruh agent; ikut dari awal |

Jangan memberi semua agent perintah luas seperti “buat semua fitur sekaligus”. Beri satu scope yang memiliki acceptance criteria dan batas file. A0 menyatukan hasilnya, bukan menulis ulang semua modul sendirian.
