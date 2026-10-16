## 3. Decision protocol: setiap fitur melewati gates

### Gate G0 — Problem and scope

Sebelum coding, A1+A0 mengeluarkan satu brief yang mencantumkan:
- User/role target dan tujuan yang terukur.
- Happy path serta minimal 5 edge/failure cases yang relevan.
- Scope in/out, dependensi, data sensitif, permission, dan resiko.
- Acceptance criteria yang dapat diuji.
- Source of truth untuk status dan data.

**Stop** jika user/goal/permission/sumber data tidak jelas. Tanyakan satu pertanyaan spesifik kepada owner, atau dokumentasikan asumsi yang aman dan reversibel.

### Gate G1 — Visual reference approval (wajib untuk halaman visual)

A2 meneliti, menyaring dan menyajikan reference board. A3 menyusun keputusan design direction/token mapping. A0 memeriksa konsistensi dengan halaman lain. Owner dapat melihat gambar dan setuju/revisi.

Sebelum disetujui, agent hanya boleh membuat eksperimen lokal/prototype yang jelas berlabel, bukan langsung menulis seluruh halaman ke branch integrasi.

Design approval mencatat: `approved`, `approved_with_changes`, atau `rejected` beserta alasan. Desain yang baru berbeda arah memerlukan review ulang.

### Gate G2 — Architecture/API/data contract

Sebelum frontend/backend berjalan paralel, sepakati:
- Domain owner; request/response schemas dan error contracts.
- Auth actor, workspace scope, permissions, ownership, data retention.
- Entity/migrations/indexes/unique keys.
- Event/job semantics, idempotency, retry and cancellation.
- Loading, empty, success, partial, `needs_input`, `waiting_approval`, and failure state.
- Compatibility/migration plan untuk existing code.

Contract ditulis dalam OpenAPI/schema/ADR, bukan hanya di chat. Frontend boleh membangun terhadap mocks hanya setelah contract sudah ditetapkan; mock harus eksplisit dan diganti oleh integration tests.

### Gate G3 — Implementation

Setiap agent diberi ticket kecil dengan:
- Branch unik `feature/<ticket>-<slug>` atau `fix/<ticket>-<slug>`.
- File/path yang boleh diubah serta paths yang harus dihindari.
- Dependency/ticket prerequisites.
- Acceptance criteria & expected evidence.
- Tests dan docs yang harus ditambahkan.

Implementasikan satu vertical slice pada satu waktu. Tidak boleh mengubah stack atau menambah package besar tanpa alasan dan approval A0. Tidak boleh menghapus, rewrite, atau rename modul yang existing hanya untuk membuat struktur terlihat bersih.

### Gate G4 — Independent review

Reviewer selain implementer memeriksa:
- Apakah scope terpenuhi dan contract tidak berubah diam-diam?
- Apakah akses pengguna lain dapat bocor melalui ID, URL, event, artifact, cache, atau background job?
- Apakah secret bisa masuk ke DOM, URL, logs, prompts, screenshots, atau exception?
- Apakah input dibatasi, output divalidasi, timeouts/retries jelas, duplicate events aman?
- Apakah UI memiliki empty/loading/error/disabled states dan semua kontrol berfungsi?
- Apakah dependency dan license sesuai?
- Apakah tests mereproduksi kebutuhan dan failure mode, bukan hanya menguji helper happy path?

### Gate G5 — QA evidence

Ticket tidak selesai sampai bukti tersedia sesuai jenis pekerjaan:
- `pytest` tests untuk backend dan test khusus yang ditambahkan.
- `npm ci`/equivalent + lint + typecheck + production build untuk frontend.
- Browser smoke test di desktop dan mobile; screenshot hasil real app.
- API contract/integration tests untuk perubahan backend/frontend.
- Migration up/down atau recovery test sesuai strategi database.
- Cross-tenant security test untuk perubahan data/identity.
- Run logs dan failure/retry test untuk worker/automation.
- Accessibility check untuk UI utama: keyboard, focus, labels, contrast, responsive.

Jika alat/runtime tidak tersedia, laporkan sebagai **NOT RUN**, jangan mengubahnya menjadi PASS. Screenshot desain statis tidak membuktikan interaksi berfungsi.

### Gate G6 — Merge / release

