import React from "react";

interface HumanMessageItemProps {
  content: string;
}

export const HumanMessageItem: React.FC<HumanMessageItemProps> = ({
  content,
}) => {
  return (
    <div className="bg-blue-200 p-2 m-2 rounded-md shadow-md text-left">
      {content}
    </div>
  );
};
