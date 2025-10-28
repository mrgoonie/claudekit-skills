---
name: postgresql-psql
description: Comprehensive guide for PostgreSQL psql - the interactive terminal client for PostgreSQL. Use when connecting to PostgreSQL databases, executing queries, managing databases/tables, configuring connection options, formatting output, writing scripts, managing transactions, and using advanced psql features for database administration and development.
license: PostgreSQL
version: 1.0.0
---

# PostgreSQL psql Skill

PostgreSQL psql (PostgreSQL interactive terminal) is the primary command-line client for interacting with PostgreSQL databases. It provides both interactive query execution and powerful scripting capabilities for database management and administration.

## When to Use This Skill

Use this skill when:
- Connecting to PostgreSQL databases from the command line
- Executing SQL queries interactively
- Writing SQL scripts for automation
- Creating and managing databases and schemas
- Managing database objects (tables, views, indexes, functions)
- Backing up and restoring databases
- Configuring connections and authentication
- Formatting and exporting query results
- Managing transactions and permissions
- Debugging SQL queries
- Automating database administration tasks
- Setting up replication and high availability
- Creating stored procedures and functions

## Core Concepts

### REPL Model
- psql operates as an interactive REPL (Read-Eval-Print Loop)
- Accepts SQL commands and meta-commands (backslash commands)
- Maintains connection state across commands within a session
- Supports command history and editing

### Command Types
- **SQL Commands**: Standard SQL statements (SELECT, INSERT, UPDATE, DELETE, etc.)
- **Meta-Commands**: psql-specific commands prefixed with backslash (e.g., `\dt`, `\d`)
- **Backslash Commands**: Control query output, session variables, and psql behavior

### Connection Model
- Single database connection per session
- Can switch databases without reconnecting
- Connection state includes current database, user, and search path
- Environmental variables and .pgpass for credential management

## Connection Options

### Basic Connection Command

```bash
psql [OPTIONS] [DBNAME [USERNAME]]
```

### Common Connection Options

```bash
# Connect with username and host
psql -U username -h hostname -p 5432 -d database_name

# Connect using connection string
psql postgresql://username:password@hostname:5432/database_name

# Connect with password prompt
psql -U postgres -h localhost -W

# Connect to specific database on local machine
psql -d myapp_development

# Environment variables (alternative)
export PGUSER=postgres
export PGPASSWORD=mypassword
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mydb
psql
```

### Connection String Formats

**Standard URI format**:
```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```

**Example**:
```
postgresql://app_user:secretpass@db.example.com:5432/production_db?sslmode=require
```

### Authentication Methods

**Password file (.pgpass)**:
```
# ~/.pgpass (chmod 600)
hostname:port:database:username:password
localhost:5432:mydb:postgres:mypassword
*.example.com:5432:*:appuser:apppass
```

**Connection via SSH tunnel**:
```bash
ssh -L 5432:localhost:5432 user@remote-host
psql -U postgres -h localhost
```

### SSL/TLS Connection Options

```bash
# Require SSL
psql -h hostname -sslmode require -U username database

# Verify certificate
psql -h hostname -sslmode verify-full \
  -sslcert=/path/to/client-cert.crt \
  -sslkey=/path/to/client-key.key \
  -sslrootcert=/path/to/ca-cert.crt database

# SSL modes: disable, allow, prefer (default), require, verify-ca, verify-full
```

## Essential Meta-Commands

### Database and Schema Navigation

```
\l or \list                    # List all databases
\l+ or \list+                  # List databases with sizes
\c or \connect DATABASE USER   # Connect to different database
\dn or \dn+                    # List schemas (namespaces)
\dt or \dt+                    # List tables in current schema
\di or \di+                    # List indexes
\dv or \dv+                    # List views
\dm or \dm+                    # List materialized views
\ds or \ds+                    # List sequences
\df or \df+                    # List functions/procedures
\da or \da+                    # List aggregates
\dT or \dT+                    # List data types
\dF or \dF+                    # List text search configurations
```

### Object Inspection Commands

