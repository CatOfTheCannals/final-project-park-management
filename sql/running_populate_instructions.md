# ✅ MySQL `LOAD DATA LOCAL INFILE` Setup (macOS & Linux)

This guide helps you bulk-load CSVs into MySQL using `LOAD DATA LOCAL INFILE`, ensuring it's properly configured on **both server and client** sides.

---

## 🧩 1. MySQL Server Configuration

Ensure `local_infile` is **enabled on the server**.

### Linux:
Edit `/etc/mysql/my.cnf` or `/etc/my.cnf` and add:

```ini
[mysqld]
local_infile=1


Restart the server:

sudo systemctl restart mysql


macOS (Homebrew):
Check config location:

mysql --help | grep -A 1 "Default options"


If needed, create /opt/homebrew/etc/my.cnf or /opt/homebrew/etc/my.cnf adding the following:

[mysqld]
local_infile=1


Restart MySQL:

brew services restart mysql


🧪 2. Verify Server Setting

mysql -u root -e "SHOW GLOBAL VARIABLES LIKE 'local_infile';"

expected output:
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| local_infile  | ON    |
+---------------+-------+


⚙️ 3. Client-Side Invocation

When running SQL files that use LOAD DATA LOCAL INFILE, always add --local-infile=1:
mysql --local-infile=1 -u root < sql/populate_data.sql



🧼 5. Example Workflow
mysql --local-infile=1 -u root < sql/teardown.sql
mysql --local-infile=1 -u root < sql/setup.sql
mysql --local-infile=1 -u root < sql/populate_data.sql
