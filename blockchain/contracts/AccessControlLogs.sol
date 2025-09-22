// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControlLogs {
    struct LogEntry {
        uint timestamp;
        string userId;
        string action;
        string decision;
        string riskScore;
    }

    LogEntry[] public logs;

    event LogAdded(
        uint indexed index,
        string userId,
        string action,
        string decision,
        string riskScore
    );

    function addLog(
        string memory userId,
        string memory action,
        string memory decision,
        string memory riskScore
    ) public {
        logs.push(LogEntry(block.timestamp, userId, action, decision, riskScore));
        emit LogAdded(logs.length - 1, userId, action, decision, riskScore);
    }

    function getLog(uint index) public view returns (
        uint,
        string memory,
        string memory,
        string memory,
        string memory
    ) {
        require(index < logs.length, "Index out of bounds");
        LogEntry memory log = logs[index];
        return (log.timestamp, log.userId, log.action, log.decision, log.riskScore);
    }

    function getLogCount() public view returns (uint) {
        return logs.length;
    }
}