```
\d or \d NAME                  # Describe table, view, index, sequence, or function
\d+ or \d+ NAME                # Extended description with details
\da PATTERN                    # List aggregate functions matching pattern
\db or \db+                    # List tablespaces
\dc or \dc+                    # List character set encodings
\dC or \dC+                    # List type casts
\dd or \dd+                    # List object descriptions/comments
\dD or \dD+                    # List domains
\de or \de+                    # List foreign data wrappers
\dE or \dE+                    # List foreign servers
\dF or \dF+                    # List text search configurations
\dFd or \dFd+                  # List text search dictionaries
\dFp or \dFp+                  # List text search parsers
\dFt or \dFt+                  # List text search templates
\dg or \dg+                    # List database roles/users
\dl or \dl+                    # List large objects (same as \lo_list)
\dL or \dL+                    # List procedural languages
\dO or \dO+                    # List collations
\dp or \dp+                    # List table access privileges
\dRp or \dRp+                  # List replication origins
\dRs or \dRs+                  # List replication subscriptions
\ds or \ds+                    # List sequences
\dt or \dt+                    # List tables
\dU or \dU+                    # List user mapping
\du or \du+                    # List roles
\dv or \dv+                    # List views
\dx or \dx+                    # List extensions
\dX or \dX+                    # List extended statistics
```

### Formatting and Output Commands

```
\a                             # Toggle between aligned and unaligned output
\C [STRING]                    # Set table title
\f [STRING]                    # Set field separator for unaligned output
\H                             # Toggle HTML output mode
\pset OPTION [VALUE]           # Set output option (detailed below)
\t [on|off]                    # Toggle tuple-only output (no headers/footers)
\T [STRING]                    # Set HTML table tag attributes
\x or \x [on|off|auto]         # Toggle expanded/vertical output
\g or \g [FILENAME|COMMAND]    # Execute query and send output to file/command
```

### \pset Options

```
\pset border [0-2]             # Set border display (0=none, 1=ascii, 2=unicode)
\pset columns WIDTH            # Set column width limit
\pset csv                      # Set CSV output format
\pset expanded [on|off|auto]   # Toggle expanded output
\pset fieldsep STRING          # Set field separator
\pset footer [on|off]          # Toggle footer display
\pset format [aligned|unaligned|csv|tsv|html|latex|latex-longtable|troff-ms]
\pset header [on|off]          # Toggle header display
\pset linestyle [ascii|old-ascii|unicode] # Set line drawing style
\pset null STRING              # Set string to represent NULL
\pset numericlocale [on|off]   # Toggle locale-specific number formatting
\pset pager [on|off|always]    # Control pager usage
\pset recordsep STRING         # Set record separator
\pset recordsep0 [on|off]      # Use null terminator between records
\pset tableattr STRING         # Set HTML table attributes
\pset title STRING             # Set query title
\pset tuples_only [on|off]     # Toggle tuple-only mode
```

### File and History Commands

```
\copy QUERY TO FILENAME [FORMAT]          # Client-side COPY (requires fewer permissions)
\copy QUERY TO STDOUT                     # Copy to standard output
\copy TABLE FROM FILENAME [FORMAT]        # Import data from file
\e or \edit                               # Edit current query buffer in editor
\e FILENAME                               # Edit file in editor
\ef [FUNCNAME]                            # Edit function definition
\ev [VIEWNAME]                            # Edit view definition
\w FILENAME or \write FILENAME            # Write current query buffer to file
\i FILENAME or \include FILENAME          # Execute SQL commands from file
\ir FILENAME or \include_relative FILE    # Execute relative path file
\s [FILENAME]                             # Show command history (or save to file)
\o FILENAME or \out FILENAME              # Send all output to file
\o                                        # Return output to terminal
```

### Batch and Script Commands

```
\echo TEXT                     # Print text (useful in scripts)
\errverbose                    # Show last error in verbose form
\q or \quit                    # Quit psql
\! COMMAND or \shell COMMAND   # Execute shell command
\cd DIRECTORY                  # Change working directory
\pwd                           # Print current working directory
\set VARIABLE VALUE            # Set psql variable
\unset VARIABLE                # Unset psql variable
\setenv VARNAME VALUE          # Set environment variable
\getenv VARNAME                # Get environment variable value
\prompt [TEXT] VARIABLE        # Prompt user for input and set variable
```

### Transaction Commands

```
\begin or BEGIN                # Start transaction
\commit or COMMIT              # Commit transaction
\rollback or ROLLBACK          # Rollback transaction
\savepoint NAME                # Create savepoint
\release SAVEPOINT             # Release savepoint
\rollback TO SAVEPOINT         # Rollback to savepoint
```

### Information Commands

