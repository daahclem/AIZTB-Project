// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControl {
    struct LogEntry {
        uint256 timestamp;
        bytes32 userId;
        bytes32 chargerId;
        uint8 decision; // 0 = Deny, 1 = Allow
        bytes32 ipfsCid;
        uint8 riskLevel; // 0 = Safe, 1 = Suspicious, 2 = Malicious
    }
    LogEntry[] public logs;
    event LogWritten(uint256 indexed idx, bytes32 userId, bytes32 ipfsCid);

    function writeLog(bytes32 userId, bytes32 chargerId, uint8 decision, bytes32 ipfsCid, uint8 riskLevel) public {
        logs.push(LogEntry(block.timestamp, userId, chargerId, decision, ipfsCid, riskLevel));
        emit LogWritten(logs.length - 1, userId, ipfsCid);
    }
    function getLog(uint256 idx) public view returns (LogEntry memory) {
        return logs[idx];
    }
    function getLogsCount() public view returns (uint256) {
        return logs.length;
    }
}
