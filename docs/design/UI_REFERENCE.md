# UI Reference — AI Workspace

This document records the visual direction from the reference screenshot supplied in the project conversation.

## Reference characteristics

- Desktop AI workspace inside a soft rounded shell with a light gray page background.
- Narrow left navigation rail for Search, AI Chat, Projects, Templates, Documents, Community, History, Settings and Help.
- Large central AI Chat workspace with a welcoming heading, concise subtitle, quick-action cards and a prominent task composer.
- Right Projects rail with a project count, new-project action and compact project cards.
- Light, minimal visual language: white panels, thin gray borders, small rounded corners, restrained shadows and compact typography.
- Responsive behavior: hide the project rail on medium screens and collapse the navigation on small screens.
- The reference is a visual direction, not a request to copy third-party branding, text or assets.

## Implemented mapping

| Reference area | Universal Task AI |
|---|---|
| Left navigation | backend/web/index.html sidebar |
| AI Chat center | welcome + composer + analysis panels |
| Quick actions | document, image, data and code task starters |
| Projects rail | right-side project list |
| Composer | task textarea, tools, character counter and run button |
| Execution visibility | approvals, run history and live events |
| Responsive shell | backend/web/ui.css media queries |

The source screenshot remains the design reference supplied by the user; repository implementation is intentionally original and uses the project's existing API endpoints.
