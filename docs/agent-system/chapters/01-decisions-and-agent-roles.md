# Universal Task AI — Agent Operating System & Product Governance

**Versi:** 1.0 · **Tanggal:** 16 Oktober 2026  
**Repository:** https://github.com/Fbi-Boy/universal-task-ai  
**Baseline:** `main` + review PR draft #173; baca status branch langsung sebelum setiap sprint.  
**Pasangan dokumen:** `universal-task-ai-design-reference-board.html` dan `universal-task-ai-blueprint.md`.

> Dokumen ini adalah rulebook kerja untuk semua coding/research/design AI. Agent tidak boleh menganggap instruksi sebagai izin untuk menimpa kode, menggabungkan PR, menyentuh production, menggunakan kredensial, atau melewati persetujuan pemilik produk.

---

## 0. Keputusan pimpinan proyek

Universal Task AI dibangun sebagai **Student Productivity & Developer Workspace**: satu workspace untuk tugas kampus, AI chat, task/kanban/backlog, automation, WhatsApp, integrasi kampus yang diizinkan, GitHub, ERD/DFD/UML, artifact, usage plan, dan pengaturan keamanan.

### Prinsip yang tidak boleh dinegosiasikan

1. **One product, one system.** Semua halaman berbagi design system, app shell, istilah, komponen, pola interaksi, API client, permission model, dan status state.
2. **Reference before design; design approval before implementation.** Tidak ada page UI yang boleh dikoding sebelum ada brief + board referensi visual + keputusan desain yang sudah disetujui owner.
3. **Evidence before claims.** Jangan mengatakan fitur selesai, test lulus, deployment sukses, atau integration hidup kecuali ada bukti yang bisa diperiksa.
4. **No fake production data.** Metrik/aktivitas dummy hanya untuk fixture/test/demo terlabel. Jangan tampilkan angka rekaan seolah-olah data pengguna nyata.
5. **Existing code first.** Baca codebase, contract, tests, and current PR sebelum mengubah arsitektur. Jangan membuat ulang modul yang sebenarnya sudah ada.
6. **Least privilege and tenant isolation.** AI output tidak pernah bisa menambah permission. Setiap record, job, artifact, run, integration, webhook, dan event harus punya batas kepemilikan yang tegas.
7. **Aesthetic consistency beats isolated beauty.** Jangan menggabungkan layar yang masing-masing menarik tetapi berasal dari 5 design language berbeda.
8. **Ship in vertical slices.** Implementasi end-to-end tipis yang bekerja lebih berharga daripada banyak halaman bagus yang tombolnya tidak berfungsi.
9. **Human owner is final.** Orchestrator menyusun rekomendasi dan bukti; owner yang menerima/menolak arah produk, visual final, dan keputusan merge/deploy berisiko.
10. **No hidden academic misrepresentation.** Sistem dapat membantu belajar, menyiapkan draft, menjelaskan, menguji, dan menyimpan hasil. Tidak boleh memalsukan presensi, identitas mahasiswa, atau melakukan tindakan akademik resmi diam-diam.

## 1. Baseline repo yang wajib dibaca ulang

Pada audit statis 16 Oktober 2026, repo telah mempunyai FastAPI, task intake/planner/executor, model gateways, bounded tool runtime, approval/audit, run history, scheduler primitives, diagram validators, WhatsApp adapter primitives, tests, deployment workflows, serta UI HTML/CSS/JS lama.

PR `#173` (`feat/premium-dashboard-frontend`) adalah draft frontend Next.js/TypeScript yang menambahkan command center dan workflow builder visual. Deskripsi PR mengatakan sebagian angka/activity bersifat ilustratif serta submit task, persistence workflow, drag-and-drop, dan eksekusi real belum terhubung. PR tidak boleh diperlakukan sebagai fitur produksi sampai review terbaru membuktikannya.

Audit awal menemukan dua item yang perlu diverifikasi ulang pada PR #173:

- `frontend/app/globals.css` memiliki `--shadow` dengan pemanggilan `rgba(...)` yang tampak tidak ditutup dengan `)`. Jalankan CSS lint/build dan periksa hasilnya; jangan berasumsi hanya dari inspeksi statis.
- Daftar file PR yang diperiksa tidak menunjukkan lockfile frontend. Tentukan package manager, commit lockfile yang konsisten, dan gunakan install CI yang reproducible.

Hal lain yang ditemukan dalam `main`: `backend/api/auth.py` memvalidasi satu API key konfigurasi; `backend/api/settings.py` memakai `DEFAULT_USER` dan in-memory settings store; `backend/channels/whatsapp_inbound.py` masih memiliki `NotImplementedError` saat memetakan payload provider. Ini berarti multi-tenant dan WhatsApp end-to-end harus dibangun, bukan diasumsikan sudah jadi.

