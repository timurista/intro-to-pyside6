import React from "react";

interface DocumentItemProps {
  content: string; // Document name
  nestedItems?: Array<string>;
}

export const DocumentItem: React.FC<DocumentItemProps> = ({
  content,
  nestedItems,
}) => {
  return (
    <div className="bg-white p-2 m-2 rounded-md shadow-md">
      📄 {content}
      {nestedItems && nestedItems.length > 0 && (
        <ul className="mt-2 pl-4">
          {nestedItems.map((item, index) => (
            <li key={index} className="list-disc">
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
