# Web UI Authentication & Analytics Plan

## Requirements

1. **Access Control**: Federated access with shareable credentials that expire
2. **PDF/EPUB Downloads**: Make generated translations downloadable from the web UI
3. **Analytics**: Track which users visited/read which parts of the translation

## Architecture Decision

The current static site (GitHub Pages) cannot support authentication and user-specific analytics. We need to choose a deployment platform:

### Option 1: Astro SSR + Vercel/Netlify (Recommended)
**Pros:**
- Keeps existing Astro codebase
- Built-in serverless functions for auth
- Easy deployment
- Can add database integration (Vercel Postgres, Supabase)
- Edge middleware for auth checks

**Cons:**
- Moves away from GitHub Pages
- Requires paid tier for analytics storage (or separate DB)

**Stack:**
- Astro SSR mode
- Vercel Edge Functions or Netlify Functions
- Database: Vercel Postgres, Supabase, or Planetscale
- Auth: Custom JWT tokens with expiration

### Option 2: Keep Static + Add Backend API
**Pros:**
- Keep GitHub Pages for static assets
- Separate auth/analytics backend
- Clear separation of concerns

**Cons:**
- Two deployments to manage
- CORS configuration needed
- More complex architecture

**Stack:**
- Frontend: Astro static site (GitHub Pages)
- Backend: FastAPI or Express.js
- Database: PostgreSQL or MongoDB
- Hosting: Railway, Render, or Fly.io

### Option 3: Firebase/Supabase (BaaS)
**Pros:**
- Minimal backend code
- Built-in auth with expiring tokens
- Real-time database
- Analytics tracking included
- Generous free tier

**Cons:**
- Vendor lock-in
- Less control over auth logic

**Stack:**
- Astro static site
- Firebase Auth + Firestore
- Or: Supabase Auth + PostgreSQL

## Recommended Approach: Astro SSR + Vercel + Supabase

This combines the best of all options:
- **Astro SSR on Vercel**: Handles routing, rendering, edge middleware
- **Supabase**: Handles auth, database (PostgreSQL), real-time subscriptions
- **Vercel Edge Config**: Store access tokens with TTL

### Features Implementation

#### 1. Access Control

**Access Token System:**
```typescript
// Token structure
interface AccessToken {
  id: string;
  email: string;
  name: string;
  created_at: timestamp;
  expires_at: timestamp;
  created_by: string; // admin who created it
  last_used_at: timestamp;
}
```

**Flow:**
1. Admin generates shareable link: `https://site.com/login?token=abc123`
2. User clicks link, token is validated (not expired)
3. Session is created, user can access the site
4. Token usage is logged
5. Admin can revoke tokens anytime

**Implementation:**
- Supabase Row Level Security (RLS) for token management
- Astro middleware checks token on each request
- Store session in HTTP-only cookie

#### 2. PDF/EPUB Downloads

**Static Files:**
```
webui/
├── public/
│   └── downloads/
│       ├── translation_english.pdf
│       ├── translation_english.epub
│       ├── translation_english_with_notes.pdf
│       └── translation_english_with_notes.epub
```

**Build Process:**
```json
// webui/package.json
{
  "scripts": {
    "generate-exports": "python3 ../scripts/generate-pdf.py --output public/downloads/translation_english.pdf && ...",
    "prebuild": "npm run generate-exports",
    "build": "astro build"
  }
}
```

**Download Page:**
- Track downloads per user
- Show file sizes, formats
- Option to include/exclude translator notes

#### 3. Analytics & Reading Progress

**Database Schema:**

```sql
-- Users table (managed by Supabase Auth)
-- access_tokens table (for invite links)
CREATE TABLE access_tokens (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  token text UNIQUE NOT NULL,
  email text NOT NULL,
  name text NOT NULL,
  created_by uuid REFERENCES auth.users(id),
  created_at timestamptz DEFAULT now(),
  expires_at timestamptz NOT NULL,
  last_used_at timestamptz,
  revoked boolean DEFAULT false
);

-- Reading progress
CREATE TABLE reading_progress (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id),
  chunk_id integer NOT NULL,
  started_at timestamptz DEFAULT now(),
  last_read_at timestamptz DEFAULT now(),
  time_spent_seconds integer DEFAULT 0,
  completed boolean DEFAULT false,
  UNIQUE(user_id, chunk_id)
);

-- Page views
CREATE TABLE page_views (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id),
  chunk_id integer,
  viewed_at timestamptz DEFAULT now(),
  session_id text,
  referrer text,
  user_agent text
);

-- Downloads
CREATE TABLE downloads (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id),
  file_name text NOT NULL,
  downloaded_at timestamptz DEFAULT now()
);
```

**Analytics Dashboard (Admin Only):**

```
/admin/analytics
├── Overview
│   ├── Total users
│   ├── Active users (last 7 days)
│   ├── Total page views
│   └── Average reading progress
├── User List
│   ├── Name, Email
│   ├── Last active
│   ├── Chunks read (39/39)
│   ├── Time spent
│   └── Downloads
└── Reading Heatmap
    └── Which chunks are most/least read
```

**Client-Side Tracking:**