```
\d+ TABLENAME                  # Show table with extended info and storage info
\dt *.*                        # List all tables in all schemas
\dn *                          # List all schemas
\du                            # List all users/roles
\db                            # List tablespaces
\dx                            # List installed extensions
\h or \help                    # List available SQL commands
\h COMMAND or \help COMMAND    # Show help for specific SQL command
\?                             # Show psql help
\copyright                     # Show PostgreSQL copyright/license info
\version or SELECT version()   # Show PostgreSQL version
```

## Command-Line Options

### Connection Options

```bash
-h, --host=HOSTNAME           # Server host name (default: localhost)
-p, --port=PORT               # Server port (default: 5432)
-U, --username=USERNAME       # PostgreSQL user name (default: $USER)
-d, --dbname=DBNAME           # Database name to connect
-w, --no-password             # Never prompt for password
-W, --password                # Force password prompt
```

### Output and Formatting Options

```bash
-A, --no-align                # Unaligned table output mode
-c, --command=COMMAND         # Run single command and exit
-C, --copy-only               # (deprecated, use \copy instead)
-d, --dbname=DBNAME           # Specify database
-E, --echo-hidden             # Display internal queries
-e, --echo-all                # Display each command before sending
-b, --echo-errors             # Display failed commands
-f, --file=FILENAME           # Execute commands from file
-F, --field-separator=CHAR    # Set field separator for unaligned output
-H, --html                    # HTML table output mode
-l, --list                    # List available databases and exit
-L, --log-file=FILENAME       # Log session to file
-n, --no-readline             # Disable readline (line editing)
-o, --output=FILENAME         # Write results to file
-P, --pset=VARIABLE=VALUE     # Set printing option
-q, --quiet                   # Run quietly (no banner, single-line mode)
-R, --record-separator=CHAR   # Set record separator for unaligned output
-S, --single-step             # Single-step mode (confirm each command)
-s, --single-transaction      # Execute file in single transaction
-t, --tuples-only             # Print rows only (no headers/footers)
-T, --table-attr=STRING       # Set HTML table tag attributes
-v, --set=VARIABLE=VALUE      # Set psql variable
-V, --version                 # Show version and exit
-x, --expanded                # Expanded table output mode
-X, --no-psqlrc               # Do not read ~/.psqlrc startup file
-1, --single-line             # End of line terminates SQL command
```

### Other Options

```bash
-a, --all                     # (deprecated)
-j, --job=NUM                 # (for parallel dumps with pg_dump)
--help                        # Show help message
--version                     # Show version
--on-error-stop               # Stop on first error
```

## Variables and Configuration

### Built-in Variables

```bash
# Prompt variables
psql -v PROMPT1='%/%R%# '     # Set primary prompt
psql -v PROMPT2='%R%# '       # Set continuation prompt
psql -v PROMPT3='>> '         # Set output mode prompt

# Prompt expansion codes:
# %n = Database user name
# %m = Database server hostname (first part)
# %> = Database server hostname full
# %p = Database server port
# %d = Database name
# %/ = Current schema
# %~ = Like %/ but ~  if schema matches user name
# %# = # if superuser, > otherwise
# %? = Last query result status
# %% = Literal %
# %[..%] = Invisible characters (for terminal control sequences)
```

### Configuration File (~/.psqlrc)

```bash
# Auto-load on psql startup
# Set default options
\set QUIET ON
\set SQLHISTSIZE 10000

# Configure output
\pset null '[NULL]'
\pset border 2
\pset linestyle unicode
\pset expanded auto
\pset pager always

# Define useful variables
\set conn_user 'SELECT current_user;'
\set dbsize 'SELECT pg_size_pretty(pg_database_size(current_database()));'
\set tables 'SELECT tablename FROM pg_tables WHERE schemaname = ''public'';'
\set functions 'SELECT proname FROM pg_proc;'

# Define shortcuts
\set uptime 'SELECT now() - pg_postmaster_start_time() AS uptime;'
\set locks 'SELECT pid, usename, pg_blocking_pids(pid) as blocked_by, query, state FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0;'

# Set timing
\timing ON

# Connect to default database
\c mydb
```

### Variable Substitution

