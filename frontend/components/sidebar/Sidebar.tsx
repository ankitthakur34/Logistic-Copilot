"use client";

import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

import { ChatSession } from "@/types/chat";

interface SidebarProps {
  chats: ChatSession[];
  activeChatId: string;
  onSelect: (id: string) => void;
  onNewChat: () => void;
}

export default function Sidebar({
  chats,
  activeChatId,
  onSelect,
  onNewChat,
}: SidebarProps) {
  return (
    <aside className="flex h-screen w-64 flex-col border-r bg-[#202123] text-white">

      {/* Header */}

      <div className="p-4">

        <Button
          onClick={onNewChat}
          variant="outline"
          className="flex w-full items-center justify-start gap-2 border-white/20 bg-transparent text-white hover:bg-white/10 hover:text-white"
        >
          <Plus size={18} />
          New Chat
        </Button>

      </div>

      {/* Chat List */}

      <ScrollArea className="flex-1 px-2">

        <div className="space-y-1">

          {chats.length === 0 && (
            <div className="px-3 py-2 text-sm text-gray-400">
              No conversations yet
            </div>
          )}

          {chats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => onSelect(chat.id)}
              className={`w-full rounded-lg px-3 py-3 text-left transition-colors ${
                activeChatId === chat.id
                  ? "bg-[#343541]"
                  : "hover:bg-[#2A2B32]"
              }`}
            >
              <div className="truncate text-sm font-medium">
                {chat.title}
              </div>

              <div className="mt-1 truncate text-xs text-gray-400">
                {chat.messages.length === 0
                  ? "Empty conversation"
                  : `${chat.messages.length} messages`}
              </div>
            </button>
          ))}

        </div>

      </ScrollArea>

      {/* Footer */}

      <div className="border-t border-white/10 p-4">

        <div className="text-xs text-gray-500">
          Logistics Copilot
        </div>

      </div>

    </aside>
  );
}