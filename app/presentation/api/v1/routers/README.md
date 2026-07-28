# API Routers — Complete Reference

## Overview

All routers are mounted under `/api/v1` through `__init__.py`. They follow a strict thin-router pattern: **zero business logic**, pure delegation to the service layer. Every endpoint authenticates, rate-limits, validates input via Pydantic, and returns typed response models.

---

## Album (`/albums`)

**Auth:** `require_couple` — user must belong to a couple.  
**Tier:** Free.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/albums` | Create a new album |
| `GET` | `/albums` | Paginated list of albums for the couple |
| `GET` | `/albums/{album_id}` | Get a single album (ownership validated by service) |
| `PATCH` | `/albums/{album_id}` | Update album metadata |
| `DELETE` | `/albums/{album_id}` | Delete album (returns 204) |

**Business rules (service layer):**
- Each couple can create multiple albums.
- Album titles must be unique within the couple.
- Only the creator can delete the album.
- Albums with memories cannot be deleted unless memories are removed first.
- Ownership validation on every single-resource operation.

---

## Memory (`/memories`)

**Auth:** `require_couple` — user must belong to a couple.  
**Tier:** Free.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/memories` | Upload a new memory (photo + metadata via multipart form) |
| `GET` | `/memories` | Paginated list, filterable by `album_id` and `category` |
| `GET` | `/memories/{memory_id}` | Get a single memory |
| `PATCH` | `/memories/{memory_id}` | Update caption or category |
| `DELETE` | `/memories/{memory_id}` | Delete memory (returns 204) |

**Business rules (service layer):**
- File uploads validated (type, size) before storage.
- S3 upload handled by the service.
- Memories belong to an album; album ownership validated.
- Only the uploader can delete.
- Category defaults to `OTHER` if not provided.
- Pagination supports album and category filtering.

---

## Ritual (`/rituals`)

**Auth:** `require_couple` — user must belong to a couple.  
**Tier:** Free.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/rituals` | Create a new ritual |
| `GET` | `/rituals` | Paginated list, filterable by `only_active` |
| `GET` | `/rituals/{ritual_id}` | Get a single ritual |
| `PATCH` | `/rituals/{ritual_id}` | Update ritual metadata |
| `DELETE` | `/rituals/{ritual_id}` | Delete ritual (returns 204) |
| `POST` | `/rituals/{ritual_id}/complete` | Mark today's entry as completed |
| `POST` | `/rituals/{ritual_id}/skip` | Mark today's entry as skipped |

**Business rules (service layer):**
- Rituals are recurring daily activities for couples.
- Each ritual tracks daily entries (completion status per day).
- A user can only mark one entry per day per ritual.
- Only the couple members can interact with the ritual.
- `complete` and `skip` are mutually exclusive per day.
- Deleting a ritual removes all its entries.
- Ownership validation on all operations.

---

## Surprise (`/surprises`)

**Auth:** `require_premium` — Premium subscription required.  
**Tier:** Premium.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/surprises` | Create a new surprise (multipart form with optional media) |
| `GET` | `/surprises` | Paginated list, filterable by `status` |
| `GET` | `/surprises/{surprise_id}` | Get a single surprise |
| `PATCH` | `/surprises/{surprise_id}` | Update surprise metadata (only if not yet opened) |
| `DELETE` | `/surprises/{surprise_id}` | Delete surprise (returns 204, only if not opened) |
| `POST` | `/surprises/{surprise_id}/open` | Open a delivered surprise |

**Lifecycle:** `LOCKED` → `DELIVERED` (auto at `unlocks_at`) → `OPENED`

**Business rules (service layer):**
- Only Premium users can create and send surprises.
- A surprise can be scheduled (`unlocks_at`) to be delivered at a future time.
- Once a surprise is opened, it becomes immutable.
- Only the sender can edit/delete before opening.
- Media uploads are stored on S3.
- Recipient validation — surprises are sent to the partner.
- `open` validates that the surprise has been delivered (not still locked).
- Ownership validation on all single-resource operations.
- Plan limit enforced: free users cannot send surprises.