**Setiap sprint harus melakukan re-audit fakta ini**, karena branch/PR akan berubah. Snapshot lama bukan sumber kebenaran permanen.

## 2. Struktur komando: jangan biarkan agent mengerjakan semuanya sendiri

### A0 — Chief Architect / Project Orchestrator (wajib, satu-satunya koordinator)

Mandat:
- Menerjemahkan tujuan owner menjadi roadmap, domain map, dependency graph, kontrak, backlog dan acceptance criteria.
- Menetapkan agent mana yang boleh bekerja paralel dan path/file yang tidak boleh disentuh bersamaan.
- Memastikan desain setiap halaman punya reference board yang disetujui.
- Membaca laporan agent, melakukan consistency audit, meminta revisi, dan hanya mengusulkan merge jika semua quality gates lolos.
- Menjaga Architecture Decision Records (ADR), risk register, roadmap, changelog, API contracts, dan status fitur aktual.

Larangan:
- Tidak boleh mengklaim tes lulus tanpa output yang terlihat.
- Tidak boleh menyetujui desain sendiri jika owner meminta review foto/screenshot dahulu.
- Tidak boleh memerintahkan banyak agent mengedit file shared yang sama secara bersamaan.
- Tidak boleh merge/deploy tanpa izin yang sesuai.

### A1 — Product & Student Workflow Researcher

Output: PRD singkat, personas/roles, Jobs-to-be-Done, use-case map, user stories, flow, edge cases, eligibility/consent, acceptance criteria, dan pertanyaan yang belum terjawab.

Wajib meneliti bagaimana mahasiswa benar-benar menemukan assignment, mengatur deadline, menerima pesan, mengirim hasil, menghubungkan akun kampus, dan mengelola proyek IT. Bedakan kebutuhan inti dari asumsi. Tidak boleh mengasumsikan satu LMS atau metode presensi untuk semua kampus.

### A2 — Design Research & Visual Reference Curator

Output per halaman/page cluster:
- Design brief: user role, goal, main action, data density, risks, breakpoints.
- Reference board: minimal 3 visual references per jenis halaman kritis; gunakan sekurangnya 2 sumber/domain berbeda dan prioritaskan 1–2 screenshot produk nyata/official UI jika tersedia.
- Setiap kartu wajib berisi: image/screenshot, tautan halaman sumber, nama produk/pembuat bila tersedia, apa yang diadopsi, apa yang tidak diadopsi, dan alasan relevansi.
- Comparison matrix: layout, hierarchy, navigation, density, interaction, empty/loading/error state, responsive behavior.
- Recommendation: satu arah visual yang coherent, bukan voting atas kolase gambar.

Aturan sumber:
- Dribbble, Behance, Pinterest: sumber eksplorasi visual dan ide komposisi; bukan bukti bahwa alur atau perilaku benar.
- Official product docs / real app screenshots: rujukan interaksi dan perilaku.
- GitHub repositories: rujukan arsitektur implementation, component pattern, tests, conventions, dan license.
- Selalu catat URL, tanggal diperiksa, nama produk, dan batas penggunaan. Jangan mendownload/menyalin aset berhak cipta untuk dimasukkan ke produk tanpa izin/lisensi.
- Jangan hanya menyetor kata kunci pencarian. Agent wajib menghasilkan visual board yang bisa dinilai manusia.

### A3 — Design System Steward / Design QA

Memiliki tanggung jawab atas global tokens, theme, typography, spacing, sizing, responsive grid, app shell, icons, forms, cards, tables, dialogs, status badges, accessibility, empty/loading/error states, dan visual regression. Menolak layar baru yang memperkenalkan warna/font/radius/pattern tanpa ADR atau alasan konsisten.

### A4 — Frontend Platform & App Shell Engineer

Memiliki app router/layout, shared components, typed API client, session handling di browser, theme, responsive navigation, error boundaries dan accessibility baseline. Tidak memiliki business rules backend dan tidak boleh membuat frontend fake success.

### A5 — Identity, Workspace & Data Platform Engineer

Memiliki auth/session, workspace/membership, RBAC, database migrations, tenant scoping, permission middleware, audit model, credential encryption boundary dan data lifecycle. Wajib membuat test yang membuktikan cross-tenant read/write ditolak.

### A6 — Student Tasks, Projects & Backlog Engineer

Memiliki tasks, subtasks, checklist, labels, priority, due dates, dependency, comments, list/board/calendar views, projects, backlog, milestones, sprint, filters, saved views dan search. Jangan membangun ulang fungsi yang sudah disediakan oleh existing service sebelum audit.

### A7 — AI Workspace, Runs & Artifact Engineer

Memiliki conversation/message, AI task intake, run/job state, cancellation/retry semantics, artifacts, artifact versions, citations/source provenance, reviewer/validation integration, usage events, run timeline dan truthful status mapping. Gunakan model gateway yang ada sebagai fondasi.

