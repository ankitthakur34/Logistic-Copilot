"use client";

import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

import { askQuestion } from "@/lib/api";

import {
  ChatMessage as Message,
  ChatSession,
} from "@/types/chat";

interface ChatWindowProps {
  chat?: ChatSession;

  onMessagesChange: (messages: Message[]) => void;
}

export default function ChatWindow({
  chat,
  onMessagesChange,
}: ChatWindowProps) {

  const [messages, setMessages] = useState<Message[]>([]);

  const [loading, setLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {

    setMessages(chat?.messages ?? []);

  }, [chat]);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({

      behavior: "smooth",

    });

  }, [messages]);

  function updateMessages(newMessages: Message[]) {

    setMessages(newMessages);

    onMessagesChange(newMessages);

  }

  async function handleSend(question: string) {

    if (!chat) return;

    const userMessage: Message = {

      id: crypto.randomUUID(),

      role: "user",

      content: question,

    };

    const userMessages = [

      ...messages,

      userMessage,

    ];

    updateMessages(userMessages);

    setLoading(true);

    try {

      const response = await askQuestion(question);

      const assistantMessage: Message = {

        id: crypto.randomUUID(),

        role: "assistant",

        content: response.answer,

        toolResults: response.tool_results,

      };

      updateMessages([

        ...userMessages,

        assistantMessage,

      ]);

    }

    catch {

      updateMessages([

        ...userMessages,

        {

          id: crypto.randomUUID(),

          role: "assistant",

          content: "Unable to contact backend.",

        },

      ]);

    }

    finally {

      setLoading(false);

    }

  }

  return (

    <div className="flex flex-1 flex-col bg-white">

      {/* Header */}

      <div className="border-b bg-white px-8 py-4">

        <h1 className="text-lg font-semibold text-slate-800">

          Logistics Copilot

        </h1>

      </div>

      {/* Messages */}

      <div className="flex-1 overflow-y-auto">

        {

          !chat ?

          (

            <div className="flex h-full items-center justify-center">

              <div className="text-center">

                <h1 className="text-4xl font-semibold text-slate-800">

                  Logistics Copilot

                </h1>

                <p className="mt-3 text-slate-500">

                  Start a new conversation from the sidebar.

                </p>

              </div>

            </div>

          )

          :

          messages.length === 0 ?

          (

            <div className="flex h-full items-center justify-center">

              <div className="text-center">

                <h1 className="text-4xl font-semibold text-slate-800">

                  Logistics Copilot

                </h1>

                <p className="mt-3 text-slate-500">

                  Ask anything about shipments, SOPs,

                  incidents, tasks or meetings.

                </p>

              </div>

            </div>

          )

          :

          (

            <div className="mx-auto flex w-full max-w-5xl flex-col gap-8 px-6 py-8">

              {

                messages.map((message) => (

                  <ChatMessage

                    key={message.id}

                    message={message}

                  />

                ))

              }

              {

                loading &&

                (

                  <ChatMessage

                    message={{

                      id: "loading",

                      role: "assistant",

                      content: "Thinking...",

                    }}

                  />

                )

              }

              <div ref={bottomRef} />

            </div>

          )

        }

      </div>

      {/* Input */}

      {

        chat &&

        (

          <div className="border-t bg-white px-6 py-5">

            <div className="mx-auto max-w-5xl">

              <ChatInput

                onSend={handleSend}

              />

            </div>

          </div>

        )

      }

    </div>

  );

}