```sql
-- Using :variable syntax
\set table_name mytable
SELECT * FROM :table_name;

-- Using :'variable' for literal strings
\set schema_name public
SELECT * FROM :"schema_name".mytable;

-- Using :'variable' syntax in string context
\set username 'postgres'
SELECT * FROM pg_tables WHERE tableowner = :'username';

-- Using :' ' for identifier quoting
\set id_name "customTable"
SELECT * FROM :"id_name";
```

## Basic SQL Operations

### Query Execution

```sql
-- Simple query with immediate execution
SELECT * FROM users;

-- Multi-line query (continues until semicolon)
SELECT id, name, email
FROM users
WHERE active = true;

-- Query with results to file
SELECT * FROM large_table \g output.txt

-- Query with pipe to command
SELECT * FROM users \g | wc -l

-- Execute previous command
\g

-- Execute as only tuples (no headers/footers)
SELECT * FROM users;
```

### Creating Objects

```sql
-- Create database
CREATE DATABASE myapp_db;

-- Create schema
CREATE SCHEMA app_schema;

-- Create table
CREATE TABLE app_schema.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index
CREATE INDEX idx_users_email ON app_schema.users(email);

-- Create view
CREATE VIEW app_schema.active_users AS
SELECT id, name, email FROM app_schema.users WHERE active = true;

-- Create function
CREATE OR REPLACE FUNCTION app_schema.get_user_count()
RETURNS INTEGER AS $$
BEGIN
  RETURN (SELECT COUNT(*) FROM app_schema.users);
END;
$$ LANGUAGE plpgsql;
```

### Data Manipulation

```sql
-- Insert single row
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Insert multiple rows
INSERT INTO users (name, email) VALUES
  ('Jane Smith', 'jane@example.com'),
  ('Bob Johnson', 'bob@example.com');

-- Insert from query
INSERT INTO users_backup SELECT * FROM users;

-- Update data
UPDATE users SET active = false WHERE last_login < now() - interval '30 days';

-- Delete data
DELETE FROM users WHERE id = 999;

-- RETURNING clause (see what was changed)
UPDATE users SET status = 'active' 
WHERE id = 1 
RETURNING id, name, status;
```

## Transaction Management

### Transaction Control

```sql
-- Begin transaction
BEGIN;
-- or
START TRANSACTION;

-- Commit changes
COMMIT;
-- or
END;

-- Rollback changes
ROLLBACK;

-- Create savepoint
SAVEPOINT sp1;
-- ... execute statements ...
ROLLBACK TO sp1;  -- Rollback to savepoint
RELEASE sp1;      -- Release savepoint

-- Multi-statement transaction
BEGIN;
  INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);
  INSERT INTO accounts (name, balance) VALUES ('Bob', 1000);
  UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice';
  UPDATE accounts SET balance = balance + 100 WHERE name = 'Bob';
COMMIT;
```

### Transaction Isolation Levels

```sql
-- Set transaction isolation level
BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- PostgreSQL default
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Show current transaction status
SHOW transaction_isolation;
```

## Advanced Features

### Full-Text Search

```sql
-- Create full-text search vector
ALTER TABLE documents ADD COLUMN search_vector tsvector;

UPDATE documents SET search_vector = 
  to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''));

-- Create index for fast search
CREATE INDEX idx_documents_search ON documents USING GIN(search_vector);

-- Search documents
SELECT * FROM documents 
WHERE search_vector @@ to_tsquery('english', 'database & tutorial');

-- Ranking results by relevance
SELECT id, title, ts_rank(search_vector, query) AS rank
FROM documents, to_tsquery('english', 'database') AS query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

### Window Functions

```sql
-- Row number
SELECT id, name, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- Running sum
SELECT id, amount, date,
  SUM(amount) OVER (ORDER BY date) AS running_total
FROM transactions;

-- Partition results
SELECT id, department, salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- LEAD/LAG (next/previous row)
SELECT id, date, amount,
  LAG(amount) OVER (ORDER BY date) AS prev_amount,
  LEAD(amount) OVER (ORDER BY date) AS next_amount
FROM transactions;
```

### JSON Operations

```sql
-- Store JSON
INSERT INTO documents VALUES (1, '{"name": "Alice", "age": 30}');

-- Access JSON fields
SELECT data -> 'name' AS name FROM documents;

-- Access with default
SELECT data ->> 'name' AS name_text FROM documents;  -- Returns text

-- Check if key exists
SELECT * FROM documents WHERE data ? 'name';

-- JSON array operations
SELECT json_array_length(data) FROM documents;