- PR menjelaskan tujuan, keputusan, scope, screenshot bila UI, test evidence, migration, risks, dan follow-up.
- CI wajib berjalan pada HEAD PR yang terakhir, bukan commit sebelumnya.
- Tidak ada blocker/high severity bug atau credential yang bocor.
- No unresolved required review; semua check yang diwajibkan lulus.
- A0+A12 memberi rekomendasi merge; owner tetap pemilik final untuk keputusan yang berisiko.
- Deployment hanya setelah staging/rehearsal, backup/rollback, health checks, dan owner approval.

---

## 4. Design research SOP — anti AI slop

### Aturan wajib per halaman

1. Tulis page brief (siapa, apa tujuan, tindakan utama, data yang penting, batas/resiko).
2. Cari **3–5 screenshot/referensi visual yang relevan**, jangan mengandalkan satu gambar. Ambil minimal 2 domain/sumber berbeda.
3. Sertakan setidaknya satu referensi dari produk nyata/official documentation untuk interaksi, serta visual inspiration yang cocok untuk hierarki/komposisi.
4. Catat URL langsung ke source page, source image, nama kreator/proyek, tanggal diperiksa, ide yang diambil dan alasan pemilihan.
5. Bandingkan referensi menggunakan rubric: task fit 25%, information hierarchy 20%, consistency with existing design system 20%, interaction clarity 15%, responsive behavior 10%, accessibility 10%.
6. Buat satu rekomendasi desain final dan tunjukkan area screenshot mana yang relevan. Jangan suruh owner menyortir 30 screenshot tanpa kesimpulan.
7. A3 mencatat keputusan ke `docs/design/DECISIONS.md` atau Design ADR: tokens, spacing, shell, layout, component choices dan alasan.
8. Owner meninjau image board/prototype. Setelah disetujui, A4 baru mengimplementasikan page.
9. Setelah implementasi, QA mengambil screenshot app nyata pada viewport standar. Bandingkan dengan board dan catat perbedaan/justifikasi.
10. Setiap redesign berikutnya reuse decisions/token/component yang sama; page baru tidak boleh mengubah design system secara lokal.

### Referensi per role (bukan cuma per URL)

Untuk halaman yang berbeda karena role, design researcher wajib menangkap setiap **perbedaan UX yang nyata** melalui screenshot terpisah: navigation visibility, allowed actions, read-only/edit states, approval controls, membership/billing tools, dan error/denied state. Jangan membuat duplikasi desain yang tidak diperlukan hanya untuk setiap role; jika layout sama dan yang berubah hanya hak aksi, dokumentasikan state comparison untuk role tersebut. Minimum persona review: Personal Student, Workspace Owner/Admin, Member/Collaborator, Viewer/Reviewer, dan Platform Support/Admin (isolated control plane). Setiap board page harus mencantumkan statusnya di approval register: `NEEDS RESEARCH`, `READY FOR OWNER REVIEW`, `APPROVED`, atau `REJECTED`.

### Cara menggunakan sumber desain

- **Pinterest / Dribbble / Behance:** untuk eksplorasi visual dan inspirasi komposisi; pilih shots yang sesuai dengan job-to-be-done, jangan tiru satu shot mentah-mentah.
- **ClickUp / Linear / GitHub Projects:** untuk informasi product management dan interaksi list/board/backlog/filters.
- **n8n / React Flow (xyflow):** untuk memahami node canvas, connections, node inspector, execution history, zoom/pan dan edge behavior.
- **dbdiagram / Eraser:** untuk ide pengelompokan entitas, relationship edges, schema navigation, code/text mode dan export.
- **shadcn/ui:** untuk aksesibilitas/composition patterns dan komponen reusable; gunakan untuk membangun sistem internal yang bertema Universal Task AI, bukan gabungan library visual.
- **GitHub template repos:** untuk implementation patterns only after checking license, maintenance, dependencies, security posture, and tests.

Screenshots adalah referensi internal. Jangan menyalin logo, proprietary illustration, foto/avatar, unique branded artwork, atau source assets tanpa hak penggunaan.

### Visual system proposal (keputusan sementara, wajib divalidasi lewat board)

Arah yang disarankan: **calm, dense, technical workspace**. Bukan landing page penuh gradient dan floating cards. Pakai struktur produk konsisten dan mengutamakan tugas nyata.

