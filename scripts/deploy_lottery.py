from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        # publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


import time

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]  # Assuming Lottery is a contract collection
    if not lottery:
        print("No lottery contract found.")
        return

    try:
        tx = fund_with_link(lottery.address)
        tx.wait(1)
    except Exception as e:
        print(f"Error funding the lottery contract: {e}")
        return

    try:
        ending_transaction = lottery.endLottery({"from": account})
        ending_transaction.wait(1)
    except Exception as e:
        print(f"Error ending the lottery: {e}")
        return

    # Wait for some time before announcing the winner
    time.sleep(180)
    try:
        winner = lottery.recentWinner()
        print(f"{winner} is the new winner!")
    except Exception as e:
        print(f"Error getting the winner: {e}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()