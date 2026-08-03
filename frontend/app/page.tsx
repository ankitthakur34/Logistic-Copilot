"use client";

import { useState } from "react";

import Sidebar from "@/components/sidebar/Sidebar";
import ChatWindow from "@/components/chat/ChatWindow";

import {
  ChatSession,
  ChatMessage,
} from "@/types/chat";

export default function Home() {

  const [chats, setChats] = useState<ChatSession[]>([]);

  const [activeChatId, setActiveChatId] = useState("");

  function createNewChat() {

    const chat: ChatSession = {

      id: crypto.randomUUID(),

      title: "New Chat",

      messages: [],

      createdAt: new Date(),

    };

    setChats(prev => [chat, ...prev]);

    setActiveChatId(chat.id);

  }

  function updateMessages(messages: ChatMessage[]) {

    if (!activeChatId) return;

    setChats(prev =>

      prev.map(chat => {

        if (chat.id !== activeChatId) {

          return chat;

        }

        let title = chat.title;

        // Rename chat using first user message
        if (
          title === "New Chat" &&
          messages.length > 0
        ) {

          const firstUserMessage = messages.find(
            m => m.role === "user"
          );

          if (firstUserMessage) {

            title =
              firstUserMessage.content.length > 35
                ? firstUserMessage.content.slice(0, 35) + "..."
                : firstUserMessage.content;

          }

        }

        return {

          ...chat,

          title,

          messages,

        };

      })

    );

  }

  const activeChat = chats.find(

    chat => chat.id === activeChatId

  );

  return (

    <div className="flex h-screen">

      <Sidebar

        chats={chats}

        activeChatId={activeChatId}

        onSelect={setActiveChatId}

        onNewChat={createNewChat}

      />

      <ChatWindow

        chat={activeChat}

        onMessagesChange={updateMessages}

      />

    </div>

  );

}