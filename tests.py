from database.agent_db import AgentDB
from database.mission_db import MissionDB


data = {
    "name": "Shlomo",
    "specialty": "Anything",
    "agent_runk": "Junior",
    "is_active": "TRUE",
    "completed_missions": 3,
    "failed_missions": 3
}

data2 = {
    "title": "a",
    "description": "b",
    "location": "c",
    "difficulty": 5,
    "importance": 3,
    "status": "ASSIGNED"
}
# data["title"], data["description"], data["location"], data["difficulty"], data["importance"], data["status"], risk
# x = AgentDB.increment_failed(2)
# x = AgentDB.get_agent_performance(2)
# x = MissionDB.get_open_missions_by_agent(4)

print(x)


# id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(50) NOT NULL,
# specialty VARCHAR(50) NOT NULL,
# is_active BOOLEAN DEFAULT TRUE NOT NULL,
# completed_missions INT DEFAULT 0 NOT NULL,
# failed_missions INT DEFAULT 0 NOT NULL,
# agent_runk ENUM('Junior', 'Senior', 'Commander') NOT NULL