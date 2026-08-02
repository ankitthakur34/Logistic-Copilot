"use client";

import { useState } from "react";

import Sidebar from "@/components/sidebar/Sidebar";
import ChatWindow from "@/components/chat/ChatWindow";

import {
  ChatSession,
  ChatMessage,
} from "@/types/chat";

export default function Home() {

  ////////////////////////////////////////////////////////
  // State
  ////////////////////////////////////////////////////////

  const [chats, setChats] = useState<ChatSession[]>([]);

  const [activeChatId, setActiveChatId] =
    useState("");

  ////////////////////////////////////////////////////////
  // New Chat
  ////////////////////////////////////////////////////////

  function createNewChat() {

    const id = crypto.randomUUID();

    const chat: ChatSession = {

      id,

      title: "New Chat",

      messages: [],

      createdAt: new Date(),

    };

    setChats(prev => [

      chat,

      ...prev,

    ]);

    setActiveChatId(id);

    return id;

  }

  ////////////////////////////////////////////////////////
  // Auto Create Chat
  ////////////////////////////////////////////////////////

  function ensureActiveChat() {

    if (activeChatId) {

      return activeChatId;

    }

    return createNewChat();

  }

  ////////////////////////////////////////////////////////
  // Active Chat
  ////////////////////////////////////////////////////////

  const activeChat = chats.find(

    c => c.id === activeChatId,

  );

  ////////////////////////////////////////////////////////
  // Update Chat
  ////////////////////////////////////////////////////////

  function updateChat(

    chatId: string,

    messages: ChatMessage[],

  ) {

    setChats(prev =>

      prev.map(chat => {

        if (chat.id !== chatId) {

          return chat;

        }

        return {

          ...chat,

          title:

            chat.title === "New Chat" && messages.length > 0

              ? messages[0].content.substring(0, 35)

              : chat.title,

          messages,

        };

      })

    );

  }

  ////////////////////////////////////////////////////////

  return (

    <div className="flex h-screen bg-slate-100">

      <Sidebar

        chats={chats}

        activeChatId={activeChatId}

        onSelect={setActiveChatId}

        onNewChat={createNewChat}

      />
     <div className="flex flex-1 overflow-hidden">

      <ChatWindow

        chat={activeChat}

        ensureChat={ensureActiveChat}

        onMessagesChange={updateChat}

      />
      </div>

    </div>

  );

}