```typescript
// Track time on page
let startTime = Date.now();
let chunkId = getCurrentChunk();

// Every 30 seconds, update reading progress
setInterval(() => {
  const timeSpent = Math.floor((Date.now() - startTime) / 1000);

  fetch('/api/track-reading', {
    method: 'POST',
    body: JSON.stringify({
      chunk_id: chunkId,
      time_spent: timeSpent
    })
  });

  startTime = Date.now();
}, 30000);

// Track chunk completion (scrolled to bottom or next chunk)
window.addEventListener('beforeunload', () => {
  markChunkComplete(chunkId);
});
```

## Implementation Phases

### Phase 1: Infrastructure Setup (Week 1)
- [ ] Convert Astro to SSR mode
- [ ] Set up Vercel project
- [ ] Set up Supabase project
- [ ] Configure database schema
- [ ] Set up environment variables

### Phase 2: Authentication (Week 1-2)
- [ ] Implement token generation system
- [ ] Create admin panel for managing tokens
- [ ] Add middleware for auth checks
- [ ] Implement login flow
- [ ] Add session management
- [ ] Test token expiration

### Phase 3: PDF/EPUB Downloads (Week 2)
- [ ] Add build script to generate exports
- [ ] Create downloads page
- [ ] Track downloads in database
- [ ] Add file metadata (size, updated date)

### Phase 4: Analytics (Week 2-3)
- [ ] Implement reading progress tracking
- [ ] Add page view tracking
- [ ] Create analytics dashboard
- [ ] Add user reading history
- [ ] Implement admin reports

### Phase 5: Polish & Deploy (Week 3)
- [ ] Add loading states
- [ ] Error handling
- [ ] Rate limiting
- [ ] Security audit
- [ ] Documentation
- [ ] Deploy to production

## File Structure

```
spastics-dance/
├── webui/
│   ├── src/
│   │   ├── middleware/
│   │   │   └── auth.ts              # Check auth on requests
│   │   ├── lib/
│   │   │   ├── supabase.ts          # Supabase client
│   │   │   ├── auth.ts              # Auth utilities
│   │   │   └── analytics.ts         # Analytics utilities
│   │   ├── pages/
│   │   │   ├── login.astro          # Token-based login
│   │   │   ├── downloads.astro      # PDF/EPUB downloads
│   │   │   ├── admin/
│   │   │   │   ├── index.astro      # Admin dashboard
│   │   │   │   ├── tokens.astro     # Manage access tokens
│   │   │   │   └── analytics.astro  # Analytics dashboard
│   │   │   └── api/
│   │   │       ├── track-reading.ts # Track reading progress
│   │   │       ├── track-download.ts # Track downloads
│   │   │       └── validate-token.ts # Validate access tokens
│   │   └── components/
│   │       ├── ProgressTracker.astro # Client-side tracking
│   │       └── AdminNav.astro        # Admin navigation
│   ├── astro.config.mjs             # Update to SSR mode
│   └── .env.example
└── scripts/
    └── generate-exports.sh          # Generate all export formats
```

## Environment Variables

```bash
# Supabase
PUBLIC_SUPABASE_URL=https://xxx.supabase.co
PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxxx...

# App
SECRET_KEY=your-secret-key-for-jwt
ADMIN_EMAIL=your-email@example.com

# Vercel (auto-configured)
VERCEL_URL=your-site.vercel.app
```

## Security Considerations

1. **Token Security:**
   - Tokens are single-use for login, then sessions are used
   - HTTP-only cookies for session storage
   - CSRF protection
   - Rate limiting on login endpoint

2. **Data Privacy:**
   - No PII stored beyond email/name
   - Reading analytics are opt-out
   - Admin access is strictly controlled
   - Row Level Security on all database tables

3. **API Security:**
   - All API routes require authentication
   - Admin routes require admin role
   - Input validation on all endpoints
   - Rate limiting on analytics endpoints

## Cost Estimate

**Free Tier (Good for ~100 users):**
- Vercel: Free (Hobby plan)
- Supabase: Free (500MB database, 2GB bandwidth)
- Total: $0/month

**Paid Tier (For production):**
- Vercel Pro: $20/month
- Supabase Pro: $25/month
- Total: $45/month

## Alternative: Simple Solution (No Backend)

If you want to avoid backend complexity, here's a simpler approach:

1. **Password Protection**: Single shared password (no user tracking)
2. **Static Downloads**: Include PDF/EPUB as static files
3. **Basic Analytics**: Privacy-friendly Plausible or Fathom ($9-14/month)

This keeps the static site architecture but sacrifices:
- Individual user tracking
- Expiring credentials
- Detailed reading analytics

## Questions to Decide

1. **Budget**: Free tier OK or willing to pay $45/month?
2. **Privacy**: How detailed should user tracking be?
3. **Admin burden**: Who will manage access tokens?
4. **Timeline**: When do you need this live?
5. **User scale**: How many people will have access?

## Next Steps

1. Choose architecture option (recommend Astro SSR + Supabase)
2. I can implement the full system with all features
3. Or we can start with a simpler MVP and add features incrementally

Let me know your preferences and I'll proceed with implementation!
