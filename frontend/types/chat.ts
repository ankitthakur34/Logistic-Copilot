export interface ToolResult {

  tool_name: string;

  success: boolean;

  sources: string[];

}

//////////////////////////////////////////////////////

export interface ChatMessage {

  id: string;

  role: "user" | "assistant";

  content: string;

  toolResults?: ToolResult[];

}

//////////////////////////////////////////////////////

export interface ChatSession {

  id: string;

  title: string;

  messages: ChatMessage[];

  createdAt: Date;

}