- Canvas: netral terang; surface putih/abu tipis; border subtle; teks kontras tinggi.
- Brand accent: pilih satu cobalt/blue atau neutral brand accent lewat token; warna status success/warning/danger/information terpisah dari brand.
- Typography: satu family UI sans (Geist/Inter atau pilihan hasil review), satu skala type dan weight.
- Icons: `lucide-react` atau satu sistem icon yang setara; tidak emoji sebagai ikon navigasi produk.
- Spacing: kelipatan basis 4/8; radius dan shadows konsisten; hindari kartu bertumpuk tanpa tujuan.
- Desktop shell: sidebar persisten + topbar/breadcrumb + page title/action bar; mobile menggunakan drawer/sheet dan toolbar yang disesuaikan.
- Workspace editing: kanban, code editor, ERD dan workflow canvas boleh memakai density/dark surfaces yang sesuai tugas, tetapi tetap menggunakan tokens global.
- Dashboard hanya menunjukkan metrik yang disuplai API. Jangan mengisi ruang kosong dengan chart dekoratif.
- Dark mode menggunakan token semantic yang sama, bukan page-specific hack.

### Component inventory yang dipelihara A3

`AppShell`, `Sidebar`, `MobileNav`, `Topbar`, `Breadcrumbs`, `PageHeader`, `PrimaryAction`, `CommandPalette`, `SearchCommand`, `FilterBar`, `DataTable`, `ListView`, `KanbanBoard`, `CalendarView`, `TaskCard`, `TaskDetailDrawer`, `StatusBadge`, `PriorityIndicator`, `AvatarGroup`, `EmptyState`, `Skeleton`, `ErrorState`, `Toast`, `ConfirmDialog`, `ApprovalPanel`, `RunTimeline`, `ArtifactCard`, `FilePreview`, `ChatMessage`, `ChatComposer`, `ToolCallRow`, `UsageMeter`, `ConnectionCard`, `WorkflowNode`, `WorkflowInspector`, `DiagramCanvas`, `DiagramToolbar`.

Komponen baru harus menyertakan states, accessibility notes, responsive behavior, test, serta penggunaan token—not duplicate CSS variant per page.

---

## 5. Page map, role matrix, dan design reference requirement

Role app yang disarankan:
- **Personal Student**: ruang kerja pribadi, chat, tugas kampus, integrasi, artifacts dan usage.
- **Workspace Owner**: pemilik workspace personal/kelompok; billing, membership, integration permissions, workspace settings.
- **Workspace Admin**: mengelola project/workflow/member sesuai izin; tidak otomatis bisa melihat secret atau mengambil alih seluruh akun.
- **Member/Student Collaborator**: mengerjakan task/project yang di-share dan menjalankan workflow yang diberi izin.
- **Viewer/Reviewer**: melihat scope yang di-share dan memberi komentar/approval jika diberikan hak.
- **Platform Support/Admin**: internal admin app terpisah; akses hanya seperlunya, ada reason, audit, dan mekanisme break-glass. Tidak disamakan dengan workspace admin.

### Screen catalog