-- JSON aggregation
SELECT json_agg(name) FROM users;

-- JSONB (binary JSON) is preferred for performance
CREATE TABLE config (id INT, settings JSONB);
INSERT INTO config VALUES (1, '{"theme": "dark", "lang": "en"}');

-- JSONB operators are more efficient
SELECT settings @> '{"theme": "dark"}' FROM config;
```

### Common Table Expressions (CTEs)

```sql
-- Simple CTE
WITH active_users AS (
  SELECT id, name, email FROM users WHERE active = true
)
SELECT * FROM active_users WHERE created_at > '2024-01-01';

-- Recursive CTE (tree traversal)
WITH RECURSIVE category_hierarchy AS (
  SELECT id, name, parent_id, 0 AS level
  FROM categories
  WHERE parent_id IS NULL
  
  UNION ALL
  
  SELECT c.id, c.name, c.parent_id, h.level + 1
  FROM categories c
  JOIN category_hierarchy h ON c.parent_id = h.id
)
SELECT * FROM category_hierarchy;

-- Multiple CTEs
WITH orders_2024 AS (
  SELECT * FROM orders WHERE EXTRACT(YEAR FROM order_date) = 2024
),
customer_totals AS (
  SELECT customer_id, SUM(total_amount) AS total
  FROM orders_2024
  GROUP BY customer_id
)
SELECT c.name, ct.total
FROM customers c
JOIN customer_totals ct ON c.id = ct.customer_id
ORDER BY ct.total DESC;
```

## Scripting with psql

### Running SQL Files

```bash
# Execute file
psql -d mydb -f script.sql

# Execute with output to file
psql -d mydb -f script.sql -o results.txt

# Execute with error stopping
psql -d mydb -f script.sql --on-error-stop

# Execute in single transaction
psql -d mydb -f script.sql -s

# Multiple files (executed in order)
psql -d mydb -f init.sql -f seed.sql -f verify.sql
```

### SQL Script Best Practices

```sql
-- sample_script.sql

-- Set execution mode
\set ON_ERROR_STOP ON
\set QUIET OFF

-- Drop existing objects if needed
DROP TABLE IF EXISTS temp_table;

