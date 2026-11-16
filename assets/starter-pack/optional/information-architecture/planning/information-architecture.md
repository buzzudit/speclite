# {{PROJECT_NAME}} Information Architecture

Status: active
Last Updated: {{DATE}}
Framework: OOUX (Object-Oriented UX)
Scope: {{SCOPE}}

## Method

OOUX identifies the system's objects first, then derives attributes, actions, relationships, and navigation from them. The inputs are the vision, workflow, and any state flow — not the current screen layout.

---

## 1. Object Map

### Core Objects

| Object | Definition | Lifecycle |
|---|---|---|
| **{{Object}}** | What it represents | Created when, expires/persists how |

### Supporting Objects

| Object | Definition | Belongs to |
|---|---|---|
| **{{Object}}** | What it represents | Parent object |

---

## 2. Object Detail

### {{Object Name}}

**Attributes (what describes it)**
- Attribute 1
- Attribute 2

**Relationships**
- belongs to 1 {{Other Object}}
- has 0..n {{Other Object}}

**Key metadata (computed)**
- Derived value and what it means

**Actions (what you do with it)**
- Action 1
- Action 2

Repeat this section for each core object.

---

## 3. Relationships Map

```
{{Object A}} ──1:N──► {{Object B}}
{{Object A}} ──1:1──► {{Object C}}
```

---

## 4. Navigation Model

OOUX derives navigation from objects, not from features or tasks. Each top-level nav item maps to a core object or a view of one.

### Top-level navigation

| Nav item | Object | View type | Why top-level |
|---|---|---|---|
| **{{Name}}** | {{Object}} | Collection / detail / dashboard | Why the user starts here |

### Detail views (reached contextually)

| View | Object | Reached from | Why not in nav |
|---|---|---|---|
| **{{Name}}** | {{Object}} | Parent screen → trigger | Requires context |

### Cross-links

| From | Target | Trigger |
|---|---|---|
| {{Screen}} | {{Screen}} | Click / action |

### Navigation principles

1. **Object-first**: every screen shows one object or a collection of one object type.
2. **Progressive disclosure**: collections → detail → actions.
3. **Contextual cross-links**: when an object references another, link to that object's detail.

---

## 5. Content Prioritization

Within each object's detail view, attributes are prioritized by decision value — what the user needs to see to take the next action.

### {{Object}} detail — priority order
1. Most decision-critical attribute
2. Next most important
3. Context and history
4. Rarely needed metadata

---

## 6. Gaps and Recommendations

Issues identified during IA construction:

| # | Finding | Recommendation |
|---|---|---|
| 1 | {{Finding}} | {{Recommendation}} |
