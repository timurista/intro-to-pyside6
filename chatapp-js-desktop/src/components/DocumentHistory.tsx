import React from "react";
import { observer } from "mobx-react";
import { rootStore } from "../stores/RootStore"; // Update the import path to your RootStore
import { AiOutlineDelete } from "react-icons/ai"; // Assuming you're using react-icons

const DocumentHistory: React.FC = observer(() => {
  const { addDocument } = rootStore.aiAgentStore;

  const handleDocumentUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      addDocument(event.target.files[0]);
    }
  };

  return (
    <div className="mb-4">
      <label className="inline-block bg-green-500 text-white px-4 py-2 rounded-md cursor-pointer">
        Upload Document
        <input type="file" className="hidden" onChange={handleDocumentUpload} />
      </label>
    </div>
  );
});

export default DocumentHistory;
