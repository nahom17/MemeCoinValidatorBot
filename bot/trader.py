
import os
import requests
import json
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import Message, VersionedMessage
from solders.instruction import Instruction, AccountMeta
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig
from solana.rpc.api import Client

def get_pumpportal_transaction(public_key, action, mint, amount, denominated_in_sol=True, slippage=1, priority_fee=0.005, pool="auto"):
    """Get transaction from PumpPortal API using the correct format"""
    url = "https://pumpportal.fun/api/trade-local"

    # Convert amount to proper format
    if denominated_in_sol:
        # Convert SOL to lamports (1 SOL = 1e9 lamports)
        amount_lamports = int(amount * 1e9)
        denominated_in_sol_str = "true"
    else:
        amount_lamports = int(amount)
        denominated_in_sol_str = "false"

    payload = {
        "publicKey": public_key,
        "action": action,
        "mint": mint,
        "amount": amount_lamports,
        "denominatedInSol": denominated_in_sol_str,
        "slippage": slippage,
        "priorityFee": priority_fee,
        "pool": pool
    }

    print(f"📡 Sending request to PumpPortal:")
    print(f"   - Action: {action}")
    print(f"   - Mint: {mint}")
    print(f"   - Amount: {amount_lamports} lamports")
    print(f"   - Denomininated in SOL: {denominated_in_sol_str}")
    print(f"   - Slippage: {slippage}%")
    print(f"   - Pool: {pool}")

    response = requests.post(url, data=payload, timeout=30)

    if response.status_code == 200:
        print("✅ Transaction received from PumpPortal")
        return response.content
    else:
        raise Exception(f"PumpPortal API failed: {response.status_code} - {response.text}")

def sign_and_send_transaction(transaction_bytes, private_key, rpc_url):
    """Sign and send transaction using the correct format"""
    try:
        # Create keypair from private key
        keypair = Keypair.from_base58_string(private_key)

        # Create versioned transaction from bytes
        tx = VersionedTransaction.from_bytes(transaction_bytes)

        # Sign the transaction
        signed_tx = VersionedTransaction(tx.message, [keypair])

        # Create RPC request
        commitment = CommitmentLevel.Confirmed
        config = RpcSendTransactionConfig(preflight_commitment=commitment)
        tx_payload = SendVersionedTransaction(signed_tx, config)

        # Send transaction to RPC
        rpc_response = requests.post(
            url=rpc_url,
            headers={"Content-Type": "application/json"},
            data=tx_payload.to_json(),
            timeout=30
        )

        if rpc_response.status_code == 200:
            result = rpc_response.json()
            if 'result' in result:
                signature = result['result']
                print(f"✅ Transaction sent successfully!")
                print(f"🔗 Transaction: https://solscan.io/tx/{signature}")
                return signature
            else:
                raise Exception(f"RPC response error: {result}")
        else:
            raise Exception(f"RPC request failed: {rpc_response.status_code} - {rpc_response.text}")

    except Exception as e:
        raise Exception(f"Failed to sign and send transaction: {e}")

def trade_local(private_key, token_mint, side="buy", amount_sol=0.00001):
    """Execute real trade on PumpFun using PumpPortal API"""
    try:
        # Setup keypair and get public key
        keypair = Keypair.from_base58_string(private_key)
        public_key = str(keypair.pubkey())
        rpc_url = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")

        print(f"🚀 Executing {side} trade for {token_mint}")
        print(f"💰 Amount: {amount_sol} SOL")
        print(f"👤 Public Key: {public_key}")
        print(f"🌐 RPC URL: {rpc_url}")

        # Get transaction from PumpPortal
        transaction_bytes = get_pumpportal_transaction(
            public_key=public_key,
            action=side,
            mint=token_mint,
            amount=amount_sol,
            denominated_in_sol=True,
            slippage=1,  # 1% slippage
            priority_fee=0.005,
            pool="auto"  # Use auto pool selection
        )

        # Sign and send transaction
        signature = sign_and_send_transaction(transaction_bytes, private_key, rpc_url)

        print(f"✅ {side.capitalize()} transaction completed: {signature}")
        return signature

    except Exception as e:
        print(f"❌ Trade failed: {e}")
        raise Exception(f"Failed to execute {side} trade: {e}")

def get_token_balance(client, wallet_address, token_mint):
    """Get token balance for selling"""
    try:
        # This is a simplified version - you might need to implement proper token balance checking
        # For now, we'll use a default amount
        return 1000000  # Default token amount to sell
    except Exception as e:
        print(f"❌ Failed to get token balance: {e}")
        return 1000000