| Page / route proposal | Main user/role | Main job + key states | Visual research before coding |
|---|---|---|---|
| Sign in / onboarding | Student, Owner | Sign-in, create workspace, connect first source, consent, errors | SaaS auth/onboarding product screenshots + official component patterns |
| Overview `/app` | Student, Owner | Deadlines, tasks due soon, recent runs, connector health; empty/new account/error | Planora dashboard + existing actual app shell + dashboard starter |
| AI Workspace `/app/ai` | Student, Member | Conversation, project context, files, plan, tool events, approval, retry/fail | AI Task Manager, AI chat screenshot + actual run timeline product patterns |
| Task Inbox `/app/tasks` | Student, Member | Inbox/today/upcoming/all; search, filter, empty, overdue | ClickUp views + Kanban Board/Flowboard |
| Task Detail | Student, Member, Reviewer | Instructions, deadline, checklist, artifact, activity, references | ClickUp task detail + editor/file management patterns |
| Project Overview | Owner, Member | Milestones, members, docs, progress from real data | Flowboard + project dashboard reference |
| Backlog / Sprint `/app/projects/:id/backlog` | Owner, Member | Prioritization, estimates, sprint, drag/drop, issue states | ClickUp Board/List / GitHub Projects board screenshot |
| Calendar / schedule | Student, Member | Deadline/class/schedule, timezone, reminder, conflict states | Calendar app patterns + actual product screenshots |
| Campus Hub | Student | Course, assignment source, deadline, sync status, consent, connector error | Official LMS screenshots/API docs and clean list/calendar references |
| Attendance reminder detail | Student | Schedule + open official source + reminder state; no spoofed attendance action | Official calendar/reminder patterns; accessibility review |
| Automations list | Owner, Member | Draft/active/paused/failed, templates, search, creation | n8n editor and SaaS automation dashboard references |
| Workflow Builder | Owner, authorized Member | Trigger/node canvas, inspector, variables, test, save/version, publish | Dribbble workflow screenshot + n8n actual canvas + React Flow docs |
| Workflow run detail | Owner, Member, Reviewer | Step timeline, logs, output, retry, cancellation, approvals | Actual automation execution UI/official documentation |
| Approval Inbox | Owner, designated Reviewer | Risk explanation, requested action, scope, approve/reject, expiration | Real approval/security console patterns; no dark patterns |
| Artifacts & Files | Student, Member | List/search, version history, provenance, preview/download/permission errors | Document workspace and file manager references |
| Developer Studio overview | IT Student, Member | Repositories, diagrams, recent code artifacts, project context | GitHub Projects screen + code workspace design references |
| GitHub connection/repositories | Owner, Member with permission | OAuth/app connection, scope, list repos, revoke, sync failures | Official GitHub UI/docs; narrow-scope consent pattern |
| ERD editor | IT Student, Member | Entities, fields, PK/FK, relations, zoom/pan, source text, validate/export | dbdiagram image + Eraser Diagrams docs |
| DFD / Flowchart / Sequence / UML | IT Student, Member | Diagram-specific palette, syntax validation, source + canvas, export | Eraser/diagram tools + one reference per supported diagram type |
| Integrations catalog | Owner | Connect/disconnect, permission scopes, health, token expiry, sync | Real integrations directory references |
| Usage & Plan `/app/settings/usage` | Owner, Student | Real use, quota, reset date, estimate, limit reached, plan change | SaaS billing patterns + maintainable open-source dashboard reference |
| Workspace members/settings | Owner/Admin | Invite, role changes, access review, leave/delete workspace confirmation | SaaS workspace and members pages |
| Profile/security/settings | All roles | Profile, session revoke, language/timezone/theme, deletion/privacy | Official design system form/settings patterns |
| Internal platform admin | Platform Admin/Support only | Users, plans, jobs, provider health, audit, support intervention | Admin dashboard reference; isolated route and role tests |

**Rule:** screen catalog is not a commitment that every page ships at once. Routes hidden until their API, role authorization, loading/error states and QA acceptance exist.

### Design approval register (starting state)

Status berikut sengaja dimulai sebagai `NEEDS RESEARCH`; screenshot di board awal adalah arah visual lintas domain, bukan approval tiap page. A0 menjaga tabel ini tetap canonical dan A2 mengisi link board sebelum tiket UI masuk coding.

| Screen/cluster | Role variants requiring visual check | Status | Board / approval record |
|---|---|---|---|
| Auth / onboarding | Student, Workspace Owner | NEEDS RESEARCH | Belum dibuat |
| App shell + Overview | Student, Owner/Admin | NEEDS RESEARCH | Baseline references only |
| AI Workspace | Student, Member; viewer state if shared | NEEDS RESEARCH | Baseline references only |
| Tasks / Task Detail | Student, Member, Reviewer | NEEDS RESEARCH | Baseline references only |
| Project / Backlog | Owner/Admin, Member, Viewer | NEEDS RESEARCH | Baseline references only |
| Calendar / Campus Hub | Student; linked account/sync errors | NEEDS RESEARCH | Belum dibuat |
| Attendance reminders | Student | NEEDS RESEARCH | Belum dibuat |
| Automations list / builder | Owner, authorized Member, Viewer | NEEDS RESEARCH | Baseline references only |
| Workflow run / Approval inbox | Owner, Member, Reviewer | NEEDS RESEARCH | Belum dibuat |
| Artifacts / Files | Owner, Member, Viewer | NEEDS RESEARCH | Belum dibuat |
| Developer Studio / GitHub | IT Student, Owner, authorized Member | NEEDS RESEARCH | Baseline references only |
| ERD | IT Student, Member, read-only Viewer | NEEDS RESEARCH | Baseline references only |
| DFD / Flowchart / Sequence / UML | IT Student, Member, Viewer | NEEDS RESEARCH | Need one board per format family |
| Integrations catalog | Workspace Owner/Admin | NEEDS RESEARCH | Belum dibuat |
| Usage / Plan / billing | Student, Workspace Owner, Platform Support | NEEDS RESEARCH | Baseline references only |
| Workspace members/settings | Owner/Admin, Member, Viewer | NEEDS RESEARCH | Belum dibuat |
| Profile/security | All roles | NEEDS RESEARCH | Belum dibuat |
| Platform admin/control plane | Platform Support/Admin only | NEEDS RESEARCH | Belum dibuat; separate visual shell review |