---

## Special Date (`/special-dates`)

**Auth:** `require_couple` — user must belong to a couple.  
**Tier:** Free (with plan limit — enforced by service).

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/special-dates` | Create a new special date |
| `GET` | `/special-dates` | Paginated list, filterable by `upcoming_only` and `recurring_only` |
| `GET` | `/special-dates/{date_id}` | Get a single special date |
| `PATCH` | `/special-dates/{date_id}` | Update special date metadata |
| `DELETE` | `/special-dates/{date_id}` | Delete special date (returns 204) |

**Business rules (service layer):**
- Titles must be unique within the couple.
- Supports yearly recurrence (e.g., anniversaries auto-renew each year).
- Countdown calculation (`days_until`, `next_occurrence`, `is_today`) computed by service.
- Leap-year handling for Feb 29 recurring dates.
- Free plan has a limit on how many special dates can be created.
- Premium users have unlimited special dates.
- Ownership validation on all single-resource operations.
- No calculated dates in the router — all date math is in the service.

---

## Love Letter (`/letters`)

**Auth:** `require_couple` — user must belong to a couple.  
**Tier:** Free.

**Lifecycle:** `DRAFT` → `SENT` → `READ`

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/letters` | Create a new draft letter |
| `GET` | `/letters` | Paginated list, filterable by `status`, `only_received`, `only_sent` |
| `GET` | `/letters/unread/count` | Returns `{"count": N}` of unread received letters |
| `GET` | `/letters/{letter_id}` | Get a single letter |
| `PATCH` | `/letters/{letter_id}` | Update a draft letter (only `DRAFT` allowed) |
| `DELETE` | `/letters/{letter_id}` | Delete a draft letter (only `DRAFT`, returns 204) |
| `POST` | `/letters/{letter_id}/send` | Send a draft → transitions to `SENT` (immutable after) |
| `POST` | `/letters/{letter_id}/read` | Mark a received letter as `READ` |

**Business rules (service layer):**
- Letters are always addressed to the user's partner (auto-resolved by service).
- Only `DRAFT` letters can be edited or deleted.
- Once `SENT`, a letter is **immutable** — cannot be edited, deleted, or unsent.
- `READ` status can only be set after `SENT`.
- Only the recipient can mark a letter as read.
- A user cannot send a letter to themselves.
- `send` validates the letter is in `DRAFT` status.
- `read` validates the letter is in `SENT` status and the user is the recipient.
- Ownership: only the author can view/edit/delete drafts; both partners can view sent/read letters.
- Unread count is scoped to received letters only.

---

## Watch Together (`/watch`)

**Auth:** `require_premium` — Premium subscription required.  
**Tier:** Premium.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/watch` | Create a new watch session |
| `GET` | `/watch` | Returns the currently active session (or `null`) |
| `GET` | `/watch/history` | Paginated list of ended sessions |
| `PATCH` | `/watch/{session_id}` | Update session metadata |
| `POST` | `/watch/{session_id}/join` | Join an existing session |
| `POST` | `/watch/{session_id}/leave` | Leave the session (returns 204) |
| `POST` | `/watch/{session_id}/end` | End the session (saves end timestamp) |
| `DELETE` | `/watch/{session_id}` | Delete an ended session (returns 204) |

**Business rules (service layer):**
- Only one **active** session per couple at a time (creating a new one auto-ends any active one).
- Session lifecycle: created → joined → (playback via WebSocket) → ended.
- Playback sync (play, pause, seek, timestamp) is handled exclusively by WebSockets, not REST.
- REST API is responsible only for **session lifecycle management**.
- Both partners can join; duplicate joins are idempotent.
- A session remains active until explicitly ended or a new session replaces it.
- Only ended sessions can be deleted.
- Active sessions cannot be deleted.
- Ownership validation on all single-resource operations.
- Premium validation enforced at the dependency level.

---

## Mood (`/mood`)

**Auth:** `require_couple` — user must belong to a couple.  
**Tier:** Free.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/mood` | Update the current user's mood (broadcasts via WebSocket) |
| `GET` | `/mood` | Returns both users' current mood + last-updated timestamps |

