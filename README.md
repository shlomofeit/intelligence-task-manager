# Intelligence Task Manager

Agent and task management system for the ShadowNet unit.
The system is stored in mysql and operated by OOP classes for data management and communication with the DB.

## Project structure

    intelligence-task-manager/
    ├── database/
    │   ├── db_connection.py
    │   ├── agent_db.py
    │   └── mission_db.py
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## Tables structure

### agents:

| שדה | סוג | הערות |
| --- | --- | --- |
| id | INT, AUTO_INCREMENT, PK | מזהה ייחודי |
| name | VARCHAR | שם הסוכן |
| specialty | VARCHAR | תחום התמחות |
| is_active | BOOLEAN | ברירת מחדל: TRUE |
| completed_missions | INT | ברירת מחדל: 0 |
| failed_missions | INT | ברירת מחדל: 0 |
| agent_rank | ENUM / VARCHAR | Junior / Senior / Commander בלבד |
##
### missions:

| שדה | סוג | הערות |
| --- | --- | --- |
| id | INT, AUTO_INCREMENT, PK | מזהה ייחודי |
| title | VARCHAR | כותרת המשימה |
| description | TEXT | תיאור מפורט |
| location | VARCHAR | מיקום |
| difficulty | INT | 1–10 בלבד |
| importance | INT | 1–10 בלבד |
| status | VARCHAR | ברירת מחדל: NEW |
| risk_level | VARCHAR | מחושב אוטומטית — לא מגיע מהמשתמש |
| assigned_agent_id | INT | NULL עד שיוך |
##

## Classes

### DB_connection

The class manages the connection to the DB and verifies that there is a DB and tables, and if not, it creates them.
The class contains the following methods:

    get_connection() - Returns active connection to MySQL db.

    create_database() - Creating the Intelligence_db if does not exist.

    create_tables() - Creating the tow tables (agents and misstions) if does not exist.

### AgentDB

The class manages reading and writing data from the agents table.
The class contains the following methods:

    create_agent(data) - Creates a new agent and returns the agent object.
        
    get_all_agents() - Returns a list of all agents.

    get_agent_by_id(id) - Returns one agent by ID, or None.

    update_agent(id, data) - UPDATE for the whole row (it is not possible to change id).

    deactivate_agent(id) - Sets agent status to inactive.

    increment_completed(id) - Updates the amount of completed tasks.

    increment_failed(id) - Updates the amount of failed tasks.

    get_agent_performance(id) - Returns a dictionary with these keys completed, failed, total, success_rate.

    count_active_agents() - Returns the number of active agents.

### MissionDB

The class manages reading and writing data from the missions table.
The class contains the following methods:

    create_mission(data) - Creates a new task and returns the entire object.

    get_all_missions() - Returns all tasks.

    get_mission_by_id(id) - Returns one task by ID, or None.

    assign_mission(m_id, a_id) - Assigns a task to an agent.

    update_mission_status(id, status) - Used for any status change.

    get_open_missions_by_agent(id) - Returns ASSIGNED/IN_PROGRESS tasks of an agent.

    count_all_missions() - Total tasks.

    count_by_status(status) - Counts by a specific status.

    count_open_missions() - Counts open tasks.

    count_critical_missions() - Counts CRITICAL tasks.

    get_top_agent() - Agent with the highest completed_missions.


## System rulls

- rank must be Junior / Senior / Commander — any other value throws an error.

- difficulty and importance must be between 1 and 10 — otherwise an error.

- risk_level is calculated automatically when creating a task — the user does not submit it.

- Agent with is_active=False cannot accept tasks.

- Agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.

- If risk_level=CRITICAL - only an agent with the Commander rank can accept the task.

- Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.

- Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.

- Only a task with the status IN_PROGRESS can be completed and changed to failed or completed.

- Only a task in NEW or ASSIGNED status can be canceled — otherwise an error.

## How to run

```
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

```