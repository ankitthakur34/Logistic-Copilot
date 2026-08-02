import { ChatSession } from "@/types/chat";

interface Props {
  chat: ChatSession;
  active: boolean;
  onClick: () => void;
}

export default function ChatItem({
  chat,
  active,
  onClick,
}: Props) {
  return (
    <button
      onClick={onClick}
      className={`
      w-full
      rounded-lg
      px-3
      py-3
      text-left
      transition

      ${
        active
          ? "bg-blue-100 border border-blue-500"
          : "hover:bg-gray-100"
      }
      `}
    >
      <div className="font-medium truncate">
        {chat.title}
      </div>

      <div className="text-xs text-gray-500">
        {chat.messages.length} messages
      </div>
    </button>
  );
}