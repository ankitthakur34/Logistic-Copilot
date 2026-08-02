"use client";

import { useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

import {
  ChatMessage as Message,
  ChatSession,
} from "@/types/chat";

import { askQuestion } from "@/lib/api";

interface ChatWindowProps {

  chat?: ChatSession;

  ensureChat: () => string;

  onMessagesChange: (

    chatId: string,

    messages: Message[],

  ) => void;

}

export default function ChatWindow({

  chat,

  ensureChat,

  onMessagesChange,

}: ChatWindowProps) {

  const [loading, setLoading] = useState(false);

  ////////////////////////////////////////////////////////

  async function handleSend(question: string) {

    const chatId = ensureChat();

    const currentMessages = chat?.messages ?? [];

    const userMessage: Message = {

      id: crypto.randomUUID(),

      role: "user",

      content: question,

    };

    const messagesAfterUser = [

      ...currentMessages,

      userMessage,

    ];

    onMessagesChange(

      chatId,

      messagesAfterUser,

    );

    setLoading(true);

    try {

      const response = await askQuestion(

        question,

      );

      const assistantMessage: Message = {

        id: crypto.randomUUID(),

        role: "assistant",

        content: response.answer,

        toolResults: response.tool_results,

      };

      onMessagesChange(

        chatId,

        [

          ...messagesAfterUser,

          assistantMessage,

        ],

      );

    }

    catch (error) {

      console.error(error);

      const assistantMessage: Message = {

        id: crypto.randomUUID(),

        role: "assistant",

        content: "Unable to contact backend.",

      };

      onMessagesChange(

        chatId,

        [

          ...messagesAfterUser,

          assistantMessage,

        ],

      );

    }

    finally {

      setLoading(false);

    }

  }

  ////////////////////////////////////////////////////////

  const messages = chat?.messages ?? [];

  ////////////////////////////////////////////////////////

  return (

    <div className="flex flex-1 flex-col bg-slate-50">

      {/* Header */}

      <div className="border-b bg-white px-8 py-6 shadow-sm">

    <div className="flex items-center justify-between">

        <div>

            <h1 className="text-2xl font-bold text-slate-900">

                🚢 Logistics Copilot

            </h1>

            <p className="mt-1 text-sm text-slate-500">

                AI Assistant for Logistics Operations

            </p>

        </div>

        <div className="rounded-full border border-blue-200 bg-blue-50 px-4 py-2">

            <span className="text-sm font-medium text-blue-700">

                Online

            </span>

        </div>

    </div>

</div>

      {/* Messages */}

      <div className="flex-1 overflow-y-auto">

        {

          messages.length === 0 && !loading ?

            (

             <div className="flex h-full items-center justify-center">

    <div className="max-w-2xl text-center">

        <div className="mb-6 text-6xl">

            🚢

        </div>

        <h1 className="text-4xl font-bold text-slate-800">

            Logistics Copilot

        </h1>

        <p className="mt-4 text-lg text-slate-500">

            AI assistant for shipment tracking, SOPs,

            incidents, meetings and logistics operations.

        </p>

        <div className="mt-10 grid grid-cols-2 gap-4">

            <div className="rounded-2xl border bg-white p-5 shadow-sm">

                Why was SHP0001 delayed?

            </div>

            <div className="rounded-2xl border bg-white p-5 shadow-sm">

                Customs Clearance SOP

            </div>

            <div className="rounded-2xl border bg-white p-5 shadow-sm">

                Show pending tasks

            </div>

            <div className="rounded-2xl border bg-white p-5 shadow-sm">

                Shipment ETA

            </div>

        </div>

    </div>

</div>

            )

            :

            (

<div className="mx-auto flex w-full max-w-5xl flex-col gap-8 px-8 py-8">
                {

                  messages.map(message => (

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

              </div>

            )

        }

      </div>

      {/* Input */}

     <div className="border-t bg-white px-8 py-6">

    <div className="mx-auto max-w-5xl">

        <ChatInput

            onSend={handleSend}

        />

    </div>

</div>

    </div>

  );

}