-- Create table
CREATE TABLE temp_table (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Insert data
INSERT INTO temp_table (name) VALUES
  ('Record 1'),
  ('Record 2'),
  ('Record 3');

-- Verify results
SELECT * FROM temp_table;

-- Cleanup
DROP TABLE temp_table;

-- Report
\echo 'Script completed successfully!'
```

### Dynamic SQL Scripts

```bash
#!/bin/bash

# Bash script with psql variables
DATABASE="myapp_db"
TABLE_NAME="users"
SCHEMA_NAME="public"

# Execute with variable substitution
psql -d $DATABASE -v table_name=$TABLE_NAME \
  -v schema_name=$SCHEMA_NAME -c "
  SELECT COUNT(*) FROM :schema_name.:table_name;
"

# Loop through databases
for db in $(psql -l | awk '{print $1}'); do
  if [[ ! "$db" =~ "template" ]]; then
    echo "Backing up $db..."
    pg_dump $db > /backups/$db.sql
  fi
done
```

## Import and Export

### COPY Commands

```sql
-- Server-side COPY (requires superuser for file operations)
COPY users (id, name, email) 
TO '/tmp/users.csv' 
WITH (FORMAT CSV, HEADER TRUE, QUOTE '"', ESCAPE '\\');

-- Import CSV
COPY users (id, name, email)
FROM '/tmp/users.csv'
WITH (FORMAT CSV, HEADER TRUE, QUOTE '"', ESCAPE '\\');

-- Tab-separated values
COPY users TO '/tmp/users.tsv' WITH (FORMAT TEXT, DELIMITER E'\t');

-- With NULL handling
COPY users TO '/tmp/users.csv' 
WITH (FORMAT CSV, NULL 'N/A', QUOTE '"');
```

### Client-side COPY (\copy)

```bash
# Export to CSV (from psql)
\copy users TO '/home/user/users.csv' WITH (FORMAT CSV, HEADER)

# Export with query results
\copy (SELECT id, name, email FROM users WHERE active = true) \
  TO '/tmp/active_users.csv' WITH (FORMAT CSV, HEADER)

# Import CSV
\copy users (id, name, email) FROM '/tmp/users.csv' WITH (FORMAT CSV, HEADER)

# Export to stdout (pipe to file)
\copy users TO STDOUT WITH (FORMAT CSV, HEADER) > users.csv

# Import from stdin
cat users.csv | \copy users FROM STDIN WITH (FORMAT CSV, HEADER)
```

### Using pg_dump and pg_restore

```bash
# Dump entire database
pg_dump -d mydb -U postgres > mydb_backup.sql

# Dump with custom format (compressed)
pg_dump -d mydb -Fc > mydb_backup.dump

# Dump specific table
pg_dump -d mydb -t users > users_backup.sql

# Dump with data only
pg_dump -d mydb -a > mydb_data.sql

# Dump schema only
pg_dump -d mydb -s > mydb_schema.sql

# Restore from SQL file
psql -d mydb_restored -f mydb_backup.sql

# Restore from custom format
pg_restore -d mydb_restored mydb_backup.dump

# List contents of dump
pg_restore -l mydb_backup.dump
```

## Performance and Debugging

### Query Analysis

```sql
-- Show query execution plan
EXPLAIN SELECT * FROM users WHERE id = 1;

-- Detailed analysis with actual execution
EXPLAIN ANALYZE SELECT * FROM users WHERE id = 1;

-- Show more details
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
  SELECT * FROM users WHERE active = true;

-- JSON output for programmatic parsing
EXPLAIN (FORMAT JSON, ANALYZE)
  SELECT COUNT(*) FROM users;
```

### Viewing Query Performance

```sql
-- Current queries
SELECT pid, usename, state, query FROM pg_stat_activity;

-- Long-running queries
SELECT pid, usename, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Blocking queries
SELECT blocked_pid, blocking_pid, blocked_statement, blocking_statement
FROM pg_stat_statements;

-- Table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Database size
SELECT pg_size_pretty(pg_database_size('mydb'));
```

### Setting Timing

```bash
# Enable query timing
\timing ON

# Disable query timing
\timing OFF

# In batch mode
psql -d mydb -c "\timing ON" -f script.sql
```

### Query Logging

```bash
# Log all queries to file
psql -d mydb -L query.log -f script.sql

# Show internal queries (system queries)
psql -d mydb -E
```

## User and Permission Management

### Creating and Managing Users

```sql
-- Create user (role)
CREATE USER appuser WITH PASSWORD 'secure_password';

-- Create role without login privilege
CREATE ROLE admin_role;

-- Alter user
ALTER USER appuser WITH PASSWORD 'new_password';

-- Create superuser
CREATE USER superuser_name WITH PASSWORD 'password' SUPERUSER;

-- List users
\du

-- Drop user
DROP USER appuser;
```

### Grant Permissions

```sql
-- Grant database usage
GRANT USAGE ON SCHEMA public TO appuser;

-- Grant table permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO appuser;

-- Grant all permissions
GRANT ALL PRIVILEGES ON users TO appuser;

-- Grant sequence permissions (for auto-increment)
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO appuser;

-- Grant to all tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO appuser;

-- Make privileges default for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO appuser;

-- View permissions
\dp users
\dp+ users
```

### Row Level Security (RLS)

```sql
-- Enable RLS on table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY user_policy ON users
  USING (id = current_user_id());  -- This would need to be implemented

-- View policies
\d+ users
```

## Advanced psql Features

### Meta-command Tricks

```bash
# Show last error in detail
\errverbose

# Execution timing
\timing

# Echo all commands sent to server
\set ECHO all

# List all variables
\set

# View specific variable
\echo :DBNAME

# Dynamic query execution
\set query 'SELECT * FROM users WHERE id = ' :user_id
:query;
```

### Prompt Customization

```bash
# Set custom prompts
psql -v PROMPT1='user@db> '
psql -v PROMPT1='%/%R%# '   # database/role# 

# In .psqlrc
\set PROMPT1 '%n@%m:%>/%/ %R%# '
\set PROMPT2 '> '
\set PROMPT3 '>> '
```

### Function and Procedure Management

```sql
-- List functions
\df

-- Show function source
\df+ function_name

-- Create function
CREATE OR REPLACE FUNCTION get_user(user_id INT)
RETURNS TABLE(id INT, name TEXT, email TEXT) AS $$
BEGIN
  RETURN QUERY
  SELECT u.id, u.name, u.email FROM users u WHERE u.id = user_id;
END;
$$ LANGUAGE plpgsql;

-- Execute function
SELECT * FROM get_user(1);

-- Stored procedure (no return value)
CREATE OR REPLACE PROCEDURE archive_old_records()
AS $$
BEGIN
  INSERT INTO archived_users
  SELECT * FROM users WHERE created_at < now() - interval '1 year';
  DELETE FROM users WHERE created_at < now() - interval '1 year';
  COMMIT;
END;
$$ LANGUAGE plpgsql;

-- Call procedure
CALL archive_old_records();
```

### Triggers and Events

```sql
-- Create trigger function
CREATE OR REPLACE FUNCTION update_user_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER user_update_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_user_timestamp();

-- View triggers
\d+ users

-- Drop trigger
DROP TRIGGER user_update_timestamp ON users;
```

## Backup and Recovery

### Database Backup Strategies

```bash
# Full database backup (custom format)
pg_dump -d production_db -Fc -j 4 > backup.dump

# Backup with compression
pg_dump -d production_db -Fc -Z 9 > backup.dump

# Parallel backup (faster for large databases)
pg_dump -d production_db -Fd -j 4 -f backup_dir

# Backup specific schemas
pg_dump -d production_db -n public -n app > schemas.sql

# Backup with custom format (allows selective restore)
pg_dump -d production_db -Fc > backup.dump

# View backup contents
pg_restore -l backup.dump | less

# Restore specific table
pg_restore -d restored_db -t users backup.dump

# List available backups
pg_dump -U postgres -l -w postgres
```

### Point-in-Time Recovery

```bash
# Full backup
pg_dump -d mydb > base_backup.sql

# Enable WAL archiving (in postgresql.conf)
wal_level = replica
archive_mode = on
archive_command = 'cp %p /archive/%f'

# Restore to point in time
pg_restore -d recovered_db base_backup.sql
# Then apply WAL files up to target time
```

## Common Patterns and Examples

### Connection Pooling Script

```bash
#!/bin/bash
# Simple connection pool using psql

MAX_CONNECTIONS=10
CONNECTION_POOL=()

for i in {1..$MAX_CONNECTIONS}; do
  (
    while true; do
      psql -d mydb -c "SELECT 1"
      sleep 60
    done
  ) &
  CONNECTION_POOL+=($!)
done

# Keep script running
wait
```

### Database Health Check

```sql
-- health_check.sql
SELECT 
  'PostgreSQL Version' AS check_type,
  version() AS result
UNION ALL
SELECT 
  'Database Size',
  pg_size_pretty(pg_database_size(current_database()))
UNION ALL
SELECT 
  'Active Connections',
  count(*)::text
FROM pg_stat_activity
UNION ALL
SELECT 
  'Cache Hit Ratio',
  ROUND(sum(heap_blks_hit)::numeric / (sum(heap_blks_hit) + sum(heap_blks_read)), 4)::text
FROM pg_statio_user_tables;
```

### Automated Maintenance

```bash
#!/bin/bash
# Weekly maintenance script

DATABASES=$(psql -t -c "SELECT datname FROM pg_database WHERE datistemplate = false AND datname != 'postgres';")

for db in $DATABASES; do
  echo "Analyzing $db..."
  psql -d "$db" -c "ANALYZE;"
  
  echo "Vacuuming $db..."
  psql -d "$db" -c "VACUUM;"
  
  echo "Reindexing $db..."
  psql -d "$db" -c "REINDEX DATABASE \"$db\";"
done
```

## Best Practices

1. **Use connection pooling** - For applications, not necessary for interactive psql
2. **Enable SSL/TLS** - Always use encrypted connections in production
3. **Use .pgpass** - Avoid hardcoding passwords in scripts
4. **Set ON_ERROR_STOP** - In scripts to prevent continuing after errors
5. **Use transactions** - Wrap related operations in explicit transactions
6. **Index strategically** - Analyze query plans and create indexes on frequent filter/join columns
7. **Monitor performance** - Regularly check slow queries and table sizes
8. **Backup regularly** - Use pg_dump with custom format for flexibility
9. **Use schemas** - Organize database objects logically
10. **Document permissions** - Keep clear records of user roles and permissions
11. **Test recovery** - Regularly practice restoring from backups
12. **Use parameterized queries** - In applications to prevent SQL injection
13. **Monitor locks** - Check for blocking queries in pg_stat_activity
14. **Maintain statistics** - Run ANALYZE regularly for query optimizer

## Tips and Tricks

### Quick Navigation

```bash
# Connect and execute in one line
psql -d mydb -c "SELECT COUNT(*) FROM users;"

# Execute file and exit
psql -d mydb -f script.sql

# Quiet mode (minimal output)
psql -q -d mydb -c "SELECT * FROM users LIMIT 1;"

# Pipe output to other commands
psql -d mydb -t -c "SELECT name FROM users;" | sort | uniq

# Verify connection without executing commands
psql -d mydb -c ""
```

### Useful .psqlrc Shortcuts

```bash
# Add to ~/.psqlrc for convenient shortcuts
\set dbsize 'SELECT pg_size_pretty(pg_database_size(current_database()))'
\set uptime 'SELECT now() - pg_postmaster_start_time() AS uptime'
\set psql_version 'SELECT version()'
\set table_sizes 'SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'\''.\'\'||tablename)) FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'\''.\'\'||tablename) DESC'

# Usage in psql:
# :dbsize
# :table_sizes
```

### Working with Large Result Sets

```bash
# Set pager for large results
\pset pager always

# Use LIMIT for testing
SELECT * FROM huge_table LIMIT 10;

# Use OFFSET for pagination
SELECT * FROM users LIMIT 10 OFFSET 0;
SELECT * FROM users LIMIT 10 OFFSET 10;

# Fetch into file instead of terminal
\copy (SELECT * FROM huge_table) TO huge_export.csv;
```

## Troubleshooting

### Connection Issues

```bash
# Verbose connection diagnostics
psql -d mydb -v verbose=on --echo-queries

# Check connection settings
psql --version
psql -d postgres -c "SHOW password_encryption;"

# TCP/IP connectivity test
psql -h hostname -d postgres -U postgres -c "SELECT 1;"
```

### Common Error Messages

```
FATAL: password authentication failed
  → Check password, user exists, .pgpass has correct permissions (600)

FATAL: no pg_hba.conf entry for host
  → Database server's pg_hba.conf needs connection rule

FATAL: database "name" does not exist
  → Create database or check database name spelling

ERROR: permission denied for schema
  → Grant USAGE on schema to user

ERROR: syntax error
  → Check SQL syntax, use \h for help on commands
```

### Performance Issues

```sql
-- Find slow queries
SELECT * FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Check for missing indexes
SELECT schemaname, tablename, attname 
FROM pg_stat_user_tables, pg_attribute 
WHERE pg_stat_user_tables.relid = pg_attribute.attrelid
AND seq_scan > 0;

-- Check cache efficiency
SELECT 
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit)  as heap_hit,
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS ratio
FROM pg_statio_user_tables;
```

## Advanced Configuration

### Performance Tuning Parameters

```bash
# In ~/.psqlrc
\set HISTSIZE 10000
\pset pager always
\pset null '[NULL]'
\pset linestyle unicode

