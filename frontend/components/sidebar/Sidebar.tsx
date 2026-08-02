"use client";

import { Plus, MessageSquare, Settings, Ship } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

interface SidebarProps {
  chats: any[];
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
    <div className="flex w-72 flex-col border-r border-slate-800 bg-slate-900 text-white">

      {/* Logo */}
      <div className="flex items-center gap-3 border-b border-slate-800 px-6 py-6">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600">
          <Ship className="h-6 w-6" />
        </div>

        <div>
          <h1 className="text-lg font-semibold">
            Logistics Copilot
          </h1>

          <p className="text-xs text-slate-400">
            AI Operations Assistant
          </p>
        </div>
      </div>

      {/* New Chat */}
      <div className="p-4">
        <Button
          onClick={onNewChat}
          className="h-11 w-full justify-start gap-2 rounded-xl bg-blue-600 hover:bg-blue-700"
        >
          <Plus size={18} />
          New Chat
        </Button>
      </div>

      <Separator className="bg-slate-800" />

      {/* Chat List */}
      <ScrollArea className="flex-1 px-3 py-3">

        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Chats
        </p>

        <div className="space-y-1">

          {chats.length === 0 && (
            <div className="px-3 py-6 text-center text-sm text-slate-500">
              No conversations yet
            </div>
          )}

          {chats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => onSelect(chat.id)}
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left transition-all duration-200

                ${
                  activeChatId === chat.id
                    ? "bg-slate-700"
                    : "hover:bg-slate-800"
                }
              `}
            >
              <MessageSquare size={18} />

              <span className="truncate text-sm">
                {chat.title}
              </span>
            </button>
          ))}

        </div>

      </ScrollArea>

      <Separator className="bg-slate-800" />

      {/* Footer */}
      <div className="flex items-center justify-between p-4">

        <div>

          <p className="text-sm font-medium">
            Demo
          </p>

          <p className="text-xs text-slate-400">
            Logistics AI
          </p>

        </div>

        <Button
          variant="ghost"
          size="icon"
          className="text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <Settings size={18} />
        </Button>

      </div>

    </div>
  );
}