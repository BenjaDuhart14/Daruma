# 🔒 Security Guide for Daruma

This guide explains how to properly secure your Daruma installation.

## ⚠️ Important: This is a Public Repository

Since this repo is public, **NEVER** commit:
- `.env` files
- API keys or tokens
- Passwords (plain text or hashed)
- Supabase URLs or project IDs
- Any personal data

---

## 1. Enable Row Level Security (RLS) on Supabase

RLS prevents unauthorized access to your data even if someone obtains your API key.

### Step 1: Run the RLS Migration

1. Go to **Supabase Dashboard** → **SQL Editor**
2. Copy and paste the contents of `sql/enable_rls.sql`
3. Click **Run**

### Step 2: Verify RLS is Enabled

Run this query in Supabase SQL Editor:

```sql
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

All tables should show `rowsecurity = true`.

---

## 2. Use Service Role Key (Not Anon Key)

After enabling RLS, you MUST switch from `anon` key to `service_role` key:

### Step 1: Get Your Service Role Key

1. Go to **Supabase Dashboard** → **Settings** → **API**
2. Find **service_role** key (under "Project API keys")
3. Copy the entire key (starts with `eyJ...`)

### Step 2: Update Streamlit Cloud Secrets

1. Go to **Streamlit Cloud** → Your App → **Settings** → **Secrets**
2. Update `SUPABASE_KEY` with the service_role key:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "eyJ...your-service-role-key..."

[auth]
email = "your@email.com"
password_hash = "$2b$12$...your-bcrypt-hash..."
```

### Step 3: Update GitHub Actions Secrets

1. Go to **GitHub** → Your Repo → **Settings** → **Secrets and variables** → **Actions**
2. Update `SUPABASE_KEY` with the service_role key

---

## 3. Use Hashed Passwords (bcrypt)

Passwords should be stored as bcrypt hashes, not plain text.

### Generate a Password Hash

```bash
cd ~/investment-tracker
python src/scripts/generate_password_hash.py
```

Or manually:

```bash
python -c "import bcrypt; print(bcrypt.hashpw(b'your-password', bcrypt.gensalt()).decode())"
```

### Update Streamlit Secrets

Replace `password` with `password_hash`:

```toml
[auth]
email = "your@email.com"
password_hash = "$2b$12$abcdefghijklmnop..."  # your generated hash
```

---

## 4. Security Checklist

Run this checklist before going to production:

- [ ] `.env` is in `.gitignore`
- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] No hardcoded API keys in code
- [ ] No Supabase URLs in committed files
- [ ] RLS enabled on all tables
- [ ] Using `service_role` key (not `anon`)
- [ ] Password stored as bcrypt hash
- [ ] GitHub repo secrets configured
- [ ] Streamlit Cloud secrets configured

---

## 5. What Each Key Can Do

| Key | Access | Where to Use |
|-----|--------|--------------|
| `anon` (public) | Blocked by RLS policies | ❌ Don't use |
| `service_role` | Bypasses RLS, full access | ✅ Backend only (Streamlit, GitHub Actions) |

**NEVER** expose `service_role` key in:
- Frontend JavaScript
- Public repositories
- Browser localStorage
- Client-side code

---

## 6. If You Suspect a Breach

1. **Immediately** rotate your Supabase API keys:
   - Go to Supabase → Settings → API → Regenerate keys
   
2. Update all secrets:
   - Streamlit Cloud
   - GitHub Actions
   - Local `.env`

3. Review Supabase logs for unauthorized access

4. Change your password and regenerate hash

---

## 7. Additional Recommendations

### For Extra Security:

1. **Enable 2FA** on:
   - GitHub account
   - Supabase account
   - Streamlit Cloud

2. **Set up alerts**:
   - GitHub security alerts
   - Supabase usage alerts

3. **Regular audits**:
   - Review GitHub Actions logs
   - Check Supabase connection logs
   - Monitor for unusual data access

---

## Need Help?

If you discover a security vulnerability, please:
1. Do NOT create a public GitHub issue
2. Email the maintainer directly
3. Allow time for a fix before disclosure

---

*Last updated: January 2026*
