import React from "react";

interface ChatItemProps {
  content: string;
}

export const ChatItem: React.FC<ChatItemProps> = ({ content }) => {
  return <div className="bg-white p-2 m-2 rounded-md shadow-md">{content}</div>;
};
