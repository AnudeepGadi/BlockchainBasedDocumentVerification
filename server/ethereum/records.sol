// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.6 <0.9.0;

contract StudentRecord {
    struct StudentData {
        string encryptedText;
    }

    StudentData public studentRecord;

    function addRecord(string memory _encryptedText) public {
        studentRecord = StudentData({
            encryptedText: _encryptedText
        });
    }

    function getRecord() public view returns (string memory) {
        return (studentRecord.encryptedText);
    }
}
