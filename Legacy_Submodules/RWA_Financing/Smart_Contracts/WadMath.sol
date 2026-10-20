// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

library WadMath {
    uint256 public constant WAD = 1e18;

    function wmul(uint256 a, uint256 b) internal pure returns (uint256) {
        return (a * b) / WAD;
    }

    function wdiv(uint256 a, uint256 b) internal pure returns (uint256) {
        return (a * WAD) / b;
    }
}
