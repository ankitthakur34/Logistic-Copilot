"use client";

import { useState } from "react";

import { Send, Paperclip, Mic } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ChatInputProps {
  onSend: (question: string) => void;
}

export default function ChatInput({
  onSend,
}: ChatInputProps) {

  const [question, setQuestion] = useState("");

  function send() {

    if (!question.trim()) return;

    onSend(question);

    setQuestion("");

  }

  return (

    <div className="rounded-3xl border bg-white shadow-lg">

      <div className="flex items-center gap-3 p-3">

        {/* Attachment */}

        <Button
          variant="ghost"
          size="icon"
          className="rounded-full"
        >
          <Paperclip size={18} />
        </Button>

        {/* Input */}

        <Input

          value={question}

          onChange={(e) => setQuestion(e.target.value)}

          onKeyDown={(e) => {

            if (e.key === "Enter" && !e.shiftKey) {

              e.preventDefault();

              send();

            }

          }}

          placeholder="Ask about shipments, SOPs, incidents..."

          className="border-0 bg-transparent text-base shadow-none focus-visible:ring-0"

        />

        {/* Mic */}

        <Button
          variant="ghost"
          size="icon"
          className="rounded-full"
        >
          <Mic size={18} />
        </Button>

        {/* Send */}

        <Button

          onClick={send}

          disabled={!question.trim()}

          className="h-11 w-11 rounded-full bg-blue-600 hover:bg-blue-700"

        >

          <Send size={18} />

        </Button>

      </div>

    </div>

  );

}