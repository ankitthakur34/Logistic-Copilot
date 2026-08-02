import { ChatSession } from "@/types/chat";
import ChatItem from "./ChatItem";
interface Props {
  chats: ChatSession[];
  activeChatId: string;
  onSelect: (id: string) => void;
}

export default function ChatHistory({
  chats,
  activeChatId,
  onSelect,
}: Props) {
  return (
    <div className="flex-1 overflow-y-auto p-3 space-y-2">

      { chats.map(chat => (
        <ChatItem
          key={chat.id}
          chat={chat}
          active={chat.id === activeChatId}
          onClick={() => onSelect(chat.id)}
        />
      ))}

    </div>
  );
}