# Environment variables for defaults
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGDATABASE=mydb
export PGPASSFILE=$HOME/.pgpass
```

### Output Formats Comparison

```
-- Aligned (default)
\pset format aligned

-- CSV
\pset format csv
\copy (SELECT * FROM users) TO STDOUT WITH (FORMAT CSV);

-- HTML
\pset format html
SELECT * FROM users LIMIT 5;

-- LaTeX
\pset format latex
SELECT * FROM users LIMIT 5;

-- Expanded (vertical)
\x
SELECT * FROM users LIMIT 1;
```

## Resources and Documentation

- Official PostgreSQL Documentation: https://www.postgresql.org/docs/
- psql Manual: https://www.postgresql.org/docs/current/app-psql.html
- PostgreSQL Wiki: https://wiki.postgresql.org/
- pgAdmin (GUI tool): https://www.pgadmin.org/
- DBA Best Practices: https://www.postgresql.org/docs/current/sql-syntax.html

## Summary

psql is a powerful, flexible command-line tool for PostgreSQL database administration and development. Key strengths:

- Interactive REPL for immediate query feedback
- Powerful meta-commands for object inspection and management
- Scripting capabilities for automation
- Extensive formatting options for different output needs
- Built-in help and documentation
- Variable substitution for dynamic queries
- Connection management and SSL/TLS support
- Performance analysis and query optimization tools

Master psql to unlock efficient PostgreSQL workflows, from simple queries to complex database administration tasks.
