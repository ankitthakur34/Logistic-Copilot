"use client";

import { Bot, User } from "lucide-react";

import { Badge } from "@/components/ui/badge";

import { ChatMessage as Message } from "@/types/chat";

interface Props {

    message: Message;

}

export default function ChatMessage({

    message,

}: Props) {

    const isUser = message.role === "user";

    return (

        <div
            className={`flex w-full ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >

            <div
                className={`flex max-w-3xl gap-4 ${
                    isUser ? "flex-row-reverse" : ""
                }`}
            >

                {/* Avatar */}

                <div
                    className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full

                    ${
                        isUser
                            ? "bg-blue-600 text-white"
                            : "bg-slate-900 text-white"
                    }`}
                >

                    {

                        isUser

                            ? <User size={20} />

                            : <Bot size={20} />

                    }

                </div>

                {/* Bubble */}

                <div
                    className={`rounded-2xl px-6 py-5 shadow-sm

                    ${
                        isUser
                            ? "bg-blue-600 text-white"
                            : "border bg-white"
                    }`}
                >

                    <p className="whitespace-pre-wrap leading-7">

                        {message.content}

                    </p>

                    {/* Sources */}

                    {

                        !isUser &&

                        message.toolResults &&

                        message.toolResults.length > 0 &&

                        (

                            <div className="mt-6 border-t pt-4">

                                <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500">

                                    Sources

                                </p>

                                <div className="flex flex-wrap gap-2">

                                    {

                                        message.toolResults.map((tool) => (

                                            <Badge
                                                key={tool.tool_name}
                                                variant="secondary"
                                                className="rounded-full"
                                            >

                                                {

                                                    tool.tool_name.toUpperCase()

                                                }

                                            </Badge>

                                        ))

                                    }

                                </div>

                            </div>

                        )

                    }

                </div>

            </div>

        </div>

    );

}