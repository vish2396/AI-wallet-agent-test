import { ChatEntry } from "@/components/ChatEntry";
import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useRef, useState } from "react";
import { useAccount } from "wagmi";
import Confetti from "react-confetti";
import useWindowSize from "react-use/lib/useWindowSize";
import Link from "next/link";

type ChatEntry = {
  message: React.ReactNode;
}[];

export default function ChatScreen({
  showImageRanking,
}: {
  showImageRanking: boolean;
}) {
  const { width, height } = useWindowSize();
  const account = useAccount();
  const [entries, setEntries] = useState<ChatEntry>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  const { isFetched, error, data, refetch } = useQuery({
    queryKey: ["transaction-request"],
    queryFn: () =>
      fetch("/api", {
        method: "POST",
        body: JSON.stringify({ address: account.address }),
      }).then((res) => res.json()),
    enabled: false,
    retry: false,
  });

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [entries]);

  const addEntry = useCallback(
    (message: React.ReactNode, removeLast = false) => {
      setEntries((prevEntries) => [
        ...prevEntries.slice(
          0,
          removeLast ? prevEntries.length - 1 : prevEntries.length
        ),
        {
          message,
        },
      ]);
    },
    [setEntries]
  );

  const handleUserInput = async (input: string) => {
    addEntry(<div className="user-message">{input}</div>);

    try {
      // Send user input to the Flask backend
      const response = await fetch("http://localhost:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      // Display the bot response
      if (data.response) {
        addEntry(<div className="bot-message">{data.response}</div>);
      } else {
        addEntry(<div className="bot-message">No response from bot</div>);
      }
    } catch (error) {
      console.error("Error communicating with the chatbot API:", error);
      addEntry(<div className="bot-message">Error communicating with the server</div>);
    }
  };
  /*const handleUserInput = (input: string) => {
    addEntry(<div className="user-message">{input}</div>);
    // Example: Simulate AI response based on input
    setTimeout(() => {
      addEntry(<div className="bot-message">AI Agent response to: {input}</div>);
    }, 1000);
  };*/

  return (
    <div ref={containerRef} className="overflow-y-auto max-h-screen">
      <div className="pb-10 mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 mt-7 flex flex-col">
        <Confetti
          width={width}
          height={height}
          tweenDuration={2000}
          run={isFetched && data?.transactionHash?.length > 0}
        />
        <ChatEntry>
          <div className="text-sm font-normal text-gray-900 dark:text-white">
            Turbocharge your machine learning with AI wallets: now, you can
            automatically pay your users to help improve your models, powered by{" "}
            <Link
              href="https://docs.cdp.coinbase.com/mpc-wallet/docs/welcome"
              target="_blank"
              className="text-blue-700"
            >
              Coinbase MPC Wallets
            </Link>
            . This sample app allows you to earn ETH on Base Sepolia in exchange
            for providing feedback to our AI agent. Try it out below!
          </div>
        </ChatEntry>
        
        {entries.map((entry: any, idx: number) => (
          <ChatEntry key={`entry-${idx}`} message={entry.message} />
        ))}
        <div className="user-input-container">
          <input
            type="text"
            className="user-input"
            placeholder="Type a message..."
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleUserInput((e.target as HTMLInputElement).value);
                (e.target as HTMLInputElement).value = "";
              }
            }}
          />
        </div>
      </div>
    </div>
  );
}