**Business rules (service layer):**
- Mood is a field on the User model — no separate table.
- Setting a mood for the first time is an upsert (None → value).
- When mood is updated, a WebSocket event is broadcast to the partner in real time.
- Redis cache stores the current mood for fast retrieval.
- The GET endpoint returns the authenticated user's mood directly + partner's mood via service.
- No mood history is persisted (only the current state is stored).
- Ownership: only the couple's members can see each other's mood.
- Response shape includes both `user_mood` and `partner_mood` with respective timestamps.

---

## Auth (`/auth`, `/couple`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login, returns JWT tokens |
| `POST` | `/auth/refresh` | Refresh access token |
| `POST` | `/auth/logout` | Invalidate refresh token |
| `POST` | `/auth/forgot-password` | Send password reset email |
| `POST` | `/auth/reset-password` | Reset password with token |
| `GET` | `/auth/me` | Get current user profile |
| `PATCH` | `/auth/me` | Update current user profile |
| `POST` | `/couple/link` | Link with a partner via code |
| `POST` | `/couple/unlink` | Leave the relationship |

---

## Dashboard (`/dashboard`)

**Auth:** `require_couple`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/dashboard` | Couple dashboard with aggregated stats |

---

## Night (`/nights`)

**Auth:** `require_couple`.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/nights` | Log a night together |
| `GET` | `/nights` | Paginated night history |
| `GET` | `/nights/{night_id}` | Get a single night entry |
| `PATCH` | `/nights/{night_id}` | Update night entry |
| `DELETE` | `/nights/{night_id}` | Delete night entry (204) |

---

## Billing (`/billing`)

Auth varies by route (public, authenticated, or webhook-specific).

| Method | Path | Description |
|--------|------|-------------|
| Various | `/billing/public/*` | Public pricing/checkout endpoints |
| Various | `/billing/auth/*` | Authenticated subscription management |
| `POST` | `/billing/webhook` | Stripe webhook receiver |

---

## Cron (`/cron`)

**Auth:** Internal (service-to-service).

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/cron/unlock-surprises` | Unlock due surprises (scheduled task) |

---

## Architectural Conventions

### Thin Router Pattern

```
Router  ──▶  Service  ──▶  Repository  ──▶  Database
  │                    │
  │  Pydantic schema   │  Business logic
  │  Auth dependency   │  Ownership checks
  │  Rate limiting     │  State transitions
  │  HTTP status codes │  Plan limit enforcement
  │  Response models   │  S3/Redis operations
```

### Dependency Chain

```
get_current_user  →  require_couple  →  require_premium  →  PremiumUser
                    (checks couple)     (checks sub)        (type alias)

CurrentUser  →  CoupleUser  →  PremiumUser
(just auth)     (auth + couple)  (auth + couple + premium)
```

### Every Endpoint Includes

1. **Auth dependency** (`CoupleUser` or `PremiumUser`)
2. **Rate limit** (`_: RateLimit`)
3. **DB session** (`db: AsyncSession = Depends(get_db_session)`)
4. **Pydantic validation** (request body or query params)
5. **Response model** (typed, with `from_attributes` where applicable)
6. **Service instantiation** (per-request, no DI framework)
7. **Proper HTTP status** (201 for creates, 204 for deletes, 200 otherwise)

### Error Handling

All exceptions are raised from the service layer using project-wide exception classes:

| Exception | HTTP Status | When |
|-----------|-------------|------|
| `NotFoundError` | 404 | Resource not found |
| `ForbiddenError` | 403 | Not authorized for this resource |
| `UnauthorizedError` | 401 | Not authenticated |
| `ConflictError` | 409 | Duplicate resource |
| `BusinessRuleError` | 422 | Invalid state transition |
| `CoupleRequiredError` | 403 | User not in a couple |
| `PremiumRequiredError` | 402 | Premium feature for free user |
| `RateLimitError` | 429 | Too many requests |