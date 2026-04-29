# Database Setup (`psql`)

## 1 Prerequisites

- Install PostgreSQL (includes `psql`)
- Ensure the PostgreSQL server is running
- From the project root, make sure these files exist:
  - `relationalSchema.sql`
  - `seed.sql`
  - `.env.example`

## 2 Create the database

```bash
# Log into Postgres as your local superuser
psql -U postgres
```

Then run in the `psql` prompt:

```sql
CREATE DATABASE CS480Project;
\q
```

If your local Postgres user is not `postgres`, replace it with your username in all commands below.

## 3 Load schema and seed data

Run these commands from the project root:

```bash
psql -U postgres -d CS480Project -f relationalSchema.sql
psql -U postgres -d CS480Project -f seed.sql
```

## 4 Configure environment variables

Copy `.env.example` to `.env`, then fill in your local credentials:

```env
DB_NAME=CS480Project
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## 5 Verify setup

```bash
psql -U your_username -d CS480Project
```

Then run:

```sql
\dt
SELECT COUNT(*) FROM Managers;
SELECT COUNT(*) FROM Client;
SELECT COUNT(*) FROM Hotel;
SELECT COUNT(*) FROM Room;
\q
```

## Common issues

- `password authentication failed`
  - Check `DB_USER` and `DB_PASSWORD` in `.env`
  - Check the `-U` user in your `psql` commands

- `database "CS480Project" does not exist`
  - Re-run the database creation step

- `could not connect to server`
  - Start the PostgreSQL service and try again