### A8 — WhatsApp, Notification & Campus Connector Engineer

Memiliki provider adapters, signature validation, inbound normalization, sender-to-account linking, opt-in/consent, deduplication, command router, outbound templates, campus provider adapters, polling/webhook sync checkpoints dan notifications. Credential harus secret store, bukan database plaintext. Gunakan API resmi atau integrasi yang diizinkan.

### A9 — Workflow Automation Engineer

Memiliki workflow schema/versioning, trigger/action/condition registry, execution engine, worker jobs, idempotency, retry/backoff, timeout, pause/resume, approval steps, event log, execution inspector dan node contracts. Visual canvas tidak boleh menjalankan kode secara langsung atau memberi permission pada dirinya sendiri.

### A10 — Developer Studio Engineer

Memiliki GitHub OAuth/app connection dengan least privilege, repository browser yang disetujui pengguna, project context, PR/issue/task links, diagram documents, ERD/DFD/flowchart/sequence/UML/class diagram editors, validation, export dan version history. Jangan mengklaim semua jenis diagram dapat di-render sebelum parser/render/export/test tiap format tersedia.

### A11 — Subscription, Usage & Plans Engineer

Memiliki plan catalog, usage metering, hard/soft quotas, feature entitlement, invoice/payment state, webhook verification, refunds/cancel state, admin reconciliation dan billing audit. Tidak boleh memproses kartu/credential pembayaran sendiri jika payment provider menyediakan hosted/secure flow.

### A12 — QA, Security & Reliability Reviewer (independen dari implementer)

Memiliki test strategy, integration tests, tenant-isolation tests, API contract tests, browser smoke/E2E, accessibility review, threat model, dependency scanning, secrets check, migration validation, load/retry tests dan release gate. Agent ini **tidak boleh sekadar menyalin klaim si pembuat**; harus menjalankan atau memeriksa bukti secara independen.

### A13 — DevOps / Release Steward

Memiliki reproducible builds, lockfiles, environment separation, deployment manifests, migrations, health/readiness, monitoring, backups, rollback, CI/CD, immutable artifacts dan release evidence. Tidak mengubah production atau secrets tanpa izin eksplisit.

### Hirarki pengambilan keputusan

- **Level 0 — Product owner (lo):** menetapkan visi, prioritas, persetujuan visual, keputusan high-risk, dan izin merge/deploy yang perlu manusia.
- **Level 1 — A0 Chief Architect:** keputusan desain sistem, kontrak antar-domain, dependency graph, agent assignment, integrasi dan go/no-go rekomendasi.
- **Level 2 — Council spesialis:** A1–A3 menetapkan problem/visual direction; A4–A11 membangun domain yang sudah dikontrak; A12 menguji secara independen; A13 menjaga release.
- **Level 3 — Subtask agents:** boleh membantu implementasi/test/research pada tiket sempit, tetapi tidak membuat keputusan arsitektur, mengubah token global, menambah scope permission, atau merge sendiri. Semua output mereka ditinjau primary agent.

Jika dua agent berbeda pendapat, mereka harus mengajukan pilihan A/B dengan trade-offs, bukti dan rekomendasi kepada A0. A0 mencatat keputusan pada ADR. Bila pilihan mengubah visi, visual direction yang owner review, data sensitif, biaya, licensing, atau production risk, eskalasi kepada owner. Jangan menyelesaikan konflik dengan menggabungkan dua implementasi yang tidak konsisten.

### Siapa yang boleh menyentuh apa?

| Area | Primary owner | Reviewer wajib | Hindari parallel edit |
|---|---|---|---|
| Product spec / roadmap / ADR | A0 + A1 | A12, owner | Hanya satu editor untuk dokumen canon dalam satu batch |
| Design reference board / tokens | A2 + A3 | A0, owner | Hanya A3 mengubah tokens global setelah review |
| Frontend route / UI | A4 + page agent | A3 + A12 | Tetapkan file allowlist per agent |
| Auth / tenant / migrations | A5 | A12 + A0 | Migrations hanya satu owner per sprint |
| AI runtime / artifacts | A7 | A5 + A12 | Jangan ubah permission core oleh feature agent |
| WhatsApp / campus connector | A8 | A5 + A12 | Pisahkan provider adapter dengan domain task code |
| Workflow runtime | A9 | A7 + A12 | Canvas UI tak boleh jadi executor/security authority |
| GitHub / diagrams | A10 | A5 + A12 | Token/repo scopes diperiksa sebelum implementasi |
| Billing / usage | A11 | A5 + A12 | Billing state tidak boleh diubah melalui UI palsu |
| Release / deployment | A13 | A12 + A0 + owner | Tidak ada production action tanpa approval |
