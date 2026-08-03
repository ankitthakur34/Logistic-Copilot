"use client";

import { Bot, User } from "lucide-react";

import { Badge } from "@/components/ui/badge";

import { ChatMessage as Message } from "@/types/chat";

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({
  message,
}: ChatMessageProps) {

  const isUser = message.role === "user";

  return (

    <div
      className={`flex gap-4 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >

      {/* Assistant */}

      {!isUser && (

        <div className="mt-1 flex h-9 w-9 items-center justify-center rounded-full bg-blue-600 text-white">

          <Bot size={18} />

        </div>

      )}

      <div
        className={`max-w-3xl ${
          isUser ? "items-end" : "items-start"
        } flex flex-col`}
      >

        {/* Message */}

        {isUser ? (

<div className="max-w-2xl rounded-3xl bg-slate-100 px-5 py-3 text-[15px] text-slate-900 border border-slate-200">
            {message.content}

          </div>

        ) : (

          <div className="px-1 text-[15px] leading-7 text-slate-800 whitespace-pre-wrap">

            {message.content}

          </div>

        )}

        {/* Sources */}

        {message.toolResults &&
          message.toolResults.length > 0 && (

            <div className="mt-4 flex flex-wrap items-center gap-2">

              <span className="text-xs font-medium text-slate-500">

                Sources

              </span>

              {message.toolResults.map((tool) => {

                const colors = {
                  rag: "bg-green-100 text-green-700 border-green-200",
                  sql: "bg-blue-100 text-blue-700 border-blue-200",
                  ml: "bg-purple-100 text-purple-700 border-purple-200",
                };

                return (
                  <Badge
                    key={tool.tool_name}
                    variant="outline"
                    className={`capitalize ${
                      colors[
                        tool.tool_name.toLowerCase() as keyof typeof colors
                      ] ??
                      "bg-slate-100 text-slate-700"
                    }`}
                  >
                    {tool.tool_name}
                  </Badge>
                );
              })}

            </div>

          )}

      </div>

      {/* User */}

      {isUser && (

        <div className="mt-1 flex h-9 w-9 items-center justify-center rounded-full bg-slate-700 text-white">

          <User size={18} />

        </div>

      )}

    </div>

  );

}