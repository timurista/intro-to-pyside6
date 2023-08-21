import React from "react";

interface AIMessageItemProps {
  content: string;
}

export const AIMessageItem: React.FC<AIMessageItemProps> = ({ content }) => {
  return (
    <div className="bg-gray-300 p-2 m-2 rounded-md shadow-md text-left">
      {content}
    </div>
  );
};
