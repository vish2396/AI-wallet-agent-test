import { useState } from "react";
import Web3 from "web3";
import Image from "next/image";

export const Navigation = () => {
  const [walletAddress, setWalletAddress] = useState<string | null>(null);
  const [web3, setWeb3] = useState<Web3 | null>(null);

  // Function to connect the wallet
  const connectWallet = async () => {
    if (typeof window.ethereum !== "undefined") {
      try {
        // Request account access
        const accounts = await window.ethereum.request({
          method: "eth_requestAccounts",
        });

        // Initialize web3
        const web3Instance = new Web3(window.ethereum);
        setWeb3(web3Instance);

        // Set the wallet address
        const address = accounts[0];
        setWalletAddress(address);

        // Log the connected wallet address in the web console
        console.log("Connected wallet address:", address);
      } catch (error) {
        console.error("Failed to connect wallet:", error);
      }
    } else {
      console.error("No Ethereum provider found. Install MetaMask.");
    }
  };

  return (
    <div className="bg-gray-800">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="relative flex h-16 items-center justify-between">
          <div className="flex flex-1 items-center items-stretch justify-between">
            <div className="flex flex-shrink-0 items-center">
              <Image
                src="/coinbase.svg"
                className="mr-2"
                alt="Coinbase"
                width={90}
                height={24}
              />
              <h2 className="text-white font-bold mt-1">AI Agent Tool</h2>
            </div>
            <div className="flex items-center">
              {walletAddress ? (
                <p className="text-white font-bold mr-4">
                  {walletAddress.substring(0, 6)}...
                  {walletAddress.substring(walletAddress.length - 4)}
                </p>
              ) : (
                <button
                  onClick={connectWallet}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                  Connect Wallet
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
