export interface ToolResult {

    tool_name: string;

    success: boolean;

    sources: string[];

}

export interface ChatResponse {

    answer: string;

    tool_results: ToolResult[];

}

const API_URL = "http://localhost:5000/chat";

export async function askQuestion(

    question: string,

): Promise<ChatResponse> {

    const response = await fetch(

        API_URL,

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

            },

            body: JSON.stringify({

                question,

            }),

        },

    );

    if (!response.ok) {

        throw new Error("Backend request failed");

    }

    return response.json();

}