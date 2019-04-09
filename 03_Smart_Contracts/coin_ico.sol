// coins ICO

// Version of compiler
pragma solidity ^0.5.1;

contract coin_ico {
    
    // Introducing the maximum number of coins available for sale
    uint public max_coins = 1000000;

    // Introducing the INR to coins conversion rate
    uint public inr_to_coins = 100;

    // Introducing the total number of the coins that have been bought by the invertors
    uint public total_coins_bought = 0;

    // Mapping from the investor address to its equity in coins and INR
    mapping(address => uint) equity_coin;
    mapping (address => uint) equity_inr;

    // Checking if an investor can buy coins
    modifier can_buy_coins(uint inr_invested) {
        require(inr_invested * inr_to_coins + total_coins_bought <= max_coins);
        _;
    }

    // Getting the equity in coins of an investor
    function equity_in_coins(address investor) external view returns (uint) {
        return equity_coin[investor];
    }

    // Getting the equity in inr of an investor
    function equity_in_inr(address investor) external view returns (uint) {
        return equity_inr[investor];
    }

    // Buying coins
    function buy_coins(address investor, uint inr_invested) external 
    can_buy_coins(inr_invested) {
        uint coins_bought = inr_invested * inr_to_coins;
        equity_coin[investor] += coins_bought;
        equity_inr[investor] += inr_invested;
        total_coins_bought += coins_bought;
    }

    // Selling coins
    function sell_coins(address investor, uint coins_sold) external {
        equity_coin[investor] -= coins_sold;
        equity_inr[investor] = equity_coin[investor] / inr_to_coins;
        total_coins_bought -= coins_sold;
    }

}

// Get the byte code using --> remix solidity ide (online)
// use the ganache for blockchain visualisation.