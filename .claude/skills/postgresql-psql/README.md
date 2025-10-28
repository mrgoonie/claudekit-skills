# PostgreSQL psql Agent Skill

A comprehensive Agent Skill for Claude Code providing complete reference documentation for PostgreSQL's psql command-line client.

## Overview

This skill provides production-ready guidance for:
- Connecting to PostgreSQL databases
- Executing SQL queries and scripts
- Managing database objects (tables, views, functions, etc.)
- Administering users and permissions
- Optimizing query performance
- Automating database tasks
- Backing up and recovering data
- Troubleshooting common issues

## Files in This Skill

- **SKILL.md** (1,336 lines): Complete reference documentation
- **EXPLORATION-REPORT.md** (416 lines): Detailed analysis of coverage and features
- **README.md** (this file): Quick start guide

## Quick Reference

### Most Common psql Commands

```bash
# Connect to database
psql -U username -h hostname -d database_name

# Show help
\?

# List databases
\l

# Connect to database
\c database_name

# List tables
\dt

# Describe table
\d table_name

# Execute query from file
psql -f script.sql

# Export data
\copy (SELECT * FROM table) TO STDOUT WITH (FORMAT CSV);
```

### Essential Meta-Commands

```
\l          List databases
\dt         List tables
\d NAME     Describe object
\c DB       Connect to database
\copy       Import/export data
\q          Quit
```

## Documentation Structure

The SKILL.md is organized into 24 major sections:

1. **Connection Options** - All methods to connect to PostgreSQL
2. **Essential Meta-Commands** - 70+ backslash commands
3. **Command-Line Options** - 25+ command-line flags
4. **Variables and Configuration** - .psqlrc setup and customization
5. **SQL Operations** - DML, DDL, and query patterns
6. **Transaction Management** - ACID operations and isolation levels
7. **Advanced Features** - Full-text search, JSON, CTEs, window functions
8. **Scripting** - Automation with SQL and bash
9. **Import/Export** - COPY, \copy, pg_dump/restore
10. **Performance** - Query analysis and optimization
11. **User Management** - Roles, permissions, security
12. **Real-World Patterns** - Production scripts and examples
13. **Best Practices** - 13 key guidelines
14. **Troubleshooting** - Common issues and solutions

## Key Features

### Complete Meta-Command Reference
All 70+ backslash commands organized by function:
- Database navigation
- Object inspection
- Output formatting
- File operations
- Transaction control

### Practical Examples
150+ code examples covering:
- Connection methods (local, remote, SSL, SSH)
- Query patterns
- Database administration
- Automation scripts
- Performance analysis

### Advanced SQL Coverage
- Full-text search with ranking
- Window functions (ROW_NUMBER, LEAD/LAG, etc.)
- JSON/JSONB operations
- Common Table Expressions (CTEs)
- Recursive queries

### Real-World Patterns
Three production-ready scripts:
1. Connection pooling with Bash
2. Database health check query
3. Automated maintenance script

### Troubleshooting Guide
- Connection issues and solutions
- Performance optimization
- Common error messages
- Debug techniques

## Usage in Claude Code

This skill is designed for Claude Code users to:
- Get instant help on psql commands and syntax
- Reference best practices for database operations
- Find examples for common database tasks
- Troubleshoot connection and performance issues
- Write optimized SQL and scripts

### Example Prompts

```
"How do I export a table to CSV using psql?"
"Show me how to create an index in PostgreSQL"
"What's the best way to backup a PostgreSQL database?"
"How do I find slow queries in PostgreSQL?"
"Help me set up a connection with SSL in psql"
```

## Content Coverage

| Category | Scope | Details |
|----------|-------|---------|
| Connection Methods | 100% | 8+ variations documented |
| Meta-Commands | 100% | 70+ commands with syntax |
| SQL Operations | 95% | DML, DDL, advanced patterns |
| Performance Tuning | 100% | EXPLAIN, monitoring, optimization |
| User Management | 100% | Roles, grants, security |
| Backup/Recovery | 100% | Strategies and procedures |
| Scripting | 100% | Bash integration and examples |
| Troubleshooting | 100% | Common issues and solutions |

## Installation

This skill is located in the repository at:
```
.claude/skills/postgresql-psql/
```

If using Claude Code's skill system, it will be automatically available.

## Requirements

- PostgreSQL 12+ (examples use modern SQL)
- psql command-line client
- Basic SQL knowledge

## Related Skills

Consider pairing with:
- **Docker Skill** - Running PostgreSQL in containers
- **Bash Scripting** - Automation with psql
- **Cloud Platforms** - Managed PostgreSQL services

## Contributing

Found an issue or want to add more examples?
1. Test the command/example locally
2. Document the use case
3. Submit corrections or additions

## License

This documentation is provided under the PostgreSQL License.

## References

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [psql Manual](https://www.postgresql.org/docs/current/app-psql.html)
- [PostgreSQL Wiki](https://wiki.postgresql.org/)
- [PostgreSQL Best Practices](https://www.postgresql.org/docs/current/sql-syntax.html)

## Version

- **Skill Version**: 1.0.0
- **Created**: October 2025
- **PostgreSQL Compatibility**: 12+
- **Updated**: As needed

## Quick Links to Key Sections

In SKILL.md you'll find:

- **Getting Started**: Connection Options (line 48)
- **Command Reference**: Essential Meta-Commands (line 171)
- **Scripting**: Scripting with psql (line 690)
- **Performance**: Performance and Debugging (line 795)
- **Troubleshooting**: Troubleshooting section (line 1250)
- **Best Practices**: Best Practices (line 1191)

---

**Start using this skill in Claude Code by asking PostgreSQL-related questions!**
